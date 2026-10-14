# Resultados dos testes manuais
Plano: [[PLANO_TESTES]]. Uma linha por passo. Estado: OK / FALHA / DÚVIDA / —(não feito).

## Sessão 1
_Data: 2026-10-14 · Máquina: PC do Ordep (Windows, VS Code, PowerShell) · Commit testado: 6619b86_

| Passo | Estado | Observado | Ação (commit / melhoria) |
|---|---|---|---|
| 0 Arranque | OK | Commit 6619b86; 83 OK, 0 FALHA; app abre em 127.0.0.1:8765 sem traceback. Visto pelo Claude: aviso pypdfium2 "PdfDocument still open" no fim dos testes (pdfread.py abre o PDF e não fecha) | ver passo 2 |
| 1 Exemplo T3 | OK | teste-t3: 5 divisões; banner NÃO UTILIZÁVEL, tabelas Circuitos e Quadro elétrico, geral 45 A; Planta + circuitos e Unifilar desenham | |
| 2 PDF → divisões | OK (com nota) | Leitura rápida; 13 divisões fechadas; escala confirmada; 13 linhas importadas; escala 50 → "NÃO confirmada". Fusões esperadas confirmadas (Hall 1+Sala+Cozinha+Despensa+Hall 2+Hall 3). Não reportado: contagem "X de 11 a ±3%". Visto pelo Claude no código: com escala errada o **Importar deixava passar** áreas ×4 (só "por confirmar") | Corrigido: Importar recusa escala errada + PDF fechado após leitura (fim do aviso PdfDocument). 2 testes novos, 85 OK. Repetição do 2.5: "NÃO confirmada (0 de 12 a ±3% · sugerida **1:116**)" → FALHA: divisões fundidas puxavam a mediana. Corrigido: sugestão escolhe a escala usual que põe mais divisões a ±3% (planta real a 1:50 → 1:100). +2 testes (um com a planta real), 87 OK. **Repetido após git pull: OK** (sugerida 1:100; Importar recusado; divisões mantidas) |
| 3 Quadro | OK | Adaptado: Hall 1 não existe (fundido), QE posto na divisão fundida; Resultado recalcula sem erro ("tudo de acordo"; nome da divisão fundida não reportado) | depende de "dividir divisões" para pôr o QE no Hall 1 real |
| 4 Aparelhagem | FALHA (resultado) | 4.1–4.9 sem falhas na interação. **4.0: divisão fundida (Hall 1+Sala+Cozinha+Despensa+Hall 2+Hall 3) ficou com uso "hall"**; 4.2: 12 pontos. A convenção "hall" dá 1 tomada por 100 m²: o open space de ~70 m² fica com ~1 tomada em vez de ~18 (sala) — subdimensiona circuitos e quadro sem aviso. Causa: `divisoes.py` usa `uso_por_nome(nomes[0])` | decisão pedida ao Ordep (ver conversa) |
| 5 Cálculos e quadro | — | | |
| 6 Equipamentos | — | | |
| 7 Tabela de alturas | — | | |
| 8 Saídas | — | | |
| 9 Robustez | — | | |

## Melhorias pedidas durante os testes (não implementar na sessão de testes)
- **Botão "Novo" pouco visível** (passo 2): o Ordep não o encontrou na barra de cima; está entre a lista pendente e "Exemplo T3", com o mesmo estilo dos outros. Sugestão: rótulo "+ Novo projeto", destacado; e trocar o `prompt()` do browser por um campo na própria página (o `prompt()` pode ser bloqueado pelo browser e não valida o identificador antes de enviar).
- **Dividir divisões fundidas / open space** (passo 2, já em "fora do âmbito" no plano): o Ordep viu Hall 1 + Sala estar/jantar + Cozinha + Despensa + Hall 2 + Hall 3 numa só divisão. Pede ferramenta para dividir, e também para distinguir zonas dentro de um open space real. Nota do Claude: não é só estético. Com a cozinha fundida na sala, a convenção não lhe aplica pontos de cozinha (forno, placa, máquinas, tomadas de bancada); e o Hall 1 (onde fica o QE) deixa de existir como divisão. Afeta os passos 3–6 e é a melhoria com mais impacto no resultado.
- **Feedback visual nos botões** (passo 2): ao carregar num botão (Detetar, Importar…) só muda o texto pequeno à direita da barra de cima. Pede popups/avisos visíveis e estado de "a trabalhar".
- **Melhorar o aspeto gráfico em geral** (passo 2): pedido genérico; precisa de ser concretizado numa sessão própria.
- **Planta-modelo editável** (passo 4, pedido do Ordep): "definir um PDF template com divisões e nome das divisões em todas; exportar como estamos a fazer mas editar a planta". Âmbito por clarificar (ver conversa 14-10): editar a geometria na app (dividir/juntar/renomear divisões) vs. exportar PDF da planta com nomes vs. modelo de PDF a pedir ao arquiteto.
