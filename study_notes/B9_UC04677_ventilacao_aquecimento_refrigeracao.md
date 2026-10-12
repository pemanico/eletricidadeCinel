# UC04677 - Propor sistemas de ventilação, aquecimento e refrigeração

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Esta UC é de **propor e especificar sistemas** (AVAC): levantar necessidades, estimar cargas, escolher soluções e dimensionar a parte elétrica. Os valores de projeto (caudais mínimos de ar novo, requisitos de desempenho energético, qualidade do ar interior) vêm da **regulamentação nacional** (sistema de certificação energética e regulamentos de desempenho energético de edifícios de habitação e de serviços) e da **norma EN 16798-1**: **confirmar nas versões em vigor**. Os exemplos de cálculo são **simplificados** e **não substituem** um projeto de AVAC nem um cálculo de cargas feito com ferramentas e métodos aprovados.
>
> **Limites de competência:** o **circuito frigorífico** (tubagens de fluido, carga e recuperação de refrigerante) e as **instalações de gás** exigem **certificação própria** (técnico certificado em gases fluorados; instalador de gás credenciado). Um eletricista **não deve** abrir um circuito frigorífico nem mexer na instalação de gás sem essa habilitação. Confirmar requisitos atuais.

## 1. Conforto térmico e qualidade do ar
- **Conforto:** depende de temperatura do ar, temperatura radiante, humidade, velocidade do ar, vestuário e atividade (modelo PMV/PPD, **EN ISO 7730**). Valores usuais de projeto: **cerca de 20 a 22 °C no inverno** e **24 a 26 °C no verão** em habitação e escritórios (confirmar na regulamentação).
- **Humidade relativa** confortável: ≈ 40 a 60%.
- **Qualidade do ar interior (QAI):** controlo de **CO₂** (indicador de ocupação; **cerca de 1 000 ppm** é referência comum de boa renovação), **humidade, partículas, compostos orgânicos voláteis, radão** em zonas relevantes.
- **Ventilação:** natural (aberturas), mecânica simples (extração), **VMC dupla fluxo com recuperação de calor** (insufla ar novo filtrado e extrai o ar viciado, recuperando **cerca de 70 a 90%** do calor).
- **Edifícios estanques** (alta eficiência) **exigem ventilação planeada**, caso contrário há condensação, bolores e má QAI.

## 2. Cargas térmicas (método simplificado, ordem de grandeza)
### Aquecimento (inverno)
**Q_aquecimento = Σ(U·A)·ΔT + 0,34·n·V·ΔT** (W)
- **U** (W/m²K): transmitância térmica; **A** (m²); **ΔT** = T_interior − T_exterior de projeto.
- **0,34** (Wh/m³K) ≈ ρ·cp/3600 do ar; **n** = renovações do ar por hora (h⁻¹); **V** = volume (m³).
**Exemplo (sala 5 x 4 x 2,7 m, V = 54 m³):**
- Parede exterior 12 m² (U = 0,6) → 7,2 W/K; janela 3 m² (U = 2,8) → 8,4 W/K; cobertura 20 m² (U = 0,5) → 10 W/K. **Σ(U·A) = 25,6 W/K.**
- ΔT = 20 − 5 = 15 K → perdas por transmissão = **384 W**.
- Ventilação com n = 0,6 h⁻¹: 0,34·0,6·54 = 11,0 W/K → **165 W**.
- **Total ≈ 549 W ≈ 0,55 kW** para aquecer esta sala.
### Arrefecimento (verão), parcelas típicas
- **Ganhos solares** pelos vãos: **A·g·I·F** (g = fator solar do vidro, I = radiação incidente, F = fator de sombreamento).
- **Ocupantes:** ≈ 75 W sensíveis + 55 W latentes por pessoa em atividade leve.
- **Equipamentos e iluminação.**
- **Transmissão** (ΔT menor que no inverno) e **ventilação** (carga sensível e latente).
**Exemplo (mesma sala, ambiente 32 °C → 24 °C):** ganho solar 3 m² · 0,6 · 500 W/m² · 0,5 = **450 W**; 2 pessoas = **260 W**; equipamentos **200 W**; iluminação **100 W**; transmissão 25,6 · 8 = **205 W**; ventilação 0,34·0,6·54·8 = **88 W** → **≈ 1,3 kW** de carga de arrefecimento.
- **Regras práticas** ("100 a 150 W/m²") **só servem para uma estimativa muito grosseira**: a orientação, os vidros e o sombreamento mudam muito o resultado.
- **Escolha do equipamento:** potência nominal **ligeiramente acima** da carga, mas **sem sobredimensionar** (arranques frequentes, pior rendimento e conforto).

## 3. Tipos de sistemas
| Sistema | Como funciona | Notas |
|---|---|---|
| **Split / multi-split (ar-ar)** | bomba de calor reversível; unidade interior + exterior | económico; aquece e arrefece; elimina caldeira em climas moderados |
| **VRF/VRV** | um módulo exterior alimenta várias unidades interiores com fluxo variável de refrigerante | escritórios, hotéis; controlo por zona; projeto específico |
| **Bomba de calor ar-água (aerotermia)** | produz água quente (e fria) para radiadores, piso radiante, ventiloconvetores e AQS | eficiente com emissores de baixa temperatura (piso radiante: ida ≈ 35 °C) |
| **Chiller + ventiloconvetores (fancoils)** | água gelada distribuída a unidades terminais | edifícios de serviços |
| **Caldeira (gás, biomassa, gasóleo)** | combustão aquece água | atenção à instalação e certificação (gás, fumos) |
| **Aquecimento elétrico direto** | resistências (radiadores, tapetes) | COP = 1; só para apoios ou necessidades pequenas |
| **Painéis solares térmicos** | AQS e apoio ao aquecimento | complementar |
| **VMC dupla fluxo** | ventilação com recuperação de calor | essencial em edifícios estanques |
- **Eficiência:** **COP** (rendimento instantâneo), **SCOP/SEER** (rendimentos sazonais de aquecimento/arrefecimento), **etiqueta energética UE**. Quanto **menor a temperatura de emissão**, **maior o COP** da bomba de calor.
- **Refrigerantes:** **R32** (GWP ≈ 675, ligeiramente inflamável A2L), **R410A** (GWP ≈ 2 088, em declínio), **R290/propano** (muito baixo GWP, inflamável A3). A legislação europeia de **gases fluorados** reduz progressivamente as quantidades disponíveis e **obriga a certificação** para manuseá-los.

## 4. Águas quentes sanitárias (AQS)
- **Energia para aquecer a água:** **E = m·cp·ΔT/3 600** (kWh), com cp = 4,186 kJ/(kg·K).
- **Exemplo:** acumulador de 200 L de 15 °C para 55 °C: E = 200·4,186·40/3 600 = **9,3 kWh**.
  - Com resistência de 2 kW: ≈ **4,7 h**. Com bomba de calor de COP 3: ≈ **3,1 kWh elétricos**.
- **Legionella:** o acumulador deve ter **ciclos regulares de temperatura ≥ 60 °C** (por exemplo, semanalmente) e evitar **água estagnada a 25 a 45 °C**; seguir regras de qualidade da água e do fabricante.
- **Termoacumuladores elétricos** continuam comuns: ver circuito dedicado em UC04673 e UC01781.

## 5. Dimensionamento elétrico (a parte que cabe ao eletricista)
- **Split de 2,5 kW de arrefecimento**, potência elétrica absorvida ≈ 0,7 kW: Ib ≈ 700/(230·0,9) ≈ **3,4 A**; circuito dedicado (curva C), cabo conforme cálculo (UC01781), **diferencial** conforme instruções do fabricante (**os inversores de AVAC podem exigir tipo A ou F**).
- **Aerotermia de 8 kW térmicos, COP = 3,5:** potência elétrica = 8/3,5 = **2,29 kW** → Ib ≈ 2 286/(230·0,95) = **10,5 A**. **Com resistência elétrica de apoio de 3 kW** (arranque em dias frios ou desinfeção): (2,29 + 3) = 5,29 kW → Ib ≈ **24,2 A** → circuito de 25 A (curva C) e cabo de 4 mm² a verificar com agrupamento e queda de tensão. **Seguir sempre o esquema e a corrente máxima da ficha técnica** (muitas máquinas têm circuitos separados para compressor e resistência de apoio).
- **Corrente de arranque:** equipamentos com inversor têm arranque suave; **ligar sempre à proteção indicada pelo fabricante** (calibre e curva).
- **Terra e equipotencialidade:** carcaças metálicas, unidades exteriores, tubagens de água (UC01782).
- **Sobretensões:** unidades exteriores em coberturas ou paredes expostas: SPD no quadro.
- **Comando e comunicação:** termóstatos (0-10 V, Modbus, KNX, Wi-Fi), **integração com GTC** (UC01784) ou **domótica** (UC03099), sondas de temperatura (Pt1000/NTC).
- **Seccionador local** junto da unidade exterior (manutenção), IP adequado e proteção UV.
- **Segurança com R32/R290:** respeitar **distâncias e volumes mínimos de instalação** definidos pelo fabricante e pela norma, e **não instalar fontes de ignição** em zonas de acumulação potencial.

## 6. Como fazer uma proposta técnica (passos)
1. **Visita e levantamento:** áreas, orientação, pé-direito, vãos, isolamento, ocupação, equipamentos, horários, distribuição existente, **quadro elétrico e potência disponível**, restrições (condomínio, fachadas, ruído).
2. **Requisitos do cliente:** conforto, orçamento, estética, controlo, **operação e manutenção**, eficiência pretendida, ruído.
3. **Estimativa de cargas** (aquecimento e arrefecimento) com método simplificado e confirmação por **cálculo regulamentar** quando exigido.
4. **Escolha da solução** (2 a 3 alternativas com vantagens e custos).
5. **Dimensionamento da parte elétrica** e **verificação da potência contratada** (UC04673); **ligação a renováveis** (FV) quando útil (UC01799).
6. **Proposta escrita:** âmbito, esquema de princípio, equipamentos (marca/modelo, potências, SCOP/SEER), **exclusões**, **garantias**, **manutenção recomendada**, prazo, preço (UC00666).
7. **Condições de licenciamento ou comunicação** (condomínios, fachada, ruído, F-gas, legalização) e **responsabilidades** de cada interveniente (eletricista, técnico frigorista, instalador de gás).

## 7. Manutenção e fiabilidade (visão geral)
- **Limpeza de filtros** (mensal a trimestral conforme uso), **limpeza de permutadores**, **verificação de condensados**, **verificação de pressões e fugas** (por técnico certificado), **verificação elétrica** (apertos, correntes, isolamento), **alarme e registos**.
- **Qualidade do ar:** substituição de filtros em VMC conforme a perda de carga.

## 8. Erros comuns
- **Sobredimensionar** o equipamento "por segurança" (ciclos curtos, pior rendimento, humidade mal controlada).
- **Ignorar a ventilação** em edifícios estanques (condensações, bolores).
- **Dimensionar a bomba de calor** sem considerar os emissores (radiadores de alta temperatura reduzem muito o COP).
- **Esquecer a potência contratada** e a corrente de apoio elétrico.
- **Unidade exterior** mal posicionada (ruído, recirculação de ar, acesso).
- **Prometer poupanças** sem simulação e sem custos reais de energia.
- **Mexer em circuitos frigoríficos ou de gás** sem certificação.
- **Condensados** sem escoamento adequado.

## 9. Exercícios (com resultados)
1. Perdas por transmissão: Σ(U·A) = 40 W/K, ΔT = 18 K. Perdas? **R: 720 W.**
2. Ventilação: 100 m³, n = 0,5 h⁻¹, ΔT = 15 K. Potência de ventilação? **R: 0,34·0,5·100·15 = 255 W.**
3. Aquecer 300 L de 15 °C para 60 °C: energia? **R: 300·4,186·45/3 600 = 15,7 kWh.**
4. Bomba de calor de 6 kW térmicos com COP 4: potência elétrica? **R: 1,5 kW.**
5. Quais as vantagens de um piso radiante com bomba de calor? **R: baixa temperatura de emissão (≈ 35 °C) → COP alto; conforto uniforme; resposta lenta (inércia).**

## 10. Fontes externas sugeridas
- **Regulamentação nacional de desempenho energético** (ADENE/DGEG: sistema de certificação energética, regulamentos de edifícios de habitação e de serviços) e **EN 16798-1** (paga: usar guias públicos).
- **Fabricantes de AVAC** (Daikin, Mitsubishi Electric, Toshiba, Fujitsu, Panasonic, Vaillant, Bosch): software de seleção, manuais e fichas técnicas.
- **ASHRAE** e **REHVA**: guias e materiais técnicos públicos sobre conforto, ventilação e eficiência.
- **Legislação de gases fluorados** (regulamento europeu) e organismos de certificação de técnicos.
- PDF do referencial da UC (ANQEP).
