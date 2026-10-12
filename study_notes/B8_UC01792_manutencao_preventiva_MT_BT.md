# UC01792 - Efetuar a manutenção preventiva de instalações de utilização MT e BT

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** As periodicidades obrigatórias, os critérios de inspeção e os requisitos de habilitação para trabalhos em MT e BT são definidos pela regulamentação portuguesa (regime das instalações elétricas de serviço particular, inspeções por entidades inspetoras, responsável técnico pela exploração, etc.): **confirmar na DGEG e nos documentos em vigor**. **Trabalhos em MT só por pessoal qualificado e autorizado** (ver UC00676 e UC04679).

## 1. Tipos de manutenção
- **Corretiva:** depois da avaria; mais cara e arriscada (paragens inesperadas).
- **Preventiva (sistemática, por calendário):** inspeções e intervenções periódicas independentemente do estado.
- **Condicionada/preditiva:** baseada em **medições de estado** (termografia, vibração, análise de óleo, qualidade de energia, tendências).
- **Melhorativa:** modifica o equipamento para reduzir falhas ou melhorar desempenho.
- **Objetivos:** **segurança**, **fiabilidade**, **disponibilidade**, **eficiência energética**, **conformidade legal** e redução do **custo total** ao longo da vida.

## 2. Planear a manutenção
1. **Inventariar os ativos** (quadros, aparelhagem, transformadores, motores, UPS, iluminação de emergência, baterias de condensadores, geradores, terras, SPD...) com **localização, características e esquemas**.
2. **Avaliar a criticidade** (impacto da falha na segurança, na produção e no custo): priorizar.
3. **Definir tarefas e periodicidades** (fabricante, regulamentação, experiência), **procedimentos** e **checklists**.
4. **Planear recursos:** pessoal qualificado, instrumentos calibrados, peças de reserva, **janelas de paragem** acordadas com o cliente.
5. **Executar e registar.**
6. **Analisar resultados**: avarias, tendências, indicadores (**MTBF**, disponibilidade, custo), e **ajustar o plano**.
- **GMAO/CMMS:** software de gestão de manutenção para planear, emitir ordens de trabalho e guardar histórico.

## 3. Segurança antes de tudo
- **Cortar, bloquear, verificar ausência de tensão** (5 regras de ouro; UC00676); em MT, **procedimentos formais**, intertravamentos e **autorização de trabalho**.
- **Instrumentos de medida com categoria (CAT) adequada** e em bom estado; **verificar o instrumento antes e depois**.
- **Condensadores e baterias:** descarregar e isolar; **UPS e baterias** têm tensão DC mesmo com a rede desligada.
- **Arco elétrico:** avaliar risco e usar EPI adequado quando é estritamente necessário trabalhar em quadros energizados (apenas se for impossível desenergizar e com qualificação).
- **Comunicação:** avisar os utilizadores de cortes, prever **alternativas de alimentação** para cargas críticas (gerador, UPS).

## 4. Manutenção preventiva em BT (por tipo de equipamento)
### Quadros elétricos e aparelhagem
- **Inspeção visual:** limpeza, humidade, sinais de aquecimento (descoloração, cheiro), identificações, esquemas, **reserva** de espaço, **tampas e IP** íntegros.
- **Termografia em carga** (com cuidado e EPI), **aperto de ligações** aos binários do fabricante (com quadro **desenergizado**), **substituição de componentes** envelhecidos.
- **Disjuntores:** ensaio de **disparo** (botão de teste, ou **injeção primária/secundária** nos eletrónicos), **limpeza**, **operação mecânica**, verificação de **regulações** (térmico/magnético, long-time/short-time/instantâneo), **resistência de contacto** em aparelhagem de potência.
- **Diferenciais:** **botão de teste** (mensal, pelo utilizador) e **ensaio com ensaiador de diferenciais** (corrente e tempo de disparo): tipo geral **≤ 300 ms** a IΔn e **≤ 40 ms** a 5·IΔn; registar valores.
- **Contactores e relés:** estado dos contactos (queimados, soldados), bobinas, **intertravamentos** e relés térmicos (regulação à corrente da chapa do motor).
- **Fusíveis:** verificação de **calibre e tipo** corretos; **não substituir por fio/calibre superior**.
- **SPD (limitadores de sobretensão):** **indicador de estado** (janela/contacto remoto); substituir cartuchos "gastos"; verificar fusível de proteção do SPD e comprimento de cabo de ligação.

### Condutores e ligações
- **Inspeção de cabos:** isolamentos, **sinais de aquecimento**, sobrecargas, **proteção mecânica**, estado dos terminais, apertos.
- **Resistência de isolamento (500 V DC, circuitos até 500 V):** referência **mínima 1 MΩ** (IEC 60364-6); valores **> 100 MΩ** indicam isolamento seco e saudável; **comparar com histórico** e corrigir pela temperatura; **desligar cargas eletrónicas** antes do teste.
- **Continuidade do PE** e **equipotencialidade**.

### Terra
- **Resistência de terra** (método de 3 pólos ou pinça): comparar com o **valor exigido** e histórico; verificar **ligações, barras de terra e eletrodos** (corrosão, ligações soltas).
- **Impedância do lacete de avaria (Zs)** em esquemas TN.

### Iluminação normal e de emergência
- **Luminárias, drivers, balastros**; **limpeza** (fator de manutenção Fm, UC04672).
- **Iluminação de emergência (UC04674):** **teste funcional** mensal, **teste de autonomia** anual, **registo**, **substituição de baterias** no fim de vida, **sinalização** íntegra.

### Motores e acionamentos (UC00668, UC03918)
- **Rolamentos, lubrificação, vibração, temperatura, corrente em cada fase, alinhamento, aperto de caixa de bornes, isolamento (megger)**, **filtros e ventiladores de variadores**, **condensadores eletrolíticos de variadores** (vida limitada, geralmente 5 a 10 anos).

### UPS e baterias (UC03088)
- **Ensaio de autonomia** (descarga controlada), **verificação de tensões das baterias**, **temperatura**, **ligações**, **ventilação**; **substituição preventiva** das baterias (valor típico 3 a 5 anos em chumbo-ácido, conforme fabricante).

### Baterias de condensadores e qualidade de energia (UC01795)
- **Corrente nos condensadores** (comparar com o nominal; aumento = capacidade perdida ou harmónicos), **temperatura**, **estado dos contactores**, **ventilação**, **reatâncias de dessintonia**; **medições de THD** periódicas.

### Fotovoltaico, VE e armazenamento (UC01799, UC04676, UC01801)
- **FV:** inspeção visual de módulos (sujidade, quebras, pontos quentes por termografia), **conectores**, **inversor**, **strings** (Voc/Isc), **resistência de isolamento DC**, **SPD**.
- **Postos VE:** teste do **diferencial e da deteção DC**, inspeção de **cabos e fichas**, **firmware** e comunicação.
- **Baterias de armazenamento:** inspeção do estado, **firmware**, ventilação e temperatura.

## 5. Manutenção preventiva em MT (visão geral; ver UC04679 para detalhe de PT)
- **Celas de MT, seccionadores, disjuntores e interruptores:** inspeção visual, **limpeza**, **verificação mecânica** (operação, lubrificação, intertravamentos), **resistência de contacto**, **ensaio de relés de proteção** (injeção), **verificação de SF6** (pressão/densidade) quando existe.
- **Transformadores (UC03895):** nível e estado do óleo, **DGA** e outros ensaios, buchas, ligações, relé Buchholz, proteções térmicas, ventilação.
- **Cabos MT:** inspeção de terminais e blindagens, **ensaios de isolamento** (por técnicos especializados, com tensão adequada).
- **Terras:** valores, ligações, tensões de passo e toque.
- **Equipamento de segurança e manobra:** **luvas, pértigas, detetores de tensão, tapetes** **verificados e dentro de validade**.
- **Documentação e esquemas** atualizados; **registo** de manobras e ensaios.
- **Inspeções legais:** nas instalações sujeitas, as **inspeções periódicas por entidades inspetoras reconhecidas** (confirmar periodicidade e âmbito), com **certificação** e correção de não conformidades.

## 6. Termografia: critérios (referência NETA)
Comparar o ponto suspeito com um **componente semelhante** em condições de carga semelhantes (ΔT):
- **1 a 3 °C:** possível defeito; **vigiar**.
- **4 a 15 °C:** provável defeito; **reparar** quando possível.
- **> 15 °C:** **defeito grave: ação imediata**.
- Medir **sempre em carga** (idealmente ≥ 40% da carga nominal), conhecer a **emissividade**, evitar reflexos, **registar a corrente** no momento da medição.
- **Exemplo:** terminal de um disjuntor a 78 °C, enquanto os outros dois de fase idêntica estão a 52 °C com a mesma corrente: ΔT = 26 °C → **defeito grave** (ligação solta, contacto deteriorado): reparar de imediato após isolar e apertar.

## 7. Indicadores simples de gestão
- **Disponibilidade (%)** = tempo em serviço / tempo total x 100.
- **MTBF** (tempo médio entre falhas) = tempo de funcionamento / nº de falhas.
- **MTTR** (tempo médio de reparação) = tempo total de reparação / nº de reparações.
- **Disponibilidade = MTBF/(MTBF + MTTR).**
- **Exemplo:** MTBF = 2 000 h e MTTR = 8 h → disponibilidade = 2 000/2 008 = **99,6%**.
- **Custo da manutenção/valor do ativo** e **% de manutenção preventiva vs corretiva** como indicadores de maturidade.

## 8. Exemplo de plano mensal/anual para um edifício de serviços (esquema)
- **Mensal:** teste funcional da iluminação de emergência; verificação de alarmes da GTC; inspeção visual do QGBT; leituras de consumo e corrente.
- **Trimestral/semestral:** inspeção de quadros secundários, termografia em carga, teste de diferenciais com ensaiador, verificação de SPD.
- **Anual:** autonomia de emergência, ensaio de isolamento, resistência de terra, aperto de ligações em quadros críticos, manutenção de UPS e baterias de condensadores, revisão de motores principais, inspeção da cobertura FV.
- **A cada poucos anos:** ensaios MT, óleo e DGA de transformadores, inspeção por entidade inspetora (conforme regulamentação), substituição de baterias.

## 9. Documentação e relatório
- **Ficha de manutenção** por equipamento (tarefas, resultados, medições, desvios, ações).
- **Relatório ao cliente:** estado geral, **não conformidades** (por gravidade), **recomendações**, **prazos** e **custos** das reparações.
- **Registo fotográfico** (termografia, estado de ligações, antes e depois).
- **Manter a rastreabilidade:** instrumentos usados e **calibração em dia**.

## 10. Erros comuns
- **Manutenção só quando avaria** (corretiva) em instalações críticas.
- **Apertar ligações com o quadro em tensão.**
- **Termografia sem carga** ou sem registo da corrente.
- **Medir isolamento com eletrónica ligada** (danifica) ou sem histórico para comparar.
- **Substituir fusíveis por calibre superior** para "deixar de disparar".
- **Sem registos** nem seguimento das recomendações.
- **Instrumentos sem calibração** ou com categoria inadequada.
- **Trabalhar em MT sem qualificação e procedimentos.**
- **Não avisar utilizadores e não prever alimentação alternativa.**

## 11. Exercícios (com resultados)
1. MTBF = 4 000 h e MTTR = 10 h: disponibilidade? **R: 4 000/4 010 = 99,75%.**
2. Terminal a 70 °C vs semelhante a 55 °C na mesma carga: classificação? **R: ΔT = 15 °C: limite entre provável defeito e defeito grave; tratar com urgência.**
3. Diferencial de 30 mA que dispara a 400 ms: conforme? **R: não (tipo geral ≤ 300 ms a IΔn); substituir.**
4. Resistência de isolamento de 0,4 MΩ a 500 V num circuito de tomadas: ação? **R: abaixo de 1 MΩ: não conforme; localizar a avaria (humidade, dano), reparar e ensaiar de novo.**
5. Como se planeia a manutenção de 120 equipamentos com orçamento limitado? **R: avaliar criticidade (segurança, produção, custo), priorizar os de maior risco, definir tarefas e periodicidades mínimas legais e ajustar com histórico.**

## 12. Fontes externas sugeridas
- **DGEG:** regime de inspeções, exploração e manutenção de instalações elétricas; lista de entidades inspetoras.
- Manuais de manutenção de fabricantes de aparelhagem, UPS, variadores e transformadores (Schneider, ABB, Siemens, Legrand, Efacec).
- Guias gratuitos de termografia e de ensaios elétricos (Fluke, FLIR, Megger, Chauvin Arnoux).
- Normas **IEC 60364-6** (verificação), **NETA MTS/ATS** (ensaios de manutenção e aceitação, pagas): usar guias de fabricantes e documentos públicos como apoio.
- Livros e cursos de gestão da manutenção (GMAO, MTBF, criticidade).
- PDF do referencial da UC (ANQEP).
