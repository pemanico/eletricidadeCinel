# UC04685 - Efetuar o projeto técnico de uma ITED

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Os elementos obrigatórios do projeto, as quantidades mínimas, as ocupações e os limites de atenuação vêm do **Manual ITED** (ANACOM): confirmar na edição em vigor. **Só um técnico de projeto ITED inscrito/registado na ANACOM pode assinar o projeto e o termo de responsabilidade**: confirmar os requisitos de acesso atuais.

## 1. Papel do projeto ITED
- Define toda a infraestrutura de telecomunicações do edifício antes da obra: percursos, tubagens, caixas, armários, cabos, tomadas, terras e ensaios.
- É um **documento técnico e legal**: acompanha o processo de licenciamento (quando aplicável) e orienta a empresa instaladora; o técnico de projeto responde por ele.
- Deve ser **coerente com os projetos de arquitetura, estabilidade e eletricidade**: o ATI, as prumadas e as caixas ocupam espaço e precisam de acessos.

## 2. Conteúdo típico do projeto
1. **Memória descritiva e justificativa:** descrição do edifício (tipologia, número de frações, pisos), soluções adotadas, conformidade com o manual.
2. **Cálculos justificativos:**
   - **Dimensionamento das tubagens** (número e diâmetro, taxa de ocupação).
   - **Balanço de atenuação** das redes: coaxial, fibra (e cobre quando aplicável).
   - **Níveis de sinal** nas tomadas (quando há distribuição de TV).
   - **Número de tomadas, cabos e fibras** por fração conforme o manual.
3. **Peças desenhadas:**
   - **Plantas** de cada piso com percursos de tubagens, caixas, tomadas e armários.
   - **Esquemas verticais** (prumadas) e **de ligações** (ATE, ATI).
   - **Cortes e pormenores** (armários, caixas de entrada).
   - **Esquema de terras** e equipotencialidade.
4. **Medições e estimativa orçamental** (mapa de quantidades, lista de materiais).
5. **Termo de responsabilidade** do técnico de projeto e **declarações** exigidas.
6. **Plano de ensaios** (quais ensaios e que valores de aceitação).

## 3. Fluxo de trabalho do projetista
1. **Recolher elementos:** plantas de arquitetura, número de frações, pisos, localização do local técnico, ligação à rede exterior.
2. **Consultar o manual** para a tipologia (moradia unifamiliar, bloco de apartamentos, comércio, misto) e extrair requisitos mínimos.
3. **Definir percursos** (caixa de entrada → ATE → prumadas → ATI → tomadas), em articulação com os outros projetistas.
4. **Dimensionar** (tubos, caixas, armários, cabos, fibras e atenuações).
5. **Desenhar** (CAD) com simbologia e legendas conforme o manual.
6. **Rever e coordenar** com arquitetura e eletricidade (conflitos de espaço, alturas, ventilação).
7. **Entregar** e acompanhar a obra (compatibilizações, alterações com registo).

## 4. Exemplo de dimensionamento de tubagem (didático)
Edifício de 6 frações; da caixa de entrada para o ATE e deste para os ATI das frações.
- Cabos por fração (exemplo ilustrativo): 2 fibras (em cabo de fibra), 1 cabo coaxial e 2 cabos de pares Cat 6, no troço ATE → ATI. Os números reais vêm do manual.
- **Prumada para 6 frações:** 6 cabos de fibra (um por fração), 6 coaxiais, 12 Cat 6 → 24 cabos (diâmetros diferentes).
- Calcular a **área total dos cabos** (soma das secções) e dividir pela taxa de ocupação máxima para obter a **secção interior mínima do tubo**; escolher o diâmetro normalizado seguinte, **ou distribuir por vários tubos** (por exemplo, um por tipo de cabo).
- Prever **tubos de reserva** para crescimento e para novas tecnologias.

*Exemplo numérico:* 12 cabos Cat 6 (Ø 6,5 mm → 33,2 mm²) + 6 coaxiais (Ø 7 mm → 38,5 mm²) + 6 cabos de fibra (Ø 6 mm → 28,3 mm²) = 398 + 231 + 170 = **799 mm²** de cabos. Com ocupação de 40%: secção interior mínima = 799/0,4 = **1 998 mm²** (≈ Ø 50 mm de diâmetro interior). Dividir por vários tubos (por exemplo, 2 tubos Ø63 e 1 de reserva) é, na prática, mais fácil de puxar e de manter (confirmar a taxa e as regras do manual).

## 5. Exemplo de balanço de atenuação (fibra, canal de fração)
- Cabo de 80 m (OS2, 0,35 dB/km): 0,028 dB.
- Conectores: 2 x 0,5 = 1,0 dB; emendas: 2 x 0,1 = 0,2 dB.
- **Total ≈ 1,23 dB**, a comparar com o **limite do manual** para este tipo de ligação. O projeto inclui esta verificação para o pior caso (fração mais distante).

## 6. Desenho e simbologia
- **CAD:** AutoCAD, LibreCAD ou outros; plantas com camadas por tipo (tubagem, cablagem, tomadas, armários).
- **Legenda de símbolos** conforme o manual; **numeração** de tomadas e cabos coerente entre plantas, esquemas e fichas de ensaio.
- **Escalas:** plantas a 1:50 ou 1:100; pormenores a escalas maiores.
- **Esquemas de princípio** (diagramas de blocos) e **esquemas verticais** que mostram as prumadas.
- Ligação à UC03077 (desenho técnico de esquemas elétricos).

## 7. Orçamento do projeto e da obra
- **Mapa de quantidades:** metros de tubo por diâmetro, metros de cabo por tipo, número de caixas, armários, tomadas, painéis, conectores, pigtails, emendas, etiquetas, horas de mão de obra e ensaios.
- **Ligação com a UC00666 (orçamentação):** custos unitários, margem, riscos, prazos, e IVA aplicável; separar claramente materiais, mão de obra e ensaios.

## 8. Erros comuns do projeto
- Não coordenar com arquitetura/estabilidade (armário sem espaço, tubos que não passam).
- Dimensionar tubos sem margem de reserva ou sem verificar a ocupação máxima.
- Esquecer os cálculos de atenuação ou os níveis de sinal.
- Usar uma edição desatualizada do manual.
- Quantidades de tomadas e cabos por fração abaixo do exigido.
- Não prever a alimentação elétrica e a terra dos armários.
- Plantas e esquemas incoerentes (numeração diferente entre desenhos).

## 9. Exercícios (com resultados)
1. 8 cabos Cat 6 (Ø 6,5 mm) num tubo com ocupação de 40%: diâmetro interior mínimo? **R: área = 8·33,2 = 265,6 mm²; /0,4 = 664 mm²; Ø = √(4·664/π) = 29 mm (tubo de Ø 32 mm exterior pode não bastar: escolher o diâmetro normalizado seguinte e confirmar o interior).**
2. Cabo coaxial de 45 m com 20 dB/100 m e um distribuidor de 7,5 dB: atenuação total? **R: 9 + 7,5 = 16,5 dB.**
3. Fibra de 120 m, 2 conectores de 0,5 dB, 1 emenda de 0,1 dB, 0,35 dB/km: atenuação? **R: 0,042 + 1,0 + 0,1 = 1,14 dB.**
4. Porque se prevê tubo de reserva? **R: crescimento e novas tecnologias sem partir paredes.**

## 10. Fontes externas sugeridas
- **ANACOM, Manual ITED:** requisitos de projeto, elementos mínimos, esquemas tipo e modelos de documentos.
- ANACOM: lista de requisitos de acesso à atividade de técnico de projeto e de entidade instaladora.
- Guias de projeto e simbologia de fabricantes (Legrand, Schneider, Nexans, Prysmian, CommScope).
- Software: AutoCAD/LibreCAD; folhas de cálculo para balanços e ocupações.
- PDF do referencial da UC (ANQEP).
