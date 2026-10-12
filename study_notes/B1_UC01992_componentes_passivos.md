# UC01992 - Implementar circuitos com componentes eletrónicos passivos

> Material de estudo (explicação + exemplos). Não é fonte normativa. Valores de catálogo (tolerâncias, séries, tensões máximas) devem ser confirmados no datasheet do componente.

## 1. Resistências
- Lei de Ohm: U = R·I. Potência: P = U·I = R·I² = U²/R.
- Associação em série: Rt = R1 + R2 + ... (a corrente é comum).
- Associação em paralelo: 1/Rt = 1/R1 + 1/R2 + ... (a tensão é comum). Para duas: Rt = R1·R2/(R1+R2).
- Código de cores (4 bandas): 1.º dígito, 2.º dígito, multiplicador, tolerância. Ex.: castanho-preto-vermelho-dourado = 10 x 10^2 = 1 kΩ ±5%.
- Séries normalizadas: E12 (±10%), E24 (±5%), E96 (±1%). Valores E12: 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82.
- Potência nominal comum: 1/4 W, 1/2 W, 1 W. Regra prática: dimensionar para dissipar no máximo 50% da potência nominal.

### Divisor de tensão
Uout = Uin · R2/(R1+R2) (sem carga). Com carga RL em paralelo com R2, usar R2∥RL.

### Exemplo resolvido 1
Uin = 12 V, R1 = 10 kΩ, R2 = 5 kΩ.
- Uout = 12 · 5/(10+5) = 4 V
- I = 12/15k = 0,8 mA
- P(R1) = I²·R1 = (0,0008)²·10000 = 6,4 mW; P(R2) = 3,2 mW. Qualquer resistência de 1/4 W serve.
- Se ligares uma carga de 5 kΩ à saída: R2∥RL = 2,5 kΩ, Uout = 12·2,5/12,5 = 2,4 V. A tensão cai de 4 V para 2,4 V. **Erro comum: ignorar o efeito da carga num divisor.**

## 2. Condensadores
- C = Q/U (farad). Energia armazenada: W = ½·C·U².
- Em paralelo: Ct = C1 + C2 + ...
- Em série: 1/Ct = 1/C1 + 1/C2 + ... (duas: C1·C2/(C1+C2)).
- Carga/descarga RC: constante de tempo τ = R·C. Aos 5τ considera-se o regime estabelecido (99,3%). Carga: uC(t) = U(1 − e^(−t/τ)).
- Tipos: cerâmico (pequeno, sem polaridade, HF), eletrolítico de alumínio (grande capacidade, **com polaridade**, tolerância larga), filme/poliéster (estável, CA), tântalo (polarizado, sensível a sobretensão).
- Escolher sempre tensão nominal ≥ 1,5 x tensão de trabalho; eletrolíticos ligados ao contrário podem rebentar.

### Exemplo resolvido 2
C1 = 10 µF e C2 = 40 µF.
- Série: 10·40/50 = 8 µF. Paralelo: 50 µF.
- Condensador de 100 µF carregado a 12 V: W = ½·100e-6·144 = 7,2 mJ.
- Carga através de 10 kΩ: τ = 10e3·100e-6 = 1 s; ao fim de 1 s está a 63% (7,6 V), aos 5 s está praticamente a 12 V.

## 3. Bobinas (indutores)
- Tensão: u = L·di/dt. Energia: W = ½·L·I².
- Série: Lt = L1 + L2 (sem acoplamento). Paralelo: 1/Lt = 1/L1 + 1/L2.
- Circuito RL: τ = L/R. A corrente não varia instantaneamente; abrir um circuito indutivo gera sobretensão (daí díodos de roda livre em relés e contactores DC).

### Exemplo resolvido 3
L = 100 mH, R = 50 Ω, U = 24 V.
- τ = 0,1/50 = 2 ms. I final = 24/50 = 0,48 A.
- W = ½·0,1·0,48² = 11,5 mJ.

## 4. Montagem prática
- Ler sempre o valor com multímetro antes de soldar (resistências com banda castanha/vermelha confundem-se).
- Verificar polaridade em eletrolíticos e tântalos.
- Condensadores em fonte de alimentação: descarregar antes de tocar.

## 5. Exercícios (com resultados)
1. Três resistências de 100 Ω, 220 Ω e 330 Ω em paralelo. Rt? **R: 56,9 Ω**
2. Divisor para obter 3,3 V a partir de 5 V com R1 = 1 kΩ. R2? **R: R2 = 1,94 kΩ (valor E24: 2 kΩ dá 3,33 V)**
3. Dois condensadores de 470 µF/16 V em série: Ct e tensão máxima aproximada? **R: 235 µF; ~32 V se equilibrados (na prática usar resistências de equilíbrio)**

## 6. Fontes externas sugeridas para o caderno
- All About Circuits, livro gratuito "Lessons in Electric Circuits" (vol. I e II).
- electronics-tutorials.ws (secções de resistências, condensadores, indutores).
- Referencial oficial da UC no Catálogo Nacional de Qualificações (ANQEP): carrega o PDF da UC para o NotebookLM alinhar o resumo com os objetivos avaliados.
- Simulador gratuito: Falstad Circuit Simulator (falstad.com/circuit) para visualizar cargas/descargas.
