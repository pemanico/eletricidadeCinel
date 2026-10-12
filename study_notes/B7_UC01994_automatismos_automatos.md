# UC01994 - Instalar e programar automatismos e autómatos

> Material de estudo (explicação + exemplos de programação). **Não é fonte normativa.** Instruções, endereçamento e ambientes de programação variam por fabricante (Siemens, Schneider, Mitsubishi, Allen-Bradley, Omron, etc.); os exemplos usam a norma IEC 61131-3 em forma genérica. **Funções de segurança (paragem de emergência, resguardos) seguem normas próprias (EN ISO 13849, IEC 62061) e não devem depender só do PLC padrão.**

## 1. Automatismos: lógica cablada vs programada
- **Cablada:** contactores, relés, temporizadores e botões ligados entre si por fios; fácil em casos simples, difícil de modificar.
- **Programada (PLC/autómato):** a lógica está num programa; alterações por software; diagnóstico e comunicação; **escala melhor** em processos complexos.
- **Relés programáveis (LOGO!, Zelio, Easy):** soluções de baixo custo para pequenos automatismos.

## 2. Estrutura de um PLC
- **CPU** (processador e memória), **fonte de alimentação**, **módulos de entradas/saídas (I/O)** digitais e analógicos, **comunicação** (Ethernet, RS-485, Profinet, Modbus), e opcionalmente **HMI** (painel operador).
- **Ciclo de scan:** **ler entradas → executar o programa → atualizar saídas** (repetido continuamente, tipicamente em poucos milissegundos).
- **Memória:** programa, dados, variáveis retentivas (mantêm valor após falha de alimentação).
- **Modos:** RUN, STOP, e (nalguns) PROGRAM.

## 3. Entradas e saídas
- **Entradas digitais (DI):** 24 V DC (a mais comum), 230 V AC (menos comum). **Sinks/sources (PNP/NPN):** respeitar o tipo do sensor e do módulo.
- **Saídas digitais (DO):** **transístor** (24 V DC, rápidas, limite de corrente baixo, p. ex. 0,5 A), **relé** (potência AC/DC, mais lentas, limitadas em número de comutações), **TRIAC** (AC).
- **Entradas analógicas (AI):** **0-10 V**, **4-20 mA** (preferível para distâncias longas e resistência a ruído: 4 mA indica "zero", 0 mA indica cabo cortado), sondas **Pt100/Pt1000** e termopares (módulos específicos).
- **Saídas analógicas (AO):** 0-10 V ou 4-20 mA para variadores, válvulas e atuadores.
- **Sensores comuns:** **fim de curso**, **indutivo** (metal), **capacitivo** (materiais diversos), **ótico/fotoelétrico**, **sondas de nível**, **pressostatos**, **termóstatos**, **encoders**.
- **NO vs NC:** botão de **paragem** e dispositivos de segurança **ligam-se em NC (normalmente fechado)** para que **um fio solto provoque paragem** (princípio de segurança positiva).
- **Dimensionamento de I/O:** contar entradas e saídas necessárias e **acrescentar ≈ 20% de reserva**.

### Exemplo de contagem
12 DI, 8 DO, 2 AI → com 20%: 14,4 DI, 9,6 DO, 2,4 AI → escolher **16 DI, 16 DO (2 módulos de 8, ou 16 DO), 4 AI** conforme a modularidade do fabricante.

## 4. Linguagens de programação (IEC 61131-3)
- **LD (Ladder, escada):** semelhante a esquemas de relés; o mais usado.
- **FBD (diagrama de blocos funcionais).**
- **ST (Structured Text):** texto estruturado tipo Pascal; bom para cálculos e lógica complexa.
- **SFC (Sequential Function Chart)** ou **GRAFCET (IEC 60848):** para sequências por etapas e transições.
- **IL (Instruction List):** obsoleta na norma atual.
- **Blocos úteis:** **temporizadores** TON (atraso na ligação), TOF (atraso na desligação), TP (pulso); **contadores** CTU, CTD, CTUD; **flip-flops** SR/RS; **comparadores e matemática**.

## 5. Exemplos de programação

### 5.1 Marcha-paragem com selo (equivalente ao circuito cablado)
```
(* STOP_OK = TRUE quando botão de paragem NÃO está premido (contacto NC cablado) *)
(* OL_OK   = TRUE quando o relé térmico NÃO disparou (NC) *)
MOTOR := (START OR MOTOR) AND STOP_OK AND OL_OK;
```
Em ladder: contacto START em paralelo com contacto MOTOR (selo), em série com STOP_OK e OL_OK, e bobina MOTOR. **Se o fio do STOP soltar, STOP_OK fica FALSE e o motor pára.**

### 5.2 Arranque estrela-triângulo com temporização
```
RUN := (START OR RUN) AND STOP_OK AND OL_OK;            (* selo *)
T_STAR(IN := RUN, PT := T#6s);                           (* TON: tempo em estrela *)
T_DEAD(IN := T_STAR.Q, PT := T#100ms);                   (* TON: tempo morto *)
KM1 := RUN;                                              (* contactor de linha *)
KM2 := RUN AND NOT T_STAR.Q AND NOT KM3;                 (* estrela *)
KM3 := T_DEAD.Q AND RUN AND NOT KM2;                     (* triângulo *)
```
- **Tempo em estrela:** o suficiente para o motor atingir ~80 a 90% da velocidade (depende da carga; 5 a 10 s é frequente).
- **Tempo morto (50 a 100 ms):** evita **curto-circuito** entre KM2 e KM3 durante a comutação.
- **Intertravamento de hardware:** além do programa, colocar **contactos auxiliares NC** de KM2 e KM3 em série com as bobinas do outro (segurança contra soldadura de contactos).

### 5.3 Enchimento de depósito com sensores de nível (descrição)
- Entradas: **N_MIN** (nível mínimo), **N_MAX** (nível máximo). Saída: **BOMBA**.
- Lógica: liga a bomba quando **N_MIN** deixa de estar coberto; desliga quando **N_MAX** é coberto: `BOMBA := (NOT N_MIN OR BOMBA) AND NOT N_MAX;` (com **histerese** natural do selo).
- Proteções: **temporizador de excesso de tempo** (a bomba não pode trabalhar mais de X minutos sem o nível subir: alarme de fuga ou falta de água), **proteção de marcha em seco** e **modo manual/automático**.

### 5.4 Contagem de peças (CTU)
- Sensor de peças ligado a uma entrada; **CTU** com PV = 10: quando atinge 10 peças, ativa uma saída (embalagem) e **reinicia** o contador.

### 5.5 SFC/GRAFCET (sequência de um ciclo de furação)
- **Etapa 0:** repouso. **Transição:** START e peça presente → **Etapa 1:** fixar peça (cilindro 1 avança) → **transição:** fim de curso de fixação → **Etapa 2:** descer broca → **transição:** fim de curso inferior → **Etapa 3:** subir broca → ... → **Etapa 0**.
- A sequência por etapas torna o programa **legível e testável** (cada etapa ativa só uma ação).

## 6. HMI e SCADA
- **HMI (painel de operador):** botões, indicadores, alarmes e parâmetros para o operador; **evitar ligar botões físicos só ao HMI** em funções críticas.
- **SCADA:** supervisão remota, históricos, tendências e relatórios.
- **Gestão de alarmes:** prioridades, textos claros, registo de data e hora, reconhecimento.

## 7. Comunicação industrial
- **Modbus RTU (RS-485) / Modbus TCP:** simples, aberto, muito usado em instrumentação, contadores e variadores.
- **Profinet, EtherNet/IP, EtherCAT:** Ethernet industrial com determinismo.
- **Profibus, CAN/CANopen, IO-Link** (comunicação com sensores/atuadores inteligentes).
- **Boas práticas:** cabo blindado e ligado à terra conforme o fabricante, **terminações de bus**, endereços únicos, **topologia documentada**, separação de potência e sinal (CEM).

## 8. Instalação e comissionamento
- **Alimentação 24 V DC:** fonte de **potência com margem ≥ 20% a 30%**, protegida a montante e fusíveis por ramal; **terra e equipotencialidade**; ligações de **0 V** corretas.
- **Cablagem:** separar **potência (230/400 V)** de **sinais (24 V, analógicos, bus)**; blindagens ligadas num só lado (analógico) conforme as recomendações; ferrules nos terminais; **etiquetagem** por borne e cabo.
- **Proteção das saídas:** relés intermédios com **díodo de roda livre** (bobinas DC) ou RC (AC); **fusível em cada saída de potência**.
- **Quadros:** ventilação, IP adequado, ordenação, esquema atualizado (UC03077).
- **Comissionamento:** testar **entradas** (simular), **saídas** (forçar), **sequência** em vazio (sem carga) e depois com carga; **testar falhas** (corte de fio, perda de alimentação, queda da rede); **backup do programa** e **versão** guardada fora do PLC.
- **Documentar:** lista de I/O (endereço, símbolo, função, localização), esquemas, programa comentado, parâmetros.

## 9. Ambientes e ferramentas de aprendizagem
- **CODESYS:** ambiente IEC 61131-3 usado por muitos fabricantes, com simulador.
- **OpenPLC:** projeto aberto para praticar com hardware barato.
- **TIA Portal (Siemens), EcoStruxure Machine Expert (Schneider), GX Works (Mitsubishi), Studio 5000 (Rockwell):** ambientes comerciais, com **simuladores** (por exemplo, PLCSIM) e versões de avaliação.
- **LOGO! Soft Comfort e Zelio Soft:** para relés programáveis, com simulação.
- **Simulação antes de instalar:** reduz erros e tempo de comissionamento.

## 10. Erros comuns
- Botão de **paragem em NO** (um fio solto não pára o equipamento).
- Sem **intertravamento de hardware** entre contactores de inversão/estrela-triângulo.
- Misturar cabos de **potência e sinal** no mesmo canal (ruído nas entradas analógicas).
- **Sem reserva de I/O** nem espaço no quadro.
- Programa sem comentários, sem lista de I/O, sem backup.
- **Funções de segurança só em software** padrão.
- Esquecer o **díodo de roda livre** nas bobinas DC (queima saídas a transístor).
- Não prever o estado das saídas **em falha de alimentação** (retornar ao estado seguro).

## 11. Exercícios (com resultados)
1. Escreve a lógica ST de um motor com 2 botões de marcha (local e remoto), uma paragem NC e térmico NC. **R: `MOTOR := (START_L OR START_R OR MOTOR) AND STOP_OK AND OL_OK;`**
2. Porque se usa 4-20 mA em vez de 0-10 V em longas distâncias? **R: corrente é menos sensível à queda de tensão e ao ruído, e 0 mA identifica fio cortado.**
3. Quanto tempo mínimo deve ter o tempo morto Y-Δ? **R: o suficiente para extinguir o arco e abrir o contactor de estrela antes de fechar o de triângulo: tipicamente 50 a 100 ms.**
4. Contagem de I/O: 20 DI, 14 DO, 4 AI, com 20% de reserva. **R: 24 DI, ≈ 17 DO (→ 24 ou 16+8), 5 AI (→ 6 ou 8) conforme a modularidade.**
5. Define para o enchimento de depósito um alarme útil. **R: alarme de "tempo excessivo de enchimento" (bomba ligada X minutos sem N_MAX): fuga, bomba avariada ou falta de água.**

## 12. Fontes externas sugeridas
- Manuais de programação e de hardware dos fabricantes e **simuladores gratuitos** (TIA Portal Trial, CODESYS, LOGO! Soft Comfort, Zelio Soft).
- **PLCopen** (IEC 61131-3) e documentação do **CODESYS** com exemplos e tutoriais.
- Normas EN ISO 13849 e IEC 62061 (pagas) para segurança de máquinas; usar guias de fabricantes (Pilz, Siemens, Schneider) como material público.
- Vídeos e cursos gratuitos de ladder e ST de fabricantes e escolas técnicas.
- PDF do referencial da UC (ANQEP).
