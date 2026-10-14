# Resultados dos testes manuais
Plano: [[PLANO_TESTES]]. Uma linha por passo. Estado: OK / FALHA / DÚVIDA / —(não feito).

## Sessão 1
_Data: 2026-10-14 · Máquina: PC do Ordep (Windows, VS Code, PowerShell) · Commit testado: 6619b86_

| Passo | Estado | Observado | Ação (commit / melhoria) |
|---|---|---|---|
| 0 Arranque | OK | Commit 6619b86; 83 OK, 0 FALHA; app abre em 127.0.0.1:8765 sem traceback. Visto pelo Claude: aviso pypdfium2 "PdfDocument still open" no fim dos testes (pdfread.py abre o PDF e não fecha) | ver passo 2 |
| 1 Exemplo T3 | OK | teste-t3: 5 divisões; banner NÃO UTILIZÁVEL, tabelas Circuitos e Quadro elétrico, geral 45 A; Planta + circuitos e Unifilar desenham | |
| 2 PDF → divisões | — | | |
| 3 Quadro | — | | |
| 4 Aparelhagem | — | | |
| 5 Cálculos e quadro | — | | |
| 6 Equipamentos | — | | |
| 7 Tabela de alturas | — | | |
| 8 Saídas | — | | |
| 9 Robustez | — | | |

## Melhorias pedidas durante os testes (não implementar na sessão de testes)
- 
