# UC01993 - Executar análise de circuitos RLC

> Material de estudo (explicação + exemplos). Não é fonte normativa.

## 1. Grandezas em corrente alternada sinusoidal
- u(t) = Û·sin(ωt + φ); ω = 2πf; U_ef = Û/√2 (230 V ef = 325 V de pico).
- Em CA os componentes comportam-se por **impedância**, em ohm:
  - Resistência: Z_R = R (tensão e corrente em fase).
  - Bobina: X_L = ω·L = 2πfL (tensão avançada 90° face à corrente).
  - Condensador: X_C = 1/(ω·C) = 1/(2πfC) (corrente avançada 90° face à tensão).
- Circuito RLC série: Z = √(R² + (X_L − X_C)²); φ = arctan((X_L − X_C)/R).
  - X_L > X_C: carácter **indutivo** (corrente atrasada). X_C > X_L: **capacitivo**.

## 2. Potências
- Ativa: P = U·I·cos φ (W). Reativa: Q = U·I·sin φ (var). Aparente: S = U·I (VA).
- S² = P² + Q². Fator de potência = cos φ = P/S.
- Cargas indutivas (motores, transformadores) consomem Q; condensadores fornecem Q.

## 3. Ressonância (série)
- Ocorre quando X_L = X_C: f0 = 1/(2π√(L·C)). Z = R (mínima), corrente máxima, φ = 0.
- Fator de qualidade: Q = X_L/R = (1/R)·√(L/C). Largura de banda: B = f0/Q.
- Atenção: na ressonância as tensões em L e C podem ser Q vezes a tensão da fonte (perigoso e útil em filtros).

## 4. Exemplo resolvido (RLC série)
R = 10 Ω, L = 50 mH, C = 100 µF, f = 50 Hz, U = 230 V.
1. X_L = 2π·50·0,05 = 15,71 Ω
2. X_C = 1/(2π·50·100e-6) = 31,83 Ω
3. X = X_L − X_C = −16,12 Ω (capacitivo)
4. Z = √(10² + 16,12²) = 18,97 Ω
5. I = 230/18,97 = 12,12 A
6. φ = arctan(−16,12/10) = −58,2° (corrente avançada); cos φ = 10/18,97 = 0,527
7. P = I²R = 1469 W; Q = I²·X = −2370 var (capacitivo); S = 230·12,12 = 2788 VA
   Verificação: √(1470² + 2370²) ≈ 2789 VA ✓
8. Ressonância: f0 = 1/(2π√(0,05·100e-6)) = 71,2 Hz; Q = (1/10)·√(0,05/100e-6) = 2,24

## 5. Correção do fator de potência (ligação à instalação elétrica)
Para elevar o cos φ de φ1 para φ2 com a mesma potência ativa P:
**Qc = P·(tan φ1 − tan φ2)**, C (por fase, trifásico em triângulo) = Qc/(3·ω·U²).

Exemplo: carga trifásica P = 10 kW, cos φ = 0,7 → 0,95.
- tan φ1 = 1,0202; tan φ2 = 0,3287
- Qc = 10·(1,0202 − 0,3287) = 6,9 kvar
- Corrente cai de I = 10000/(√3·400·0,7) = 20,6 A para 10000/(√3·400·0,95) = 15,2 A (menos perdas e cabos menos carregados).
- Cuidado: condensadores em redes com harmónicos podem entrar em ressonância paralela com a indutância da rede; nesses casos usa-se bateria com reatâncias de dessintonia.

## 6. Erros comuns
- Somar tensões em módulo (U_R + U_L + U_C ≠ U): somam-se vetorialmente.
- Confundir sinal de φ (indutivo vs capacitivo).
- Esquecer a unidade: µF, mH. Converter antes de calcular.

## 7. Exercícios (com resultados)
1. Bobina de 0,2 H a 50 Hz: X_L? **R: 62,8 Ω**
2. Condensador de 20 µF a 50 Hz: X_C? **R: 159,2 Ω**
3. Circuito RLC série com L = 10 mH e C = 10 µF: f0? **R: 503 Hz**
4. Carga monofásica 230 V, 2 kW, cos φ = 0,8: corrente? **R: 10,9 A**

## 8. Fontes externas sugeridas
- All About Circuits, vol. II (AC), capítulos de reatância, impedância e ressonância.
- MIT OpenCourseWare 6.002 (resposta em frequência e ressonância).
- Guias de correção do fator de potência de fabricantes (Schneider, ABB, Legrand): úteis para a ponte com UC01795.
- PDF do referencial da UC (ANQEP).
