# UC01995 - Implementar circuitos com semicondutores

> Material de estudo (explicação + exemplos). Não é fonte normativa. Valores de componentes (Vf, correntes máximas) vêm do datasheet.

## 1. Díodo
- Junção PN. Polarização direta conduz após a tensão limiar: ~0,7 V (silício), ~0,3 V (Schottky), 1,8-3,3 V (LED conforme a cor).
- Polarização inversa: bloqueia até à tensão de rutura.
- Parâmetros a ler no datasheet: I_F (corrente direta máxima), V_RRM (tensão inversa máxima), V_F.
- Díodo Zener: usado em polarização inversa na zona de rutura para fixar tensão (regulação simples).
- Díodo de roda livre: em paralelo com bobinas (relés, contactores DC) para absorver a sobretensão na abertura.

## 2. LED: cálculo da resistência série
R = (U_alim − V_F) / I_F

**Exemplo resolvido 1:** alimentação 12 V, LED vermelho V_F = 2 V, I_F = 20 mA.
- R = (12 − 2)/0,02 = 500 Ω → valor normalizado E12 mais próximo acima: **560 Ω**.
- I real = 10/560 = 17,9 mA.
- P_R = I²·R = 0,0179²·560 = 0,18 W → usar resistência de **1/2 W** (a de 1/4 W trabalharia a 72% da sua potência).

## 3. Retificação
- **Meia onda**: 1 díodo; só conduz um semiciclo; ripple elevado; usado em baixas correntes.
- **Onda completa com ponte (4 díodos)**: conduzem dois díodos de cada vez; perde-se 2 x 0,7 V.
- Valor médio sem filtro (ponte): U_dc ≈ 0,9·U_ef − 1,4 V. Com condensador de filtro, a tensão sobe para perto do pico.
- Ripple (aprox.) com condensador de filtro: ΔV ≈ I / (f_rip · C), onde f_rip = 100 Hz em onda completa (rede de 50 Hz).

**Exemplo resolvido 2 (fonte linear simples):** secundário 12 V ef, ponte retificadora, carga 0,5 A, C = 2200 µF.
- U_pico = 12·√2 = 16,97 V; menos 1,4 V dos díodos → ~15,6 V no pico.
- ΔV = 0,5/(100·2200e-6) = 2,27 V → a tensão varia entre ~13,3 V e 15,6 V.
- Um regulador 7809 (9 V) precisa de uma tensão de entrada ≥ ~11 V (queda mínima de ~2 V): fica com folga.
- Dissipação no regulador (pior caso, entrada 15,6 V): P = (15,6 − 9)·0,5 = 3,3 W → exige **dissipador**.
- Dimensionar o díodo da ponte: I_F ≥ 2 x corrente de carga (picos de carga do condensador) e V_RRM ≥ 2 x U_pico (≥ 50 V; 1N400x ou ponte 1-2 A).

## 4. Transístor como interruptor (introdução)
- BJT NPN em corte (I_B = 0) ou saturação (I_B suficiente): I_B ≥ I_C/β_mín com folga de 2 a 5 vezes.
- Exemplo: comandar um relé de 12 V / 50 mA com BJT de β_mín = 100: I_B ≥ 0,5 mA; com fator 5: 2,5 mA. Com saída de microcontrolador de 5 V e V_BE = 0,7 V: R_B = (5 − 0,7)/2,5 mA = 1,72 kΩ → 1,5 kΩ. Díodo de roda livre em paralelo com o relé.

## 5. Erros comuns
- Ligar LED sem resistência série.
- Esquecer a polaridade (díodo, eletrolítico).
- Ignorar a dissipação térmica em reguladores lineares (a potência perdida é (U_in − U_out)·I).
- Ponte retificadora com tensão inversa insuficiente para o pico da rede.

## 6. Exercícios (com resultados)
1. LED verde V_F = 2,2 V, 10 mA, alimentação 5 V: R? **R: 280 Ω → 270 Ω ou 330 Ω**
2. Retificador de meia onda, 24 V ef de entrada: tensão de pico e valor médio sem filtro. **R: 33,9 V (menos 0,7 V de díodo); média ≈ 0,318·33,2 = 10,6 V**
3. Zener 5,1 V alimentado por 12 V através de resistência com carga de 20 mA e corrente mínima de Zener 5 mA: R? **R: (12 − 5,1)/0,025 = 276 Ω → 270 Ω; P_R = 6,9²/270 ≈ 0,18 W; P_Z = 5,1 V x até 25,5 mA = 130 mW (sem carga)**

## 7. Fontes externas sugeridas
- All About Circuits, vol. III (semicondutores).
- electronics-tutorials.ws: díodos, retificadores, fontes de alimentação.
- Datasheets (1N4007, 7809, BC547, 2N2222) disponíveis gratuitamente nos fabricantes.
- PDF do referencial da UC (ANQEP).
