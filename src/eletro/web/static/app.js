const $ = s => document.querySelector(s);
const esc = t => String(t ?? "").replace(/[&<>"]/g, c => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
const S = {slug: null, P: null, perfil: null, R: null, tab: "divisoes", sujo: false, dxfInfo: null, painelModo: false, pdf: null, pdfSel: null, pdfDet: null};
const TABS = [["divisoes", "Divisões"], ["equip", "Equipamentos"], ["alim", "Alimentação / quadro"], ["conv", "Convenção"], ["res", "Resultado"],
  ["planta", "Planta + circuitos"], ["unif", "Unifilar"], ["mat", "Material"], ["rev", "Revisões"], ["dxf", "DXF do arquiteto"], ["pdf", "PDF do arquiteto"], ["exp", "Exportar"]];
const msg = (t, err) => { const m = $("#msg"); m.textContent = t; m.className = err ? "err" : ""; };
async function api(url, body, raw) {
  const r = await fetch(url, body === undefined ? {} : {method: "POST", body: raw ? body : JSON.stringify(body)});
  const ct = r.headers.get("content-type") || "";
  const d = ct.includes("json") ? await r.json() : await r.text();
  if (!r.ok) throw new Error(d.erro || "erro");
  return d;
}
let tmr; const marcar = () => { S.sujo = true; $("#sujo").textContent = "● por guardar"; clearTimeout(tmr); tmr = setTimeout(calc, 400); };
async function calc() {
  try { S.R = await api(`/api/p/${S.slug}/calc`, {project: S.P, perfil: S.perfil}); msg("calculado"); }
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
  const f = V[S.tab]; $("#main").innerHTML = ""; f($("#main"));
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
    S.P.rooms = r.divisoes; S.P.openings = r.aberturas; S.P.base = r.base;
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
    if (!S.P.panel || !ids.has(S.P.panel.room_id)) S.P.panel = S.P.rooms.length ? {room_id: S.P.rooms[0].id, pos: S.P.rooms[0].polygon[0]} : null;
    msg(`${x.divisoes.length} divisões importadas no piso ${x.piso} (por confirmar). Guarde para criar revisão.`); marcar(); S.tab = "divisoes"; render(); } catch (e) { msg(e.message, true); } };
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
