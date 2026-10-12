# Registo de decisões (não reabrir sem motivo novo)
| # | Data | Decisão | Porquê |
|---|---|---|---|
| D1 | 2026-10 | Um caderno NotebookLM por bloco de UC; as notas em `study_notes/` são apoio, não normativas. Fontes normativas (RTIEBT, manual ITED/ANACOM, DGEG, e-Redes) em `sources/`. | Citações rastreáveis; notas geradas por IA podem ter erros. |
| D2 | 2026-10 | Cálculos sempre em código (`src/eletro/calc`), nunca pelo LLM. | Erro real: tabela de 4 mm² dada como 32 A (correto 28 A) levou a 3G4 em vez de 3G6. |
| D3 | 2026-10 | Caso de uso v1: moradia-tipo unifamiliar, monofásica, BT, com ITED. Sem FV/VE/trifásico. | Foco; é o caso mais comum numa atividade paralela. |
| D4 | 2026-10 | Saída de desenho: DXF (edição final em CAD). PDF só exportação. | Permite acabamento manual. |
| D5 | 2026-10 | Projetos dinâmicos: `Project` JSON é a fonte única; desenhos/quadros/orçamento são vistas geradas; ajustes manuais em `overrides` com `base`; conflito é mostrado, nunca apagado; revisões versionadas. | Pedido explícito do Ordep: projetos sempre dinâmicos. |
| D6 | 2026-10 | Software calcula e valida; agentes orquestram, leem documentos e redigem; humano decide e assina. | Fiabilidade e responsabilidade. |
| D7 | 2026-10 | Ordem das UC = ordem da lista dada pelo Ordep (a confirmar com o calendário real). As 7 primeiras UC (eletrónica) não geram módulos de software. | Evitar software sem valor; usar esse tempo para orçamento e ingestão. |
| D8 | 2026-10 | Saídas são RASCUNHOS não assinados até estar claro o que a carteira/exame permite. Dados de PDF/foto entram `confirmed=false`. | Habilitação para assinar projetos NÃO é automática. |
| D9 | 2026-10 | Primeira versão com valor comercial: motor de orçamento, antes do gerador de projeto. App web só quando o motor existir. | Orçamento não depende de assinatura nem de UC de dimensionamento. |
| D10 | 2026-10 | Cérebro = pasta `brain/` no repo (cofre Obsidian). Uma só fonte de verdade. | Evitar três cópias divergentes (memória, Project, repo). |
| D11 | 2026-10-12 | O Claude mantém o cérebro atualizado por iniciativa própria, sem pedir autorização. | Instrução do Ordep: "sempre que precisares atualiza o cérebro". |
| D12 | 2026-10-12 | Objetivo final: projeto gerado automaticamente com regras por defeito e todos os cálculos; app web para editar e regenerar com novos cálculos e diff. Regras entram como DADOS (YAML) com fonte e estado A VALIDAR/VALIDADA; todas as saídas listam as regras ainda não validadas. Comprimentos de cabo estimados pela geometria (sobreponíveis). Ordem: motor (sem UI) → app web → orçamento. | Pedido do Ordep; evitar regras normativas de memória apresentadas como verdade (erro dos 4 mm²). **Pendente: confirmação do Ordep de que aceita regras A VALIDAR.** |
| D12 | 2026-10-12 | Objetivo final: projeto calculado AUTOMATICAMENTE com as regras por defeito do RTIEBT e todos os cálculos; app web onde o Ordep altera dados e o sistema recalcula e emite novo projeto (nova revisão). | Pedido explícito do Ordep. Regras só a partir do texto da Portaria 949-A/2006 consolidada (não de memória), codificadas como dados com artigo citado + testes. |

