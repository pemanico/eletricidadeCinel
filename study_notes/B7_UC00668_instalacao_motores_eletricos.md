# UC00668 - Executar a instalação de motores elétricos

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Dados de motores (η, cos φ, corrente de arranque, classes) vêm da chapa de características e do catálogo do fabricante. Requisitos de eficiência (classes IE) e de ecoprojeto são regulamentados na UE e mudam: confirmar. Esta UC liga-se a UC04675 (instalações industriais: proteção e arranque), UC03918 (variadores), UC01994 (automatismos) e UC00676 (segurança).

## 1. Tipos de motores
- **Assíncrono trifásico de rotor em gaiola:** o mais usado na indústria; robusto, barato, sem manutenção de escovas.
- **Assíncrono monofásico (condensador):** habitação e pequenas cargas (bombas, portões, ventiladores); binário de arranque limitado.
- **Rotor bobinado:** arranque com resistências rotóricas (casos de arranque pesado).
- **Síncrono e síncrono de ímanes permanentes (PMSM) / BLDC:** velocidade síncrona; muito eficientes com variador.
- **Corrente contínua (DC):** controlo de velocidade simples; menos usados hoje; **servomotores** em posicionamento.

## 2. Chapa de características (leitura)
Elementos típicos: **tensão e ligação** (230/400 V Δ/Y ou 400/690 V Δ/Y), **corrente nominal**, **potência no veio (kW)**, **cos φ**, **rotações (rpm)**, **frequência (50 Hz)**, **classe de isolamento** (B, F, H), **grau de proteção IP** (IP55 comum), **serviço (S1 contínuo)**, **classe de eficiência (IE)**, **forma construtiva (B3, B5, B14)**.

### Ligações estrela/triângulo conforme a chapa
| Chapa | Rede 400 V trifásica | Observação |
|---|---|---|
| **230/400 V** | ligar em **estrela (Y)** | em triângulo a 400 V, queima (tensão por enrolamento 400 V em vez de 230 V) |
| **400/690 V** | ligar em **triângulo (Δ)** | permite arranque **estrela-triângulo** a 400 V |
- **Regra:** a **tensão menor** da chapa corresponde à ligação em **triângulo**; a **maior**, a **estrela**.
- **Caixa de bornes:** pontes ou barras entre U1-V1-W1 e U2-V2-W2 de acordo com o esquema da tampa.

## 3. Velocidade, escorregamento e binário
- **Velocidade síncrona:** **n_s = 120·f / p** (f em Hz; p = nº de polos). Em 50 Hz: **2 polos 3 000 rpm; 4 polos 1 500 rpm; 6 polos 1 000 rpm; 8 polos 750 rpm**.
- **Escorregamento:** **s = (n_s − n)/n_s**. Exemplo: motor de 4 polos a 1 450 rpm: s = (1 500 − 1 450)/1 500 = **3,33%**.
- **Binário nominal:** **T [N·m] = 9 550 · P [kW] / n [rpm]**. Exemplo: 15 kW a 1 470 rpm → T = 9 550·15/1 470 = **97,4 N·m**.
- **Curva binário-velocidade:** binário de arranque, mínimo, máximo (rutura) e nominal: o binário resistente da carga tem de ficar **abaixo** do binário do motor em toda a rampa.

## 4. Eficiência e classes IE (referência UE)
- **IE1 (standard), IE2 (alta), IE3 (premium), IE4 (super premium)**. A UE exige tipicamente **IE3** (ou IE2 com variador) para motores trifásicos na gama de 0,75 a 1 000 kW, e IE4 em algumas gamas a partir de datas definidas nos regulamentos de ecoprojeto. **Confirmar as datas e âmbitos em vigor.**
- **Poupança:** motores de maior eficiência custam mais, mas em serviço contínuo o custo de energia ao longo da vida **supera o preço do motor** (ordem de grandeza: a energia pode ser 90% ou mais do custo de ciclo de vida).

## 5. Dimensionamento do motor a partir da carga (exemplo de bomba)
**Potência hidráulica:** **P_hid [kW] = ρ·g·Q·H / 1 000** (ρ = 1 000 kg/m³; g = 9,81 m/s²; Q em m³/s; H em m).
- **Exemplo:** Q = 20 m³/h (0,00556 m³/s), H = 25 m, rendimento da bomba 0,65.
  - P_hid = 1 000·9,81·0,00556·25/1 000 = **1,36 kW**.
  - P_veio = 1,36/0,65 = **2,10 kW**.
  - Com margem de 15%: 2,41 kW → **motor normalizado de 3 kW** (valores comuns: 0,75; 1,1; 1,5; 2,2; 3; 4; 5,5; 7,5; 11; 15 kW).
- **Evitar sobredimensionar demais:** motores a baixa carga têm pior rendimento e cos φ.
- **Ventiladores:** potência varia com o **cubo da velocidade**: reduzir a velocidade 20% reduz a potência cerca de 49%, justificando **variadores** (UC03918).
- **Corrente nominal (exemplo):** motor de 15 kW, 400 V, η = 0,92, cos φ = 0,86 → **27,4 A** (ver UC04675).

## 6. Arranque e proteção (resumo; ver UC04675)
- **Direto (DOL):** I_arr ≈ 6 a 8 x In; binário elevado.
- **Estrela-triângulo:** reduz I_arr para ≈ 1/3; **motor com enrolamentos para Δ à tensão da rede**; comutação com tempo morto e intertravamento.
- **Soft starter:** rampa de tensão, menor stress mecânico.
- **Variador de frequência:** controlo de velocidade/binário, arranque suave, poupança; atenção a cabos blindados, harmónicos e isolamento do motor.
- **Proteção:** disjuntor-motor ou fusíveis aM + **relé térmico regulado à In da chapa**; **classe de disparo** ajustada ao arranque; sondas **PTC** em motores críticos.
- **Inversão do sentido de rotação:** **trocar duas fases quaisquer** (trifásico). Em monofásico com condensador, **inverter as ligações do enrolamento auxiliar** (conforme esquema do fabricante).

## 7. Instalação mecânica
- **Base e fixação:** superfície plana e rígida, parafusos adequados, calços para correção de altura; **evitar "pé coxo"** (soft foot).
- **Alinhamento do acoplamento** (laser ou relógio comparador): desalinhamento causa vibração, desgaste dos rolamentos e falhas prematuras.
- **Transmissão por correias:** tensão correta e alinhamento das polias; **cuidado com cargas radiais** nos rolamentos.
- **Ventilação:** não bloquear a entrada de ar; temperatura ambiente e altitude podem exigir **derating** (valores do fabricante).
- **Proteções mecânicas:** resguardos em partes móveis (veios, acoplamentos, correias).
- **Rolamentos:** lubrificação conforme o fabricante (tipo e intervalo); sobrelubrificar também danifica.

## 8. Instalação elétrica
- **Cabos:** secção por aquecimento, queda de tensão em regime e **no arranque** (UC01781, UC04675); **bucins** estanques (IP) adequados.
- **Caixa de bornes:** apertos ao binário especificado; **terminais bem crimpados**; verificar o **sentido de rotação** antes de acoplar à carga.
- **Terra:** **PE ligado ao terminal do motor** e equipotencialidade da carcaça e do equipamento acionado.
- **Cabo blindado com variador:** blindagem ligada à terra a 360° em ambos os lados (CEM); considerar **filtros dV/dt** em cabos longos.
- **Seccionador local** (de manutenção) junto ao motor, bloqueável (UC00676).
- **Proteção contra reinício** automático inesperado após falha de rede, quando perigoso.

## 9. Ensaios antes de colocar em serviço
- **Resistência de isolamento (megóhmetro 500 V DC, motores até 500 V):** referência **≥ 1 MΩ** como mínimo prático (IEEE 43 recomenda 1 MΩ + 1 MΩ por kV nominal); **valores bons ≥ 100 MΩ** em motores secos. Medir a **temperatura** (humidade e frio baixam a leitura).
- **Índice de polarização (PI):** razão entre a leitura aos 10 min e a de 1 min; **PI ≥ 2** em geral indica isolamento saudável.
- **Resistência dos enrolamentos** (equilíbrio entre fases, diferenças pequenas).
- **Continuidade do PE**, verificação de **ligações** (Y/Δ) e **apertos**.
- **Teste em vazio** (sem carga acoplada): **sentido de rotação**, **corrente em vazio** (valor típico 30 a 50% da nominal em motores pequenos, menos em grandes), **ruído e vibração**.
- **Teste com carga:** **corrente em cada fase** (**desequilíbrio** entre fases ≤ ~5%), **temperatura** da carcaça e dos rolamentos, **vibração** (ISO 20816).
- **Registo** dos valores como referência para manutenção futura.

## 10. Diagnóstico de avarias (rápido)
| Sintoma | Causas prováveis |
|---|---|
| Não arranca, zumbe | falta de uma fase, rotor bloqueado, tensão baixa, condensador avariado (monofásico) |
| Disparo do térmico | sobrecarga, falta de fase, tensão baixa, ventilação bloqueada, regulação do térmico errada |
| Aquecimento excessivo | sobrecarga, ventilação obstruída, tensões desequilibradas, harmónicos, partidas excessivas |
| Vibração e ruído | desalinhamento, rolamentos, desequilíbrio, base solta |
| Corrente desequilibrada | tensões desiguais, ligações com mau contacto, enrolamento avariado |
| Baixa resistência de isolamento | humidade, contaminação, envelhecimento, enrolamento danificado |

## 11. Segurança
- **Cortar, bloquear e verificar a ausência de tensão** antes de abrir a caixa de bornes (UC00676).
- **Condensadores de motores monofásicos:** podem reter carga: descarregar.
- **Partes rotativas:** resguardos instalados; nunca usar roupa solta; **não arrancar com o acoplamento sem proteção**.
- **Ruído e calor:** proteção auditiva em salas de máquinas; superfícies quentes sinalizadas.
- **Atmosferas explosivas (ATEX):** motores e instalação têm requisitos específicos (não improvisar).

## 12. Erros comuns
- Ligar um motor **230/400 V em triângulo a 400 V**.
- Térmico regulado ao **calibre do disjuntor** em vez da **corrente da chapa**.
- Sobredimensionar o motor e o cabo sem verificar queda de tensão no arranque.
- Não alinhar o acoplamento.
- Sem **teste de isolamento** antes de ligar, ou sem registo dos valores.
- Cabo de variador não blindado ou blindagem mal ligada.
- Esquecer o **seccionador de manutenção** à vista do motor.
- Arrancar sem verificar o sentido de rotação (danifica bombas e ventiladores).

## 13. Exercícios (com resultados)
1. Motor de 6 polos em 50 Hz: velocidade síncrona? **R: 1 000 rpm.**
2. Motor de 4 polos que gira a 1 440 rpm: escorregamento? **R: 4%.**
3. 7,5 kW a 1 450 rpm: binário? **R: 9 550·7,5/1 450 = 49,4 N·m.**
4. Rede 400 V e motor 400/690 V: ligação? **R: triângulo (Δ).**
5. Bomba: Q = 36 m³/h, H = 30 m, η_bomba = 0,7: potência de veio e motor? **R: P_hid = 9,81·1 000·0,01·30/1 000 = 2,94 kW; P_veio = 4,2 kW; motor de 5,5 kW (com margem).**
6. Ventilador a 80% da velocidade: potência relativa aproximada? **R: 0,8³ = 0,512 → ≈ 51%.**

## 14. Fontes externas sugeridas
- Catálogos e manuais de instalação de fabricantes de motores (WEG, ABB, Siemens, Leroy-Somer): chapas, ligações, dimensionamento, manutenção.
- Guias de eficiência energética em motores e regulamento de ecoprojeto da UE (documentos públicos da Comissão Europeia e da DGEG/ADENE).
- Guias de alinhamento e vibração (SKF, Schaeffler): material técnico gratuito.
- PDF do referencial da UC (ANQEP).
