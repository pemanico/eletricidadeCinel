# Roadmap (ordem das UC = ordem da lista dada pelo Ordep; confirmar com o calendário real do CINEL)
Regra: um módulo só avança quando a UC foi dada e o teste foi verificado contra a fonte.

## Fase A - UC01992, 01988, 01993, 03077, 01995, 02845, 03918 (eletrónica e desenho)
Pouco valor direto para projeto de moradias. NÃO forçar módulos de eletrónica no sistema.
Trabalho útil em paralelo (independente das UC):
- schema do projeto (feito) e entrada JSON/DXF (ingest)
- **motor de orçamento**: tabela de preços de fornecedores, margem sobre preço, IVA, mão de obra (exemplo 1823,35 -> 2990,29 EUR como teste)
- UC03077: gerador de esquema unifilar (símbolos, legenda) a partir de dados
- pequena lib calc/basico.py (Ohm, série/paralelo, RLC) só para tirar dúvidas de estudo

## Fase B - UC01781, 01782 (condutores, proteções, terras)
Módulo calc/cabos (feito, tabelas a validar), queda de tensão, Icc, DDR, terras. Primeira fase com valor real.

## Fase C - UC04672, 04673, 04674, 04675 (iluminação, residencial, coletivas, industriais)
Regras por divisão (nº de pontos, circuitos), quadro de cargas, potência a contratar, unifilar de moradia T3.

## Fase D - UC01799, 04676, 01801, 03088, 01788, 04672 (FV, VE, armazenamento, conversão, contagem)
## Fase E - UC00668, 01994, 03099, 01784 (motores, automatismos, domótica, GTE)
## Fase F - UC03895, 04679, 01795, 01792 (transformadores, PT, qualidade, manutenção)
## Fase G - ITED UC04680-04685, UC00666 (orçamentos, validar motor), UC01793/04678/04677 (documentação, clientes, AVAC)
## Fase H - agentes: orquestrador, redator de memória descritiva, revisor de coerência (unifilar vs quadro vs memória)
