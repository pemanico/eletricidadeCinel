# Plano de testes da app (manual, passo a passo)
_Criado: 2026-10-14. Usar com `/testar` num chat novo. Resultados em [[RESULTADOS_TESTES]]._

## Regras da sessão de testes
- **Um passo de cada vez.** O Claude explica o passo; o Ordep executa na app (PC dele, Windows) e diz o que viu; o Claude compara com o esperado e regista em [[RESULTADOS_TESTES]] (OK / FALHA / DÚVIDA + nota) antes de passar ao seguinte.
- **Testar, não construir.** Durante a sessão não há funcionalidades novas. Uma FALHA é diagnosticada; se for bug e a correção for pequena: corrigir com teste automático, `python run_tests.py`, commit. Se for grande ou for desejo novo: vai para a lista "Melhorias pedidas" em RESULTADOS_TESTES e segue-se em frente.
- **Valores esperados** abaixo vêm de verificações feitas pelo Claude na nuvem (Linux, Chromium). Diferenças no Windows são exatamente o que se quer apanhar.
- Ficheiros de teste: o PDF de alterações em obra do Ordep (o mesmo da sessão de 13-10; página 5 = piso 0). Não vão para o Git.
- A tabela de alturas real é alterada no passo 7: no fim, decidir se fica (commit) ou se se desfaz (`git checkout data/convencoes/simbolos_alturas.json`).

## Passos

### 0. Arranque
1. `git pull` na pasta `E:\Cinel\projectAI\eletricidadeCinel`.
2. Ativar o venv (`.\.venv\Scripts\Activate.ps1`; o prompt passa a começar por `(.venv)`) e `pip install -r requirements.txt`. Novas desde 13-10: pikepdf, pdfplumber, pypdfium2, numpy, scipy.
3. `python run_tests.py` → **esperado: 83 OK**, nenhuma FALHA.
4. `python run_app.py` → abre http://127.0.0.1:8765, sem erros na consola do terminal.

### 1. Exemplo T3 (sanidade)
1. "Exemplo T3", identificador `teste-t3`.
2. Separador Divisões: 5 divisões (Sala, Cozinha, Quarto 1, Quarto 2, WC).
3. Resultado: banner **NÃO UTILIZÁVEL COMO PROJETO**; tabelas Circuitos e **Quadro elétrico** presentes; geral 45 A.
4. Planta + circuitos e Unifilar desenham.

### 2. PDF do arquiteto → divisões
1. "Novo" projeto `casa`. Separador **PDF do arquiteto** → carregar o PDF de alterações (23 págs.). Esperado: lista de páginas, **página 5 marcada** ("PLANTA DO PISO 0 PROPOSTO", 1:100, piso 0, 22 áreas no quadro); leitura em ~5–10 s.
2. Paredes = `arq_corte`, Caixilhos = `arq_vista 1`, escala 100, piso 0 (já preenchidos). **Detetar**.
3. Esperado: 13 divisões fechadas; **6 de 11 a ±3%** (Garagem, Escritório, Lavandaria, Quarto 1, Quarto 2, IS.1); escala **confirmada**; erros: sala/cozinha/halls fundidos, Quarto 3+Closet fundidos, IS.2/IS.3/IS.4 abaixo do quadro; alpendres "não fechado". Pré-visualização colorida.
4. **Importar**. Divisões: 13 linhas, todas por confirmar.
5. Teste de erro: escala 50 → Detetar → deve dar erro de escala e sugerir 1:100. Voltar a 100.

### 3. Quadro
1. Alimentação/quadro ou paleta "QE" no editor: pôr o quadro no **Hall 1** (onde o arquiteto marcou QE).
2. Resultado recalcula sem erro.

### 4. Aparelhagem (planta)
1. Separador **Aparelhagem (planta)**: paredes a cinzento, divisões a bege, paleta à esquerda.
2. **Preencher pela convenção** → esperado ~87 pontos em 13 divisões; nenhum fora das paredes.
3. Zoom com a roda, arrastar o fundo, "Ajustar vista".
4. Colocar uma **Tomada uso geral** na sala → altura **0,30**; numa IS → **1,10**; na garagem → **1,10**. Interruptor → 1,10. Ponto de luz → "teto".
5. Mudar a altura de uma tomada para 0,45 → origem **MANUAL** (laranja). "Repor altura da convenção" → volta.
6. Arrastar um símbolo para outra divisão → a divisão muda; se a altura era da convenção, ajusta-se.
7. Selecionar e **Del** → apaga. Esc → larga a paleta.
8. "mostrar circuitos" → percursos tracejados e id do circuito em cada ponto.
9. Guardar nova revisão ("aparelhagem v1").

### 5. Cálculos e quadro
1. Resultado → Circuitos: coluna "pontos de" = planta; nenhum circuito de luz/tomadas com mais de 8 pontos.
2. Tabela **Quadro elétrico**: geral, DDR-1/DDR-2 com circuitos, disjuntores (curva, cabo, PE), módulos.
3. Tabela **Aparelhagem e circuitos**: cada ponto com circuito e "cabo desde o quadro"; dentro do mesmo circuito, os metros crescem.
4. Circuito manual: escolher 9 tomadas → circuito `TOM-X` → Verificações deve dar **NAO_CUMPRE 801.5.3**. Desfazer (apagar o campo).
5. Mover uma tomada para longe do quadro → o comprimento e a queda do circuito aumentam.
6. Conferir à mão UM circuito curto (quadro → 1–2 pontos): medir na planta e comparar com "cabo desde o quadro" (luz: teto; tomadas: paredes; fator 1,2).

### 6. Equipamentos
1. Equipamentos: acrescentar termoacumulador 2000 W numa IS (ou cozinha: forno).
2. No editor, pôr o símbolo correspondente (Ligação termoacumulador / Caixa de ligação) nessa divisão.
3. Resultado: circuito `EQ-…` com "pontos de" = planta; mover o símbolo muda o comprimento. Sem equipamento definido, um ponto dedicado dá AVISO.

### 7. Tabela de alturas
1. Separador **Tabela de alturas**: versão 1, histórico com "tabela inicial".
2. Mudar Tomada uso geral 0,30 → 0,40 e **Gravar sem fonte** → recusa.
3. Com fonte ("teste guiado 14-10") → versão 2, histórico com a linha.
4. Voltar ao editor: faixa "N pontos com altura de uma versão antiga" → **Reaplicar** → tomadas da convenção a 0,40; a tomada MANUAL fica.
5. Decidir: manter (commit do JSON) ou desfazer (`git checkout data/convencoes/simbolos_alturas.json` + reiniciar a app).

### 8. Saídas
1. Material: aparelhagem por tipo ("colocada na planta") + cabos por secção.
2. Exportar → Relatório HTML (banner + quadro + planta), **DXF planta** e **DXF unifilar**: abrir no programa de CAD do Ordep. Verificar camadas (ARQ-PAREDES, ELE-…, ELE-ALTURAS) e se os textos se leem.
3. Revisões: comparar rev. anterior → mostra `+ ponto …` / `~ ponto ….height_m`.

### 9. Robustez
1. PDF do arquiteto: carregar um ficheiro que não é PDF → mensagem "não é um PDF", sem erro interno.
2. Projeto novo vazio → Resultado com mensagem clara ("sem divisões"), não erro 500.
3. Fechar e reabrir a app → o projeto `casa` mantém-se com a última revisão.

## Fora do âmbito destes testes (limitações conhecidas)
Dividir divisões fundidas na app; Icc/Zs/disparo magnético; tabelas ed. 2000 por confirmar; símbolos sem rotação; vários pisos sobrepostos na "Planta + circuitos"; DWG.
