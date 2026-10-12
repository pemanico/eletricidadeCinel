# Estado atual
_Atualizado: 2026-10-12 20:55 (antes do início do curso, que começa 19-10-2026)_

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
**Ainda NÃO existe no motor:** potência de cálculo/simultaneidade; verificação de curto-circuito (Icc, poder de corte, Icc mínima: falta dado da e-Redes); diferenciais e proteção contra contactos indiretos; terras e equipotencial; quadro de cargas e unifilar; tomadas em WC (volumes); mapa de quantidades; orçamento; app web.
Limitações conhecidas: agrupamento sequencial pela ordem das divisões (iluminação percorre a casa toda numa ordem arbitrária); WC com circuito de tomadas próprio; tabelas da edição 2000 por confirmar.

## Próximo passo (por ordem)
1. (feito) DXF validado visualmente pelo Ordep. Melhorar portas/janelas (abertura na parede em vez de linha sobreposta) e acrescentar pontos elétricos como dados (regenerar com `PYTHONPATH=src python -m eletro.cli draw examples/moradia_t3/projeto.json -o saida/t3_rev1.dxf`) e reportar o que falha.
2. Leitor de DXF para a ingestão (planta existente → Project, `confirmed=false`).
3. Motor de orçamento (tabela de preços, margem sobre preço, IVA, mão de obra), com o exemplo 1823,35 → 2990,29 € como teste. Só depois disso, app web.
4. Regras de pontos por divisão, quadro de cargas, unifilar: SÓ depois de dadas as UC e com fonte normativa citada.

## Visão acordada (D12)
Motor de regras+cálculo (YAML com fonte/estado) → app web de edição/recálculo/diff → orçamento. Aguarda OK do Ordep às regras A VALIDAR.

## Não fazer ainda
App web, agentes de memória descritiva, FV/VE, trifásico. Ver [[DECISOES]].
