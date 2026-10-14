# Estado atual
_Atualizado: 2026-10-14 (fim de tarde; curso começa 19-10-2026)_

## Feito
- Notas de estudo em 9 blocos cobrindo todas as UC + UFPRA/UFPCT (`study_notes/`). Material de estudo gerado por IA, NÃO normativo.
- Repo privado `pemanico/eletricidadeCinel` (GitHub) com: schema do projeto (polígonos, aberturas, equipamentos, quadro, revisões, overrides), deteção de conflitos de overrides, diff entre revisões, gerador de DXF (R12, sem dependências), CLI (`validate|draw|diff`), módulo de cabos com golden tests, 3 agentes (`ingestao-planta`, `projetista-rascunho`, `revisor-coerencia`).
- 10 testes a passar (`python run_tests.py`).

## Em curso / não validado
- DXF gerado só foi validado estruturalmente; **por abrir em QCAD/LibreCAD/AutoCAD**. Ficheiro entregue ao Ordep e guardado em `examples/moradia_t3/t3_rev1.dxf` (a pasta `saida/` não vai para o Git). **Feedback do Ordep (2026-10-12 21:01): o DXF abre; divisões, quadro, janelas e áreas corretos.** Porta não mencionada (por confirmar se se vê: está desenhada como linha sobre a parede). Desenho é só a base: ainda sem pontos elétricos.
- Tabelas de capacidade de corrente (calc/cabos.py) vêm das notas de estudo; **por validar na norma/RTIEBT**.

## Atualização 2026-10-12 (noite)
- PDFs do RTIEBT carregados em `sources/normativas/`. Regras de habitação extraídas em `docs/REGRAS_HABITACAO_RTIEBT.md` (aguardam confirmação). `calc/cabos.py` passou a usar o Quadro 52-C1 do RTIEBT (corrigido erro meu); 11 testes a passar.

## Motor v1 (2026-10-12 noite)
Feito: `python -m eletro.cli calc examples/moradia_t3/projeto.json` calcula pontos, circuitos, secções, Iz, quedas de tensão, potência mínima, com estado e fonte por linha. 22 testes (valores calculados à mão).
**Atualização (22:50):** o motor já tem potência de cálculo (convenção), potência a contratar, disjuntor geral, DDR 30 mA em 2 grupos, curvas, PE (Q.54F), módulos do quadro, quadro de cargas em texto e ITED por divisão. 31 testes.
**Ainda NÃO existe:** verificação de disparo magnético/Icc mínima/I²t (faltam Zs e Icc), seleção por selectividade, terras e equipotencial (elétrodo, ligações), esquema unifilar gráfico, quadro de cargas em DXF/PDF, tomadas em WC (volumes 701), ATI/tubagem ITED, mapa de quantidades, orçamento, trifásico, app web.
Limitações conhecidas: agrupamento sequencial pela ordem das divisões (iluminação percorre a casa toda numa ordem arbitrária); WC com circuito de tomadas próprio; tabelas da edição 2000 por confirmar.

## Como retomar
Novo chat: `/retomar` (ou ler brain/00_LEIA_PRIMEIRO.md + ESTADO.md). Última linha de trabalho: app web v1 concluída e no GitHub (commit 6627536+). Próximo: DXF real do arquiteto → agentes → orçamento.

## 2026-10-13
README reescrito; `engine.pendencias()` + banner "NÃO UTILIZÁVEL COMO PROJETO" no relatório, no texto e na app enquanto houver POR_CONFIRMAR/AVISO/NAO_CUMPRE. 43 testes. Revisão externa (Grok) aceite em parte; prioridade acordada: RTIEBT original + DXF real (do Ordep) → comparar com projeto real executado → orçamento (precisa de preços) → trajetos/agentes. Aviso: os golden tests usam as mesmas tabelas do código, não são validação independente.

## 2026-10-13 (noite): app verificada no PC do Ordep (Windows)
- Repo local do Ordep: `E:\Cinel\projectAI\eletricidadeCinel` (VS Code, Windows). O Ordep confirmou: testes OK e `python run_app.py` a correr.
- Verificado por mim no browser da app Claude, ligado a http://127.0.0.1:8765 no PC dele: criado `moradia-t3` (Exemplo T3), calculado; Resultado, Planta+circuitos (SVG), Unifilar (SVG), Material e Exportar funcionam; banner "NÃO UTILIZÁVEL COMO PROJETO" presente (17 por confirmar, 4 avisos, 0 não cumpre); acentos corretos; consola sem erros; `app.js` servido como `text/javascript`.
- DXF planta (14796 bytes) e unifilar (8998 bytes) exportados no Windows têm o mesmo tamanho que no Linux da nuvem. Relatório HTML com banner.
- Nenhuma alteração de código nesta sessão (nada falhou no Windows).
- PDF da casa do Ordep (planta de execução, folha A0, 1 página) analisado SEM alterar código; o PDF NÃO vai para o Git (dados pessoais no carimbo). Factos verificados: vetorial (188k linhas, 158k de espessura 0 = tramas/soalho); escala 1:50 no carimbo, coerente com as cotas da cave (9,06 ext. = 8,30 + 2×0,38); 2 plantas na mesma folha (piso 0 com ~18 divisões, incl. ala oblíqua dos quartos; cave); nomes das divisões em texto; SEM áreas escritas; cotas só na cave (16); camadas perdidas (69 objetos OCG mas sem /OCProperties; Creator=PDFium → PDF regravado, não o original do arquiteto); texto duplicado sobreposto ("VVii..0022").
- 2.º PDF (projeto de acústica, licenciamento, piso 0, 1 página, 1:100): plot direto do AutoCAD LT 2023 → **camadas preservadas** (arq_corte, arq_vista 1, arq_tracejado_vista 1, arq_tramas, arq_estereotomia, 0, TITULOS, TABELAS, FA FOLHA, FA ROTULO, CYPE_TABELA_DE_SIMBOLOS). Renderizada só `arq_corte`: são só as paredes cortadas (342 segmentos), limpas, com aberturas nas portas/vãos. Sem nomes de divisões nem áreas; não tem a cave; fase licenciamento (pode diferir da execução). Também não vai para o Git.
- 3.º PDF (projeto de alterações em obra, 23 págs, AutoCAD LT 2023, camadas preservadas). **Pág. 5 = Planta do piso 0 PROPOSTO, 1:100, 03-2024 (LIC.04): o caso de referência.** Tem: `arq_corte` (paredes, 912 segm.), `arq_cotas` (cotas em camada própria → validar escala), nomes das divisões em texto, **quadro de áreas úteis (22 divisões: Hall 1 4.72, …, Sala 47.97, Piscina 28.00 m²)** → validação cruzada, posição do QE e siglas de equipamentos (PF, MO, MLR, MLL). Págs. 15–23 = vermelhos/amarelos; piso -1 só aparece em vermelhos/amarelos (pág. 17).
- Decisão pendente do Ordep: (a) pedir ao arquiteto o PDF original/DWG; (b) contorno semi-automático com o PDF como fundo + escala 1:50 + snap a vértices de parede + nomes importados; (c) extração automática de divisões (cara: portas abrem os polígonos).
- **Próximo:** DXF real do arquiteto no separador "DXF do arquiteto" → relatar camadas/unidade/divisões antes de mexer em código. Risco já identificado: acentos em DXF ANSI_1252 (ver [[ARMADILHAS]]). Agentes e orçamento: não nesta fase.

## 2026-10-14 (noite): cálculos ponto a ponto + quadro — FEITO
Pedido do Ordep: cálculos de todas as tomadas/pontos de luz e dimensionamento do quadro. O motor já calculava circuitos e quadro; faltava ligar à aparelhagem colocada.
- Divisões com aparelhagem colocada: cada ponto de luz/tomada pertence a um circuito. Automático = por proximidade ao quadro (cadeia de vizinho mais próximo, máx. 8 pontos, 801.5.3); ou **escolhido à mão** no editor (campo "Circuito", ex. TOM-COZ; >8 dá NAO_CUMPRE; misturar luz e tomadas dá AVISO). Divisões sem pontos continuam pela convenção.
- **Comprimento real** (`calc/percursos.py`): iluminação pelo teto (sobe do quadro a 1,5 m, desce a cada ponto pela altura), tomadas/dedicados pelas paredes à altura dos pontos; horizontais em L × fator 1,2; entre pisos 3 m + AVISO. Cabo desde o quadro até cada ponto (tabela "Aparelhagem e circuitos"). Equipamentos usam o ponto dedicado colocado na divisão. Secção/Iz/queda/PE e quadro (geral, DDR, disjuntores, módulos, potência) recalculados a partir disto.
- App: Resultado com tabela **Quadro elétrico** (geral, DDR e circuitos protegidos, disjuntores com curva/cabo/PE, caixa) e **Aparelhagem e circuitos**; editor com "mostrar circuitos" (percurso e id por ponto) e escolha manual do circuito; planta e DXF desenham a cadeia real.
- Casa real (piso 0, preenchida pela convenção): 4 ILUM + 5 TOM, todas 1,5/2,5 mm². Exemplo T3: TOM a 18–28 m, 2,5 mm².
- 81 testes (percursos calculados à mão: teto 6,4/13,0 m; parede 4,2/6,2 m).
- **Pontos para debate:** Ib das tomadas = In (16 A) em todo o comprimento é conservador (convenção); com percurso pelo teto as tomadas passavam a 4 mm² — por isso tomadas vão pelas paredes. Icc/Zs e disparo magnético continuam NÃO verificados (falta Icc da e-Redes); tabelas da ed. 2000 por confirmar.

## 2026-10-14 (fim de tarde): tabela de alturas editável na app — FEITO
O Ordep vai alterar as alturas durante o curso. Por isso:
- Separador **"Tabela de alturas"**: altura por defeito e exceções por divisão (acrescentar/alterar/remover) para os 15 símbolos; **fonte obrigatória** ("UC, formador, data" / "norma, secção"); gravar cria **versão nova** + linha no **histórico** (data, autor, alteração de→para, fonte). Ficheiro: `data/convencoes/simbolos_alturas.json` (antes `_v1`), no repositório → o Ordep faz commit/push das alterações.
- Cada ponto guarda `height_ver` (versão da tabela que lhe deu a altura). Se a tabela mudar: AVISO no resultado ("N pontos com altura da tabela antiga") e faixa no editor com **"Reaplicar tabela vN"** (só pontos CONVENCAO; os MANUAL não mudam).
- Testes usam uma cópia CONGELADA da tabela inicial (`tests/golden/fixtures/simbolos_alturas_ref.json`): as alterações do Ordep não partem os testes; a tabela real só é testada em estrutura (válida, fonte em todos os valores). 77 testes; Chromium: editar 3 valores, recusa sem fonte, gravar v2, aviso de 32 pontos, reaplicar, aviso desaparece (servidor de teste com cópia da tabela; ficheiro real intacto).

## 2026-10-14: aparelhagem na planta com alturas ao chão — FEITO
Pedido do Ordep: "só PDF" (DWG fica para depois); colocar na app os símbolos dos componentes elétricos e preencher automaticamente as alturas ao chão.
- Novo separador **"Aparelhagem (planta)"**: escolher o piso; fundo = paredes do PDF importado; paleta com 15 símbolos (luz teto/parede, interruptor, comutadores, botão, tomadas uso geral/bancada/estanque/dedicada, AC, caixa de ligação, termoacumulador, RJ45, TV) e QE. Clicar no símbolo e depois na planta: a divisão é detetada pela posição e a **altura é preenchida pela convenção** (por tipo e por uso da divisão: ex. tomada 0,30 m, mas 1,10 m em WC e garagem). Arrastar move (se mudar de divisão e a altura for da convenção, recalcula); editar a altura → origem MANUAL (fica a laranja); "Repor altura da convenção"; Del apaga; zoom com a roda; tabela do piso.
- **"Preencher pela convenção"**: gera a aparelhagem nas divisões vazias do piso (ou substitui, com a caixa marcada) com as contagens da convenção e posições iniciais ao longo das paredes reais (funciona na ala oblíqua), interruptores junto à porta, metade das tomadas da cozinha como bancada, ligações dos equipamentos.
- O motor passa a usar os pontos colocados (contagens por divisão = origem PLANTA; circuitos refeitos); avisa quando fica abaixo da convenção, ponto dedicado sem equipamento, ITED abaixo da dotação. Verificações de alturas com fonte: **RTIEBT 701.71.2** (iluminação em WC acima do chuveiro: AVISO abaixo de 2,25 m convencionado) e **801.3.5.5** (garagem: aparelhagem > 1 m, POR CONFIRMAR se se aplica a moradia); altura acima do pé-direito.
- Planta (SVG/DXF) desenha os símbolos do catálogo com a altura (camada ELE-ALTURAS, "h1.10"); material lista a aparelhagem por tipo; revisões mostram pontos (+/~).
- Ficheiros: `data/convencoes/simbolos_alturas_v1.json`, `rules/alturas.py`, `cad/colocar.py`, `schema/project.py` (Ponto), `engine.py`, `cad/desenho.py`, `calc/material.py`, `web/*`. Importar PDF grava também `base_p<piso>.dxf` (paredes por piso para o editor).
- Verificado: 74 testes; Chromium com a planta real (preencher 87 pontos em 13 divisões, colocar, editar altura, arrastar, apagar, resultado, material, planta, guardar). NÃO verificado no PC do Ordep.
- **Limites:** símbolos não rodam com a parede; percursos de cabo continuam em estrela a partir do centro (comprimentos não usam as posições reais); a planta "Planta + circuitos" sobrepõe os pisos; divisões fundidas pelo PDF (sala aberta) recebem pontos como uma só divisão → dividir primeiro.
- **Próximo:** o Ordep testa no PC (`git pull`, `pip install -r requirements.txt`, `python run_tests.py`, `python run_app.py`) e diz que alturas/símbolos quer diferentes; depois: dividir divisões fundidas na app; comprimentos de cabo a partir das posições reais.

## 2026-10-13 (noite): PDF do arquiteto na app — FEITO (parte do PDF fechada, a pedido do Ordep)
- Novo separador **"PDF do arquiteto"**: carregar PDF → lista de páginas (designação, escala, piso, nº de áreas no quadro, camada de paredes sugerida; sugere a planta "proposto" com mais áreas) → escolher página, camada de paredes, camada de caixilhos/aros, escala e piso → **Detetar** (pré-visualização SVG colorida + avisos/erros + tabela área calculada vs quadro) → **Importar** (substitui só as divisões desse piso; `confirmed=False`; paredes passam a fundo da planta e entram na exportação DXF).
- Código: `cad/pdfread.py`, `cad/divisoes.py`, `web/service.py` (pdf_analisar/pdf_detetar/pdf_importar), `web/server.py` (rotas `pdf`, `pdf_detetar`, `pdf_importar`; corpo binário até 60 MB), `web/static/app.js`. Dependências novas em `requirements.txt`: pikepdf, pdfplumber, pypdfium2, numpy, scipy → **no PC do Ordep: `pip install -r requirements.txt`**.
- Resultado na planta real (PDF de alterações, pág. 5, piso 0): 13 divisões fechadas; **6 de 11 comparáveis a ±3% do quadro** (Garagem −0,3%, Escritório −1,2%, Lavandaria −1,6%, Quarto 1 −1,7%, Quarto 2 −2,1%, IS.1 −3,0%); escala 1:100 confirmada pelas áreas. Assinalados (não escondidos): espaço aberto Hall 1+Sala+Cozinha+Dispensa+Hall 2+Hall 3 fundido (dividir à mão); Quarto 3+Closet fundidos; IS.2/IS.3 −24% e IS.4 −83% (resguardos de duche/banheira partem a divisão); Circulação só parcial; Alpendres = não fechados (não importados); 7 espaços fechados sem nome (roupeiros/courettes).
- Verificado: 58 testes (`python run_tests.py`); fluxo completo no Chromium (carregar → detetar → importar → planta com paredes a cinzento → resultado). Corrigidos 2 defeitos antigos: projeto novo gravava JSON sem listas (`equipment` undefined na app) e cálculo de projeto vazio dava erro 500 (agora mensagem clara).
- NÃO verificado no PC do Ordep (ligação ao computador caiu). Fazer: `git pull`, `pip install -r requirements.txt`, `python run_tests.py`, `python run_app.py`, testar o separador com o PDF.
- **Próximo:** testar com o **DWG** do Ordep (DWG é binário: converter para DXF ASCII com ODA File Converter/LibreCAD/AutoCAD, ou ler direto se houver biblioteca); reaproveitar `cad/divisoes.py` (paredes → divisões) no DXF, porque o importador DXF atual só aceita polilinhas fechadas de áreas.

## APP WEB v1 (2026-10-12, última fase)
Arrancar: `python run_app.py` → http://127.0.0.1:8765 (só localhost; dados em `projetos/<slug>/`, **ignorado pelo Git**: fazer cópia à parte).
Separadores: Divisões, Equipamentos, Alimentação/quadro (posicionar quadro clicando na planta; comprimentos manuais), Convenção (JSON editável, guardado por projeto), Resultado, Planta+circuitos (SVG), Unifilar (SVG), Material, Revisões (diff, carregar revisão antiga), DXF do arquiteto, Exportar (relatório HTML, DXF planta, DXF unifilar, JSON).
Código: `web/service.py` (lógica), `web/server.py` (HTTP stdlib), `web/relatorio.py`, `web/static/{index.html,app.js}`, `calc/material.py`, `cad/desenho.py`, `cad/dxfread.py`. 42 testes. Verificado com Chromium (Playwright): criar exemplo, editar, nova revisão, diff, importar DXF sintético.
**Limitações conhecidas (honestas):**
- DXF do arquiteto só testado com um DXF SINTÉTICO (`tests/golden/arq_dxf.py`). Falta testar com um ficheiro real: pedir ao Ordep um DXF ASCII de uma planta real. DWG/DXF binário não são lidos.
- DXF exportado: reescreve linhas/polilinhas do arquiteto (camadas ARQ-*) + camadas elétricas; NÃO reproduz textos, blocos, hatches nem arcos do arquiteto; não testado em AutoCAD.
- Importar DXF numera as divisões r1..rN pela ordem do ficheiro e substitui as atuais: equipamentos ligados a ids antigos podem ficar na divisão errada → rever após importar.
- Posições de pontos e trajetos na planta são INDICATIVAS (estrela a partir do ponto central); legenda e etiquetas junto ao quadro sobrepõem-se.
- Material: quantidades sem preços; tubagem, caixas, ATI/ITED, bornes não dimensionados.
- Sem autenticação (é local). Não expor à rede.
**Próximo:** (1) DXF real do arquiteto; (2) agentes (conforme pedido: depois da app); (3) orçamento (preços); (4) trajetos de cabo por paredes/teto em vez de estrela; (5) Icc/Zs e verificação magnética.

## Próximo passo (histórico, ver acima)
1. (feito) DXF validado visualmente pelo Ordep. Melhorar portas/janelas (abertura na parede em vez de linha sobreposta) e acrescentar pontos elétricos como dados (regenerar com `PYTHONPATH=src python -m eletro.cli draw examples/moradia_t3/projeto.json -o saida/t3_rev1.dxf`) e reportar o que falha.
2. Leitor de DXF para a ingestão (planta existente → Project, `confirmed=false`).
3. Motor de orçamento (tabela de preços, margem sobre preço, IVA, mão de obra), com o exemplo 1823,35 → 2990,29 € como teste. Só depois disso, app web.
4. Regras de pontos por divisão, quadro de cargas, unifilar: SÓ depois de dadas as UC e com fonte normativa citada.

## Visão acordada (D12)
Motor de regras+cálculo (YAML com fonte/estado) → app web de edição/recálculo/diff → orçamento. Aguarda OK do Ordep às regras A VALIDAR.

## Não fazer ainda
Agentes de memória descritiva, FV/VE, trifásico. Ver [[DECISOES]].
