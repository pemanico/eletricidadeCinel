const $ = s => document.querySelector(s);
const esc = t => String(t ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const S = {slug: null, P: null, perfil: null, R: null, tab: "divisoes", sujo: false, dxfInfo: null, painelModo: false, pdf: null, pdfSel: null, pdfDet: null, cat: null, ap: {piso: 0, sel: null, pal: null, vb: null, fundo: {}, alturas: true}};
const TABS = [["divisoes", "Divisões"], ["apar", "Aparelhagem (planta)"], ["alt", "Tabela de alturas"], ["equip", "Equipamentos"], ["alim", "Alimentação / quadro"], ["conv", "Convenção"], ["res", "Resultado"],
  ["planta", "Planta + circuitos"], ["unif", "Unifilar"], ["mat", "Material"], ["rev", "Revisões"], ["dxf", "DXF do arquiteto"], ["pdf", "PDF do arquiteto"], ["exp", "Exportar"]];
// mensagens de resultado de uma acao ficam 10 s; o "calculado" automatico nao as apaga
const msg = (t, err, auto) => { const m = $("#msg"); if (auto && Date.now() - (+m.dataset.t || 0) < 10000) return;
  m.textContent = t; m.className = err ? "err" : ""; if (!auto) m.dataset.t = Date.now(); };
async function api(url, body, raw) {
  const r = await fetch(url, body === undefined ? {} : {method: "POST", body: raw ? body : JSON.stringify(body)});
  const ct = r.headers.get("content-type") || "";
  const d = ct.includes("json") ? await r.json() : await r.text();
  if (!r.ok) throw new Error(d.erro || "erro");
  return d;
}
let tmr; const marcar = () => { S.sujo = true; $("#sujo").textContent = "● por guardar"; clearTimeout(tmr); tmr = setTimeout(calc, 400); };
async function calc() {
  try { S.R = await api(`/api/p/${S.slug}/calc`, {project: S.P, perfil: S.perfil}); msg("calculado", false, true); }
  catch (e) { S.R = null; msg(e.message, true); }
  if (["res", "planta", "unif", "mat"].includes(S.tab)) render();
}
async function listar(sel) {
  const l = await api("/api/projetos"); $("#sel").innerHTML = l.map(p => `<option value="${esc(p.slug)}">${esc(p.slug)} — ${esc(p.name)}</option>`).join("");
  if (sel) $("#sel").value = sel; return l;
}
async function abrir(slug) {
  const d = await api(`/api/p/${slug}`); S.slug = slug; S.P = d.project; S.perfil = d.perfil; S.sujo = false;
  $("#sujo").textContent = ""; $("#rev").textContent = S.P.revision; await calc(); render();
}
function usos() { return Object.keys(S.perfil.dotacao || {}); }
function render() {
  $("#tabs").innerHTML = TABS.map(([k, n]) => `<button class="${k === S.tab ? "on" : ""}" data-t="${k}">${n}</button>`).join("");
  $("#tabs").querySelectorAll("button").forEach(b => b.onclick = () => { S.tab = b.dataset.t; render(); });
  if (!S.P) { $("#main").innerHTML = "<p>Crie ou escolha um projeto.</p>"; return; }
  const f = V[S.tab]; $("#main").innerHTML = ""; const pr = f($("#main")); if (pr && pr.catch) pr.catch(e => msg(e.message, true));
}
const polyTxt = p => (p || []).map(q => q.join(",")).join(" ; ");
function polyParse(t) { return t.split(";").map(s => s.trim()).filter(Boolean).map(s => s.split(",").map(Number)); }
function bind(el, fn) { el.oninput = el.onchange = () => { fn(el); marcar(); }; }
const V = {};
V.divisoes = m => {
  const rs = S.P.rooms;
  m.innerHTML = `<p class="mut">Polígono em metros: "x,y ; x,y ; …" (≥3 pontos). Se alterar o polígono, deixe a área vazia para ser recalculada. Dados importados ficam por confirmar.</p>
  <table><tr><th>id</th><th>Nome</th><th>Uso</th><th>Polígono (m)</th><th>Área m²</th><th>Conf.</th><th>Origem</th><th></th></tr>` +
    rs.map((r, i) => `<tr><td>${esc(r.id)}</td><td><input type=text data-i=${i} data-k=name value="${esc(r.name)}"></td>
    <td><select data-i=${i} data-k=use>${usos().map(u => `<option ${u === r.use ? "selected" : ""}>${u}</option>`).join("")}</select></td>
    <td><input type=text data-i=${i} data-k=polygon value="${esc(polyTxt(r.polygon))}"></td>
    <td>${r.area_m2 ?? ""}</td><td><input type=checkbox data-i=${i} data-k=confirmed ${r.confirmed ? "checked" : ""}></td><td>${r.source}</td>
    <td><button data-del=${i}>✕</button></td></tr>`).join("") + `</table><div class=row><button id=add>+ Divisão</button></div>`;
  m.querySelectorAll("[data-k]").forEach(el => bind(el, e => {
    const r = rs[+e.dataset.i], k = e.dataset.k;
    if (k === "polygon") { r.polygon = polyParse(e.value); r.area_m2 = null; }
    else if (k === "confirmed") r.confirmed = e.checked; else r[k] = e.value;
  }));
  m.querySelectorAll("[data-del]").forEach(b => b.onclick = () => { const id = rs[+b.dataset.del].id; rs.splice(+b.dataset.del, 1);
    S.P.openings = S.P.openings.filter(o => o.room_id !== id); S.P.equipment = (S.P.equipment || []).filter(o => o.room_id !== id); marcar(); render(); });
  $("#add").onclick = () => { let n = 1; while (rs.some(r => r.id === "r" + n)) n++;
    rs.push({id: "r" + n, name: "Nova divisão", use: usos()[0], polygon: [[0, 0], [3, 0], [3, 3], [0, 3]], area_m2: null, height_m: 2.6, floor: 0, source: "manual", confirmed: false}); marcar(); render(); };
};
V.equip = m => {
  const eq = S.P.equipment, kinds = ["termoacumulador", "forno", "placa", "avac", "maq_lavar", "outro"];
  m.innerHTML = `<table><tr><th>id</th><th>Tipo</th><th>Divisão</th><th>Potência W</th><th></th></tr>` + eq.map((e, i) => `<tr><td><input type=text data-i=${i} data-k=id value="${esc(e.id)}"></td>
   <td><select data-i=${i} data-k=kind>${kinds.map(k => `<option ${k === e.kind ? "selected" : ""}>${k}</option>`).join("")}</select></td>
   <td><select data-i=${i} data-k=room_id>${S.P.rooms.map(r => `<option value="${r.id}" ${r.id === e.room_id ? "selected" : ""}>${esc(r.name)}</option>`).join("")}</select></td>
   <td><input type=number data-i=${i} data-k=power_w value="${e.power_w}"></td><td><button data-del=${i}>✕</button></td></tr>`).join("") + `</table><div class=row><button id=add>+ Equipamento</button></div>`;
  m.querySelectorAll("[data-k]").forEach(el => bind(el, e => { eq[+e.dataset.i][e.dataset.k] = e.dataset.k === "power_w" ? +e.value : e.value; }));
  m.querySelectorAll("[data-del]").forEach(b => b.onclick = () => { eq.splice(+b.dataset.del, 1); marcar(); render(); });
  $("#add").onclick = () => { if (!S.P.rooms.length) return; let n = 1; while (eq.some(e => e.id === "e" + n)) n++;
    eq.push({id: "e" + n, kind: "forno", room_id: S.P.rooms[0].id, power_w: 2000}); marcar(); render(); };
};
V.alim = m => {
  const s = S.P.supply, pn = S.P.panel, cl = S.P.circuit_length_m;
  const num = (k, l, un) => `<label>${l} <input type=number step=any data-s=${k} value="${s[k] ?? ""}"> ${un}</label>`;
  m.innerHTML = `<h3>Alimentação</h3><div class=row><label>Fases <select data-s=phases><option ${s.phases === 1 ? "selected" : ""}>1</option><option ${s.phases === 3 ? "selected" : ""}>3</option></select></label>
   ${num("contracted_kva", "Potência contratada", "kVA")}${num("icc_ka", "Icc", "kA (pedir à e-Redes)")}${num("r_terra_ohm", "R terra", "Ω (medida)")}</div>
   <h3>Quadro elétrico</h3><div class=row><label>Divisão <select id=pr>${S.P.rooms.map(r => `<option value="${r.id}" ${pn && pn.room_id === r.id ? "selected" : ""}>${esc(r.name)}</option>`).join("")}</select></label>
   <label>x <input type=number step=0.05 id=px value="${pn ? pn.pos[0] : 0}"></label><label>y <input type=number step=0.05 id=py value="${pn ? pn.pos[1] : 0}"></label>
   <button id=pclick>Posicionar clicando na planta</button></div>
   <h3>Comprimentos manuais por circuito (m)</h3><p class=mut>Por defeito são estimados. Aqui substitui por valor medido. Vazio = estimado.</p>
   <div class=row>${(S.R?.resultado.circuitos || []).map(c => `<label>${c.id} <input type=number step=0.1 data-c=${c.id} value="${cl[c.id] ?? ""}"> <span class=mut>(${c.comprimento_origem} ${c.comprimento_m})</span></label>`).join("")}</div>`;
  m.querySelectorAll("[data-s]").forEach(el => bind(el, e => { const k = e.dataset.s; s[k] = k === "phases" ? +e.value : (e.value === "" ? null : +e.value); }));
  const setP = () => { S.P.panel = {room_id: $("#pr").value, pos: [+$("#px").value, +$("#py").value]}; };
  ["#pr", "#px", "#py"].forEach(k => bind($(k), setP));
  $("#pclick").onclick = () => { S.painelModo = true; S.tab = "planta"; render(); };
  m.querySelectorAll("[data-c]").forEach(el => bind(el, e => { if (e.value === "") delete cl[e.dataset.c]; else cl[e.dataset.c] = +e.value; }));
};
V.conv = m => {
  m.innerHTML = `<p class=mut>Convenção de projeto (dotação por uso, secções mínimas, simultaneidade, quadro…). Tudo aqui é CONVENÇÃO editável, não norma. Fica guardada neste projeto.</p>
  <textarea id=ta>${esc(JSON.stringify(S.perfil, null, 1))}</textarea><div class=row><button class=p id=ap>Aplicar</button><button id=gp>Guardar convenção no projeto</button></div>`;
  const ler = () => { try { return JSON.parse($("#ta").value); } catch (e) { msg("JSON inválido: " + e.message, true); return null; } };
  $("#ap").onclick = () => { const p = ler(); if (p) { S.perfil = p; calc(); } };
  $("#gp").onclick = async () => { const p = ler(); if (!p) return; try { await api(`/api/p/${S.slug}/perfil`, {perfil: p}); S.perfil = p; msg("convenção guardada"); calc(); } catch (e) { msg(e.message, true); } };
};
const tab = (cab, rows) => `<table><tr>${cab.map(c => `<th>${c}</th>`).join("")}</tr>${rows.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join("")}</tr>`).join("")}</table>`;
V.res = m => {
  if (!S.R) { m.innerHTML = "<p class=err>Sem resultado (ver mensagem).</p>"; return; }
  const r = S.R.resultado, q = r.quadro;
  const pd = r.pendencias, bloq = pd && pd.bloqueado ? `<div style="border:2px solid #c62828;padding:8px;margin-bottom:8px"><b>NÃO UTILIZÁVEL COMO PROJETO</b> — ${pd.NAO_CUMPRE} não cumpre · ${pd.POR_CONFIRMAR} por confirmar · ${pd.AVISO} avisos · ${pd.erros_circuito} circuitos com erro</div>` : "";
  m.innerHTML = bloq + `<p>Potência mínima RTIEBT 801.5.2.2: <b>${r.potencia_minima_kva} kVA</b>${q ? ` · instalada ${q.p_inst_w} W · cálculo ${q.p_calc_w} W (${q.s_calc_kva} kVA) → contratar <b>${q.potencia_a_contratar_kva} kVA</b> · geral <b>${q.geral_in_a} A</b> · ${q.modulos.total_modulos} módulos` : ""}</p>
  ${S.R.conflitos.map(c => `<p class=err>CONFLITO: ${esc(c)}</p>`).join("")}<h3>Circuitos</h3>` +
    tab(["id", "tipo", "pts", "Ib", "In", "curva", "mm²", "Iz", "L m", "origem", "queda %", "máx %", "DDR", "erro"], r.circuitos.map(c => [c.id, c.tipo, c.pontos, c.ib_a, c.in_a, c.curva, c.s_mm2, c.iz_a, c.comprimento_m, c.comprimento_origem, c.queda_pct, c.queda_max_pct, c.ddr, c.erro || ""])) +
    `<h3>Verificações</h3><table>${r.verificacoes.map(v => `<tr><td class="e ${v.estado}">${v.estado}</td><td>${esc(v.ref)}</td><td>${esc(v.texto)}</td></tr>`).join("")}</table>
  <h3>Pressupostos</h3><ul>${r.pressupostos.map(x => `<li>${esc(x)}</li>`).join("")}</ul>`;
};
V.planta = m => {
  if (!S.R) { m.innerHTML = "<p class=err>Sem resultado.</p>"; return; }
  m.innerHTML = `<p class=mut>${S.painelModo ? "<b>Clique na planta para colocar o quadro.</b> " : ""}Posições dos pontos indicativas (RASCUNHO). Cinzento = DXF do arquiteto.</p><div class=svgbox id=sv>${S.R.planta_svg}</div>`;
  const svg = $("#sv svg");
  if (S.painelModo) svg.style.cursor = "crosshair";
  svg.onclick = ev => {
    if (!S.painelModo) return; const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
    const q = pt.matrixTransform(svg.getScreenCTM().inverse()), vb = svg.viewBox.baseVal, x = q.x, y = 2 * vb.y + vb.height - q.y;
    const base = S.P.base ? S.P.base.unit_m : 1;
    const sala = S.P.rooms.find(r => inside([x, y], r.polygon));
    if (!sala) { msg("clique dentro de uma divisão", true); return; }
    S.P.panel = {room_id: sala.id, pos: [Math.round(x * 100) / 100, Math.round(y * 100) / 100]}; S.painelModo = false; marcar(); render();
  };
};
function inside(p, poly) { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
  const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi) c = !c; } return c; }
V.unif = m => { m.innerHTML = S.R ? `<div class=svgbox>${S.R.unifilar_svg}</div>` : "<p class=err>Sem resultado.</p>"; };
V.mat = m => { m.innerHTML = S.R ? `<p class=mut>Quantidades; sem preços. Comprimentos estimados + 10%. Tubagem/caixas/ATI não dimensionados.</p>` +
  tab(["Categoria", "Descrição", "Qtd", "Un", "Nota"], S.R.material.map(x => [x.categoria, x.descricao, x.qtd, x.un, x.nota])) : "<p class=err>Sem resultado.</p>"; };
V.rev = async m => {
  const l = await api(`/api/p/${S.slug}/revisoes`);
  m.innerHTML = `<p>Revisão atual: <b>${S.P.revision}</b>. ${S.sujo ? "<b>Há alterações por guardar.</b>" : ""}</p>
  <div class=row>Comparar <select id=da>${l.map(n => `<option>${n}</option>`).join("")}</select> → <select id=db>${l.map((n, i) => `<option ${i === l.length - 1 ? "selected" : ""}>${n}</option>`).join("")}</select>
  <button id=cmp>Ver diferenças</button> <button id=rest>Carregar a primeira para edição</button></div><pre id=dif></pre>`;
  $("#cmp").onclick = async () => { const d = await api(`/api/p/${S.slug}/diff?a=${$("#da").value}&b=${$("#db").value}`); $("#dif").textContent = d.length ? d.join("\n") : "Sem alterações"; };
  $("#rest").onclick = async () => { S.P = await api(`/api/p/${S.slug}/revisao?n=${$("#da").value}`); marcar(); render(); msg("revisão carregada; guarde para criar nova revisão"); };
  m.querySelector("#rest").textContent = "Carregar a revisão 'de' para edição";
};
V.dxf = m => {
  const b = S.P.base, i = S.dxfInfo;
  m.innerHTML = `<p>A planta do arquiteto é a base. Aceita <b>DXF ASCII</b> (guardar do CAD como DXF; DWG não é lido). ${b ? `Base atual: ${esc(b.file)} (1 unid. = ${b.unit_m} m).` : "Sem base."}</p>
  <div class=row><input type=file id=f accept=".dxf"></div>${i ? `<p>Unidade detetada: ${i.unidade_m ?? "desconhecida"} m/unid. · camada sugerida: <b>${i.sugestao_camada_divisoes ?? "nenhuma"}</b></p>
  ${tab(["Camada", "polilinhas fechadas", "abertas", "linhas", "textos", "blocos"], Object.entries(i.camadas).map(([k, v]) => [k, v.poli_fechadas, v.poli_abertas, v.linhas, v.textos, v.blocos]))}
  ${i.avisos.map(a => `<p class=mut>⚠ ${esc(a)}</p>`).join("")}
  <div class=row><label>Camada das divisões <select id=cam>${Object.keys(i.camadas).map(c => `<option ${c === i.sugestao_camada_divisoes ? "selected" : ""}>${esc(c)}</option>`).join("")}</select></label>
  <label>Metros por unidade <input type=number id=un step=any value="${i.unidade_m ?? 0.001}"></label>
  <button class=p id=imp>Importar divisões (substitui as atuais)</button></div><p class=mut>As divisões importadas ficam <b>por confirmar</b>. Equipamentos e quadro mantêm-se se a divisão existir.</p>` : ""}`;
  $("#f").onchange = async ev => { try { const t = await ev.target.files[0].text(); S.dxfInfo = await api(`/api/p/${S.slug}/dxf`, t, true); msg("DXF lido"); render(); } catch (e) { msg(e.message, true); } };
  if (i) $("#imp").onclick = async () => { try {
    const r = await api(`/api/p/${S.slug}/importar`, {camada: $("#cam").value, unit_m: +$("#un").value});
    S.P.rooms = r.divisoes; S.P.openings = r.aberturas; S.P.base = r.base; S.P.points = []; S.ap.fundo = {};
    S.P.equipment = (S.P.equipment || []).filter(e => r.divisoes.some(d => d.id === e.room_id));
    if (!S.P.panel || !r.divisoes.some(d => d.id === S.P.panel.room_id)) S.P.panel = r.divisoes.length ? {room_id: r.divisoes[0].id, pos: r.divisoes[0].polygon[0]} : null;
    msg(r.avisos.join(" | ") || `${r.divisoes.length} divisões importadas`); marcar(); S.tab = "divisoes"; render(); } catch (e) { msg(e.message, true); } };
};
V.pdf = m => {
  const a = S.pdf, pg = a && S.pdfSel ? a.paginas.find(p => p.pagina === S.pdfSel) : null, r = S.pdfDet;
  const cor = {erro: "#c62828", aviso: "#9a6700", info: "var(--mut)"};
  m.innerHTML = `<p>PDF <b>vetorial</b> plotado do CAD (com camadas). Escolha a página (planta de um piso), a camada das paredes e a dos caixilhos/aros. As divisões detetadas ficam <b>por confirmar</b> e são validadas contra o quadro de áreas do arquiteto, se existir.</p>
  <div class=row><input type=file id=fp accept=".pdf,application/pdf"> <span class=mut id=fpst></span></div>
  ${a ? `${a.avisos.map(x => `<p class=err>⚠ ${esc(x)}</p>`).join("")}
  ${tab(["", "Pág.", "Designação", "Escala", "Piso", "Áreas no quadro", "Camada paredes (sug.)"], [])
    .replace("</table>", a.paginas.filter(p => p.vetorial).map(p => `<tr><td><input type=radio name=pg value=${p.pagina} ${p.pagina === S.pdfSel ? "checked" : ""}></td><td>${p.pagina}</td><td>${esc(p.designacao)}</td><td>${p.escala ? "1:" + p.escala : "?"}</td><td>${p.piso ?? ""}</td><td>${p.n_areas_quadro || ""}</td><td>${esc(p.sugestao_camada_paredes || "")}</td></tr>`).join("") + "</table>")}` : ""}
  ${pg ? `<div class=row>
    <label>Paredes <select id=cp>${Object.entries(pg.camadas).map(([c, n]) => `<option value="${esc(c)}" ${c === pg.sugestao_camada_paredes ? "selected" : ""}>${esc(c)} (${n})</option>`).join("")}</select></label>
    <label>Caixilhos/aros <select id=cv><option value="">(nenhuma)</option>${Object.entries(pg.camadas).map(([c, n]) => `<option value="${esc(c)}" ${c === pg.sugestao_camada_vaos ? "selected" : ""}>${esc(c)} (${n})</option>`).join("")}</select></label>
    <label>Escala 1: <input type=number id=ce value="${pg.escala || 100}"></label>
    <label>Piso <input type=number id=cpi value="${pg.piso ?? 0}" style="width:60px"></label>
    <button class=p id=det>Detetar divisões</button></div>` : a ? "<p class=mut>Escolha uma página.</p>" : ""}
  ${r ? `<h3>Resultado (página ${r.pagina}, piso ${r.piso}) — ${r.resumo.divisoes} divisões fechadas, ${r.resumo.ok} de ${r.resumo.comparadas} batem com o quadro (±3%), <span style="color:#c62828">${r.resumo.erros} erros</span>, <span style="color:#9a6700">${r.resumo.avisos} avisos</span></h3>
    ${r.escala ? `<p>Escala: ${r.escala.validada ? "<b style='color:#1a7f37'>confirmada</b> pelas áreas" : "<b class=err>NÃO confirmada</b>"} (${r.escala.dentro_3pct ?? 0} de ${r.escala.n} divisões a ±3%${r.escala.escala_sugerida ? ` · sugerida 1:${r.escala.escala_sugerida}` : ""})</p>` : ""}
    ${r.avisos.map(x => `<p style="margin:2px 0;color:${cor[x.nivel]}">${x.nivel === "erro" ? "✖" : "⚠"} ${esc(x.msg)}</p>`).join("")}
    ${tab(["Divisão", "Estado", "Área calculada m²", "Quadro m²", "Dif. %"], r.validacao.map(v => [v.nome, v.estado, v.area_calc ?? "", v.area_quadro ?? "", v.dif_pct ?? ""]))}
    <div class=row><button class=p id=impp>Importar para o piso ${r.piso} (substitui só as divisões deste piso)</button>${r.resumo.erros ? `<span class=err>Há ${r.resumo.erros} erros: as divisões com erro entram na mesma, por confirmar, para corrigir à mão.</span>` : ""}</div>
    <div class=svgbox>${r.svg}</div>
    <p class=mut>Verde: bate com o quadro · amarelo: 3–8% · vermelho: &gt;8% ou divisões fundidas · azul: sem área no quadro.</p>` : ""}`;
  $("#fp").onchange = async ev => { const f = ev.target.files[0]; if (!f) return; $("#fpst").textContent = "a ler…";
    try { S.pdf = await api(`/api/p/${S.slug}/pdf`, await f.arrayBuffer(), true); S.pdfSel = S.pdf.sugestao_pagina; S.pdfDet = null; msg(`PDF lido: ${S.pdf.paginas.length} páginas`); render(); }
    catch (e) { $("#fpst").textContent = ""; msg(e.message, true); } };
  m.querySelectorAll("input[name=pg]").forEach(x => x.onchange = () => { S.pdfSel = +x.value; S.pdfDet = null; render(); });
  const params = () => ({pagina: S.pdfSel, camadas_paredes: [$("#cp").value], camadas_vaos: $("#cv").value ? [$("#cv").value] : [], escala: +$("#ce").value, piso: +$("#cpi").value});
  if (pg) $("#det").onclick = async () => { msg("a detetar…"); try { S.pdfDet = await api(`/api/p/${S.slug}/pdf_detetar`, params()); msg("deteção concluída"); render(); } catch (e) { msg(e.message, true); } };
  if (r) $("#impp").onclick = async () => { try {
    const x = await api(`/api/p/${S.slug}/pdf_importar`, params());
    const fora = S.P.rooms.filter(d => (d.floor ?? 0) !== x.piso), novos = new Set(x.divisoes.map(d => d.id));
    const ids = new Set(fora.map(d => d.id).concat([...novos]));
    S.P.rooms = fora.concat(x.divisoes);
    S.P.openings = (S.P.openings || []).filter(o => ids.has(o.room_id) && !novos.has(o.room_id)).concat(x.aberturas);
    S.P.equipment = (S.P.equipment || []).filter(e => ids.has(e.room_id)); S.P.base = x.base;
    S.P.points = (S.P.points || []).filter(q => ids.has(q.room_id) && !novos.has(q.room_id)); S.ap.fundo = {}; S.ap.piso = x.piso;
    if (!S.P.panel || !ids.has(S.P.panel.room_id)) S.P.panel = S.P.rooms.length ? {room_id: S.P.rooms[0].id, pos: S.P.rooms[0].polygon[0]} : null;
    msg(`${x.divisoes.length} divisões importadas no piso ${x.piso} (por confirmar). Guarde para criar revisão.`); marcar(); S.tab = "divisoes"; render(); } catch (e) { msg(e.message, true); } };
};
// ---------- Aparelhagem colocada na planta (editor) ----------
const dentro = (pt, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j];
  if ((yi > pt[1]) !== (yj > pt[1]) && pt[0] < (xj - xi) * (pt[1] - yi) / (yj - yi) + xi) c = !c; } return c; };
const pisos = () => [...new Set(S.P.rooms.map(r => r.floor ?? 0))].sort((a, b) => b - a);
const alturaDef = (kind, room) => { const s = S.cat.simbolos[kind]; if (!s) return null; const h = (s.por_uso || {})[room.use] ?? s.altura; return h === "teto" ? null : h; };
const fonteDe = (kind, room) => { const s = S.cat.simbolos[kind]; if (!s || !room) return ""; return (s.por_uso || {})[room.use] !== undefined ? (s.fontes_por_uso || {})[room.use] || "" : s.fonte || ""; };
const velhos = () => { const rooms = Object.fromEntries(S.P.rooms.map(r => [r.id, r]));
  return (S.P.points || []).filter(q => q.height_origem === "CONVENCAO" && rooms[q.room_id] && S.cat.simbolos[q.kind] && alturaDef(q.kind, rooms[q.room_id]) !== q.height_m); };
const fmtH = (q, room) => q.height_m == null ? `teto (${room ? room.height_m : "?"} m)` : q.height_m.toFixed(2) + " m";
function simboloSVG(kind, x, y, k, extra = "") {
  const s = S.cat.simbolos[kind]; if (!s) return `<text x="${x}" y="${-y}" font-size="${k}" fill="red">?</text>`;
  const sw = (k * 0.14).toFixed(4), c = s.cor;
  const el = s.desenho.map(e => e.c ? `<circle cx="${x + e.c[0] * k}" cy="${-(y + e.c[1] * k)}" r="${e.c[2] * k}" fill="none" stroke="${c}" stroke-width="${sw}"/>`
    : e.l ? `<line x1="${x + e.l[0] * k}" y1="${-(y + e.l[1] * k)}" x2="${x + e.l[2] * k}" y2="${-(y + e.l[3] * k)}" stroke="${c}" stroke-width="${sw}"/>`
    : e.p ? `<polyline points="${e.p.map(([a, b]) => `${x + a * k},${-(y + b * k)}`).join(" ")}" fill="none" stroke="${c}" stroke-width="${sw}"/>`
    : `<text x="${x + e.t[0] * k}" y="${-(y + e.t[1] * k)}" font-size="${e.t[2] * k}" fill="${c}" font-family="sans-serif">${esc(e.t[3])}</text>`).join("");
  return `<g ${extra}><rect x="${x - 1.2 * k}" y="${-y - 1.2 * k}" width="${2.4 * k}" height="${2.4 * k}" fill="transparent"/>${el}</g>`;
}
function iconePal(kind) { return `<svg viewBox="-1.6 -1.6 3.2 3.2" width="26" height="26">${simboloSVG(kind, 0, 0, 1)}</svg>`; }
async function garantirFundo(piso) {
  if (S.ap.fundo[piso] === undefined) { try { S.ap.fundo[piso] = (await api(`/api/p/${S.slug}/fundo?piso=${piso}`)).segmentos; } catch (e) { S.ap.fundo[piso] = []; } }
}
V.apar = async m => {
  if (!S.cat) S.cat = await api("/api/simbolos");
  S.P.points = S.P.points || [];
  const ps = pisos(); if (!ps.includes(S.ap.piso)) S.ap.piso = ps.length ? ps[ps.length > 1 && ps.includes(0) ? ps.indexOf(0) : 0] : 0;
  await garantirFundo(S.ap.piso);
  const kinds = Object.keys(S.cat.simbolos), A = S.ap;
  m.innerHTML = `<div class=row><label>Piso <select id=apiso>${ps.map(f => `<option value=${f} ${f === A.piso ? "selected" : ""}>${f}</option>`).join("")}</select></label>
    <button class=p id=apre>Preencher pela convenção (divisões vazias)</button>
    <label><input type=checkbox id=asub> substituir o que está no piso</label>
    <label><input type=checkbox id=aalt ${A.alturas ? "checked" : ""}> mostrar alturas</label>
    <button id=afit>Ajustar vista</button><span class=mut>Roda do rato = zoom · arrastar o fundo = mover · Del = apagar · Esc = largar</span></div>
  <div id=apvel></div>
  <div style="display:grid;grid-template-columns:230px 1fr 260px;gap:10px;align-items:start">
    <div id=apal style="max-height:72vh;overflow:auto"><p class=mut style="margin:0 0 4px">Clique num símbolo e depois na planta. A altura é preenchida pela convenção (editável).</p>
      ${kinds.map(k => { const s = S.cat.simbolos[k]; return `<button data-k="${k}" title="${esc(s.nome)}" style="display:flex;gap:6px;align-items:center;width:100%;text-align:left;margin:2px 0;${A.pal === k ? "outline:2px solid var(--ac)" : ""}">${iconePal(k)}<span style="flex:1">${esc(s.nome)}<br><span class=mut>${s.altura === "teto" ? "teto" : s.altura.toFixed(2) + " m"}${s.por_uso ? " *" : ""}</span></span></button>`; }).join("")}
      <button data-k="__QE" style="width:100%;margin-top:6px;${A.pal === "__QE" ? "outline:2px solid var(--ac)" : ""}">▭ Quadro elétrico (QE)</button>
      <p class=mut>* altura diferente em algumas divisões. Tabela de alturas v${S.cat.versao} (editável no separador "Tabela de alturas").</p></div>
    <div class=svgbox style="padding:0"><svg id=apsvg style="width:100%;height:72vh;touch-action:none;background:#fff;display:block"></svg></div>
    <div id=apdet></div></div>
  <h3>Aparelhagem do piso ${A.piso}</h3><div id=aptab></div>`;
  const svg = $("#apsvg");
  const salasPiso = () => S.P.rooms.filter(r => (r.floor ?? 0) === A.piso && r.polygon && r.polygon.length > 2);
  const salaEm = pt => salasPiso().find(r => dentro(pt, r.polygon));
  const limites = () => { const pts = salasPiso().flatMap(r => r.polygon).concat((S.ap.fundo[A.piso] || []).flat()); if (!pts.length) return [0, -10, 10, 10];
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]); const x0 = Math.min(...xs) - .5, x1 = Math.max(...xs) + .5, y0 = Math.min(...ys) - .5, y1 = Math.max(...ys) + .5; return [x0, -y1, x1 - x0, y1 - y0]; };
  if (!A.vb || A.vbPiso !== A.piso) { A.vb = limites(); A.vbPiso = A.piso; }
  const kSimb = () => Math.max(S.cat.tamanho_simbolo_m, A.vb[2] / Math.max(svg.clientWidth, 300) * 9);
  function desenhar() {
    svg.setAttribute("viewBox", A.vb.join(" "));
    const sw = A.vb[2] / Math.max(svg.clientWidth, 300), k = kSimb(), rooms = Object.fromEntries(S.P.rooms.map(r => [r.id, r]));
    let h = (S.ap.fundo[A.piso] || []).map(([a, b]) => `<line x1="${a[0]}" y1="${-a[1]}" x2="${b[0]}" y2="${-b[1]}" stroke="#999" stroke-width="${sw * 1.2}"/>`).join("");
    h += salasPiso().map(r => { const cx = r.polygon.reduce((s, p) => s + p[0], 0) / r.polygon.length, cy = r.polygon.reduce((s, p) => s + p[1], 0) / r.polygon.length;
      return `<polygon points="${r.polygon.map(p => `${p[0]},${-p[1]}`).join(" ")}" fill="${r.confirmed ? "#e8f3ec" : "#f6f1e3"}" fill-opacity=".55" stroke="#bbb" stroke-width="${sw}"/>
        <text x="${cx}" y="${-cy}" font-size="${sw * 11}" fill="#888" text-anchor="middle" font-family="sans-serif">${esc(r.name)}</text>`; }).join("");
    if (S.P.panel && rooms[S.P.panel.room_id] && (rooms[S.P.panel.room_id].floor ?? 0) === A.piso) { const [x, y] = S.P.panel.pos;
      h += `<rect x="${x - 2 * k}" y="${-y - k}" width="${4 * k}" height="${2 * k}" fill="#fff" stroke="#d62728" stroke-width="${k * .15}"/><text x="${x - 1.4 * k}" y="${-y + .5 * k}" font-size="${1.3 * k}" fill="#d62728" font-family="sans-serif">QE</text>`; }
    for (const q of S.P.points) { const r = rooms[q.room_id]; if (!r || (r.floor ?? 0) !== A.piso) continue;
      h += simboloSVG(q.kind, q.pos[0], q.pos[1], k, `data-q="${q.id}" style="cursor:move"`);
      if (q.id === A.sel) h += `<circle cx="${q.pos[0]}" cy="${-q.pos[1]}" r="${1.6 * k}" fill="none" stroke="#0969da" stroke-width="${k * .2}" stroke-dasharray="${k * .4}"/>`;
      if (A.alturas && !(q.kind === "luz_teto" && q.height_m == null)) { const hh = q.height_m == null ? "teto" : q.height_m.toFixed(2); h += `<text x="${q.pos[0] + 1.2 * k}" y="${-q.pos[1] + 1.6 * k}" font-size="${k * .95}" fill="${q.height_origem === "MANUAL" ? "#9a6700" : "#666"}" font-family="sans-serif">${hh}</text>`; } }
    svg.innerHTML = h; svg.style.cursor = A.pal ? "crosshair" : "grab";
  }
  function detalhe() {
    const q = S.P.points.find(x => x.id === A.sel), d = $("#apdet");
    if (!q) { d.innerHTML = `<p class=mut>${A.pal ? `A colocar: <b>${esc(A.pal === "__QE" ? "Quadro elétrico" : S.cat.simbolos[A.pal].nome)}</b>. Clique na planta.` : "Selecione um símbolo na planta para editar."}</p>`; return; }
    const r = S.P.rooms.find(x => x.id === q.room_id), def = alturaDef(q.kind, r);
    d.innerHTML = `<h3 style="margin-top:0">${esc(q.id)}</h3><p>Divisão: <b>${esc(r ? r.name : q.room_id)}</b> (${esc(r ? r.use : "")})</p>
      <label>Tipo <select id=dk>${kinds.map(k => `<option value="${k}" ${k === q.kind ? "selected" : ""}>${esc(S.cat.simbolos[k].nome)}</option>`).join("")}</select></label>
      <p><label>Altura ao eixo (m) <input type=number step=0.05 min=0 id=dh value="${q.height_m ?? ""}" placeholder="teto"></label><br>
      <span class=mut>Tabela v${S.cat.versao}: ${def == null ? "teto" : def.toFixed(2) + " m"} · origem: <b class="${q.height_origem === "MANUAL" ? "CONVENCAO" : ""}">${q.height_origem}</b>${q.height_ver ? ` (v${q.height_ver})` : ""}<br>Fonte: ${esc(fonteDe(q.kind, r))}</span></p>
      <p><label>x <input type=number step=0.05 id=dx value="${q.pos[0]}"></label> <label>y <input type=number step=0.05 id=dy value="${q.pos[1]}"></label></p>
      <p><label>Nota <input id=dn value="${esc(q.note || "")}" style="width:100%"></label></p>
      <div class=row><button id=drep>Repor altura da convenção</button><button id=ddel class=err>Apagar</button></div>`;
    $("#dk").onchange = e => { q.kind = e.target.value; if (q.height_origem === "CONVENCAO") { q.height_m = alturaDef(q.kind, r); q.height_ver = S.cat.versao; } mudou(); };
    $("#dh").onchange = e => { q.height_m = e.target.value === "" ? null : Math.round(+e.target.value * 100) / 100; q.height_origem = "MANUAL"; mudou(); };
    $("#dx").onchange = $("#dy").onchange = () => { mover(q, [+$("#dx").value, +$("#dy").value]); mudou(); };
    $("#dn").onchange = e => { q.note = e.target.value; marcar(); };
    $("#drep").onclick = () => { q.height_m = def; q.height_origem = "CONVENCAO"; q.height_ver = S.cat.versao; mudou(); };
    $("#ddel").onclick = () => apagar(q.id);
  }
  function tabela() {
    const rooms = Object.fromEntries(S.P.rooms.map(r => [r.id, r]));
    const qs = S.P.points.filter(q => rooms[q.room_id] && (rooms[q.room_id].floor ?? 0) === A.piso);
    $("#aptab").innerHTML = qs.length ? `<table><tr><th>id</th><th>Divisão</th><th>Tipo</th><th>Altura</th><th>Origem</th><th>Nota</th></tr>${qs.map(q => `<tr data-r="${q.id}" style="cursor:pointer;${q.id === A.sel ? "background:var(--bg2)" : ""}"><td>${esc(q.id)}</td><td>${esc(rooms[q.room_id].name)}</td><td>${esc(S.cat.simbolos[q.kind]?.nome || q.kind)}</td><td>${fmtH(q, rooms[q.room_id])}</td><td class="${q.height_origem === "MANUAL" ? "CONVENCAO" : "mut"}">${q.height_origem}</td><td>${esc(q.note || "")}</td></tr>`).join("")}</table>`
      : `<p class=mut>Sem aparelhagem neste piso: o cálculo usa a convenção (contagens por área). Use "Preencher pela convenção" para começar e depois ajuste.</p>`;
    $("#aptab").querySelectorAll("[data-r]").forEach(tr => tr.onclick = () => { A.sel = tr.dataset.r; tudo(); });
  }
  function aviso() {
    const v = velhos(), el = $("#apvel");
    el.innerHTML = v.length ? `<div style="border:1px solid #9a6700;padding:6px 8px;margin:6px 0;display:flex;gap:10px;align-items:center"><span>⚠ <b>${v.length}</b> ponto(s) têm a altura de uma versão antiga da tabela (agora v${S.cat.versao}). Os pontos com altura MANUAL não mudam.</span><button class=p id=arepl>Reaplicar tabela v${S.cat.versao}</button></div>` : "";
    if (v.length) $("#arepl").onclick = async () => { try { const r = await api(`/api/p/${S.slug}/reaplicar`, {project: S.P}); S.P.points = r.points; msg(`${r.alterados} altura(s) atualizadas para a tabela v${r.versao}. Guarde para criar revisão.`); mudou(); } catch (e) { msg(e.message, true); } };
  }
  const tudo = () => { desenhar(); detalhe(); tabela(); aviso(); };
  const mudou = () => { marcar(); tudo(); };
  function mover(q, pt) {
    const r = salaEm(pt);
    if (!r) { msg("fora de qualquer divisão deste piso: posição não alterada", true); return false; }
    q.pos = [Math.round(pt[0] * 100) / 100, Math.round(pt[1] * 100) / 100];
    if (r.id !== q.room_id) { q.room_id = r.id; if (q.height_origem === "CONVENCAO") { q.height_m = alturaDef(q.kind, r); q.height_ver = S.cat.versao; } }
    return true;
  }
  function apagar(id) { S.P.points = S.P.points.filter(x => x.id !== id); if (A.sel === id) A.sel = null; mudou(); }
  const novoId = () => { const u = new Set(S.P.points.map(q => q.id)); let i = 1; while (u.has("q" + i)) i++; return "q" + i; };
  const pt = ev => { const p = svg.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY; const t = p.matrixTransform(svg.getScreenCTM().inverse()); return [t.x, -t.y]; };
  let drag = null;
  svg.onpointerdown = ev => {
    const g = ev.target.closest("[data-q]");
    if (A.pal) {
      const p = pt(ev), r = salaEm(p);
      if (!r) { msg("clique dentro de uma divisão deste piso", true); return; }
      if (A.pal === "__QE") { S.P.panel = {room_id: r.id, pos: [Math.round(p[0] * 100) / 100, Math.round(p[1] * 100) / 100]}; A.pal = null; render(); marcar(); return; }
      const q = {id: novoId(), kind: A.pal, room_id: r.id, pos: [Math.round(p[0] * 100) / 100, Math.round(p[1] * 100) / 100], height_m: alturaDef(A.pal, r), height_origem: "CONVENCAO", height_ver: S.cat.versao, note: ""};
      S.P.points.push(q); A.sel = q.id; mudou(); return;
    }
    if (g) { A.sel = g.dataset.q; drag = {q: S.P.points.find(x => x.id === A.sel), moveu: false}; svg.setPointerCapture(ev.pointerId); tudo(); return; }
    drag = {pan: true, x: ev.clientX, y: ev.clientY, vb: A.vb.slice()}; svg.setPointerCapture(ev.pointerId);
  };
  svg.onpointermove = ev => {
    if (!drag) return;
    if (drag.pan) { const f = A.vb[2] / svg.clientWidth; A.vb[0] = drag.vb[0] - (ev.clientX - drag.x) * f; A.vb[1] = drag.vb[1] - (ev.clientY - drag.y) * f; desenhar(); return; }
    const p = pt(ev); if (salaEm(p)) { drag.q.pos = [Math.round(p[0] * 100) / 100, Math.round(p[1] * 100) / 100]; drag.moveu = true; desenhar(); }
  };
  svg.onpointerup = () => { if (drag && drag.q && drag.moveu) { mover(drag.q, drag.q.pos); mudou(); } else if (drag && drag.pan && Math.abs(A.vb[0] - drag.vb[0]) < 1e-9 && Math.abs(A.vb[1] - drag.vb[1]) < 1e-9) { A.sel = null; tudo(); } drag = null; };
  svg.onwheel = ev => { ev.preventDefault(); const p = pt(ev), f = ev.deltaY > 0 ? 1.2 : 1 / 1.2;
    A.vb = [p[0] - (p[0] - A.vb[0]) * f, -p[1] - (-p[1] - A.vb[1]) * f, A.vb[2] * f, A.vb[3] * f]; desenhar(); };
  m.querySelectorAll("#apal [data-k]").forEach(b => b.onclick = () => { A.pal = A.pal === b.dataset.k ? null : b.dataset.k; A.sel = null; m.querySelectorAll("#apal [data-k]").forEach(x => x.style.outline = x.dataset.k === A.pal ? "2px solid var(--ac)" : ""); tudo(); });
  $("#apiso").onchange = e => { A.piso = +e.target.value; A.sel = null; render(); };
  $("#aalt").onchange = e => { A.alturas = e.target.checked; desenhar(); };
  $("#afit").onclick = () => { A.vb = limites(); desenhar(); };
  $("#apre").onclick = async () => { try {
    const r = await api(`/api/p/${S.slug}/preencher`, {project: S.P, piso: A.piso, so_vazias: !$("#asub").checked});
    S.P.points = r.points; A.sel = null; msg(`${r.gerados} pontos gerados em ${r.divisoes} divisões (alturas da convenção). Ajuste e guarde a revisão.`); marcar(); tudo(); } catch (e) { msg(e.message, true); } };
  document.onkeydown = ev => { if (S.tab !== "apar" || ["INPUT", "SELECT", "TEXTAREA"].includes(document.activeElement.tagName)) return;
    if (ev.key === "Delete" && A.sel) apagar(A.sel); if (ev.key === "Escape") { A.pal = null; A.sel = null; render(); } };
  tudo();
};
// ---------- Tabela de alturas (editavel, versionada, com fonte) ----------
V.alt = async m => {
  S.cat = await api("/api/simbolos");
  const C = S.cat, kinds = Object.keys(C.simbolos), USOS = ["sala", "quarto", "cozinha", "wc", "hall", "corredor", "arrumos", "garagem", "varanda", "escritorio", "lavandaria", "outro"];
  const fmt = v => v === "teto" ? "teto" : (+v).toFixed(2);
  m.innerHTML = `<p>Tabela de alturas ao eixo, a partir do pavimento acabado: <b>versão ${C.versao}</b>. Partilhada por todos os projetos. Cada alteração exige <b>fonte</b> (ex. "UC 6006, formador, 2026-11-03" ou "Manual ITED §x") e cria uma versão nova. Os pontos já colocados <b>não mudam sozinhos</b>: no editor aparece o aviso para reaplicar (só os pontos com altura da tabela; os MANUAL ficam).</p>
  <p class=mut>Ficheiro <code>data/convencoes/simbolos_alturas.json</code> no repositório: faça commit/push para o guardar no GitHub. Valores sem fonte confirmada continuam a ser CONVENÇÃO.</p>
  <table><tr><th></th><th>Símbolo</th><th>Altura por defeito (m)</th><th>Fonte</th><th>Exceções por divisão</th></tr>
  ${kinds.map(k => { const s = C.simbolos[k], pu = s.por_uso || {}, fu = s.fontes_por_uso || {};
    return `<tr><td>${iconePal(k)}</td><td>${esc(s.nome)}</td>
    <td><input data-k="${k}" data-u="*" class=aval value="${fmt(s.altura)}" style="width:70px" ${s.altura === "teto" ? "title='teto = pé-direito da divisão'" : ""}></td>
    <td class=mut style="max-width:260px">${esc(s.fonte || "")}</td>
    <td>${Object.keys(pu).map(u => `<div><b>${u}</b> <input data-k="${k}" data-u="${u}" class=aval value="${fmt(pu[u])}" style="width:60px"> <button data-del="${k}|${u}" title="remover exceção">✕</button> <span class=mut>${esc(fu[u] || "")}</span></div>`).join("")}
      <div><select data-nu="${k}"><option value="">+ exceção…</option>${USOS.filter(u => !(u in pu)).map(u => `<option>${u}</option>`).join("")}</select></div></td></tr>`; }).join("")}</table>
  <div class=row style="position:sticky;bottom:0;background:var(--bg);padding:8px 0;border-top:1px solid var(--bd)"><span id=apend class=mut>Sem alterações.</span>
    <label>Fonte <input id=afonte size=40 placeholder="obrigatória: UC, formador, data / norma, secção"></label><label>Autor <input id=aautor size=10 value="Ordep"></label>
    <button class=p id=agrav disabled>Gravar nova versão</button><button id=adesc disabled>Descartar</button></div>
  <h3>Histórico</h3>${tab(["Versão", "Data", "Autor", "Alteração", "Fonte"], [...(C.historico || [])].reverse().map(h => [h.versao, h.data, h.autor, h.alteracao, h.fonte]))}`;
  const pend = new Map();      // chave kind|uso -> {kind, uso, altura}
  const atual = (k, u) => u === "*" ? C.simbolos[k].altura : (C.simbolos[k].por_uso || {})[u];
  const mostrar = () => { const n = pend.size; $("#apend").textContent = n ? `${n} alteração(ões) por gravar: ` + [...pend.values()].map(a => `${a.kind}[${a.uso}] ${a.altura === null ? "removida" : fmt(a.altura)}`).join(", ") : "Sem alterações.";
    $("#agrav").disabled = !n; $("#adesc").disabled = !n; };
  const ler = v => { v = v.trim().replace(",", "."); if (v.toLowerCase() === "teto") return "teto"; const x = Number(v); return v === "" || isNaN(x) ? undefined : Math.round(x * 100) / 100; };
  m.querySelectorAll(".aval").forEach(el => el.onchange = () => { const k = el.dataset.k, u = el.dataset.u, v = ler(el.value);
    if (v === undefined) { msg("altura inválida: número em metros (ex. 1.10) ou 'teto'", true); el.value = fmt(atual(k, u)); return; }
    if (v === atual(k, u)) pend.delete(k + "|" + u); else pend.set(k + "|" + u, {kind: k, uso: u, altura: v}); el.style.background = pend.has(k + "|" + u) ? "#fff3cd" : ""; mostrar(); });
  m.querySelectorAll("[data-del]").forEach(b => b.onclick = () => { const [k, u] = b.dataset.del.split("|"); pend.set(k + "|" + u, {kind: k, uso: u, altura: null}); b.parentElement.style.textDecoration = "line-through"; mostrar(); });
  m.querySelectorAll("[data-nu]").forEach(sel => sel.onchange = () => { const k = sel.dataset.nu, u = sel.value; if (!u) return;
    const d = document.createElement("div"); d.innerHTML = `<b>${u}</b> <input class=aval value="${fmt(C.simbolos[k].altura)}" style="width:60px;background:#fff3cd">`; sel.parentElement.before(d);
    const inp = d.querySelector("input"); pend.set(k + "|" + u, {kind: k, uso: u, altura: ler(inp.value)});
    inp.onchange = () => { const v = ler(inp.value); if (v === undefined) { msg("altura inválida", true); return; } pend.set(k + "|" + u, {kind: k, uso: u, altura: v}); mostrar(); };
    [...sel.options].find(o => o.value === u)?.remove(); sel.value = ""; mostrar(); });
  $("#adesc").onclick = () => render();
  $("#agrav").onclick = async () => { const fonte = $("#afonte").value.trim();
    if (fonte.length < 3) { msg("indique a fonte das alterações", true); $("#afonte").focus(); return; }
    try { const r = await api("/api/simbolos", {alteracoes: [...pend.values()].map(a => ({...a, fonte})), autor: $("#aautor").value});
      S.cat = r.tabela; msg(`Tabela gravada: versão ${S.cat.versao} (${r.alteracoes.length} alteração(ões)). Faça commit do ficheiro para o guardar no GitHub.`); render(); if (S.P) calc(); }
    catch (e) { msg(e.message, true); } };
};
V.exp = m => {
  m.innerHTML = `<div class=row><button id=r>Relatório HTML (memória de cálculo + material)</button><button id=d1>DXF planta + circuitos</button><button id=d2>DXF unifilar</button><button id=j>Resultado JSON</button></div>
  <p class=mut>O DXF da planta contém as linhas/polilinhas do arquiteto (camadas ARQ-*) mais as camadas elétricas. Textos e blocos do arquiteto não são reproduzidos; não testado em AutoCAD.</p>`;
  const baixar = async (url, body, nome, tipo) => { const r = await fetch(url, {method: "POST", body: JSON.stringify(body)}); if (!r.ok) { msg((await r.json()).erro, true); return; }
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([await r.text()], {type: tipo})); a.download = nome; a.click(); };
  $("#r").onclick = async () => { const r = await fetch(`/api/p/${S.slug}/relatorio`, {method: "POST", body: JSON.stringify({project: S.P})}); const w = window.open(); w.document.write(await r.text()); w.document.close(); };
  $("#d1").onclick = () => baixar(`/api/p/${S.slug}/export_dxf`, {project: S.P, que: "planta"}, `${S.slug}_planta_rev${S.P.revision}.dxf`, "application/dxf");
  $("#d2").onclick = () => baixar(`/api/p/${S.slug}/export_dxf`, {project: S.P, que: "unifilar"}, `${S.slug}_unifilar_rev${S.P.revision}.dxf`, "application/dxf");
  $("#j").onclick = () => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([JSON.stringify(S.R?.resultado, null, 1)], {type: "application/json"})); a.download = `${S.slug}_resultado.json`; a.click(); };
};
$("#sel").onchange = e => abrir(e.target.value);
$("#novo").onclick = async () => { const s = prompt("Identificador (a-z, 0-9, - _)"); if (!s) return; try { await api("/api/projetos", {slug: s}); await listar(s); abrir(s); } catch (e) { msg(e.message, true); } };
$("#exemplo").onclick = async () => { const s = prompt("Identificador para a cópia do exemplo", "moradia-t3"); if (!s) return; try { await api("/api/projetos", {slug: s, exemplo: true}); await listar(s); abrir(s); } catch (e) { msg(e.message, true); } };
$("#guardar").onclick = async () => { try { const r = await api(`/api/p/${S.slug}/guardar`, {project: S.P, motivo: $("#motivo").value}); $("#motivo").value = ""; msg(`revisão ${r.revision} guardada`); await abrir(S.slug); } catch (e) { msg(e.message, true); } };
window.addEventListener("beforeunload", e => { if (S.sujo) e.preventDefault(); });
(async () => { const l = await listar(); if (l.length) abrir(l[0].slug); else render(); })();
