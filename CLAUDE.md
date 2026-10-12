# Regras do repositório
- Cálculos SEMPRE em src/eletro/calc (código). O LLM nunca calcula secções, quedas de tensão, Icc ou cargas.
- Toda a regra normativa implementada em src/eletro/rules tem de citar fonte (diploma/artigo/norma + versão) em comentário.
- Cada módulo novo traz golden tests tirados de exemplos verificados (tests/golden). Sem teste, não entra.
- Dados vindos de PDF/foto entram com confirmed=False; nada segue para saída sem confirmação humana.
- study_notes/ são material de estudo gerado por IA, NÃO fonte normativa. A fonte são os ficheiros em sources/.
- Saídas (memória, orçamento) são RASCUNHOS. Assinatura e responsabilidade: técnico habilitado.
