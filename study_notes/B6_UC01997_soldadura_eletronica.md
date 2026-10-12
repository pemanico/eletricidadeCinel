# UC01997 - Efetuar soldadura simples em eletrónica

> Material de estudo (explicação). **Não é fonte normativa.** Temperaturas e tempos são valores de referência de prática corrente; ler sempre o datasheet do componente (temperatura e tempo máximos de soldadura) e as instruções do fabricante da liga e do fluxo.

## 1. Princípio
A soldadura mole une componentes a pistas (PCB) ou condutores com uma **liga de estanho** com ponto de fusão baixo (≈ 180 a 220 °C). O **fluxo** (resina/flux) remove óxidos e permite que a liga molhe as superfícies. Uma boa junta é **eletricamente e mecanicamente fiável** e de aspeto brilhante e côncavo.

## 2. Ligas e fluxos
| Liga | Composição | Fusão aprox. | Notas |
|---|---|---|---|
| **Sn63/Pb37** | estanho/chumbo (eutética) | 183 °C | funde e solidifica sem fase pastosa; juntas brilhantes; **contém chumbo** |
| **Sn60/Pb40** | estanho/chumbo | 183-190 °C | muito usada em reparação e hobby |
| **SAC305 (sem chumbo)** | Sn 96,5 / Ag 3 / Cu 0,5 | ~217-220 °C | exigida pela RoHS na maioria dos produtos na UE; requer mais temperatura; juntas mais baças |
- **Chumbo:** é tóxico. **Lavar as mãos** depois de manusear, não comer nem beber junto da bancada, extrair fumos. A **diretiva RoHS** restringe o chumbo em muitos equipamentos eletrónicos novos na UE: **confirmar o que se aplica ao produto** em que trabalhas (reparação, equipamento novo, setor).
- **Fio de solda com núcleo de fluxo** (rosin core) de 0,5 a 1,0 mm para componentes normais; 0,3 a 0,5 mm para SMD.
- **Fluxo de resina (rosin) "no-clean"** ou **ativo** (exige limpeza posterior): usar o indicado para a aplicação. **Nunca usar fluxo de canalizador (ácido)** em eletrónica: corrói as pistas.

## 3. Ferramentas
- **Ferro de soldar com controlo de temperatura** (estação): 40 a 80 W, com **pontas** de diferentes formas (cónica, bisel, faca). Evitar ferros sem controlo.
- **Suporte com esponja húmida ou limpador de latão** (recomendado) para limpar a ponta.
- **Sugador de solda e mecha (desoldering braid)** para retirar estanho.
- **Pinças, alicates de corte e descarnar**, pinça de apoio, lupa ou microscópio, tapete resistente ao calor, **extrator de fumos**.
- **Ar quente (hot air)** para SMD e retrabalho; **pasta de solda** e **fluxo** para SMD.
- **Multímetro** (continuidade e curtos), **lupa/microscópio** para inspeção.

## 4. Temperatura e tempo
- **Referência:** **320 a 350 °C** para ligas com chumbo; **350 a 380 °C** para sem chumbo (a temperatura da ponta, não a da liga). Superfícies com grande massa térmica (planos de massa) pedem mais.
- **Tempo de contacto:** **2 a 4 segundos** por junta; acima disso risco de **levantar a pista** e **danificar o componente** (díodos, LEDs, CIs são sensíveis).
- **Ponta limpa e estanhada** (com uma película fina de liga) transmite melhor o calor. Uma ponta oxidada obriga a mais tempo e pior resultado.

## 5. Procedimento para uma junta em PCB (componente de furo)
1. **Preparar:** componente inserido e fixo (dobrar ligeiramente os terminais, ou apoiar a placa), superfícies limpas.
2. **Aquecer** simultaneamente **o terminal e a pista** com a ponta (1 a 2 s).
3. **Aplicar a solda** no encontro da ponta com o terminal/pista (**não na ponta do ferro**) até formar um cone.
4. **Retirar a solda** e depois o ferro (1 a 2 s depois).
5. **Deixar arrefecer sem mexer** (a junta mexida fica "fria").
6. **Cortar** o excesso do terminal rente à junta.
7. **Inspecionar** com lupa.

## 6. Qualidade da junta
**Junta boa:** brilhante (ligas com chumbo) ou ligeiramente baça (sem chumbo), **forma côncava** (cone com menisco), **molha** a pista e o terminal, sem excessos.
**Defeitos comuns:**
- **Junta fria:** aspeto baço, granulado ou esférico; liga não molhou bem; contacto intermitente. Corrigir com mais fluxo e reaquecer.
- **Ponte de solda (short):** liga une duas pistas/pinos; remover com mecha.
- **Pouca solda:** junta fina, terminal visível; reforçar.
- **Demasiada solda (bola):** esconde a forma; remover o excesso.
- **Pista levantada/queimada:** excesso de calor; pode exigir reparação com fio.
- **Terminal não molhado:** faltou aquecer o terminal.
- **Fluxo carbonizado:** ponta demasiado quente ou tempo excessivo.

## 7. Ordem de montagem na PCB
Do mais baixo para o mais alto, para que a placa assente bem ao soldar: **resistências e díodos → bases de circuitos integrados (sockets) → condensadores cerâmicos e de filme → transístores e reguladores → condensadores eletrolíticos → conectores e componentes volumosos**. Verificar **polaridade e orientação** (díodos, LEDs, eletrolíticos, CIs) **antes** de soldar.

## 8. SMD (superfície)
- **Componentes de passo largo** (resistências 0805/1206, SOIC): **pinça**, fluxo, solda fina; soldar primeiro **um terminal** para fixar e depois os restantes.
- **Passo fino (QFP, QFN, BGA):** normalmente com **ar quente e pasta de solda**, microscópio e prática; **BGA** exige estação de retrabalho.
- **Tombstoning** (componente levantado numa extremidade): aquecimento desigual, quantidade de solda desigual.
- **Remover um SMD:** ar quente (≈ 350 a 380 °C) ou ferro com **liga de baixo ponto de fusão**; manter a placa e os componentes vizinhos protegidos.

## 9. Dessoldar
- **Sugador:** aquecer a junta, aproximar o sugador e disparar.
- **Mecha:** colocar sobre a junta e aquecer por cima; a mecha absorve a liga por capilaridade.
- **Dessoldar CIs de furo:** remover cada pino individualmente ou usar base/estação de dessoldar; **não puxar** sem a liga fundida (arranca a metalização do furo).

## 10. ESD (descarga eletrostática)
Componentes **CMOS, MOSFET, memórias, CIs** podem ser destruídos por descargas que nem se sentem.
- **Pulseira antiestática** ligada à terra, **tapete ESD**, embalagens antiestáticas.
- **Humidade** do ambiente > 40% ajuda; **evitar vestuário sintético** junto da bancada.
- Tocar numa massa antes de pegar em componentes sensíveis; **não tocar nos pinos**.

## 11. Segurança na bancada
- **Queimaduras:** ponta a 350 °C; nunca pousar o ferro fora do suporte; cuidado com cabos.
- **Fumos de fluxo** (irritam vias respiratórias): extração local ou boa ventilação.
- **Chumbo:** lavar as mãos, não levar para a boca.
- **Projeções de solda e de terminais cortados:** **óculos de proteção**.
- **Eletricidade:** nunca soldar com a placa alimentada; descarregar condensadores.
- **Álcool isopropílico:** inflamável; longe do ferro quente.

## 12. Normas e qualidade (referência)
- **IPC-A-610** (aceitabilidade de montagens eletrónicas) e **IPC J-STD-001** (requisitos de soldadura) são as referências da indústria. As normas completas são pagas; fabricantes e escolas disponibilizam guias visuais gratuitos de defeitos de soldadura.

## 13. Exercícios práticos e perguntas
1. Qual a diferença de temperatura de trabalho entre ligas com e sem chumbo? **R: sem chumbo (SAC305) funde cerca de 30 a 35 °C acima (≈ 217 °C vs 183 °C), exigindo ferro mais quente.**
2. Porque se aquece o terminal e a pista ao mesmo tempo? **R: para que a liga molhe ambos e forme uma ligação metalúrgica.**
3. O que é uma junta fria e como se corrige? **R: junta mal molhada, baça e granulada; reaquecer com um pouco de fluxo/solda nova.**
4. Em que ordem se soldam os componentes de uma placa? **R: dos mais baixos para os mais altos (resistências, díodos, sockets, condensadores pequenos, ..., eletrolíticos e conectores).**
5. **Prática:** soldar um kit simples (pisca-LED com 555, ou uma fonte regulada) e fotografar as juntas (para o portefólio); trocar um componente com sugador e mecha.

## 14. Fontes externas sugeridas
- Tutoriais e vídeos gratuitos de soldadura de fabricantes de ferramentas e escolas técnicas (Hakko, Weller, Pace, Adafruit "Guide to Excellent Soldering", SparkFun).
- Guias visuais de defeitos de soldadura (IPC-A-610 em versões de apoio).
- Datasheets dos componentes: **temperatura e tempo máximos de soldadura**.
- PDF do referencial da UC (ANQEP).
