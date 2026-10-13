# Estado atual
_Atualizado: 2026-10-12 (fim do dia; curso começa 19-10-2026)_

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

## APP WEB v1 (2026-10-12, última fase)
Arrancar: `PYTHONPATH=src python -m eletro.web.server 8765` → http://127.0.0.1:8765 (só localhost; dados em `projetos/<slug>/`, **ignorado pelo Git**: fazer cópia à parte).
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
