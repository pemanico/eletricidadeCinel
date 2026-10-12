# UC03918 - Implementar circuitos de eletrónica de potência

> Material de estudo (explicação + exemplos). Não é fonte normativa. Valores limite (tensões, correntes, Rds_on, Rθ) vêm do datasheet.

## 1. Dispositivos
- **Díodo de potência**: retificação, roda livre. Atenção a tensão inversa e tempo de recuperação.
- **Tirístor (SCR)**: dispara com pulso na gate e **só pára quando a corrente desce abaixo da corrente de manutenção** (ou no zero natural da CA). Controla meia onda.
- **TRIAC**: dois sentidos; usado em reguladores de luz, controlo de aquecimento por ciclos completos. Não controla bem cargas fortemente indutivas sem snubber.
- **MOSFET de potência**: comandado por tensão, comutação rápida; perdas de condução = I²·Rds_on; usado em baixas e médias tensões (até algumas centenas de volt) e alta frequência.
- **IGBT**: tensões e correntes altas (variadores de frequência, inversores solares/VE), frequências até dezenas de kHz.

## 2. Retificadores controlados
- Monofásico em ponte totalmente controlada (carga com corrente contínua): **U_dc = (2·√2/π)·U_ef·cos α ≈ 0,9·U_ef·cos α**, onde α é o ângulo de disparo.
- Exemplo: U_ef = 230 V, α = 60°: U_dc = 0,9·230·0,5 ≈ **103,5 V**. Com α = 0° obtém-se ≈ 207 V (valor máximo).
- Para α > 90° (com carga e fonte de energia) o conversor funciona como inversor (regeneração).
- Fator de potência diminui com α crescente (a corrente fica desfasada).

## 3. Conversores DC-DC
- **Buck (redutor)**: U_out = D·U_in, com D (duty cycle) entre 0 e 1.
- **Boost (elevador)**: U_out = U_in/(1−D).
- **Buck-boost (inversor)**: U_out = −U_in·D/(1−D).
- Em modo de condução contínua do buck: ΔI_L = (U_in − U_out)·D / (f·L).

### Exemplo resolvido: buck de 24 V para 12 V / 2 A
- D = 12/24 = **0,5**.
- Escolhendo ripple de corrente na bobina de 30% de I_out: ΔI = 0,6 A; f = 100 kHz.
- L = (U_in − U_out)·D/(f·ΔI) = 12·0,5/(100e3·0,6) = **100 µH**.
- A bobina deve suportar I_pico = 2 + 0,3 = 2,3 A sem saturar (escolher I_sat ≥ 3 A).
- Perdas no MOSFET (condução): P = I²·Rds_on·D = 4·0,010·0,5 = 20 mW (as de comutação são normalmente maiores a 100 kHz).
- Condensador de saída: ΔU_out ≈ ΔI/(8·f·C). Com C = 100 µF: 0,6/(8·100e3·100e-6) = 7,5 mV.

## 4. Inversores e PWM
- **PWM sinusoidal**: compara uma onda de referência sinusoidal com uma portadora triangular para gerar pulsos cuja média segue a sinusoide.
- **Variador de frequência** (U/f constante): retificador + barramento DC com condensadores + inversor IGBT trifásico. Rampa de aceleração, proteção do motor, frenagem.
- Em instalações: atenção a harmónicos injetados na rede, cabos blindados entre variador e motor, ligações de terra de alta frequência (CEM), e a fugas de corrente que afetam diferenciais (usar tipo B ou F quando indicado pelo fabricante).

## 5. Dissipação térmica
- Temperatura da junção: **T_j = T_a + P·(Rθ_jc + Rθ_cs + Rθ_sa)**.
- Exemplo: P = 10 W, T_a = 40 °C, T_j máx = 125 °C (mantendo margem, vamos dimensionar para 110 °C), Rθ_jc = 1,5 K/W, Rθ_cs = 0,5 K/W.
  - Rθ_sa ≤ (110 − 40)/10 − 1,5 − 0,5 = 5,0 K/W → escolher dissipador com valor **≤ 5 K/W** (idealmente 3 a 4 K/W, para margem).

## 6. Proteção e snubbers
- Snubber RC em paralelo com TRIAC/tirístor para cargas indutivas (limita dv/dt).
- Fusíveis ultrarrápidos (I²t baixo) para proteger semicondutores; disjuntores comuns não protegem semicondutores.
- Díodo de roda livre em cargas indutivas DC (ou TVS).

## 7. Erros comuns
- Confundir ângulo de disparo α com ângulo de condução.
- Escolher MOSFET apenas pela tensão e ignorar Rds_on e perdas de comutação.
- Dissipador subdimensionado (T_j alta reduz brutalmente a vida útil).
- Ignorar harmónicos e CEM em instalações com variadores.

## 8. Exercícios (com resultados)
1. Buck: U_in = 12 V, U_out = 5 V; D? **R: 0,417**
2. Boost: U_in = 5 V, D = 0,6; U_out? **R: 12,5 V (ideal)**
3. Retificador controlado ponte, 230 V, α = 90°: U_dc? **R: 0 V (média nula)**
4. Dissipador de 4 K/W, dissipação 15 W, T_a = 35 °C: aumento de temperatura do dissipador? **R: 60 K → 95 °C (muito quente: reavaliar)**

## 9. Fontes externas sugeridas
- Notas de aplicação gratuitas: Texas Instruments (conversores DC-DC), Infineon (MOSFET/IGBT), ST.
- electronics-tutorials.ws e All About Circuits (secções de tirístores e conversores).
- Para variadores: manuais de instalação de fabricantes (ABB, Siemens, Schneider), com requisitos de CEM e cabos.
- Simulação: LTspice (muito usado para conversores).
- PDF do referencial da UC (ANQEP).
