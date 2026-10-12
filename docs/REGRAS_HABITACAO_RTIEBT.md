# Regras extraídas do RTIEBT para habitação (para confirmação do Ordep antes de codificar)
Fonte: Portaria 949-A/2006 consolidada, versão à data de 19-8-2015 (com Portaria 252/2015), PDF em `sources/normativas/`. Páginas = "Pág. X de 169" do PDF.
Estado: EXTRAÍDAS, NÃO CODIFICADAS. Cada linha só vira regra no código depois de confirmada.

## A. Texto oficial confirmado (secção 801.5 e 801.1.1.3)
| Ref. | Regra | Pág. |
|---|---|---|
| 801.1.1.3.3 | Instalação sem recetores trifásicos e ≤ 10,35 kVA (45 A, 230 V): monofásica. Acima de 10,35 kVA: trifásica (monofásica só com acordo do distribuidor). Repartir potências pelas fases, tanto quanto possível equilibradas. | 114-115 |
| 801.1.1.3.1 | Esquema de ligação à terra em regra TT (TN só se a rede pública for TN). | 115 |
| 801.5.2.1 | Se TN em habitação: TN-S, com proteção por diferenciais; neutro ligado à ligação equipotencial principal a montante dos diferenciais. | 142 |
| 801.5.2.2 | Potências mínimas de dimensionamento: monofásico 3,45 kVA (1 compartimento), 6,90 kVA (2 a 6 compartimentos), 10,35 kVA (mais de 6). Com recetores trifásicos: 6,90 kVA (até 6 comp.), 10,35 kVA (mais de 6), trifásico. | 142 |
| 801.5.3 | Circuitos finais em regra monofásicos; máx. 8 pontos de utilização por circuito (2 ou mais tomadas 16 A agrupadas num aparelho contam 1); aparelhos fixos de climatização em circuitos próprios, máx. 5 aparelhos por circuito. | 143 |
| 801.5.4.1 | Diferenciais com IΔn ≤ 0,5 A podem garantir proteção contra incêndio. | 143 |
| 801.5.5.1 | Proteção contra sobreintensidades por disjuntores (fusíveis só para canalizações que alimentem outros quadros ou 1 aparelho de potência elevada, e sinalização/medição). | 143 |
| 801.5.6.1 | Com disjuntor de entrada com função diferencial: resistência de terra das massas < 100 Ω; se não for possível, diferenciais adequados à resistência de terra efetiva. | 143 |
| 801.5.6.2 | Todos os circuitos com condutor de proteção (quadros, tomadas, massas dos aparelhos). | 143 |
| 801.5.6.4 | Tomadas ≤ 16 A com obturadores; > 16 A com tampa e só as necessárias. | 143 |
| 801.5.8 | Secções mínimas por tipo de circuito (tabela, ver B). Exceção: 1,5 mm² para tomadas em circuitos de iluminação se (a) comandadas por dispositivo independente ou pelo comando da iluminação do compartimento e (b) o compartimento tiver climatização fixa distinta. | 143 |
| 801.5.9 | Corte automático por diferenciais em todas as partes da instalação; ou disjuntor de entrada com diferencial, ou diferenciais nos circuitos com a parte a montante em classe II. | 143-144 |
| 801.5.10 | Rede aérea: recomenda-se proteção contra sobretensões atmosféricas na origem. | 144 |
| 801.1.1.1 | Potências mínimas e fatores de utilização e simultaneidade "fixados de acordo com as necessidades"; **não há coeficientes numéricos**. | 114 |

## B. Dados que NÃO estão no PDF consolidado (193 tabelas/figuras aparecem como "ver documento original")
- **Quadro das secções mínimas (801.5.8).** Da edição anotada de 2000: iluminação 1,5; tomadas 2,5; termoacumuladores 2,5; máquinas de lavar/secar roupa ou loiça 2,5; fogões 4; climatização ambiente 2,5 (mm²). POR CONFIRMAR no DR original (a tabela de 2006 pode ter mudado).
- **Quadros de correntes admissíveis 52-C1 a 52-C14, fatores 52-D e 52-E.** Lidos da edição de 2000 (ver `src/eletro/calc/cabos.py`). POR CONFIRMAR.

## C. O que o RTIEBT NÃO diz (nas partes lidas) e por isso não pode ser "regra por defeito" normativa
- **Número mínimo de tomadas, pontos de luz e interruptores por divisão.** Não encontrei na secção 801.5. Terá de vir de outra fonte (guia técnico da DGEG/CERTIEL, norma de dimensionamento, ou convenção de projeto assumida e identificada como tal).
- **Fatores de simultaneidade e potência de cálculo para habitação** (801.1.1.1 remete para "as necessidades").

## D. Aviso sobre a anotada
`RTIEBT_anotada_slideshare` é a **Edição de 2000** (cabeçalho das páginas). Serve como apoio de leitura; as secções devem ser comparadas com a Portaria de 2006/2015.
