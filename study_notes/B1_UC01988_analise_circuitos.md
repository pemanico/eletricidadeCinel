# UC01988 - Analisar o funcionamento de circuitos elétricos e eletrónicos

> Material de estudo (explicação + exemplos). Não é fonte normativa.

## 1. Leis fundamentais
- **Ohm:** U = R·I.
- **Kirchhoff das correntes (LKC):** a soma das correntes num nó é zero (o que entra = o que sai).
- **Kirchhoff das tensões (LKT):** a soma das tensões numa malha fechada é zero.
- **Potência:** P = U·I. Num circuito, potência fornecida = potência dissipada (balanço de potências).

## 2. Divisores
- Tensão (série): U_Rk = U · Rk/Rt.
- Corrente (paralelo, duas resistências): I1 = I · R2/(R1+R2) (a corrente maior vai para a resistência menor).

## 3. Métodos de análise
1. **Redução série/paralelo** (circuitos simples).
2. **Malhas** (LKT) ou **nós** (LKC), com sistema de equações.
3. **Superposição**: com várias fontes, calcula-se o efeito de cada uma (as outras fontes de tensão em curto-circuito, as de corrente em aberto) e somam-se. Só vale em circuitos lineares e **não** se aplica à potência.
4. **Thévenin**: qualquer parte linear vista de dois terminais equivale a Uth em série com Rth. Uth = tensão em aberto; Rth = resistência vista com as fontes anuladas.
5. **Máxima transferência de potência**: RL = Rth, com P_max = Uth²/(4·Rth) (rendimento de 50%, por isso não se usa em energia, só em sinal).

## 3.1 Exemplo resolvido (redução + Thévenin)
Fonte 12 V; R1 = 4 Ω em série com (R2 = 6 Ω ∥ R3 = 3 Ω).

**Redução:**
- R2∥R3 = 6·3/9 = 2 Ω; Rt = 4 + 2 = 6 Ω
- I = 12/6 = 2 A (corrente em R1)
- U no paralelo = 2·2 = 4 V
- I2 = 4/6 = 0,667 A; I3 = 4/3 = 1,333 A (soma = 2 A ✓)
- Balanço de potências: fonte 12·2 = 24 W; R1: 2²·4 = 16 W; R2: 0,667²·6 = 2,67 W; R3: 1,333²·3 = 5,33 W; total 24 W ✓

**Thévenin visto por R3:** retira-se R3.
- Uth = 12 · 6/(4+6) = 7,2 V
- Rth = 4∥6 = 2,4 Ω
- I3 = 7,2/(2,4+3) = 1,333 A ✓ (igual ao método anterior)

## 3.2 Exemplo resolvido (malhas)
Duas malhas: malha 1 com fonte 10 V, R1 = 2 Ω, R3 = 4 Ω (ramo comum); malha 2 com fonte 6 V, R2 = 3 Ω, R3 = 4 Ω (ramo comum). Correntes de malha I1 e I2 no mesmo sentido (horário).
- Malha 1: 10 = (2+4)·I1 − 4·I2 → 6·I1 − 4·I2 = 10
- Malha 2: −6 = −4·I1 + (3+4)·I2 → −4·I1 + 7·I2 = −6
- Resolução: de (1) I1 = (10 + 4·I2)/6. Em (2): −4(10+4·I2)/6 + 7·I2 = −6 → −6,667 − 2,667·I2 + 7·I2 = −6 → 4,333·I2 = 0,667 → I2 = 0,154 A; I1 = 1,769 A.
- Corrente em R3 = I1 − I2 = 1,615 A.

## 4. Erros comuns
- Trocar o sentido da queda de tensão ao aplicar LKT (definir sempre o sentido da malha e ser consistente).
- Aplicar superposição à potência.
- Esquecer que um voltímetro real tem resistência finita e altera o circuito que mede.
- Em Thévenin, esquecer de anular as fontes antes de calcular Rth.

## 5. Exercícios (com resultados)
1. 24 V em série com 100 Ω, 200 Ω e 300 Ω: corrente e tensão em cada uma. **R: 40 mA; 4 V, 8 V, 12 V**
2. Corrente total de 3 A dividida entre 6 Ω e 12 Ω em paralelo: correntes. **R: 2 A e 1 A**
3. Fonte 20 V, Rth interno de 5 Ω: qual a RL para máxima potência e qual é essa potência? **R: 5 Ω; 20²/(4·5) = 20 W**

## 6. Fontes externas sugeridas
- All About Circuits, vol. I (DC), capítulos de análise de rede (malhas, nós, Thévenin).
- MIT OpenCourseWare 6.002 Circuits and Electronics (aulas e notas gratuitas).
- Simulação para confirmar resultados: LTspice (gratuito) ou Falstad.
- PDF do referencial da UC (ANQEP).
