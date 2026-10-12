# UC04676 - Instalar infraestruturas de carregamento de VE

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Requisitos específicos (proteções, regras de licenciamento, rede MOBI.E, instalações em condomínios e parques) estão em regulamentação em evolução: **confirmar na versão em vigor** (RTIEBT/IEC 60364-7-722, regras da DGEG e da MOBI.E, instruções do fabricante do posto de carregamento).

## 1. Modos de carregamento (IEC 61851-1)
| Modo | Descrição | Uso |
|---|---|---|
| **1** | Tomada normal sem comunicação | Desaconselhado/proibido em muitos países para VE |
| **2** | Cabo com caixa de controlo e proteção (IC-CPD) numa ponta | Emergência/ocasional; **não** substitui um posto dedicado |
| **3** | Posto de carregamento dedicado (wallbox) com comunicação (pilot) | Standard em habitação e comercial (corrente alternada) |
| **4** | Carregador DC externo (rápido) | Carregamento rápido em estações |

## 2. Fichas e comunicação
- **Tipo 2 (IEC 62196-2):** ficha padrão europeia para AC (monofásico ou trifásico).
- **CCS Combo 2:** carregamento DC (acrescenta dois pinos DC à ficha Tipo 2).
- **CHAdeMO:** DC (ainda existente em alguns veículos mais antigos).
- **Sinal de controlo (CP, pilot):** o posto indica ao veículo a corrente máxima disponível por **PWM a 1 kHz**; **duty cycle = I/0,6 (%)** para 6 a 51 A. Exemplo: 16 A → 26,7%; 32 A → 53,3%.
- **Proximity (PP):** identifica a capacidade do cabo.
- **Autenticação/gestão (OCPP, RFID, app):** postos conectados à backend de gestão; comunicação com a rede de mobilidade elétrica.

## 3. Potências e tempos de carga
- **Monofásico:** 230 V · 16 A = **3,7 kW**; 32 A = **7,4 kW**.
- **Trifásico:** 400 V · 16 A = **11,1 kW**; 32 A = **22,2 kW** (o veículo limita a potência aceite pelo carregador de bordo).
- **Tempo de carga (aproximado):** t = Energia / (P · η), η ≈ 0,9 (perdas de carga).
  - **Exemplo:** bateria de 60 kWh, de 20% a 80% (energia = 36 kWh) em wallbox de 7,4 kW: t = 36/(7,4·0,9) = **5,4 h**.
  - O mesmo em 11 kW (trifásico, se o veículo aceitar): ≈ 3,6 h; em 3,7 kW: ≈ 10,8 h.
  - Carregamento DC rápido: potência muito superior, curva decrescente com o estado de carga.
- **Carga contínua:** o carregamento ocorre durante muitas horas à corrente máxima; **dimensionar o circuito para 100% da corrente nominal do posto**, sem contar com simultaneidade.

## 4. Circuito dedicado e proteções (referência, confirmar na versão em vigor)
- **Circuito exclusivo** para o posto de carregamento, a partir do quadro (nunca derivado de um circuito de tomadas existente).
- **Proteção contra sobreintensidades:** disjuntor curva C (ou B) com calibre ≥ corrente nominal do posto; cabo dimensionado para a corrente contínua (UC01781: agrupamento, temperatura, queda de tensão).
- **Proteção diferencial:** o circuito deve ter diferencial **30 mA**. O posto deve **detetar correntes de fuga contínuas** (≥ 6 mA DC): ou o diferencial é **tipo B** (ou tipo F + deteção DC), ou o posto tem **proteção DC integrada (RDC-DD)** e se usa **tipo A**. **Consultar a ficha técnica do posto e o RTIEBT.**
- **Perda de PEN/neutro (TN-C-S, TT conforme o caso):** o RTIEBT/IEC 60364-7-722 exige **proteção contra ligação perdida do neutro e perigo de tensão de contacto** em esquemas com neutro/PE combinados a montante (muitos postos têm deteção integrada).
- **Limitador de sobretensão (SPD):** recomendado no quadro, especialmente para postos exteriores.
- **Terra:** ligação de proteção do posto e de eventuais partes metálicas exteriores; resistência de terra verificada (UC01782).
- **Posto exterior:** IP54 ou superior, IK adequado, proteção UV; ficha e cabo com suporte para não ficarem no chão.

### Exemplo resolvido: posto de 7,4 kW em moradia (potência contratada de 10,35 kVA)
1. **Corrente do posto:** 32 A (monofásico).
2. **Circuito dedicado:** disjuntor **C32** (ou B32) + diferencial 30 mA tipo A com RDC-DD no posto (ou tipo B), cabo dimensionado para 32 A contínuos, p. ex. **6 mm²** em B1 sem agrupamento (36 A de referência, confirmar fatores) ou **10 mm²** se agrupado/longo.
3. **Queda de tensão:** com 6 mm² e L = 20 m: 2·0,0225·20·32/6 = 4,8 V = **2,1%** ✓ (confirmar limite aplicável).
4. **Impacto na potência contratada:** o posto sozinho absorve 7,4 kW; com 10,35 kVA contratados sobra pouco para o resto da casa. **Soluções:** (a) aumentar a potência contratada; (b) **gestão dinâmica de carga** (balanceamento): o posto reduz a corrente quando o consumo da casa aumenta, medindo a corrente na entrada com um TC/medidor; (c) limitar o posto a 16 A (3,7 kW) ou 20 A ajustando o posto, com circuito e proteção coerentes.
5. **Contador/ligação:** se a potência contratada aumentar, o pedido é feito ao comercializador; a distribuidora ajusta os aparelhos de entrada (UC01788).

## 5. Gestão de energia e integração
- **Balanceamento dinâmico de carga** entre vários postos (parques de condomínio): limita a potência total conforme a potência disponível.
- **Integração com fotovoltaico:** modo "solar" (carga com excedentes) em alguns postos; exige medição de produção/consumo.
- **Carregamento inteligente (smart charging):** carga em horas de vazio/tarifas baixas, controlo remoto, relatórios.
- **Instalações coletivas:** em condomínios existem regras e infraestruturas pré-cabladas (prumada/caminhos de cabos); medição individual por lugar e rateio da energia.

## 6. Ensaios e entrega
- Continuidade do PE e resistência de terra.
- Resistência de isolamento (500 V DC).
- Teste dos diferenciais (disparo e tempo) e da proteção DC do posto.
- Verificação da sequência de comunicação (pilot) com testador de postos (EVSE tester) e polaridade/sequência de fases.
- Configuração do posto (corrente máxima, balanceamento, OCPP) e **documentação ao cliente**.

## 7. Erros comuns
- Ligar o posto a um circuito de tomadas existente.
- Cabo dimensionado "pelo calibre da tomada" sem considerar a carga contínua e o agrupamento.
- Diferencial tipo AC sem proteção DC (risco de cegar o diferencial por fuga DC do carregador).
- Esquecer o impacto na potência contratada (disparos do disjuntor geral).
- Instalar o posto a longa distância do quadro sem verificar a queda de tensão.
- Usar tomada industrial com cabo Modo 2 como solução permanente em exterior.

## 8. Exercícios (com resultados)
1. Posto trifásico de 22 kW (32 A) com veículo que aceita 11 kW: tempo para 30 kWh? **R: 30/(11·0,9) ≈ 3,0 h.**
2. Corrente de 20 A no posto: duty cycle do pilot? **R: 20/0,6 = 33,3%.**
3. Casa com 6,9 kVA contratados e consumo base de 3 kW, posto de 7,4 kW: o que acontece sem gestão dinâmica? **R: soma 10,4 kW > 6,9 kVA: o disjuntor geral dispara; usar balanceamento dinâmico ou reduzir a corrente do posto (p. ex. 16 A = 3,7 kW).**
4. Posto de 16 A (3,7 kW), cabo 2,5 mm² em B1, 25 m: queda de tensão? **R: 2·0,0225·25·16/2,5 = 7,2 V = 3,1% (rever limite; 4 mm² dá 1,96%).**

## 9. Fontes externas sugeridas
- DGEG e **MOBI.E**: regras da rede de mobilidade elétrica, licenciamento e requisitos técnicos.
- Guias de instalação gratuitos de fabricantes (Wallbox, Schneider EVlink, ABB Terra AC, Easee, Hager Witty): proteções exigidas, esquemas, comissionamento.
- RTIEBT e IEC 60364-7-722, IEC 61851-1 (pagas): usar guias de fabricante como material público.
- PDF do referencial da UC (ANQEP).
