> **ERRATA (2026-10-12):** nesta nota, a 'correção' do exemplo do termoacumulador usou capacidades de corrente da tabela IEC 60364-5-52:2009 (método B1: 4 mm² = 28 A). O **RTIEBT, Quadro 52-C1, método B** (tubo embebido em alvenaria), dá **32 A para 4 mm²**. Com os fatores k1 = 0,94 e k2 = 0,70, Iz = 21,06 A ≥ In = 20 A: **4 mm² cumpre sob o RTIEBT** (3G4 + C20 + DDR 30 mA). A tabela a usar em Portugal é a do RTIEBT. Todos os valores de capacidade de corrente desta nota são IEC 2009 B1, não RTIEBT, e por rever. Ver `src/eletro/calc/cabos.py` e `docs/REGRAS_HABITACAO_RTIEBT.md`.

# UC01781 - Dimensionar condutores, proteções e circuitos de instalações de energia elétrica

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Os valores de tabelas (capacidades de corrente, fatores de correção, limites de queda de tensão, secções mínimas) são valores de referência da IEC 60364-5-52 e podem diferir da versão em vigor do RTIEBT. Confirma sempre na norma/RTIEBT antes de usar em obra.

## CORREÇÃO ao exemplo dado no chat (importante)
No exemplo do termoacumulador (4,6 kW, 230 V, 25 m, B1, 35 °C, 3 circuitos agrupados) usei para 4 mm² uma capacidade de 32 A. O valor de referência de tabela para Cu/PVC, método B1, 2 condutores carregados, é **28 A** (2,5 mm² → 21 A; 6 mm² → 36 A). Com os fatores k1 = 0,94 e k2 = 0,70 (k = 0,658):
- 4 mm²: Iz = 28 x 0,658 = **18,4 A < In = 20 A** → **não cumpre**
- 6 mm²: Iz = 36 x 0,658 = **23,7 A ≥ In = 20 A** → **cumpre**

Resultado correto desse exemplo: **cabo 3G6 mm² + disjuntor C20 + diferencial 30 mA** (não 3G4). Queda de tensão com 6 mm²: 2·0,0225·25·20/6 = 3,75 V = 1,6%. Esta correção ilustra porque os valores de tabela têm de ser lidos na norma e não de memória.

---

## 1. Sequência de dimensionamento (ordem de trabalho)
1. **Levantar cargas e fatores:** potência instalada, fator de simultaneidade, fator de utilização, cos φ.
2. **Corrente de projeto Ib.**
3. **Calibre da proteção In** (Ib ≤ In).
4. **Método de instalação** e condições (temperatura ambiente, agrupamento, isolamento PVC ou XLPE, Cu ou Al).
5. **Secção pelo aquecimento** (Iz ≥ In com fatores de correção).
6. **Queda de tensão.**
7. **Curto-circuito:** poder de corte, solicitação térmica do cabo, Icc mínima (disparo magnético).
8. **Contactos indiretos** (Zs ou diferencial).
9. **Secções mínimas** do RTIEBT por tipo de circuito.
10. **Secção final = a maior das obtidas.** Depois dimensionar neutro e PE.

## 2. Corrente de projeto
- Monofásico: Ib = P / (U·cos φ), U = 230 V.
- Trifásico: Ib = P / (√3·U·cos φ), U = 400 V.
- Motores: P é a potência no veio; a potência elétrica é Pn/η e a corrente deve considerar η·cos φ (ou ler a corrente nominal da chapa de características).
- Várias cargas num circuito/quadro: aplica-se fator de simultaneidade; para a entrada da instalação usar valores de potência contratada.

## 3. Coordenação condutor/proteção (sobrecarga)
Duas condições (IEC 60364-4-43):
1. **Ib ≤ In ≤ Iz**
2. **I2 ≤ 1,45·Iz**, onde I2 é a corrente de funcionamento convencional da proteção.
   - Disjuntores modulares (EN 60898): I2 = 1,45·In, logo a condição 1 chega.
   - Fusíveis gG: I2 = 1,6 a 1,9·In conforme calibre → verificar a condição 2.
- **Iz = I'z · k1 · k2 (· k3 ...)**: I'z da tabela (método, isolamento, material, condutores carregados); k1 temperatura ambiente; k2 agrupamento.
- **Condutores carregados:** monofásico = 2, trifásico equilibrado = 3 (o neutro não conta se não há harmónicos relevantes). Com harmónicos de ordem 3 elevados (cargas eletrónicas), o neutro pode ficar carregado: contar 4 condutores e/ou aumentar a secção do neutro.
- Proteção contra sobrecarga não é obrigatória em alguns casos (circuito sem derivações, risco de abertura intempestiva, etc.), mas confirma no RTIEBT antes de omitir.

### Fatores de referência (IEC 60364-5-52, confirmar)
**k1, temperatura ambiente** (referência 30 °C ao ar):
| °C | PVC (70 °C) | XLPE (90 °C) |
|---|---|---|
| 30 | 1,00 | 1,00 |
| 35 | 0,94 | 0,96 |
| 40 | 0,87 | 0,91 |
| 45 | 0,79 | 0,87 |
| 50 | 0,71 | 0,82 |

**k2, agrupamento** (circuitos juntos em tubo/embebidos, método A a D): 2 circuitos 0,80; 3 → 0,70; 4 → 0,65; 5 → 0,60; 6 → 0,57. Em tabuleiro perfurado, camada única encostados (método E/F): 2 → 0,88; 3 → 0,82; 4 → 0,77. (Os valores variam com a disposição: ler a tabela correspondente.)

### Capacidades de corrente I'z de referência, Cu (A), IEC 60364-5-52 (confirmar)
| S (mm²) | B1 PVC 2 carr. | B1 PVC 3 carr. | E PVC 3 carr. | E XLPE 3 carr. |
|---|---|---|---|---|
| 1,5 | 15,5 | 13,5 | 18,5 | 22 |
| 2,5 | 21 | 18 | 25 | 30 |
| 4 | 28 | 24 | 34 | 40 |
| 6 | 36 | 31 | 43 | 51 |
| 10 | 50 | 42 | 60 | 70 |
| 16 | 68 | 56 | 80 | 94 |
| 25 | 89 | 73 | 101 | 119 |
| 35 | 110 | 89 | 126 | 148 |

(Método B1 = condutores isolados em tubo sobre parede/embebido em parede termicamente condutora; E = cabo multicondutor ao ar em tabuleiro perfurado.)

## 4. Aparelhos de proteção
- **Disjuntores (EN 60898, uso doméstico/similar)**: disparo magnético instantâneo: **B** 3-5·In, **C** 5-10·In, **D** 10-20·In. Curva B para cabos longos/Icc baixa; C uso geral; D para cargas com picos de arranque (transformadores, motores).
- **Disjuntores industriais (IEC 60947-2)**: regulação térmica e magnética, maior poder de corte.
- **Fusíveis gG**: uso geral (cabos); **aM**: acompanhamento de motores (só curto-circuito, exigem relé térmico).
- **Relé térmico / disjuntor-motor**: proteção contra sobrecarga de motores, regulado para a corrente nominal da chapa.
- **Diferenciais (DDR)**: 30 mA proteção adicional (tomadas, casas de banho, exterior); 300 mA/500 mA proteção contra incêndio/seletividade. Tipos AC, A, F, B conforme formas de onda das cargas (variadores, carregadores VE, inversores podem exigir tipo F ou B).
- **Poder de corte (Icu/Icn)** do aparelho ≥ Icc máxima presumida no seu ponto de instalação. Se for inferior, usa-se filiação (backup) documentada pelo fabricante.
- **Seletividade:** o aparelho a montante não deve abrir antes do mais próximo da avaria. Dá-se por intensidade (calibres bem diferentes), por tempo (regulação) ou, com tabelas do fabricante, por energia. Verificar nas tabelas de seletividade do fabricante.

## 5. Queda de tensão
- Monofásico (resistivo): **ΔU = 2·ρ·L·Ib / S**.
- Trifásico, geral: **ΔU = √3·Ib·L·(R·cos φ + X·sen φ)** (R = ρ/S por m; X ≈ 0,08 mΩ/m para cabos multicondutores).
- ρ de referência: Cu 0,0225 Ω·mm²/m (a ~90 °C) ou 0,0206 a 70 °C; Al 0,036.
- **O limite é regulamentar, não universal.** A IEC 60364 sugere como referência 3% iluminação / 5% outros usos medidos desde a origem da instalação; o RTIEBT pode fixar outros valores. Confirmar a versão em vigor e o tipo de ligação à rede.
- Em cabos longos e/ou correntes elevadas, a queda de tensão decide frequentemente a secção (ver exemplos).

## 6. Curto-circuito
1. **Poder de corte** ≥ Icc máx. no ponto de montagem.
2. **Solicitação térmica do cabo:** **I²t ≤ k²·S²**; k = 115 (Cu/PVC), 143 (Cu/XLPE), 76 (Al/PVC), 94 (Al/XLPE). O I²t (energia passante) vem da curva do aparelho ou do catálogo. Para disjuntores modulares limitadores, geralmente cumpre em secções ≥ 1,5 mm² com In ≤ 63 A, mas não se assume: verificar.
3. **Icc mínima** (curto-circuito no extremo do circuito, com condutores quentes) tem de provocar o disparo magnético dentro do tempo admissível: Icc_min ≥ Im (limite superior do disparo magnético: 5·In curva B, 10·In curva C, 20·In curva D).
- Estimativa de Icc em qualquer ponto: Icc = U0 / Zs (por fase-neutro ou fase-terra); a impedância soma-se à montante.

## 7. Contactos indiretos (esquemas TN)
- Corte automático: **Zs · Ia ≤ U0** (U0 = 230 V); Ia é a corrente que garante o disparo no tempo exigido (≤ 0,4 s para circuitos terminais até 32 A em 230/400 V; ≤ 5 s para circuitos de distribuição).
- Tomadas ainda levam diferencial 30 mA (proteção adicional).
- Esquema TT: ver UC01782 (RA·IΔn ≤ 50 V).

## 8. Condutores neutro e de proteção (PE)
- **Neutro:** em circuitos monofásicos e em polifásicos com secção de fase ≤ 16 mm² Cu: S_N = S_fase. Acima disso (e sem harmónicos significativos) permite-se reduzir (mín. 16 mm² Cu).
- **PE (secção mínima, se o PE for do mesmo material):** S_fase ≤ 16 → S_PE = S_fase; 16 < S_fase ≤ 35 → 16 mm²; S_fase > 35 → S_fase/2.
- Nunca interromper o PE com aparelhos de corte; nunca usar o neutro como PE em esquemas TT/TN-S.

## 9. Secções mínimas (referência, confirmar no RTIEBT)
Iluminação: 1,5 mm² Cu. Tomadas de uso geral: 2,5 mm² Cu. Circuitos de aparelhos de maior potência (fogão, termoacumulador): conforme cálculo, tipicamente ≥ 4 a 6 mm². Ligações a quadros e circuitos de comando têm regras próprias.

## 10. Erros comuns
- Ler k2 de memória (ou ignorá-lo): é o mais subestimado.
- Usar o mesmo I'z para PVC e XLPE.
- Esquecer o neutro carregado em circuitos com harmónicos (informática, LED, variadores).
- Escolher curva C em cabo muito longo e não verificar a Icc mínima.
- Verificar só a secção pelo aquecimento: a secção final é a maior de todos os critérios.
- Esquecer que a proteção a montante tem de aguentar o I²t da proteção à jusante (filiação/seletividade).

## 11. Exercícios (com resultados indicativos; confirmar tabelas)
1. Circuito monofásico 230 V, 3,68 kW (16 A), cos φ = 1, Cu/PVC em B1, 30 °C, sem agrupamento. In, S mínima? **R: Ib = 16 A; In = 16 A; I'z ≥ 16 → 2,5 mm² (21 A) cumpre pelo aquecimento; verificar queda de tensão e Icc mínima conforme comprimento.**
2. O mesmo circuito agrupado com mais 4 circuitos (5 no total) a 40 °C. **R: k = 0,87·0,60 = 0,522; I'z ≥ 16/0,522 = 30,7 A → 6 mm² (36 A).**
3. Disjuntor C32 e Icc mínima no extremo de 250 A. Cumpre o disparo magnético? **R: Im = 10·32 = 320 A > 250 A → não garante disparo magnético; passar para curva B (5·32 = 160 A) ou aumentar a secção.**
4. Fase 25 mm²: secção mínima do PE? **R: 16 mm².**

## 12. Fontes externas sugeridas
- RTIEBT (Portaria 949-A/2006, DGEG, site dgeg.gov.pt): regras nacionais, versão em vigor.
- Guias técnicos gratuitos de fabricantes (Schneider Electric "Guia de Projeto", Legrand, ABB): tabelas de seletividade, filiação, curvas de disparo.
- Cabos: catálogos de fabricantes (Prysmian, General Cable/Nexans): capacidades de corrente e quedas de tensão por mV/A/m.
- A norma IEC 60364 é paga e protegida por direitos de autor: não a carregues sem licença; usa o RTIEBT e os guias de fabricantes.
- PDF do referencial da UC (ANQEP).
