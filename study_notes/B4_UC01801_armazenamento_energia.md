# UC01801 - Projetar soluções de armazenamento de energia

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Os valores de baterias (ciclos, rendimento, DoD, tensão) variam por fabricante e tecnologia: usar o datasheet. Requisitos de segurança e localização de baterias (incêndio, ventilação) seguem a regulamentação e as instruções do fabricante.

## 1. Conceitos
- **Capacidade nominal (kWh):** energia total armazenada. **Capacidade útil** = nominal x DoD (profundidade de descarga admitida).
- **Potência (kW):** potência contínua que a bateria/inversor consegue fornecer ou absorver.
- **C-rate:** potência/energia por hora (C/2 → descarga completa em 2 h).
- **Rendimento round-trip:** energia que sai / energia que entrou (tipicamente **90 a 95%** em lítio, menor em chumbo).
- **Ciclos de vida:** número de ciclos a determinado DoD até a capacidade cair (p. ex. 80% da inicial).
- **Estado de carga (SoC)** e **estado de saúde (SoH).**

## 2. Tecnologias
| Tecnologia | DoD útil típico | Ciclos (ref.) | Notas |
|---|---|---|---|
| **LFP (LiFePO4)** | 90-100% | 4 000 a 8 000 | mais segura termicamente, dominante em armazenamento doméstico |
| **NMC (iões de lítio)** | 80-90% | 2 000 a 4 000 | mais densidade energética, mais sensível a temperatura |
| **Chumbo-ácido (AGM/gel)** | 40-50% | 300 a 1 500 | barata ao início, vida curta, manutenção |
| **Fluxo (vanádio)** | ~100% | > 10 000 | grandes instalações, baixa densidade, caras |
(valores de ordem de grandeza: confirmar no datasheet)

## 3. Topologias
- **Acoplamento DC (inversor híbrido):** FV e bateria no mesmo inversor, com menos conversões (rendimento melhor); ideal em instalações novas.
- **Acoplamento AC (inversor de bateria separado):** liga-se ao lado AC; fácil de adicionar a um sistema FV existente, com mais conversões.
- **Backup/ilhamento (EPS/UPS):** alimenta circuitos essenciais quando falha a rede (exige quadro de essenciais e inversor com função de backup).
- **Off-grid:** sem rede; dimensionamento por dias de autonomia e fonte de recurso (FV, gerador).
- **Tensão do banco:** baixa tensão (48 V) ou alta tensão (100 a 600 V). Para a mesma potência, **alta tensão = menor corrente = cabos mais finos**.

## 4. Dimensionamento
### Capacidade
1. **Perfil de consumo e produção:** quanta energia queres deslocar (do dia para a noite) e o excedente FV disponível.
2. **Energia a fornecer:** E_carga (kWh/dia).
3. **Capacidade nominal:** **C_nom = E_carga / (DoD · η_conversão)**.
4. **Potência da bateria/inversor:** ≥ potência máxima das cargas que se pretende alimentar em simultâneo.

**Exemplo resolvido:** casa que consome 6 kWh entre o pôr do sol e a manhã; bateria LFP (DoD útil 90%), inversor/conversão η = 0,95.
- C_nom = 6/(0,90·0,95) = **7,0 kWh** → bateria comercial de **7 a 8 kWh** (p. ex., módulos de 2,5 a 5 kWh em série/paralelo).
- Potência: se a casa consome 3 kW à noite, bateria e inversor de **≥ 3 kW** (idealmente 5 kW para picos).
- Excedente FV disponível: verificar que o campo FV produz, em média, pelo menos os 6 kWh a mais do que o consumo diurno: **sem excedente, a bateria não carrega**.
- **Corrente a 5 kW:** em 48 V (51,2 V nominal): ≈ **98 A**: cabos de 25 a 35 mm² e proteção DC robusta; em 200 V: **25 A** (muito mais simples).

### Valor económico (verificação prática)
- **Poupança anual** ≈ energia deslocada x (preço da energia comprada − valor da injeção do excedente).
- **Retorno do investimento** = custo / poupança anual; avaliar com tarifas reais e com a degradação da bateria. Em muitos casos, a bateria só se justifica quando há grande diferença entre o preço de compra e o de injeção, ou quando o backup tem valor.

## 5. Segurança e instalação
- **Proteção contra sobrecorrente no lado DC** (fusível/disjuntor DC com poder de corte DC adequado) e **seccionador DC** acessível.
- **BMS (Battery Management System):** protege contra sobretensão, subtensão, sobrecorrente, temperatura e equilibra as células; comunicar com o inversor (CAN/RS485) conforme o fabricante.
- **Localização:** local seco, ventilado, com temperatura dentro dos limites do fabricante (evitar sol direto e geadas), afastado de materiais combustíveis e de saídas de evacuação, conforme as instruções do fabricante e a regulamentação aplicável (SCIE, RTIEBT e requisitos de seguradoras).
- **Cabos:** secção para a corrente máxima e queda de tensão; **comprimentos iguais** entre módulos em paralelo para equilibrar correntes.
- **Terra e equipotencialidade:** carcaças das baterias e do inversor.
- **Risco de incêndio:** lítio exige instalação conforme o fabricante e certificações (por exemplo, IEC 62619 para baterias industriais/estacionárias, IEC 62477-1 para conversores): verificar a documentação.
- **Manutenção:** firmware, estado de saúde e limpeza; registo de ciclos.

## 6. Autoconsumo com e sem bateria (ordem de grandeza)
- Sem bateria: autoconsumo típico de 30 a 40% em moradias com consumo concentrado à noite.
- Com bateria dimensionada (**cerca de 1 a 2 kWh por kWp** em casas típicas): autoconsumo pode passar para **60 a 80%**.
- Estes valores dependem muito do perfil; **simular com dados reais** (contador, curva de carga a 15 min) antes de propor.

## 7. Erros comuns
- Dimensionar a bateria sem haver excedente FV para a carregar.
- Esquecer o DoD e o rendimento na capacidade.
- Cabos DC finos em sistemas de 48 V com potências elevadas (queda de tensão, aquecimento).
- Instalar a bateria sem seguir distâncias, ventilação e temperatura do fabricante.
- Misturar baterias de lotes, tecnologias ou idades diferentes.
- Prometer retorno do investimento sem tarifas reais e sem degradação.

## 8. Exercícios (com resultados)
1. Carga noturna de 8 kWh, LFP com DoD 95% e η = 0,95: C_nom? **R: 8/(0,95·0,95) = 8,9 kWh.**
2. Banco de 10 kWh em 51,2 V a descarregar 3 kW: corrente? **R: 3 000/51,2 = 58,6 A.**
3. Mesmo banco em HV 400 V: corrente? **R: 7,5 A.**
4. Bateria de chumbo, DoD 50%, para 4 kWh úteis: capacidade nominal? **R: 8 kWh (sem contar perdas).**

## 9. Fontes externas sugeridas
- Guias de projeto gratuitos de fabricantes (BYD, Pylontech, Huawei, SMA, Victron, Fronius).
- PVGIS para a produção FV associada; DGEG para requisitos de ligação e armazenamento.
- IEC 62619 e IEC 62477-1 (pagas): usar documentação de fabricantes como material público.
- PDF do referencial da UC (ANQEP).
