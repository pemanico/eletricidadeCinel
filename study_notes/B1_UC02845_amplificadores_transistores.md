# UC02845 - Implementar circuitos amplificadores com transístores

> Material de estudo (explicação + exemplos). Não é fonte normativa. β e restantes parâmetros variam muito entre exemplares: usar o datasheet e projetar de modo a depender pouco de β.

## 1. Fundamentos do BJT
- Três regiões: **corte** (I_B ≈ 0), **ativa** (amplificação, I_C = β·I_B), **saturação** (V_CE ≈ 0,2 V, interruptor fechado).
- Relações: I_E = I_B + I_C = (β+1)·I_B; V_BE ≈ 0,7 V (silício).
- Para amplificar, o transístor tem de estar polarizado na região ativa: define-se o **ponto de funcionamento (Q)**, tipicamente com V_CE ≈ V_CC/2 para máxima excursão simétrica.

## 2. Polarização por divisor de tensão (a mais usada)
Divisor R1/R2 na base + resistência de emissor R_E (estabiliza face a β e à temperatura, realimentação negativa).
- V_BB = V_CC · R2/(R1+R2); R_B = R1∥R2.
- I_E = (V_BB − V_BE) / (R_E + R_B/(β+1)).
- Se R_B << (β+1)·R_E (regra: R_B ≤ 0,1·(β+1)·R_E), I_E ≈ (V_BB − 0,7)/R_E e o circuito é "rígido".

### Exemplo resolvido (emissor comum)
V_CC = 12 V, R1 = 47 kΩ, R2 = 10 kΩ, R_C = 2,2 kΩ, R_E = 470 Ω, β = 100.
1. V_BB = 12·10/57 = 2,105 V; R_B = 47k∥10k = 8,25 kΩ.
2. I_E = (2,105 − 0,7)/(470 + 8250/101) = 1,405/551,7 = **2,55 mA** (a aproximação "rígida" daria 2,99 mA, 17% de erro, porque R_B não é muito menor que (β+1)·R_E = 47,5 kΩ).
3. I_C = I_E·β/(β+1) = 2,52 mA.
4. V_E = 2,55 m · 470 = 1,20 V; V_C = 12 − 2,52 m · 2,2 k = 6,45 V; **V_CE = 5,26 V** (perto de V_CC/2 = 6 V: bom ponto Q).
5. Resistência dinâmica do emissor: r_e = 25 mV/I_E = 9,8 Ω.
6. Ganho em tensão:
   - com C_E de bypass em R_E: A_v ≈ −R_C/r_e = −2200/9,8 ≈ **−224**
   - sem bypass: A_v ≈ −R_C/(r_e + R_E) = −2200/480 ≈ **−4,6** (mais estável e linear, muito menos ganho).
7. Com carga R_L ligada ao coletor (via condensador de acoplamento), R_C passa a R_C∥R_L no cálculo do ganho em CA: com R_L = 2,2 kΩ, o ganho com bypass cai para ~−112.
8. A impedância de entrada é ≈ R_B∥(β·r_e): 8,25k ∥ 0,98k ≈ 0,88 kΩ (baixa). Por isso o amplificador carrega fontes de sinal de alta impedância.

## 3. Configurações básicas
| Configuração | Ganho tensão | Ganho corrente | Z_in | Z_out | Uso |
|---|---|---|---|---|---|
| Emissor comum | alto, inverte fase | alto | média | média/alta | Amplificação geral |
| Coletor comum (seguidor de emissor) | ≈ 1 | alto | alta | baixa | Adaptação de impedâncias, buffer |
| Base comum | alto | ≈ 1 | baixa | alta | Alta frequência |

## 4. Classes de amplificadores de potência
- **Classe A**: conduz 360°; mais linear, rendimento baixo (máx. 25% com carga resistiva, 50% com carga acoplada por transformador).
- **Classe B**: cada transístor conduz 180° (push-pull); rendimento até 78,5%; distorção de cruzamento.
- **Classe AB**: ligeira polarização para eliminar a distorção de cruzamento; compromisso mais comum em áudio.
- **Classe C**: conduz < 180°; alto rendimento, usado em RF com carga ressonante.
- Classe D (comutada/PWM): rendimento > 90%, usada em amplificadores modernos e embebidos.

## 5. Realimentação e resposta em frequência
- Realimentação negativa reduz o ganho mas melhora linearidade, estabilidade e largura de banda.
- Condensadores de acoplamento e de bypass criam pólos de baixa frequência: f_c = 1/(2π·R·C).
- Capacidades parasitas do transístor limitam o ganho em altas frequências.

## 6. Erros comuns
- Projetar com um valor de β "único" (varia 2 a 3 vezes).
- Esquecer a influência de R_L e da impedância da fonte no ganho real.
- Ponto Q demasiado perto do corte ou saturação, o que corta o sinal.
- Dissipação térmica ignorada em andares de potência (fuga térmica).

## 7. Exercícios (com resultados)
1. Com I_E = 1 mA, r_e? **R: 25 Ω**
2. Seguidor de emissor: ganho em tensão e Z_in aproximada com β = 100, R_E = 1 kΩ. **R: ≈ 0,97 (próximo de 1); Z_in ≈ β·(R_E + r_e) ≈ 102 kΩ, com divisor de polarização em paralelo**
3. Amplificador classe B alimentado a ±12 V com carga de 8 Ω: potência máxima na carga? **R: pico útil ≈ 11 V (12 V menos perdas); P = 11²/(2·8) ≈ 7,6 W**

## 8. Fontes externas sugeridas
- All About Circuits, vol. III, capítulos sobre transístores bipolares e amplificadores.
- electronics-tutorials.ws: secção de amplificadores.
- Datasheets BC547/BC337/2N2222 para valores reais de β e V_CE(sat).
- Simulação: LTspice ou Falstad (permite ver deslocamento do ponto Q e distorção).
- PDF do referencial da UC (ANQEP).
