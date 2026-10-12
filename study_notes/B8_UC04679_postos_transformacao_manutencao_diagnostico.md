# UC04679 - Efetuar a manutenção preventiva e o diagnóstico de postos de transformação de energia elétrica

> Material de estudo (explicação). **Não é fonte normativa e não habilita para trabalhos em média tensão.** Em Portugal, os postos de transformação (PT) e as instalações de média tensão (MT) têm **regulamentação própria** (por exemplo, o regulamento de segurança de subestações e postos de transformação e de seccionamento) e **regras de exploração** (técnico responsável pela exploração, procedimentos de manobra e de trabalho, inspeções periódicas). **A manutenção e as manobras em MT só podem ser feitas por pessoal formado, qualificado e autorizado**, com procedimentos formais. Confirma na DGEG, na e-Redes e na regulamentação em vigor. Este ficheiro é material de estudo para perceberes o que existe, o que se inspeciona e como se diagnostica.

## 1. O que é um posto de transformação
Instalação que **transforma a energia de MT (por exemplo, 10 ou 20 kV) para BT (400 V)** para alimentar uma ou várias instalações de utilização. Pode ser **de serviço público** (propriedade do operador da rede) ou **de serviço particular** (propriedade do cliente, com contagem em MT ou BT).

### Tipos
- **Cabina (alvenaria/betão)**: compartimento no edifício ou independente.
- **Pré-fabricado (compacto)**: cabina metálica ou de betão, entregue montada.
- **Aéreo (em poste)**: transformador no poste, para potências menores em zonas rurais.
- **Interior (em edifício)** vs **exterior**.

## 2. Constituição principal
- **Celas de MT (aparelhagem de MT):** em invólucro metálico, normalmente com **isolamento a ar ou SF6**:
  - **Cela de chegada/saída de cabos** (linha).
  - **Cela de proteção do transformador:** **interruptor-seccionador com fusíveis**, ou **disjuntor MT** com relé de proteção.
  - **Cela de medida (contagem MT)** nos casos aplicáveis (TC e TT).
  - **Seccionadores de terra** (ligação à terra de cabos e do transformador para trabalhos).
- **Transformador de potência** (UC03895): em óleo ou seco, com proteções próprias.
- **Quadro geral de BT (QGBT):** disjuntor geral (protegendo o secundário), saídas, **medida**, compensação do fator de potência, SPD.
- **Ligações:** cabos MT (terminais, blindagens ligadas à terra), barramentos BT.
- **Sistema de terras:** **terra de proteção (massas)** e **terra de serviço (neutro BT)**; regras de **separação** e **tensões de passo e de toque** na regulamentação (confirmar).
- **Auxiliares:** **iluminação normal e de emergência**, **ventilação** (natural ou forçada), **retenção de óleo** (fossa de recolha em transformadores em óleo), **extintor adequado (CO₂)**, **sinalização**, **esquemas unifilares** afixados, **tapete/banco isolante**, **luvas e pértiga isolantes**, **detetor de tensão MT**, **cadeado e etiquetas**.

## 3. Segurança: princípios (o que está em causa)
- **Perigo de morte por arco elétrico e contacto indireto/direto**: em MT, mesmo **aproximar-se** pode provocar descarga (distâncias de segurança regulamentadas).
- **Regras gerais de segurança elétrica (UC00676):** **cortar, bloquear, verificar ausência de tensão, colocar à terra e em curto-circuito, proteger a vizinhança e sinalizar**. Em MT, a **verificação e a colocação à terra** são feitas com **equipamento específico** e **procedimentos formais**.
- **Autorização de trabalho:** **plano de manobras** e **autorização/permissão de trabalho** entre o **responsável pela exploração** e o executante; **comunicação formal** de início e de fim.
- **Intertravamentos mecânicos e por chave (key interlocks):** impedem manobras indevidas (por exemplo, abrir a porta do transformador com a cela MT fechada). **Nunca anular intertravamentos.**
- **Condições do local:** acesso seguro, sinalização, **iluminação de emergência**, **extintores**, plano de evacuação; **SF6 e óleo** têm riscos ambientais e para a saúde (gestão de gases fluorados e de óleos conforme a lei).
- **EPI específico:** capacete com viseira para arco, vestuário resistente a arco, luvas isolantes de classe adequada, calçado dielétrico.
- **Nunca trabalhar sozinho** em PT, nem sem autorização e sem formação específica.

## 4. Plano de manutenção preventiva (estrutura)
**Periodicidade:** definida pelo **fabricante**, pela **regulamentação** e pela **avaliação de risco e criticidade**; é comum combinar **inspeção visual frequente** (por exemplo, trimestral ou semestral) com **ensaios e manutenção mais profunda** (por exemplo, anual, ou a cada poucos anos com paragem programada). **Confirmar as periodicidades obrigatórias.**

### Inspeção visual e geral (com o PT em serviço, sem abrir celas, a distância de segurança)
- **Estado do compartimento:** limpeza, humidade, infiltrações, sinais de roedores/insetos, **ventilação desobstruída**.
- **Sinalização, esquemas e livros de registo** afixados e legíveis.
- **Equipamentos de segurança** (extintor, luvas, pértigas, tapete isolante, iluminação de emergência) **em validade e em bom estado**.
- **Transformador:** nível de óleo, **fugas**, estado das **buchas (bornes)**, **ruído** e **vibração anormais**, **temperatura** (termómetro/termóstato), **cor do silica gel**, fecho do depósito.
- **Celas de MT:** indicadores de posição e de presença de tensão, **manómetro/indicador de pressão do SF6** (se existir), alarmes.
- **QGBT:** estado das ligações, aquecimento localizado, **sinalização de alarmes**, medidas (tensões e correntes).
- **Termografia (câmara térmica) com o PT em carga**, sem abrir proteções, pelo visor ou conforme o procedimento do fabricante.

### Manutenção com o PT fora de serviço (isolado e com procedimentos)
- **Limpeza** de isoladores, buchas, barramentos e celas (a seco ou conforme o fabricante), **retirando pó e humidade**.
- **Verificação e aperto de ligações** de potência (binários do fabricante) e **ligações de terra**.
- **Verificação mecânica** de seccionadores e interruptores: **operação manual**, **lubrificação** conforme o fabricante, **intertravamentos**, **mecanismos**.
- **Substituição de fusíveis MT** em caso de atuação (**substituir os três** ao mesmo tempo).
- **Ensaios elétricos** (secção 5).
- **Proteções:** teste de **relés de proteção** com **injeção** de corrente (primária ou secundária), verificação de **regulações e disparos**, **baterias e fontes auxiliares**.
- **Transformador em óleo:** **análise de óleo** (rigidez dielétrica, humidade, acidez, **análise de gases dissolvidos (DGA)**), reposição de nível, substituição de **silica gel**, verificação do **relé Buchholz** e das válvulas.
- **Transformador seco:** limpeza dos enrolamentos (poeiras), verificação das **sondas de temperatura** e da **ventilação forçada**.

## 5. Ensaios e medições (visão geral)
| Ensaio | Objetivo | Referência/interpretação |
|---|---|---|
| **Resistência de isolamento** (megóhmetro, tensão adequada) | estado do isolamento de enrolamentos, cabos e barramentos | comparar com **valores de referência** e com medições anteriores; corrigir pela **temperatura**; calcular o **índice de polarização (PI ≥ 2** é frequentemente indicativo de bom estado) |
| **Relação de transformação (TTR) e grupo de ligação** | detetar espiras em curto, mudança de taps incorreta | desvios típicos até **±0,5%** do valor da placa |
| **Resistência dos enrolamentos** | contactos, soldaduras, espiras | comparar fases e histórico; **desequilíbrio** baixo |
| **Resistência de contacto (micro-ohmímetro)** em aparelhagem | qualidade dos contactos | em **µΩ**, comparar com o fabricante e com ensaios anteriores |
| **Resistência de terra** | segurança contra tensões de passo e de toque | **valor máximo exigido** pelo projeto e regulamentação; medição das **terras de proteção e de serviço** |
| **Rigidez dielétrica do óleo** | capacidade isolante | valores de aceitação conforme normas (por exemplo, IEC 60422), e histórico |
| **DGA (gases dissolvidos no óleo)** | diagnosticar defeitos internos (descargas, sobreaquecimento) | interpretação por gases (hidrogénio, metano, etileno, acetileno, monóxido de carbono) e métodos de diagnóstico (por exemplo, triângulo de Duval; ver IEC 60599) |
| **Termografia** | pontos quentes em ligações e aparelhagem | diferença de temperatura (**ΔT**) em relação a componentes semelhantes em carga comparável; referências típicas (NETA): **1 a 3 °C** possível defeito; **4 a 15 °C** provável defeito, programar reparação; **> 15 °C** defeito grave, ação imediata |
| **Ensaio dos relés de proteção** | verificar disparos e tempos | conforme as regulações aprovadas |
| **Ensaio de tensão aplicada / tangente de delta** (casos particulares) | isolamento de equipamento em fim de vida | por técnicos especializados |

## 6. Diagnóstico de avarias (sintomas e causas prováveis)
| Sintoma | Causas prováveis |
|---|---|
| **Disparo da proteção MT (fusível ou relé)** | curto-circuito, defeito no transformador, sobrecarga prolongada, inrush na energização, falha de cabo |
| **Alarme de temperatura do transformador** | sobrecarga, ventilação inadequada, ambiente quente, harmónicos, falha de ventilação forçada |
| **Relé Buchholz: alarme (gás)** | sobreaquecimento localizado, descargas parciais, ar no sistema |
| **Relé Buchholz: disparo (fluxo de óleo)** | defeito interno grave, curto-circuito entre espiras |
| **Ruído anómalo, vibração** | aperto do núcleo, sobretensão, harmónicos, sobrecarga, ligações soltas |
| **Cheiro a queimado, fumo** | ligação com aquecimento, isolamento em avaria, **retirar de serviço e investigar** |
| **Queda de tensão no QGBT** | transformador sobrecarregado, taps mal escolhidos, rede MT fraca |
| **Disparos do disjuntor geral BT** | sobrecarga da instalação, defeito na instalação, falta de seletividade |
| **Fugas de óleo** | juntas, válvulas, buchas; verificar nível e programar reparação |
| **Falha de comunicação ou de telecomando** | alimentação auxiliar, ligações, módulos |
- **Procedimento sugerido:** recolher **histórico e alarmes**, fazer **inspeção visual e medição de carga**, comparar com **ensaios anteriores**, **isolar e colocar em segurança** antes de ensaios com contacto, **identificar a causa** e documentar.
- **Nunca reenergizar** após disparo de proteção interna do transformador (Buchholz, sobrepressão) **sem investigação e autorização**.

## 7. Documentação e registo
- **Livro/registo de manutenção:** data, trabalhos, medições, resultados, equipamentos usados, quem executou e quem autorizou.
- **Esquemas unifilares atualizados e afixados.**
- **Relatórios de ensaios** com valores, **condições** (temperatura, humidade), **instrumentos e calibrações**.
- **Plano de ações corretivas** com prioridades e prazos; **peças de reserva críticas** (fusíveis MT, indicadores, buchas).
- **Gestão da manutenção:** software de gestão de manutenção (GMAO/CMMS) para planear e registar.

## 8. Impacto ambiental
- **Óleo mineral e de substituição:** recolha, armazenamento e **eliminação** por entidades licenciadas; **sem despejos**; **bacia de retenção** em bom estado.
- **SF6:** gás de efeito de estufa muito potente; **manuseio, recuperação e reporte de fugas** por pessoal certificado, conforme a legislação sobre gases fluorados.
- **PCB em transformadores antigos:** verificar a presença (regulamentação específica).

## 9. Erros comuns
- **Trabalhar em MT sem qualificação, autorização e procedimento.**
- **Anular intertravamentos** ou "rebater" a chave por pressa.
- **Reenergizar sem investigar** o disparo.
- **Substituir um só fusível MT** em vez dos três.
- **Esquecer a verificação do estado e da validade do EPI e dos equipamentos de manobra.**
- **Medir resistência de isolamento sem descarregar** e sem registar a temperatura.
- **Termografia sem carga** (não mostra o defeito).
- **Sem registo** nem comparação com ensaios anteriores.
- **Ignorar a ventilação** do compartimento.

## 10. Perguntas de estudo (com resultados)
1. Para que serve o relé Buchholz? **R: deteta gases e fluxo de óleo (alarme e disparo) por defeitos internos em transformadores com depósito de expansão.**
2. Porque se faz termografia com o PT em carga? **R: porque os pontos quentes só aparecem quando circula corrente.**
3. Quantos fusíveis MT se substituem quando um funde? **R: os três.**
4. O que é um intertravamento por chave e porquê usar? **R: impede manobras fora de sequência (ex.: aceder ao transformador sem pôr à terra e isolar a cela), eliminando erro humano.**
5. Diferença entre terra de proteção e terra de serviço num PT? **R: de proteção liga massas metálicas; de serviço liga o neutro do secundário BT; regras de separação e valores definidos na regulamentação.**
6. Qual é o princípio do índice de polarização? **R: razão entre a resistência de isolamento aos 10 min e aos 1 min; PI alto indica isolamento seco e saudável.**

## 11. Fontes externas sugeridas
- **DGEG:** regulamentação de segurança de postos de transformação, regimes de exploração e inspeção.
- **e-Redes (operador da rede):** normas técnicas de postos de transformação, procedimentos de segurança.
- Manuais de fabricantes (Efacec, Schneider RM6/SM6, ABB UniGear/SafeRing, Siemens 8DJH): manutenção, ensaios, intertravamentos.
- Guias de termografia e de testes de transformadores (Fluke, Megger, Omicron) e **normas IEC 60076, 60422, 60599** (pagas: usar documentação de fabricantes e guias como material público).
- Cursos de formação certificada em **trabalhos em instalações de MT** (entidades reconhecidas).
- PDF do referencial da UC (ANQEP).
