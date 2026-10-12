# UC01784 - Instalar componentes de sistemas de gestão técnica

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Protocolos, classes de eficiência energética de edifícios e requisitos regulamentares (SCE, RECS, F-gases, etc.) devem ser confirmados nas versões em vigor. Parâmetros de sensores e atuadores vêm dos datasheets.

## 1. O que é a gestão técnica (GTC / BMS / BACS)
Sistema que **monitoriza e controla** as instalações técnicas de um edifício: **AVAC** (aquecimento, ventilação e ar condicionado), **iluminação**, **energia e contagens**, **segurança e acessos**, **elevadores**, **bombagem**, **água**, **alarmes técnicos**. Objetivos: **conforto**, **eficiência energética**, **segurança e manutenção** (alarmes e tendências).
- **Nomes equivalentes:** GTC (gestão técnica centralizada), **BMS** (Building Management System), **BACS** (Building Automation and Control System), **GTB**.
- **Eficiência energética:** a norma **EN 15232 / ISO 52120-1** classifica o nível de automação e controlo do edifício em classes **A (alto desempenho) a D (sem automação eficiente)** e estima o potencial de poupança. Confirmar a edição em vigor.

## 2. Arquitetura em três níveis
1. **Nível de campo:** **sensores** (temperatura, humidade, CO₂, pressão, caudal, presença, luminosidade), **atuadores** (válvulas, registos/dampers, variadores, relés), **contadores** (energia, água, calor).
2. **Nível de automação:** **controladores DDC/PLC** que executam o controlo (PID, sequências) e comunicam com o nível de campo e de gestão.
3. **Nível de gestão:** **servidor e interface gráfica (SCADA/BMS)**: supervisão, alarmes, programações horárias, tendências, relatórios, acesso remoto.
- **Redes:** Ethernet/IP (gestão e automação), **BACnet/IP**, **Modbus TCP**, **KNX**, **M-Bus**, **LonWorks** (legado), **OPC UA** (integração).

## 3. Protocolos de comunicação
| Protocolo | Uso típico | Notas |
|---|---|---|
| **BACnet (ISO 16484-5)** | automação de edifícios (AVAC) | normalizado, interoperável, muito usado em BMS |
| **Modbus (RTU/TCP)** | contadores, variadores, chillers, bombas de calor | simples, aberto, endereçamento por registos |
| **KNX** | iluminação, estores, climatização de sala | ver UC03099 |
| **M-Bus (EN 13757)** | contagem de energia térmica, água, gás, elétrica | 2 fios, mestre/escravo (até ≈ 250 escravos por segmento) |
| **DALI** | iluminação | integrável com gateway |
| **OPC UA** | integração IT/OT | cifrado e estruturado |
- **Gateways** convertem entre protocolos; cada ponto de integração é um **risco de falha** e de segurança.

## 4. Sensores e atuadores principais
### Sondas de temperatura
- **Pt100/Pt1000 (RTD):** resistência varia com a temperatura. Pt100 = 100 Ω a 0 °C; **Pt1000 = 1 000 Ω a 0 °C**. Coeficiente ≈ 0,385%/°C.
  - **Exemplo (Pt1000):** 0 °C → 1 000 Ω; 20 °C → 1 077,9 Ω; 25 °C → 1 097,3 Ω; 50 °C → 1 194,0 Ω.
  - **Ligação a 2, 3 ou 4 fios:** a 2 fios a resistência dos cabos soma-se (erro), a 3 fios compensa-se, a 4 fios é a mais precisa. **Pt1000 sofre menos erro por resistência de cabo do que Pt100.**
- **NTC:** termístor de resposta não linear; económico (sondas de ambiente, fancoils).
- **Humidade:** sensores capacitivos; **CO₂** (NDIR) como indicador de ocupação/qualidade do ar; **pressão diferencial** (filtros, caudais).
### Atuadores
- **Válvulas** (2 vias, 3 vias, de caudal variável) com atuador **0-10 V**, 3 pontos ou on/off; **kvs** define o caudal.
- **Registos (dampers) e atuadores de ar:** com mola de retorno em aplicações de segurança.
- **Variadores de frequência** em ventiladores e bombas (poupança energética).
- **Relés e contactores** para cargas.
### Sinais
- **0-10 V**, **4-20 mA**, **on/off**, **pulsos** (contadores), **bus**.

## 5. Controlo
- **On/Off com histerese:** simples; usado em termóstatos de baixa exigência.
- **PID:** **P** (proporcional): reação ao erro; **I** (integral): elimina erro estático; **D** (derivativo): antecipa. **Ajustar** com cuidado (começar só com P, depois I; D raramente necessário em AVAC). Oscilações sinalizam ganho excessivo.
- **Sequências de operação:** descrevem como o sistema funciona (por exemplo, "se T_sala < setpoint − 0,5 °C, abre válvula de aquecimento 0-100% por PI; se CO₂ > 900 ppm, aumenta o caudal de ar novo"). **Escreve-se antes de programar**.
- **Programações horárias, feriados, modos (conforto, económico, standby, noite).**
- **Compensação em função da temperatura exterior (curva de aquecimento).**
- **Intertravamentos e proteções:** anti-gelo da bateria, caudal mínimo, pressostato de filtro sujo, falha de ventilador.

## 6. Balanço térmico: potência de um circuito de água
**P = ṁ · cp · ΔT**, com **ṁ** (kg/s), **cp ≈ 4 186 J/(kg·K)** para água, **ΔT** (K).
- **Exemplo:** caudal de 2 m³/h (≈ 0,556 kg/s) com ΔT = 5 K: P = 0,556 · 4 186 · 5 ≈ **11 628 W ≈ 11,6 kW**.
- Uso: calcular a **potência de uma bateria**, validar **caudalímetros e contadores de energia térmica** e **verificar o rendimento** de chillers/bombas de calor (COP = potência térmica útil / potência elétrica consumida).

## 7. Contagem e monitorização de energia
- **Contadores de energia elétrica** (com Modbus ou M-Bus), **de calor/frio** (caudalímetro + 2 sondas de temperatura), **de água** (pulsos ou M-Bus).
- **Intervalo de aquisição:** tipicamente 15 minutos (alinha com a curva de carga do operador).
- **Indicadores:** kWh/m², kWh por utilizador, **perfil de carga base** (consumo noturno/fins de semana revela desperdício), deteção de desvios.
- **Dashboards e relatórios** para gestor do edifício; **alertas** de consumo anómalo.
- **Ligação** a fotovoltaico, armazenamento e VE (UC01799, UC01801, UC04676).

## 8. Alarmes e manutenção
- **Alarmes técnicos:** falha de equipamento, temperatura fora de limites, filtros sujos, falta de caudal, fuga, comunicação perdida.
- **Prioridades** (crítico, importante, informativo), **textos claros**, **reconhecimento e registo**.
- **Manutenção preditiva:** horas de funcionamento, vibração, tendências de consumo e de temperatura de retorno.
- **Relatório e histórico**: ajuda a justificar intervenções e a otimizar.

## 9. Projeto e instalação (passos)
1. **Levantamento do edifício e dos sistemas técnicos**; objetivos do cliente.
2. **Lista de pontos (I/O list):** para cada ponto, tipo (AI/AO/DI/DO/bus), localização, sinal, endereço, ponto de alarme.
3. **Sequências de operação e esquemas de princípio** (um por sistema).
4. **Seleção de controladores e protocolo**; reserva de pontos (≥ 10 a 20%).
5. **Cablagem:** cabos de sinal blindados, separação de potência, **etiquetagem por ponto**, **terminações de bus**, topologia respeitada (RS-485: cadeia, sem estrela, terminação nas pontas).
6. **Quadros de automação:** fonte 24 V com margem, proteções, bornes identificados, esquema atualizado.
7. **Programação, gráficos e alarmes**; **comissionamento ponto a ponto** (simular, forçar, verificar o sentido de atuadores, calibrar sondas).
8. **Testes funcionais** das sequências (inclusive modos de falha) e **formação do operador**.
9. **Documentação final**: lista de pontos, esquemas, programas, backup, manual.

## 10. Segurança informática (OT)
- **Separar a rede do BMS** da rede corporativa e da Internet (VLAN/firewall); **não expor** portas BACnet/Modbus à Internet.
- **Passwords fortes**, **contas individuais**, **atualizações** de firmware, **desativar serviços não usados**.
- **Acesso remoto via VPN**; **registo** de acessos e alterações.
- **Backup** dos programas e configurações e **plano de recuperação**.
- Em edifícios com contratos de manutenção, definir **quem pode alterar o quê**.

## 11. Erros comuns
- **Instalar sem sequência de operação escrita** (cada um programa à sua maneira).
- **Lista de pontos incompleta** (faltam alarmes, contadores ou reserva).
- **Sondas mal posicionadas** (ao sol, perto de aberturas, sem pocket correto) → decisões erradas.
- **Cabos de sinal junto de cabos de potência** (ruído, leituras instáveis).
- **Topologia RS-485 em estrela** ou sem terminação.
- **PID mal ajustado** (oscilação, desgaste de válvulas).
- **Sem testes de falha** (perda de comunicação, cortes de energia) nem modo manual de emergência.
- **Rede do BMS aberta à Internet** com credenciais por defeito.
- **Nenhuma formação ao operador** nem documentação.

## 12. Exercícios (com resultados)
1. Pt1000 a 50 °C: resistência aproximada? **R: ≈ 1 194 Ω.**
2. Circuito de água a 3 m³/h com ΔT = 6 K: potência térmica? **R: ṁ = 0,833 kg/s; P ≈ 0,833·4 186·6 ≈ 20,9 kW.**
3. Um chiller entrega 100 kW de frio com 28 kW elétricos: COP? **R: 100/28 ≈ 3,6.**
4. Porque se prefere Pt1000 a Pt100 em cabos longos a 2 fios? **R: a mesma resistência de cabo representa um erro relativo 10 vezes menor em Pt1000.**
5. Quantos pontos reservar numa lista de pontos para futuras expansões? **R: tipicamente 10 a 20%.**

## 13. Fontes externas sugeridas
- **BACnet International** (bacnet.org) e guias de aplicação de fabricantes (Siemens Desigo, Schneider EcoStruxure Building, Honeywell, Johnson Controls, Trend, Distech).
- **EN 15232 / ISO 52120-1** (pagas): usar guias de fabricantes e documentos de organizações do setor como material público.
- Documentação de **ADENE/DGEG** sobre eficiência energética em edifícios (SCE, RECS) e gestão de energia.
- Guias de cibersegurança OT/ICS de entidades europeias (ENISA) e nacionais.
- PDF do referencial da UC (ANQEP).
