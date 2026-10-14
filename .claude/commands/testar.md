---
description: Teste guiado da app, passo a passo (plano em brain/PLANO_TESTES.md)
---
Lê brain/00_LEIA_PRIMEIRO.md, brain/ESTADO.md, brain/PLANO_TESTES.md e brain/RESULTADOS_TESTES.md. Corre `python run_tests.py` e `git log --oneline -3` e diz em 3 linhas: commit atual, resultado dos testes automáticos, próximo passo do plano por fazer (primeiro passo com estado "—" na sessão aberta; se não houver sessão aberta, cria "Sessão N" com data e commit).

Depois conduz o teste UM passo de cada vez, em português europeu:
1. Diz ao Ordep o que fazer nesse passo (só esse) e o que deve ver.
2. Espera pela resposta dele (texto ou captura de ecrã). Não avances sem resposta.
3. Compara com o esperado. Regista o resultado em brain/RESULTADOS_TESTES.md (OK / FALHA / DÚVIDA + o que foi observado).
4. FALHA: diagnostica. Bug com correção pequena → corrige com teste automático em tests/golden, `python run_tests.py`, commit e push, e pede ao Ordep para repetir o passo (`git pull`, reiniciar a app). Correção grande ou funcionalidade nova → regista em "Melhorias pedidas" e segue para o passo seguinte.
5. Ao fim de cada 2–3 passos, commit de RESULTADOS_TESTES.md.

Regras: segue o CLAUDE.md; não construas funcionalidades novas nesta sessão; sê direto e aponta o que está mal mesmo que o Ordep não o tenha notado. No fim, corre /handoff.
