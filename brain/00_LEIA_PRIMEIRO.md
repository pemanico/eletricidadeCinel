# Cérebro do projeto eletricidadeCinel
Fonte única de verdade para qualquer chat novo (Claude Code, claude.ai, ou tu). Cofre Obsidian: abre a pasta `brain/` no Obsidian (links `[[...]]`).

## Ordem de leitura num chat novo
1. [[ESTADO]] — onde estamos e qual é o próximo passo (SEMPRE atualizado)
2. [[DECISOES]] — o que ficou decidido e porquê (não reabrir sem motivo)
3. [[DUVIDAS_ABERTAS]] — o que falta confirmar (legal, calendário, validações)
4. [[PROGRESSO_UC]] — UC dadas, módulos de software ligados
5. [[ARMADILHAS]] — erros já cometidos e limitações do ambiente
6. [[GLOSSARIO]] — termos e siglas
Contexto técnico: `README.md`, `ROADMAP.md`, `docs/PLANO_PROJETO.md`, `docs/AGENTES.md`, `CLAUDE.md`.

## Quem és tu e como trabalhamos
- Ordep, Lisboa, comunicação em português europeu. Curso EFA Técnico/a de Instalações Elétricas, CINEL, 19-10-2026 a 31-07-2028, 1545 h, pós-laboral.
- Objetivo: estudar e construir, módulo a módulo, um sistema de software + agentes que ajude a montar projetos, orçamentos e propostas para moradias; uso como atividade paralela.
- Estilo pedido: debate como adulto, questionar ideias, apontar falhas e pontos cegos, mostrar oportunidades, sem validações desnecessárias. Passo a passo.
- Perfil técnico: engenharia de dados (PySpark, Oracle SQL, Node.js/TypeScript). Usa agentes e Claude Code.

## Regra de manutenção
**Instrução permanente do Ordep: o Claude atualiza o cérebro sempre que for preciso, sem pedir autorização** (estado, decisões, dúvidas, progresso, armadilhas), com commit e push. O Ordep não tem de lembrar.
No fim de cada sessão: atualizar [[ESTADO]] (e [[DECISOES]]/[[DUVIDAS_ABERTAS]] se mudaram), fazer commit. Comando: `/handoff`. No início: `/retomar`.
