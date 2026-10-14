"""Relatorio HTML (RASCUNHO) com todos os calculos, verificacoes, quadro de cargas e material."""
from __future__ import annotations
from html import escape as h
from ..engine import Resultado, pendencias
from ..schema.project import Project
from ..calc.material import lista_material
from ..rules.alturas import carregar as _carregar_cat, CATALOGO_DEFAULT

def _cat():
    return _carregar_cat(str(CATALOGO_DEFAULT))
from ..cad.desenho import planta, unifilar, para_svg

COR_ESTADO = {"CUMPRE": "#1a7f37", "NAO_CUMPRE": "#c62828", "CONVENCAO": "#9a6700", "POR_CONFIRMAR": "#6639ba", "AVISO": "#0969da"}

def _tab(cab, linhas, cls=""):
    t = f'<table class="{cls}"><thead><tr>' + "".join(f"<th>{h(str(c))}</th>" for c in cab) + "</tr></thead><tbody>"
    for l in linhas:
        t += "<tr>" + "".join(f"<td>{h(str(c))}</td>" for c in l) + "</tr>"
    return t + "</tbody></table>"

CSS = """body{font:14px/1.45 system-ui,sans-serif;max-width:1000px;margin:24px auto;padding:0 16px;color:#1f2328}
h1{font-size:22px}h2{font-size:17px;border-bottom:1px solid #d0d7de;padding-bottom:4px;margin-top:28px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:13px}th,td{border:1px solid #d0d7de;padding:4px 8px;text-align:left}
th{background:#f6f8fa}.b{border:2px solid #c62828;padding:8px 12px;background:#fff5f5;margin:12px 0}
.e{font-weight:600}svg{max-width:100%;height:auto;border:1px solid #d0d7de}"""

def relatorio_html(p: Project, r: Resultado, cat: dict | None = None) -> str:
    cat = cat or _cat()
    o = [f"<!doctype html><html lang='pt'><meta charset='utf-8'><title>Memoria de calculo - {h(p.name)}</title><style>{CSS}</style><body>",
         f"<h1>Memória de cálculo — {h(p.name)} (revisão {r.revisao})</h1>",
         "<div class='b'><b>RASCUNHO NÃO ASSINADO.</b> Gerado por software a partir de convenções editáveis e tabelas (edição 2000) por confirmar. "
         "A validação, assinatura e responsabilidade são de técnico habilitado.</div>"]
    pd = pendencias(r)
    if pd["bloqueado"]:
        o.append(f"<div class='b'><b>NÃO UTILIZÁVEL COMO PROJETO.</b> Pendências: {pd['NAO_CUMPRE']} não cumpre · {pd['POR_CONFIRMAR']} por confirmar (tabelas/fontes) · {pd['AVISO']} avisos · {pd['erros_circuito']} circuitos com erro. Resolver todas antes de qualquer uso fora do estudo.</div>")
    o.append("<h2>1. Pressupostos</h2><ul>" + "".join(f"<li>{h(x)}</li>" for x in r.pressupostos) + "</ul>")
    o.append(f"<h2>2. Potência</h2><p>Mínima regulamentar (RTIEBT 801.5.2.2): <b>{r.potencia_minima_kva} kVA</b> · compartimentos contados: {r.n_compartimentos}.</p>")
    nomes = {x.id: x.name for x in p.rooms}
    o.append("<h2>3. Pontos por divisão (convenção)</h2>" + _tab(["Divisão", "Luz", "Tomadas", "Interruptores"],
             [(nomes.get(i, i), d["luz"], d["tomadas"], d["interruptores"]) for i, d in r.pontos.items()]))
    o.append("<h2>4. Circuitos</h2>" + _tab(["Circuito", "Tipo", "Pts", "Ib (A)", "In (A)", "Curva", "Secção mm²", "Iz (A)", "L (m)", "Origem L", "Queda %", "Máx %", "Nota"],
             [(c.id, c.tipo, c.pontos, c.ib_a, c.in_a, c.curva, c.s_mm2, c.iz_a, c.comprimento_m, c.comprimento_origem, c.queda_pct, c.queda_max_pct, c.erro or "") for c in r.circuitos]))
    if r.quadro:
        q = r.quadro
        o.append("<h2>5. Quadro de cargas</h2>" + _tab(["Circuito", "Tipo", "Pinst (W)", "Pcalc (W)", "In", "Curva", "PE mm²", "DDR"],
                 [(c.id, c.tipo, f"{c.p_inst_w:.0f}", f"{c.p_calc_w:.0f}", c.in_a, c.curva, c.pe_mm2, c.ddr) for c in r.circuitos if not c.erro]))
        o.append(f"<p>Total instalada <b>{q.p_inst_w:.0f} W</b>; de cálculo <b>{q.p_calc_w:.0f} W ({q.s_calc_kva:.2f} kVA)</b> → potência a contratar <b>{q.potencia_a_contratar_kva} kVA</b>; "
                 f"geral <b>{q.geral_in_a} A</b>; {q.n_mcb} disjuntores; {q.modulos['total_modulos']} módulos.</p>")
        o.append(_tab(["DDR", "In (A)", "IΔn (mA)", "Tipo", "Circuitos", "I cálculo (A)"], [(d["id"], d["in_a"], d["idn_ma"], d["tipo"], ", ".join(d["circuitos"]), d["corrente_calculo_a"]) for d in q.ddr]))
    o.append("<h2>6. Verificações</h2><table><thead><tr><th>Estado</th><th>Referência</th><th>Texto</th></tr></thead><tbody>" +
             "".join(f"<tr><td class='e' style='color:{COR_ESTADO.get(v.estado,'#000')}'>{h(v.estado)}</td><td>{h(v.ref)}</td><td>{h(v.texto)}</td></tr>" for v in r.verificacoes) + "</tbody></table>")
    if r.ited:
        o.append("<h2>7. ITED</h2>" + _tab(["Divisão", "RJ45", "TV", "Estado", "Fonte"], [(i, d["rj45"], d["tv"], d["estado"], d["fonte"]) for i, d in r.ited.items()]))
    o.append("<h2>8. Lista de material</h2>" + _tab(["Categoria", "Descrição", "Qtd", "Un", "Nota"], [(m["categoria"], m["descricao"], m["qtd"], m["un"], m["nota"]) for m in lista_material(r, pontos=p.points, catalogo=cat)]) +
             "<p>Sem preços. Tubagem, caixas, ATI e bornes não dimensionados.</p>")
    o.append("<h2>9. Planta com circuitos (" + ("aparelhagem colocada; percursos indicativos" if p.points else "posições indicativas") + ")</h2>" + para_svg(planta(p, r, catalogo=cat)))
    o.append("<h2>10. Esquema unifilar</h2>" + para_svg(unifilar(r), esp=1.5))
    return "".join(o) + "</body></html>"
