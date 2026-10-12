# Agentes e software: como se dividem
Princípio: **o software calcula e valida; os agentes orquestram, leem documentos e redigem; o humano decide e assina.**

| Camada | Responsabilidade | Onde |
|---|---|---|
| Modelo (fonte única) | Project, revisões, overrides | src/eletro/schema |
| Cálculo | cabos, (futuro) cargas, Icc, iluminação | src/eletro/calc |
| Regras normativas | só com fonte citada e teste | src/eletro/rules |
| Vistas | planta DXF (futuro: unifilar, orçamento, memória) | src/eletro/cad, docs |
| CLI | interface comum humano/agente | src/eletro/cli.py |
| Agentes | ingestão, rascunho, revisão | .claude/agents |

## Agentes (v1)
- **ingestao-planta**: planta → JSON, tudo `confirmed=false`, lista de dúvidas.
- **projetista-rascunho**: valida, aplica alterações com revisão, gera DXF e diff.
- **revisor-coerencia**: só leitura; incoerências por gravidade.
Futuros: orçamentista (quando o motor de preços existir), redator de memória descritiva (quando houver cálculos e regras com fonte).

## Limites conhecidos
- O DXF próprio (R12) foi validado estruturalmente em testes, ainda não aberto em QCAD/AutoCAD: abrir e dizer o que falha.
- Os agentes são definições para Claude Code (usar no repo). A aplicação web terá de chamar o mesmo núcleo via API (fase posterior).
- Regras de pontos por divisão, cargas e unifilar NÃO estão implementadas: dependem das UC e da validação normativa.
