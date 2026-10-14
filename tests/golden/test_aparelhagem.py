"""Golden tests: aparelhagem colocada na planta (simbolos + alturas ao chao).
Valores esperados: catalogo data/convencoes/simbolos_alturas_v1.json (CONVENCAO) e regras com fonte em
rules/alturas.py (RTIEBT 701.71.2 e 801.3.5.5). Geometria verificada com formas conhecidas."""
import json, math, tempfile
from pathlib import Path
import arq_pdf
from eletro.schema.project import Project, Ponto
from eletro.schema.dynamic import diff
from eletro.rules import alturas
from eletro.cad import colocar
from eletro.cad.dxfread import _dentro
from eletro.web.service import Servico

CAT = alturas.carregar(str(alturas.CATALOGO_DEFAULT))

def _sv():
    tmp = tempfile.mkdtemp(); sv = Servico(tmp); sv.criar("t3", exemplo=True)
    return sv

def _t3_preenchido():
    sv = _sv(); P = sv.abrir("t3")["project"]
    P["points"] = sv.preencher("t3", P, 0)["points"]
    return sv, P

def _verifs(res, ref=None):
    return [v for v in res["resultado"]["verificacoes"] if ref is None or v["ref"] == ref]

def test_catalogo_completo_e_coerente():
    assert CAT["estatuto"] == "CONVENCAO"
    for k, s in CAT["simbolos"].items():
        assert s["categoria"] in ("luz", "interruptor", "tomada", "dedicado", "ited"), k
        assert s["altura"] == "teto" or 0 < s["altura"] < 3, k
        assert s["desenho"] and s["nome"], k
    pr = CAT["preenchimento"]
    for k in [pr["luz"], pr["interruptor"], pr["tomada"], *pr["equipamento"].values(), *pr["ited"].values()]:
        assert k in CAT["simbolos"], k

def test_alturas_por_defeito_e_por_uso():
    h = lambda k, u: alturas.altura_por_defeito(k, u, CAT, 2.6)
    assert h("tomada", "sala") == 0.30 and h("tomada", "wc") == 1.10 and h("tomada", "garagem") == 1.10
    assert h("interruptor", "quarto") == 1.10 and h("tomada_bancada", "cozinha") == 1.10
    assert h("luz_teto", "sala") == 2.6 and h("luz_parede", "wc") == 2.25 and h("tomada_ac", "quarto") == 2.20

def _sala(uso, pe=2.6):
    from eletro.schema.project import Room
    return Room(id="r", name="X", use=uso, polygon=[(0, 0), (3, 0), (3, 3), (0, 3)], height_m=pe)

def test_regra_701_71_2_iluminacao_wc_acima_do_chuveiro():
    r = {"r": _sala("wc")}
    baixo = alturas.verificar([Ponto(id="a", kind="luz_parede", room_id="r", pos=(1, 1), height_m=2.0)], r, CAT)
    assert [x[:2] for x in baixo] == [("RTIEBT 701.71.2", "AVISO")]
    assert alturas.verificar([Ponto(id="a", kind="luz_parede", room_id="r", pos=(1, 1), height_m=2.3)], r, CAT) == []
    assert alturas.verificar([Ponto(id="a", kind="luz_teto", room_id="r", pos=(1, 1))], r, CAT) == []   # teto 2.6 m

def test_regra_801_3_5_5_garagem_acima_de_1m_por_confirmar():
    r = {"r": _sala("garagem")}
    x = alturas.verificar([Ponto(id="a", kind="tomada", room_id="r", pos=(1, 1), height_m=0.3)], r, CAT)
    assert [v[:2] for v in x] == [("RTIEBT 801.3.5.5", "POR_CONFIRMAR")]
    assert alturas.verificar([Ponto(id="a", kind="tomada", room_id="r", pos=(1, 1), height_m=1.1)], r, CAT) == []

def test_altura_acima_do_pe_direito_avisa():
    x = alturas.verificar([Ponto(id="a", kind="tomada_ac", room_id="r", pos=(1, 1), height_m=2.8)], {"r": _sala("quarto", 2.6)}, CAT)
    assert any("pe-direito" in v[2] for v in x)

def test_schema_pontos_validados():
    base = json.loads((Path(__file__).parents[2] / "examples/moradia_t3/projeto.json").read_text(encoding="utf-8"))
    for pts, erro in (([{"id": "q1", "kind": "tomada", "room_id": "nao_existe", "pos": [1, 1]}], "inexistente"),
                      ([{"id": "q1", "kind": "tomada", "room_id": "r1", "pos": [1, 1]}] * 2, "repetidos")):
        try:
            Project.model_validate({**base, "points": pts}); assert False
        except ValueError as e:
            assert erro in str(e)

def test_preencher_reproduz_a_convencao_e_alturas():
    sv, P = _t3_preenchido()
    conv = sv.calcular("t3", sv.abrir("t3")["project"])["resultado"]
    res = sv.calcular("t3", P)["resultado"]
    for rid, d in conv["pontos"].items():           # mesmas contagens, agora com origem PLANTA
        assert res["pontos"][rid]["origem"] == "PLANTA"
        assert all(res["pontos"][rid][k] == d[k] for k in ("luz", "tomadas", "interruptores")), rid
    assert [c["id"] for c in res["circuitos"]] == [c["id"] for c in conv["circuitos"]]
    rooms = {r["id"]: r for r in P["rooms"]}
    for q in P["points"]:
        assert _dentro(q["pos"], rooms[q["room_id"]]["polygon"]), q
        assert q["height_m"] == alturas.altura_por_defeito(q["kind"], rooms[q["room_id"]]["use"], CAT, None), q
        assert q["height_origem"] == "CONVENCAO"
    coz = [q["kind"] for q in P["points"] if rooms[q["room_id"]]["use"] == "cozinha" and q["kind"].startswith("tomada")]
    assert coz.count("tomada_bancada") == int(len(coz) * 0.5 + 0.5)

def test_preencher_so_vazias_nao_mexe_no_que_existe():
    sv, P = _t3_preenchido()
    sala = next(r for r in P["rooms"] if r["use"] == "sala")["id"]
    mantidos = [q for q in P["points"] if q["room_id"] == sala]
    P["points"] = mantidos
    novo = sv.preencher("t3", P, 0, so_vazias=True)["points"]
    chave = lambda q: (q["id"], q["kind"], tuple(q["pos"]), q["height_m"], q["height_origem"])
    assert [chave(q) for q in novo if q["room_id"] == sala] == [chave(q) for q in mantidos]
    assert len(novo) > len(mantidos)

def test_menos_pontos_que_a_convencao_e_assinalado():
    sv, P = _t3_preenchido()
    sala = next(r for r in P["rooms"] if r["use"] == "sala")
    tom = [q for q in P["points"] if q["room_id"] == sala["id"] and q["kind"] == "tomada"]
    P["points"] = [q for q in P["points"] if q["id"] != tom[0]["id"]]
    res = sv.calcular("t3", P)
    assert res["resultado"]["pontos"][sala["id"]]["tomadas"] == len(tom) - 1
    assert any("abaixo da convencao" in v["texto"] and v["estado"] == "CONVENCAO" for v in _verifs(res))

def test_ponto_dedicado_sem_equipamento_avisa():
    sv, P = _t3_preenchido()
    q = next(r for r in P["rooms"] if r["use"] == "quarto")
    P["points"].append({"id": "qx", "kind": "tomada_ac", "room_id": q["id"], "pos": P["points"][0]["pos"], "height_m": 2.2})
    P["points"][-1]["pos"] = colocar.centroide([tuple(v) for v in q["polygon"]])
    res = sv.calcular("t3", P)
    assert any("sem equipamento" in v["texto"] for v in _verifs(res, "projeto"))

def test_ited_vem_da_planta():
    sv, P = _t3_preenchido()
    sala = next(r for r in P["rooms"] if r["use"] == "sala")["id"]
    P["points"] = [q for q in P["points"] if not (q["room_id"] == sala and q["kind"] == "tv")]
    res = sv.calcular("t3", P)
    assert res["resultado"]["ited"][sala]["tv"] == 0
    assert any("abaixo da dotacao" in v["texto"] for v in _verifs(res, "Manual ITED"))

def test_material_planta_e_dxf_mostram_tipos_e_alturas():
    sv, P = _t3_preenchido()
    res = sv.calcular("t3", P)
    ap = {m["descricao"]: m["qtd"] for m in res["material"] if m["categoria"] == "Aparelhagem"}
    n_tom = sum(1 for q in P["points"] if q["kind"] == "tomada")
    assert ap["Tomada 2P+T uso geral"] == n_tom and "Interruptor simples" in ap
    assert "ELE-ALTURAS" in res["planta_svg"] and "h1.10" in res["planta_svg"] and "h0.30" in res["planta_svg"]
    dxf = sv.exportar_dxf("t3", P, "planta")
    assert "ELE-ALTURAS" in dxf and "h1.10" in dxf

def test_revisoes_mostram_pontos():
    sv, P = _t3_preenchido()
    a = Project.model_validate(sv.abrir("t3")["project"]); b = Project.model_validate(P)
    d = diff(a, b)
    assert sum(1 for x in d if x.startswith("+ ponto ")) == len(P["points"])
    P2 = json.loads(json.dumps(P)); P2["points"][0]["height_m"] = 0.45; P2["points"][0]["height_origem"] = "MANUAL"
    assert any(x.startswith(f"~ ponto {P2['points'][0]['id']}.height_m") for x in diff(b, Project.model_validate(P2)))

def test_geometria_colocacao_em_divisao_obliqua_e_em_L():
    ang = math.radians(32)
    R = lambda x, y: (10 + x * math.cos(ang) - y * math.sin(ang), 5 + x * math.sin(ang) + y * math.cos(ang))
    rot = [R(0, 0), R(4, 0), R(4, 3), R(0, 3)]
    pts = colocar.no_perimetro(rot, 6, 0.15)
    assert len(pts) == 6 and all(_dentro(p, rot) for p in pts)
    def dist_borda(p):
        best = 9
        for i in range(4):
            (x1, y1), (x2, y2) = rot[i], rot[(i + 1) % 4]
            t = max(0, min(1, ((p[0] - x1) * (x2 - x1) + (p[1] - y1) * (y2 - y1)) / ((x2 - x1) ** 2 + (y2 - y1) ** 2)))
            best = min(best, math.hypot(p[0] - x1 - t * (x2 - x1), p[1] - y1 - t * (y2 - y1)))
        return best
    assert all(abs(dist_borda(p) - 0.15) < 0.01 for p in pts)
    L_ = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 4), (0, 4)]             # centroide geometrico fora da forma
    assert _dentro(colocar.centroide(L_), L_)
    assert all(_dentro(p, L_) for p in colocar.luzes(L_, 3) + colocar.junto_porta(L_, [(0.5, 4)], 2))

def test_fundo_por_piso_apos_importar_pdf():
    with tempfile.TemporaryDirectory() as tmp:
        sv = Servico(tmp); sv.criar("c")
        sv.pdf_analisar("c", arq_pdf.pdf())
        sv.pdf_importar("c", 1, ["PAREDES"], ["VISTA"], 50, 0)
        f = sv.fundo_piso("c", 0)["segmentos"]
        assert len(f) > 20 and (Path(tmp) / "c" / "base_p0.dxf").exists()
        assert sv.fundo_piso("c", -1)["segmentos"] == f        # sem base do piso -1: recorre a base.dxf

def test_app_tem_editor_de_aparelhagem():
    js = (Path(__file__).parents[2] / "src/eletro/web/static/app.js").read_text(encoding="utf-8")
    assert '["apar", "Aparelhagem (planta)"]' in js and "/preencher" in js and "/api/simbolos" in js
