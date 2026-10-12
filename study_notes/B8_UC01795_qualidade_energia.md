# UC01795 - Verificar a qualidade da energia elétrica e implementar soluções perante perturbações na rede

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Os limites abaixo seguem a **EN 50160** (características da tensão em redes públicas de distribuição) e a série **IEC 61000** (compatibilidade eletromagnética). **Confirmar nas edições em vigor** e nos requisitos do operador da rede; os valores aplicam-se a pontos de ligação em condições de referência.

## 1. O que é qualidade da energia
Conjunto de características da **tensão e da corrente** (forma, amplitude, frequência, simetria, continuidade) que permitem que o equipamento funcione como previsto, **sem avarias, sobreaquecimento ou perda de dados**. Má qualidade custa em **avarias, paragens, perdas e consumo adicional**.

## 2. Tipos de perturbações
| Perturbação | O que é | Causas típicas | Efeitos |
|---|---|---|---|
| **Cavas de tensão (sags/dips)** | descida da tensão < 90% Un por curta duração | curto-circuitos na rede, arranque de grandes motores | reinício de PLC, variadores, UPS; paragens de produção |
| **Sobretensões temporárias e transitórias** | tensão acima de 110% (temporária) ou picos curtos (transitórias) | manobras, descargas atmosféricas, falhas | danos em equipamento eletrónico |
| **Interrupções** | tensão < 5% Un (breves < 3 min; longas ≥ 3 min) | faltas, manobras, manutenção | paragem total |
| **Harmónicos** | componentes de tensão/corrente em múltiplos da frequência fundamental | cargas não lineares (variadores, fontes comutadas, LED, retificadores, UPS) | aquecimento, perdas, ressonâncias, disparos intempestivos |
| **Desequilíbrio de tensão** | tensões trifásicas diferentes | cargas monofásicas desiguais, faltas de fase | aquecimento de motores, binário reduzido |
| **Flicker (cintilação)** | variações rápidas de tensão que provocam variação da luz | soldadura, fornos de arco, cargas com variações rápidas | desconforto visual, mau funcionamento |
| **Variações de frequência** | desvio de 50 Hz | desequilíbrios de produção/consumo na rede | relógios, sincronização |
| **Baixa tensão/sobretensão sustentada** | tensão fora de ±10% Un | queda de tensão em cabos longos, regulação | desempenho reduzido, avarias |

## 3. Limites de referência (EN 50160, BT, condições normais)
- **Tensão de alimentação:** **230 V ± 10%** em **95% do tempo** (médias de 10 minutos numa semana) e entre **+10% e −15%** em 100% do tempo.
- **Frequência:** 50 Hz **± 1%** em 99,5% do ano; **+4%/−6%** em 100% do tempo (sistemas interligados).
- **Desequilíbrio (componente inversa):** ≤ **2%** em 95% da semana.
- **Flicker (Plt):** ≤ **1** em 95% da semana.
- **Distorção harmónica total de tensão (THDu):** ≤ **8%** em 95% da semana (incluindo harmónicos até à 40.ª ordem).
- **Harmónicos individuais de tensão (referência):** 3.ª ≈ 5%; 5.ª ≈ 6%; 7.ª ≈ 5%; 9.ª ≈ 1,5%; 11.ª ≈ 3,5%; 13.ª ≈ 3%.
- **Cavas, sobretensões e interrupções:** a norma dá **valores indicativos** e classes; o número de ocorrências varia muito com a rede (confirmar).
- **Equipamentos:** limites de emissão de harmónicos de corrente em **IEC 61000-3-2** (até 16 A por fase) e **IEC 61000-3-12** (16 a 75 A).

## 4. Harmónicos em detalhe
### Origem
Cargas **não lineares** absorvem corrente não sinusoidal: **retificadores e variadores** (6 pulsos), **fontes de alimentação comutadas** (PC, TV), **LED drivers**, **UPS**, **soldadura**, **fornos de arco**, **carregadores de VE**.
- **Retificador de 6 pulsos:** harmónicos de ordem **6k ± 1** (5, 7, 11, 13, 17, 19...).
- **Monofásicas com fontes comutadas:** predominam **3.ª, 9.ª, 15.ª** (triplas), que **se somam no neutro** em sistemas trifásicos a 4 fios (não se cancelam).

### Cálculo da distorção (THD)
**THD_I = √(ΣI_h²) / I_1** (h ≥ 2).
- **Exemplo:** I1 = 100 A, I3 = 33 A, I5 = 20 A, I7 = 14 A.
  - THD_I = √(33² + 20² + 14²)/100 = √1 685/100 = **41,0%**.
  - **Corrente eficaz verdadeira (true RMS):** √(100² + 1 685) = **108,1 A** (um instrumento de média, não true RMS, subestima).
- **Fator de potência com distorção:** **PF = cos φ_deslocamento / √(1 + THD²)**. Com cos φ = 0,95 e THD = 41%: PF = 0,95/√(1 + 0,168) = **0,879**. A distorção reduz o fator de potência mesmo que o desfasamento seja pequeno.

### Efeitos
- **Aquecimento** de transformadores, cabos e motores (perdas adicionais); **corrente no neutro** muito elevada: em cargas de fontes comutadas trifásicas o neutro pode conduzir até cerca de **√3 (≈ 1,73) vezes** a corrente de fase.
- **Ressonância** entre **condensadores de correção do fator de potência** e a indutância da rede, que **amplifica** harmónicos e queima condensadores.
- **Disparos intempestivos** de proteções e **erros em contadores e instrumentos**.
- **Interferência em equipamentos sensíveis** e redes de comunicação.

## 5. Soluções para harmónicos
- **Reatâncias de linha** (3 a 5%) à entrada de variadores: reduzem THD de corrente e protegem o variador.
- **Filtros passivos sintonizados:** circuito LC sintonizado numa harmónica (p. ex. a 5.ª); baratos, mas dependem da rede e podem ressonar com outras harmónicas.
- **Filtros ativos (AHF):** medem a corrente harmónica e injetam corrente em contrafase; mais flexíveis, adaptam-se à carga, mais caros.
- **Retificadores de 12 ou 18 pulsos**, **retificadores ativos (AFE)** em variadores grandes.
- **Transformadores com desfasamento (Dyn, Dzn)** e **ligação em triângulo** (retêm as harmónicas triplas).
- **Redistribuição de cargas** e **neutro sobredimensionado** (S_N ≥ S_fase, até 1,5 a 2 x em casos de cargas eletrónicas dominantes).
- **Condensadores com reatâncias de dessintonia** (ver secção 6).

## 6. Correção do fator de potência em redes com harmónicos
- **Reatância de dessintonia (p%)** em série com cada condensador desloca a frequência de ressonância **abaixo** da 5.ª harmónica, evitando a ressonância:
  - **p = 5,67%** → f_r = 50/√0,0567 ≈ **210 Hz (4,2.ª ordem)**: para redes com 5.ª harmónica relevante.
  - **p = 7%** → f_r ≈ **189 Hz (3,8.ª ordem)**: **o mais comum** para redes com harmónicas de 5.ª.
  - **p = 14%** → f_r ≈ **134 Hz (2,7.ª ordem)**: para redes com 3.ª harmónica relevante.
- **Condensadores reforçados** (sobretensão e corrente harmónica) e **regulador automático** com escalões.
- **Dimensionamento:** Qc = P·(tan φ1 − tan φ2) (UC01993); **aumentar potência dos condensadores para compensar a fundamental** em bateria com dessintonia (sobretensão nos condensadores).
- **Medir antes**: se THD de tensão > cerca de 5% ou a bateria tem historial de avarias, **não instalar condensadores simples**.

## 7. Cavas, interrupções e sobretensões: soluções
- **UPS online** (UC03088) para cargas críticas; **DVR (restaurador dinâmico de tensão)** e **estabilizadores/ reguladores**.
- **Variadores e PLC com "ride-through"** (suportam cavas curtas com energia do barramento DC); **alimentação 24 V DC com condensador/tampão**.
- **Contactores com retardo de queda** e **temporização de reinício** em motores.
- **Limitadores de sobretensão (SPD)** coordenados (UC01782); **transformadores de isolamento** e **filtros de rede** para sobretensões transitórias.
- **Redundância** (duas alimentações com comutador automático/ATS) para cargas críticas.

## 8. Desequilíbrio e flicker
- **Desequilíbrio:** redistribuir cargas monofásicas pelas três fases; verificar **ligações soltas** e **fusíveis fundidos** (perda de fase); proteção de **falta de fase** em motores.
- **Flicker:** reduzir impedância da rede no ponto de ligação (aumentar potência de curto-circuito), compensação dinâmica (**SVC/STATCOM**), **separar** cargas geradoras de flicker.

## 9. Como medir e diagnosticar
- **Analisador de qualidade de energia (PQA)**: **classe A** (IEC 61000-4-30) para medições de conformidade; mede tensão, corrente, potências, harmónicos até à 50.ª, flicker, cavas, transitórios, desequilíbrio, com **registo temporal**.
- **Período de medição:** **uma semana** completa (referência da EN 50160), com intervalos de 10 minutos, **mais curto** para diagnóstico de eventos.
- **Pontos de medição:** **ponto de ligação à rede (PCC)** e nos **quadros** das cargas problemáticas; medir **tensões e correntes** em todas as fases e no **neutro**.
- **Instrumentação:** **sensores de corrente flexíveis (Rogowski)** para cabos grandes; **true RMS**; atenção a **CAT** (categoria de medida) do equipamento e à **segurança** (UC00676).
- **Procedimento:**
  1. Identificar o **sintoma** e o **momento** (avarias, disparos, cintilação).
  2. Fazer a **medição** com o PQA.
  3. **Analisar** os registos contra os limites (EN 50160, requisitos do cliente/fabricante).
  4. **Localizar a fonte** (a montante da carga ou na própria instalação).
  5. **Escolher solução**, implementar e **medir de novo** para validar.
- **Relatórios:** gráficos de tendência, distribuição estatística (percentil 95), eventos com data e hora, **conclusões e recomendações**.

## 10. Erros comuns
- Medir só **alguns minutos** e concluir sobre a conformidade.
- Usar **multímetro de média** (não true RMS) em cargas não lineares.
- **Instalar condensadores sem dessintonia** em redes com harmónicas (ressonância e avaria).
- **Neutro subdimensionado** em instalações com muitas cargas eletrónicas.
- Atribuir cada falha à "rede" **sem medir** as perturbações internas.
- Ignorar **ligações soltas** (causam desequilíbrio, sobreaquecimento e flicker).
- Aplicar **filtros** sem estudo prévio de ressonâncias.
- Não **validar com nova medição** depois da solução.

## 11. Exercícios (com resultados)
1. I1 = 50 A, I5 = 10 A, I7 = 6 A: THD_I? **R: √(100 + 36)/50 = 23,3%.**
2. PF com cos φ = 0,98 e THD = 30%? **R: 0,98/√(1+0,09) = 0,94.**
3. Reatância de dessintonia de 7%: frequência de ressonância? **R: 50/√0,07 ≈ 189 Hz.**
4. Tensão medida na rede de 245 V: está dentro de 230 V ±10%? **R: limite superior 253 V: sim (+6,5%).**
5. Porque o neutro pode ficar mais carregado que as fases com cargas de fonte comutada? **R: as harmónicas triplas (3.ª, 9.ª...) somam-se no neutro em vez de se cancelarem.**
6. Que tipo de harmónicas gera um retificador de 6 pulsos? **R: 5.ª, 7.ª, 11.ª, 13.ª, ... (6k ± 1).**

## 12. Fontes externas sugeridas
- **EN 50160** e **IEC 61000** (pagas): usar guias técnicos de fabricantes e do operador como material público.
- **Guias de qualidade de energia gratuitos** de fabricantes (Schneider Electric, ABB, Siemens, Fluke, Janitza) e do **Leonardo Energy / European Copper Institute** (guias sobre harmónicos e qualidade de energia).
- **ERSE:** regulamento de qualidade de serviço (continuidade e qualidade da onda de tensão em Portugal).
- Manuais de analisadores de qualidade de energia (Fluke, Chauvin Arnoux, Metrel): procedimentos práticos.
- PDF do referencial da UC (ANQEP).
