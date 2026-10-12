# Plano do projeto: moradia-tipo (passo 1)

## Decisões fixadas
- Caso de uso inicial: moradia unifamiliar, monofásica, BT, com ITED. Sem FV, VE nem trifásico na v1 (entram como extensões).
- Saída de desenho: **DXF** (edição final em CAD; QCAD/LibreCAD ou AutoCAD). PDF só como exportação.
- **Projetos dinâmicos**: o desenho nunca é a fonte; é sempre gerado.

## Princípio de projeto dinâmico
1. **Fonte única de verdade**: `Project` (JSON versionado). Plantas, unifilar, quadro de cargas, memória e orçamento são *vistas* geradas.
2. **Regenerável**: alterar uma divisão, um equipamento ou a potência contratada regenera tudo o que depende disso.
3. **Revisões**: cada alteração cria uma revisão (nº, data, motivo, autor). Gerar diff entre revisões (o que mudou nos circuitos, secções, preços).
4. **Edição manual protegida**: o que o técnico ajusta à mão (ex.: posição de um símbolo) fica guardado como *override* e sobrevive à regeneração; conflitos são mostrados, não apagados.
5. **Coerência automática**: o revisor compara unifilar, quadro de cargas, memória e orçamento do mesmo modelo.
6. Entradas de PDF/foto entram com `confirmed=False` e não passam para saída sem validação humana.

## Entradas necessárias (v1)
- Divisões: id, nome, uso, área, pé-direito, polígono (coordenadas), portas e janelas.
- Posição do quadro e do ponto de entrada da rede.
- Ligação: nº de fases, potência pretendida.
- Equipamentos especiais: termoacumulador, forno, placa, AVAC, outros.
- Preferências do cliente: tomadas extra, iluminação especial.

## Saídas
Desenhadas (DXF): 1) plantas de pontos por piso, 2) caminhos de cabos/tubagem e quadro, 3) unifilar, 4) terras e equipotencial, 5) esquema ITED.
Escritas: memória descritiva e justificativa, cálculos justificativos, mapa de quantidades, condições técnicas, orçamento.
Conteúdo mínimo legal de cada peça: **confirmar na DGEG**.

## Nível de automação
| Peça | Automação |
|---|---|
| Contagem de pontos por divisão (regras) | alta |
| Quadro de cargas, secções, proteções, unifilar, lista de materiais | alta |
| Colocação de símbolos na planta | proposta automática + validação humana |
| Caminhos reais de cabos | manual (depende da obra) |

## Convenções de desenho (UC03077)
Camadas por sistema (ILUM, TOM, QUADRO, ITED, TERRAS, COTAS, TEXTO), simbologia única numa biblioteca, legenda gerada, escala e carimbo com revisão. A definir ao iniciar a UC03077.

## Próximos passos (por ordem)
1. Estender o schema: polígonos, portas/janelas, equipamentos, revisões, overrides.
2. Gerador DXF mínimo: contorno das divisões + legenda (ezdxf), ligado ao `Project`.
3. Regras de pontos por divisão, só depois de dada a UC04673 e confirmadas no RTIEBT.
4. Motor de orçamento ligado ao modelo.
5. Revisor de coerência entre peças.
6. Aplicação web sobre o mesmo motor.
