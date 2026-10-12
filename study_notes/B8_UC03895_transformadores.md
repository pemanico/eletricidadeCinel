# UC03895 - Aplicar transformadores

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Perdas, tensão de curto-circuito, regulação e requisitos de ecoprojeto dependem do fabricante e dos regulamentos da UE em vigor (IEC 60076; regulamento de ecoprojeto de transformadores): confirmar nos datasheets e na regulamentação. **Trabalhos em transformadores de média tensão só por pessoal qualificado e autorizado** (ver UC00676 e UC04679).

## 1. Princípio e relações fundamentais
- Um transformador transfere energia entre dois enrolamentos por **indução magnética**, **sem alterar a frequência**.
- **Relação de transformação:** **a = N1/N2 = U1/U2 = I2/I1** (valores ideais).
- **Potência aparente (kVA):** monofásico S = U·I; trifásico **S = √3·U·I**. Em carga ideal S1 = S2 (a diferença são as perdas).
- **Fluxo no núcleo:** U ≈ 4,44·f·N·Φ_max; por isso, um transformador a 50 Hz **não deve** funcionar com tensão aplicada de forma contínua a uma frequência inferior (saturação do núcleo).

### Exemplo: transformador de distribuição de 630 kVA, 20 kV / 400 V
- **Corrente primária:** I1 = 630 000/(√3·20 000) = **18,2 A**.
- **Corrente secundária:** I2 = 630 000/(√3·400) = **909 A**.
- **Relação de transformação:** 20 000/400 = **50**.

## 2. Constituição
- **Núcleo magnético:** chapa magnética de grão orientado, laminada (reduz perdas por correntes de Foucault).
- **Enrolamentos:** cobre ou alumínio; **primário** e **secundário**; isolamentos (papel/óleo ou resina).
- **Refrigeração e dielétrico:**
  - **Em óleo (ONAN: óleo natural, ar natural):** muito comum em distribuição; o óleo isola e arrefece; **depósito de expansão** ou **hermético** (enchimento integral).
  - **Seco (resina epóxi, "cast resin", AN/AF):** sem óleo; **recomendado em edifícios, locais com risco de incêndio e interiores**; mais caro, menor resistência a sobrecargas, **sensível a humidade e poeiras** conforme a instalação.
- **Acessórios:** comutador de tomadas (taps), **bornes MT e BT**, **placa de características**, ganchos de elevação, **rodas** (movimentação), terminais de terra.

## 3. Grupos de ligação (trifásicos)
- **Símbolo:** letra maiúscula (primário: **D** triângulo, **Y** estrela, **Z** ziguezague), letra minúscula (secundário: **d, y, z**; **n** se o neutro estiver acessível) e **índice horário** (desfasamento em múltiplos de 30°).
- **Dyn11:** o grupo **mais usado em distribuição**: primário em triângulo (MT), secundário em estrela com neutro acessível (BT); **desfasamento de 30° (índice 11)**. Vantagens: o **triângulo** retém as harmónicas de 3.ª ordem e **equilibra cargas desequilibradas** no secundário.
- **Yzn11 / Dzn0:** ligações em ziguezague para neutros muito desequilibrados.
- **Mudança de grupo ou índice** afeta o **paralelismo**: transformadores com desfasamentos diferentes **não podem ser ligados em paralelo**.

## 4. Características elétricas principais
- **Potência nominal (kVA)**, **tensões primária e secundária**, **frequência**, **grupo de ligação**, **tensão de curto-circuito (u_k)**, **perdas em vazio (P0)** e **perdas em carga (P_k)**, **corrente de vazio (I0)**, **classe de isolamento/ aquecimento**.
- **u_k (impedância de curto-circuito):** fração da tensão nominal necessária para fazer circular a corrente nominal com o secundário em curto-circuito; valores típicos **4%** (até cerca de 630 kVA) e **6%** (potências superiores).
  - **Icc no secundário (barramento infinito a montante):** **Icc ≈ In / u_k**: para 630 kVA, 400 V, u_k = 4%: 909/0,04 = **22,7 kA** (ver UC04675).
- **Corrente de magnetização inicial (inrush):** ao energizar, pode atingir **8 a 12 x In** por décimos de segundo; influi na **escolha de fusíveis e regulações de proteção** (evitar disparos).
- **Perdas:**
  - **P0 (vazio):** perdas no ferro, **constantes** enquanto energizado (24 h/dia).
  - **P_k (carga):** perdas no cobre, **proporcionais ao quadrado da carga** (P_k·x²).
  - Os regulamentos de **ecoprojeto da UE** impõem **limites máximos de perdas** para transformadores novos: confirmar a fase em vigor.

## 5. Rendimento e regulação
### Rendimento
**η = P_saída / (P_saída + P0 + P_k·x²)**, onde x = S/S_n.
- **Exemplo (valores ilustrativos):** 630 kVA, **P0 = 0,8 kW**, **P_k = 6,5 kW**, carga plena (x = 1) e cos φ = 0,9: P_saída = 567 kW.
  - η = 567/(567 + 0,8 + 6,5) = **98,73%**.
  - A **50% de carga**: P_saída = 283,5 kW; perdas = 0,8 + 6,5·0,25 = 2,43 kW; η = **99,15%**.
- **Rendimento máximo:** quando as perdas em carga igualam as em vazio: **x_ótimo = √(P0/P_k)** = √(0,8/6,5) = **0,35** (35% da carga).
  - **Consequência prática:** transformadores que trabalham a baixa carga a maior parte do tempo têm rendimento elevado, mas **as perdas em vazio contam sempre**: nota-se na fatura em instalações com carga baixa durante a noite.

### Regulação de tensão (queda interna)
**ΔU% ≈ x·(u_r·cos φ + u_x·sen φ)**, com u_r = P_k/S_n·100 e u_x = √(u_k² − u_r²).
- **Exemplo:** u_r = 6,5/630 = 1,03%; u_x = √(4² − 1,03²) = 3,86%; x = 1, cos φ = 0,9 (sen φ = 0,436): ΔU = 1,03·0,9 + 3,86·0,436 = 0,93 + 1,68 = **2,6%**.
- **Tomadas (taps):** comutador **sem carga (off-load)** típico **±2 x 2,5%** do lado MT, ajustado por pessoal qualificado **com o transformador desenergizado**, para compensar a tensão da rede. Existem comutadores **em carga (OLTC)** em potências maiores.

## 6. Paralelismo de transformadores
**Condições:**
1. **Mesma relação de transformação** (tensões iguais).
2. **Mesmo grupo de ligação e índice horário.**
3. **u_k semelhantes** (diferença ≲ 10%) para que a carga se **reparta proporcionalmente à potência**.
4. **Relação entre potências ≤ 3:1.**
5. **Mesma sequência de fases e polaridade.**
- Se u_k diferem, o transformador de **menor u_k** carrega mais e pode sobrecarregar antes do outro.
- O paralelo exige **dispositivos de proteção e de corte** adequados e **poder de corte** ≥ Icc somada.

## 7. Proteção e vigilância
- **Lado MT:** **fusíveis MT** ou **disjuntor com proteção** dimensionados segundo as tabelas do fabricante para a potência, a tensão e o **inrush**; proteção de **sobrecorrente e de defeito à terra**.
- **Lado BT:** disjuntor geral (QGBT); **poder de corte** ≥ Icc; **proteção contra sobrecargas**.
- **Dispositivos próprios de transformadores em óleo:**
  - **Relé Buchholz** (em transformadores com depósito de expansão): deteta **gases** e **fluxo de óleo** (alarme e disparo).
  - **Termóstato/termómetro de óleo:** alarme e disparo por **sobretemperatura**.
  - **Válvula de segurança/sobrepressão** e **indicador de nível de óleo**.
  - **Secador de ar (silica gel)** no depósito de expansão.
- **Transformadores secos:** **sondas PT100 ou PTC** nos enrolamentos ligadas a **relés de temperatura** (alarme e disparo); **ventilação forçada** conforme o fabricante.
- **Proteção contra sobretensões:** limitadores de sobretensão no lado MT (descarregadores) quando exigido.

## 8. Instalação e ensaios de receção
- **Local:** ventilado, acessível, com **bacia de retenção de óleo** quando em óleo (dimensionada pelo volume), **distâncias de segurança**, **resistência ao fogo** conforme a regulamentação (compartimentação, extintores).
- **Ligações:** cabos MT com **terminais adequados**; barramentos BT dimensionados para a corrente (909 A neste exemplo), **apertos ao binário** especificado; **ligação à terra** do tanque/estrutura.
- **Ensaios de receção/comissionamento** (referência; procedimentos do fabricante):
  - **Resistência de isolamento** entre enrolamentos e à massa (**megóhmetro de tensão adequada**; registo de temperatura e do **índice de polarização**).
  - **Relação de transformação e grupo de ligação** (TTR).
  - **Resistência dos enrolamentos** (comparar fases).
  - **Verificação dos dispositivos de proteção** e da **posição do comutador**.
  - **Verificação do nível de óleo e fugas.**
  - **Energização em vazio**, medição de tensões e **corrente de vazio**; depois **ensaio com carga**.
- **Registo de ensaios** como **referência para a manutenção futura**.

## 9. Outros tipos de transformadores
- **Autotransformador:** um único enrolamento com tomada intermédia; mais económico para relações próximas de 1, **sem isolamento galvânico** (cuidado em segurança).
- **Transformador de isolamento:** relação 1:1 para separar galvanicamente (segurança em locais especiais, informática, equipamentos médicos).
- **Transformadores de comando e de baixa tensão de segurança (SELV):** quadros de automação, iluminação a 12/24 V; **curto-circuito pode queimar**: usar proteção no primário e no secundário.
- **Transformadores de medida:** **TC (corrente)** e **TT (tensão)**; **TC com secundário nunca em aberto em carga** (UC01788).
- **Transformadores de potência para renováveis e VE:** com requisitos de **harmónicos** e fatores K.

## 10. Erros comuns
- Ligar em paralelo transformadores com **grupos de ligação diferentes** ou u_k muito diferentes.
- **Fusível MT** escolhido só pela corrente nominal (ignorando o **inrush**).
- **Alterar o comutador com o transformador energizado** (off-load).
- Instalar em local **sem ventilação** (sobreaquecimento) ou sem bacia de retenção de óleo.
- **Secundário de TC aberto** em carga.
- Confundir **kVA com kW** no dimensionamento.
- **Sobrecarregar** um transformador seco em ambiente quente sem derating.
- Subestimar **harmónicos** (aquecimento extra por perdas adicionais).

## 11. Exercícios (com resultados)
1. Transformador 400 kVA, 20 kV/400 V: correntes primária e secundária? **R: I1 = 11,5 A; I2 = 577 A.**
2. Icc do secundário com u_k = 4% (barramento infinito)? **R: 577/0,04 = 14,4 kA.**
3. Perdas P0 = 0,5 kW e P_k = 4,6 kW: carga de rendimento máximo? **R: √(0,5/4,6) = 0,33 → 33%.**
4. Duas unidades de 630 kVA com u_k = 4% e 5%: como se reparte a carga? **R: a de u_k = 4% carrega mais (proporcional a 1/u_k): 55,6% vs 44,4%; a unidade de 4% chega a 100% quando a total é 90% da soma.**
5. Pode ligar-se em paralelo um Dyn11 com um Dyn5? **R: não; desfasamento diferente (30° vs 150°).**

## 12. Fontes externas sugeridas
- Catálogos e manuais de fabricantes (Efacec, Schneider, ABB, Siemens, Legrand/Cahors): características, perdas, tabelas de fusíveis, ensaios.
- **IEC 60076** (paga): usar documentos de fabricantes e guias técnicos como material público.
- Regulamento de ecoprojeto da UE para transformadores (texto público no EUR-Lex) e documentos da DGEG.
- Normas técnicas e guias da e-Redes/operador de rede sobre postos de transformação.
- PDF do referencial da UC (ANQEP).
