# UC01782 - Executar circuitos de terra e de proteção contra descargas atmosféricas

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Limites de resistência de terra, secções mínimas e classes de proteção devem ser confirmados no RTIEBT, na IEC/EN 62305 e na regulamentação em vigor. Valores de resistividade do solo são ordens de grandeza: medir no local.

## PARTE A - Ligação à terra

### 1. Esquemas de ligação à terra (IEC 60364)
Duas letras: 1.ª = ligação da alimentação à terra (T = direta, I = isolada/impedância); 2.ª = massas da instalação (T = terra local, N = ligadas ao neutro da alimentação).
- **TT**: neutro da rede à terra no transformador; massas da instalação com **terra própria**. É o esquema habitual em instalações alimentadas pela rede pública de BT. Proteção por **dispositivo diferencial (DDR)** obrigatória na prática.
- **TN-S**: neutro e PE separados em toda a instalação. **TN-C**: PEN comum (não admitido em secções pequenas, < 10 mm² Cu). **TN-C-S**: PEN a montante, separado em PE + N a jusante (a partir da separação nunca mais se ligam).
- **IT**: neutro isolado ou ligado à terra por impedância; usado onde a continuidade é crítica (blocos operatórios, algumas indústrias). Exige monitor de isolamento.
- Qual se aplica numa instalação nova depende do que a rede de distribuição fornece: confirmar com o operador de rede / projeto.

### 2. Tensão de contacto e proteção contra contactos indiretos
- Tensão de contacto limite convencional: **50 V CA** (25 V em locais húmidos/agrícolas e outros casos particulares: confirmar RTIEBT).
- **Esquema TT:** condição **RA · IΔn ≤ 50 V** (RA = resistência da terra das massas; IΔn = sensibilidade do diferencial).
  - IΔn = 30 mA → RA ≤ 1 667 Ω; 300 mA → RA ≤ 167 Ω; 500 mA → RA ≤ 100 Ω.
  - A condição teórica é muito folgada, mas na prática procura-se terra baixa por estabilidade, sobretensões e funcionamento fiável dos aparelhos. Valores de referência práticos (confirmar com a regulamentação e requisitos da distribuidora): valores baixos (dezenas de Ω) são bom objetivo de projeto.
- **Esquema TN:** **Zs · Ia ≤ U0** (ver UC01781).
- **Equipotencialidade:** ligar entre si as partes condutoras (tubagens metálicas de água/gás/aquecimento, estruturas metálicas, PE) elimina diferenças de potencial perigosas.

### 3. Constituição da instalação de terra
1. **Elétrodo de terra** (piquet, fita, malha, anel, fundações).
2. **Condutor de terra** (liga o elétrodo ao terminal principal).
3. **Terminal/barra principal de terra** (acessível, desligável para medição).
4. **Condutores de proteção (PE)** até às massas.
5. **Ligação equipotencial principal** (e suplementar quando exigida, ex.: casas de banho).

**Secções mínimas de referência (IEC 60364-5-54, confirmar):**
- Condutor de terra em Cu: 2,5 mm² se protegido mecanicamente e contra corrosão; **16 mm²** se enterrado sem proteção mecânica (ou 25 mm² de aço galvanizado em alguns casos).
- Ligação equipotencial principal: ≥ metade da maior secção PE da instalação, mínimo **6 mm² Cu** (não é necessário exceder 25 mm² Cu).
- PE: ver regra na UC01781 (S_fase ≤ 16 → S; 16-35 → 16; > 35 → S/2).
- Cores: PE verde-amarelo; neutro azul.

### 4. Elétrodos e resistência de terra (ordem de grandeza)
**Resistividade do solo ρ (Ω·m), valores típicos muito variáveis:** terreno húmido/argiloso 30-100; terra vegetal 50-200; arenoso seco 200-1 000; rocha > 1 000. Varia com humidade e estação: dimensionar para a pior estação.

**Fórmulas:**
- **Piquet vertical** (comprimento L, diâmetro d): R ≈ ρ/(2πL) · (ln(4L/d) − 1). Estimativa grosseira: **R ≈ ρ/L**.
- **Condutor horizontal enterrado** (comprimento L): R ≈ 2ρ/L.
- **Vários piquets em paralelo**, afastados ≥ 2 vezes o comprimento: R ≈ R1/n (ligeiramente pior se estiverem mais próximos).
- **Anel/fundações** (condutor em torno da edificação): bom elétrodo, usado em instalações novas.

**Exemplo 1 (piquet):** ρ = 100 Ω·m, piquet de aço-cobre L = 2,5 m, d = 16 mm.
- R = 100/(2π·2,5) · (ln(4·2,5/0,016) − 1) = 6,37 · (6,44 − 1) = **34,6 Ω**.
- Dois piquets afastados ≥ 5 m: ≈ **17-19 Ω**.
- Para chegar a ~10 Ω em ρ = 100 Ω·m, faltaria cerca de 3 a 4 piquets ou um anel horizontal de 20 m (R ≈ 2·100/20 = 10 Ω).

**Exemplo 2 (verificação TT):** terra medida RA = 45 Ω, diferencial 30 mA.
- UL = RA · IΔn = 45 · 0,03 = **1,35 V** ≪ 50 V ✓.
- Com diferencial 300 mA: 45 · 0,3 = 13,5 V ✓ (também cumpre). Com RA = 200 Ω e 300 mA: 60 V > 50 V → **não cumpre** (exceder 167 Ω).

### 5. Ensaios e medição (verificação inicial)
- **Resistência da terra:** método de 3 pólos (queda de potencial, sonda de tensão a ~62% da distância ao elétrodo auxiliar de corrente) ou método com pinça (loop) em sistemas com várias terras. Medir com o elétrodo desligado da instalação (ou com o equipamento adequado).
- **Impedância do lacete de avaria (Zs):** esquemas TN.
- **Continuidade** dos condutores de proteção e equipotencialidade.
- **Resistência de isolamento:** 500 V DC para circuitos até 500 V; valor mínimo de referência **1 MΩ** (IEC 60364-6).
- **Ensaio dos diferenciais:** corrente de disparo (entre 50% e 100% de IΔn) e tempo (≤ 300 ms para o tipo geral a IΔn; ≤ 40 ms a 5·IΔn).
- Registar valores e instrumento (calibração válida) na ficha de verificação.

### 6. Erros comuns
- Ligar a terra do edifício apenas ao quadro e esquecer a equipotencial das tubagens metálicas.
- Medir com o terminal de terra ligado a outras massas e aceitar o valor sem questionar.
- Dimensionar o diferencial só por IΔn sem pensar no tipo (AC/A/F/B) face às cargas (carregadores VE, variadores, inversores).
- Misturar neutro e PE a jusante da separação em TN-C-S.
- Terra de proteção e de descargas sem equipotencialidade entre elas (diferença de potencial na descarga).

---

## PARTE B - Proteção contra descargas atmosféricas

### 7. Norma e conceito
- Referência: **IEC/EN 62305** (partes 1-4): princípios gerais, avaliação do risco, danos físicos/perigo de vida, sistemas elétricos e eletrónicos. Em instalações elétricas BT, o RTIEBT trata ainda a proteção contra sobretensões (limitadores de sobretensão, SPD).
- **Avaliação de risco** (IEC 62305-2) decide se é obrigatória proteção e que nível: depende da densidade de raios do local, dimensões da estrutura, ocupação, conteúdo, serviços ligados (linhas elétricas e telecomunicações). Em edifícios correntes, muitas vezes é uma ferramenta de software normalizada.
- Dois subsistemas complementares:
  - **LPS externo (SPCDA/pára-raios):** captores + descidas + terra → conduz a descarga para a terra sem danificar a estrutura.
  - **Proteção interna:** equipotencialidade + limitadores de sobretensão (SPD) → evita faíscas perigosas e protege equipamentos.

### 8. LPS externo
- **Níveis de proteção (LPL I a IV)**, I = mais exigente.
- **Captores:** haste Franklin, condutores em malha/gaiola de Faraday, cabos suspensos.
- **Método da esfera rolante:** raio da esfera por classe: I = 20 m; II = 30 m; III = 45 m; IV = 60 m. As zonas que a esfera não toca são protegidas.
  - Raio de proteção ao nível do solo de um captor vertical de altura h: **r = √(h·(2R − h))**.
  - **Exemplo 3:** haste de 10 m. Classe I (R = 20 m): r = √(10·30) = **17,3 m**; Classe II (R = 30 m): √(10·50) = **22,4 m**; Classe III (R = 45 m): √(10·80) = **28,3 m**; Classe IV (R = 60 m): √(10·110) = **33,2 m**.
  - Classe mais exigente = raio menor = mais captores para cobrir a mesma área.
- **Malha:** dimensões típicas por classe (ex.: classe I 5x5 m; II 10x10 m; III 15x15 m; IV 20x20 m).
- **Descidas:** distância média entre descidas por classe (ex.: I e II 10 m; III 15 m; IV 20 m); no mínimo 2 descidas; devem ser simétricas e o mais direitas possível.
- **Distância de segurança (s):** entre LPS e instalações internas, para evitar faíscas perigosas; **s = ki · kc/km · l** (l = comprimento ao longo do captor/descida até ao ponto de equipotencialidade). Se não for possível cumprir, liga-se por **equipotencialidade direta** ou por SPD tipo 1.
- **Materiais:** cobre, aço galvanizado, alumínio (não enterrado), aço inox. Secções mínimas de referência (confirmar IEC 62305-3): captores/descidas Cu 50 mm², aço 50 mm², Al 70 mm².
- **Terra do LPS:** de preferência **elétrodo único integrado** (anel, fundações) ligado à terra de proteção da instalação para evitar diferenças de potencial. Resistência: a norma privilegia a geometria do elétrodo mais do que um valor de Ω.

### 9. Proteção interna: equipotencialidade e SPD
- **Ligação equipotencial para descargas:** todas as entradas metálicas (água, gás, estruturas, calhas, blindagens) ligadas ao terminal principal, diretamente ou por **SPD** quando não admitem ligação direta (linhas elétricas, telecom).
- **SPD (limitadores de sobretensão):**
  - **Tipo 1 (T1):** suporta corrente de descarga direta (onda **10/350 µs**, Iimp); instalado à entrada quando há LPS externo ou linha aérea exposta.
  - **Tipo 2 (T2):** sobretensões induzidas/de manobra (onda **8/20 µs**, In e Imax); no quadro geral/secundário.
  - **Tipo 3 (T3):** proteção fina junto do equipamento sensível.
  - Parâmetros a ler: **Uc** (tensão máxima de funcionamento contínuo, ≥ 1,1 · U0 em TT/TN), **Up** (nível de proteção, deve ficar abaixo da suportabilidade ao choque do equipamento: categorias de sobretensão I a IV da IEC 60664), In, Iimp, Imax.
  - **Coordenação:** distância entre SPD de tipos diferentes (≥ 10 m de cabo, ou usar SPD coordenados do mesmo fabricante).
  - **Ligações curtas:** o comprimento total dos cabos de ligação do SPD (derivação para a barra de terra) deve ser **≤ 0,5 m**, porque cada metro de cabo acrescenta ~1 kV de queda de tensão em descargas rápidas (~1 µH/m).
  - **Proteção do SPD:** fusível ou disjuntor a montante conforme especificação do fabricante, para sobrecorrentes de curto-circuito do SPD.
- **Categorias de sobretensão (230/400 V):** I 1,5 kV (equipamento sensível); II 2,5 kV (eletrodomésticos); III 4 kV (quadros e aparelhagem); IV 6 kV (origem da instalação, contadores).

### 10. Exemplo de seleção rápida de SPD
Moradia ligada à rede aérea, sem pára-raios, TT, 230/400 V:
- Quadro geral: SPD tipo 2, Uc ≥ 255 V (1,1·230 = 253), Up ≤ 1,5 kV, In ≥ 20 kA (8/20).
- Se o quadro de entrada e o quadro secundário (sensíveis) estiverem a > 10 m, repetir tipo 2 (ou tipo 3) junto do equipamento sensível.
- Linhas de telecom/ITED/antena: SPD próprio de telecom, ligados à mesma equipotencial.
- Com pára-raios externo (LPS) ou linha aérea muito exposta: SPD tipo 1 (ou 1+2) na entrada.
(Confirmar sempre com a avaliação de risco e as indicações do fabricante.)

### 11. Erros comuns
- Instalar SPD com cabos de ligação longos (anula a proteção).
- Tipo 2 onde era necessário tipo 1 (instalação com LPS externo).
- Não proteger as linhas de telecom e antena (a sobretensão entra por aí).
- Terra do pára-raios separada da terra da instalação sem equipotencialidade.
- Esquecer o fusível de proteção do SPD quando o fabricante o exige.

---

## Exercícios (com resultados)
1. Elétrodo com RA = 80 Ω, DDR 300 mA em TT: cumpre? **R: UL = 80·0,3 = 24 V ≤ 50 V ✓.**
2. Terreno ρ = 50 Ω·m, fita horizontal de 15 m: R aproximada? **R: 2·50/15 ≈ 6,7 Ω.**
3. Captor vertical de 8 m, classe II (R = 30 m): raio de proteção ao solo? **R: √(8·(60−8)) = √416 ≈ 20,4 m.**
4. Cabo de ligação do SPD com 1,5 m: que queda de tensão adicional aproximada numa descarga rápida (1 kV/m)? **R: ≈ 1,5 kV adicionais à tensão Up do SPD → reduzir o comprimento para ≤ 0,5 m.**
5. SPD com Uc de 275 V, rede 230/400 V TT: adequado? **R: Sim (≥ 1,1·230 = 253 V).**

## Fontes externas sugeridas
- RTIEBT (DGEG): terras, equipotencialidade, sobretensões.
- Guias técnicos gratuitos de fabricantes de proteção contra descargas (DEHN, OBO Bettermann, Hager, Schneider): guias de projeto e de seleção de SPD.
- IEC/EN 62305: norma paga, protegida por direitos de autor: usar os guias de fabricantes como material público.
- Medição: manuais dos medidores de terra e de loop (Fluke, Metrel, Chauvin Arnoux) com procedimentos passo a passo.
- PDF do referencial da UC (ANQEP).
