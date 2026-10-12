# Roadmap (ligado aos blocos de UC; reordenar conforme o calendário real do CINEL)
| Fase | Quando | Módulo de software | UCs | Critério de pronto |
|---|---|---|---|---|
| 0 | semana 1 | schema + cabos (feito) | 01781 | golden tests passam |
| 1 | ao dar UC01781/04673 | quadro de cargas + circuitos de moradia (regras por divisão) + unifilar textual | 01781, 04673, 03077 | T3 de exemplo gera quadro de cargas e lista de circuitos |
| 2 | UC01782 | terras, DDR, Icc mínima/máxima | 01782 | verifica exemplos de haste e proteção |
| 3 | UC04672 | iluminação (método dos lúmens) | 04672 | escritório exemplo = 8 luminárias |
| 4 | ITED (04680-04685) | ITED: tubagem, ATI/ATE, cabos | 04680..85 | enchimento de tubos e esquema ITED |
| 5 | ao longo do curso | **tabela de preços + orçamento** (margem sobre preço, IVA) | 00666 | exemplo 1823,35→2990,29 € reproduzido |
| 6 | meio do curso | FV, VE, armazenamento | 01799, 04676, 01801 | dimensionamento + verificação |
| 7 | depois | ingest DXF e PDF | — | salas extraídas, `confirmed=False` |
| 8 | depois | agentes: orquestrador, redator (memória descritiva), revisor de coerência | todas | revisor deteta incoerência injetada |
Regra: não avançar fase sem a UC dada e sem o teste verificado contra a fonte.
