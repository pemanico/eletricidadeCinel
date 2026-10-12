# UC03099 - Instalar sistemas de domótica

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Parâmetros de protocolos (limites de comprimento, nº de dispositivos, correntes) vêm das especificações KNX/DALI e dos datasheets dos fabricantes: confirmar. Preços, licenças de software e requisitos de certificação KNX mudam: consultar a KNX Association e os fabricantes.

## 1. O que é domótica
Sistema que **automatiza e integra** funções de uma habitação ou edifício: iluminação, estores, climatização, segurança, energia, multimédia, controlo remoto e cenários. Os elementos são **sensores** (entradas), **atuadores** (saídas), **controladores/lógica** e **interfaces** (botões, painéis, apps, voz).

## 2. Arquiteturas e meios de comunicação
- **Centralizada:** um controlador central (PLC/gateway) liga a todos os dispositivos; simples, mas o controlador é ponto único de falha.
- **Distribuída (descentralizada):** cada dispositivo tem inteligência e comunica por um bus; o sistema continua a funcionar parcialmente se um dispositivo falhar (**KNX** é o exemplo mais conhecido).
- **Meios:** par entrançado (bus), **rádio** (Zigbee, Z-Wave, Bluetooth Mesh, Wi-Fi, Thread, KNX RF), **power line** (PLC doméstico), Ethernet/IP.

## 3. Principais protocolos e normas
| Sistema | Meio | Características |
|---|---|---|
| **KNX (EN 50090 / ISO/IEC 14543-3)** | par entrançado (TP), rádio, IP | norma aberta, interoperabilidade entre fabricantes, programação com ETS |
| **DALI (IEC 62386)** | 2 fios | iluminação digital (regulação, endereçamento individual) |
| **Zigbee** | rádio 2,4 GHz (malha) | baixo consumo; muito usado em sensores e lâmpadas |
| **Z-Wave** | rádio sub-GHz (868 MHz na UE) | malha; interoperabilidade entre produtos certificados |
| **Matter / Thread** | IP (Wi-Fi, Thread, Ethernet) | padrão recente de interoperabilidade entre ecossistemas |
| **Modbus / BACnet** | RS-485 / IP | edifícios, climatização, energia (ver UC01784) |
| **Wi-Fi/proprietário** | rádio | soluções de consumo; dependência de nuvem e do fabricante |
- **Sistema aberto vs fechado:** KNX é aberto e independente do fabricante; soluções proprietárias podem prender o cliente a um ecossistema. **Explica ao cliente a diferença antes de escolher**.

## 4. KNX em detalhe (par entrançado, TP)
### Topologia
- **Linha:** até **64 dispositivos** com 1 fonte de alimentação; extensível a **256** com repetidores de linha (4 segmentos).
- **Área:** até **15 linhas**, ligadas por acopladores de linha a uma linha principal.
- **Sistema:** até **15 áreas**, ligadas por acopladores de área.
- Capacidade total teórica: 15 x 15 x 256 = **57 600 dispositivos** (muito acima de qualquer habitação).
### Endereços
- **Endereço físico (A.L.D):** **Área.Linha.Dispositivo**, p. ex. **1.1.5**. Identifica o dispositivo na topologia.
- **Endereço de grupo:** comunica funções, p. ex. **1/0/3** (grupo principal/intermédio/subgrupo = "Luzes / Sala / Candeeiro"). Um **sensor** envia para um endereço de grupo; **os atuadores** associados a esse grupo reagem.
### Alimentação e cabo
- **Tensão do bus:** 21 a 30 V DC (nominal ≈ 29 V), fornecida por **fonte de alimentação KNX** (160 mA, 320 mA, 640 mA...) com choke integrado.
- **Cabo KNX** (p. ex. YCYM 2x2x0,8 mm ou equivalente certificado): par vermelho/preto = bus; par amarelo/branco = reserva.
- **Limites por linha:** comprimento total do cabo ≤ **1 000 m**; fonte → dispositivo mais afastado ≤ **350 m**; entre dois dispositivos ≤ **700 m**; entre duas fontes ≥ **10 m**.
- **Separação do cabo de bus e dos cabos de 230 V:** **≥ 4 mm** (isolamento) na mesma caixa ou caminho, ou usar cabo com isolamento reforçado, conforme as instruções do fabricante.
- **Consumo:** cada dispositivo consome tipicamente ~10 mA (ler datasheet).
- **Dimensionar a fonte:** **Σ correntes ≤ corrente da fonte** com margem (por exemplo, 20%).

**Exemplo:** moradia T3 com 40 dispositivos KNX (média 10 mA) → 400 mA; com 20% de margem 480 mA → **fonte de 640 mA** ✓ (320 mA não chegaria).

### Programação e ferramentas
- **ETS (Engineering Tool Software):** software oficial de projeto e programação KNX (versões Lite e Professional, licenças pagas): importa os produtos dos fabricantes (ficheiros de catálogo), atribui endereços físicos e de grupo, parametriza e descarrega.
- **Interface de programação:** USB ou IP (router/interface IP).
- **Boas práticas:** documentar a atribuição de endereços de grupo (tabela), nomear dispositivos por local/função, guardar o projeto ETS e **entregar uma cópia ao cliente**.
- **KNX Secure (Data Secure e IP Secure):** comunicação cifrada, recomendada em redes IP e edifícios sensíveis.

## 5. Dispositivos típicos
- **Atuadores de comutação** (4/8/12 canais, 16 A) para iluminação e tomadas; **atuadores de regulação (dimmers)**; **atuadores de estores/persianas**; **atuadores de climatização** (válvulas de colector, fancoils).
- **Sensores/botões:** botões de pressão (1 a 8 teclas), painéis tácteis, **sensores de presença e de luminosidade**, sensores de janela/porta, sonda de temperatura, **termóstatos** de sala.
- **Estação meteorológica** (vento, chuva, luminosidade): para proteção de estores e toldos.
- **Gateways/interfaces IP**, **servidores de visualização** (apps), **integrações** com som, sistemas de alarme e climatização.
- **Medição de energia:** contadores KNX e integração com fotovoltaico/VE (UC01799, UC04676).

## 6. Iluminação com DALI (resumo)
- **DALI:** 2 fios de bus (polaridade livre), **até 64 endereços** por linha, **16 grupos**, **16 cenas**; tensão do bus ≈ 9,5 a 22,5 V, corrente máx ≈ 250 mA; comprimento máx ≈ 300 m (confirmar secção do cabo e queda).
- **Vantagens:** regulação e endereçamento individual de cada luminária, feedback de estado e falhas, controlo por cenários e sensores, ideal para escritórios e edifícios.
- **DALI-2:** versão atual com certificação de interoperabilidade; **verificar compatibilidade dos drivers e controladores**.

## 7. Projeto de uma instalação domótica (passos)
1. **Levantamento de necessidades:** o que o cliente quer automatizar (e o que **não** quer), orçamento, prioridades, futuro.
2. **Lista de funções por divisão** (luz, estores, clima, segurança, cenas).
3. **Escolha do sistema** (aberto/fechado, cabo/rádio, nova construção vs reabilitação).
4. **Arquitetura e topologia** (linhas, quadro técnico, caminhos de cabos).
5. **Lista de dispositivos e dimensionamento** (fontes, atuadores, canais, correntes).
6. **Esquemas** e **plantas** (UC03077); tabela de endereços de grupo.
7. **Instalação, programação (ETS/ferramenta do fabricante) e comissionamento.**
8. **Formação do cliente e documentação.**
- **Reabilitação:** sem possibilidade de passar cabo → soluções por **rádio** (KNX RF, Zigbee, Z-Wave) e atuadores atrás de interruptores existentes; limites de fiabilidade e bateria.
- **Quadro elétrico:** prever **espaço** para atuadores (módulos DIN), fontes e ventilação; manter circuitos de potência e bus separados.

## 8. Segurança, privacidade e ciber-risco
- **Dispositivos IoT são computadores:** alterar passwords por defeito, atualizar firmware, **separar a rede** (VLAN/rede de convidados), **não expor** o sistema diretamente à Internet; acesso remoto por **VPN** ou serviço seguro do fabricante.
- **Câmaras IP e fechaduras inteligentes** merecem cuidado extra (cifra, autenticação forte).
- **RGPD:** câmaras que captam espaços públicos ou pessoas de fora do agregado exigem cuidado legal.
- **Segurança elétrica:** atuadores de 230 V dentro de quadros ou caixas com proteção; **seccionamento** claro; **segurança de equipamentos de segurança** (alarmes e deteção de incêndio têm regras próprias, não devem depender só da domótica).
- **Falha segura:** definir o estado dos atuadores em falha de bus (p. ex. estores sobem, luzes acendem em emergência, fechaduras por defeito conforme o risco).

## 9. Comissionamento e testes
- Verificar **tensão do bus** (≥ 21 V), **corrente** e **polaridade**.
- **Teste de cada dispositivo** (programação do endereço físico, função, parâmetros).
- **Teste de cenas e lógicas** (casa vazia, noite, ausência, alarme).
- **Teste de falha** (desligar a fonte, cortar o bus, perda de rede IP) e **recuperação**.
- **Backup do projeto** e **documentação** (esquemas, tabela de endereços, passwords, contactos).

## 10. Erros comuns
- Vender "domótica" sem definir funções e orçamento (expectativas erradas).
- **Fonte KNX subdimensionada** ou cabo de bus junto de cabos de 230 V sem separação.
- Misturar fabricantes sem confirmar compatibilidade ou certificação.
- Sem **documentação nem backup do projeto ETS** (o cliente fica refém do instalador).
- Soluções rádio em locais com muitas paredes de betão sem teste de cobertura.
- Ignorar ciber-segurança e deixar passwords por defeito.
- Sem prever **atualizações e manutenção** (quem responde por avarias depois da entrega).

## 11. Exercícios (com resultados)
1. 52 dispositivos KNX de 12 mA numa linha: corrente total e fonte adequada? **R: 624 mA → fonte de 640 mA no limite; melhor dividir em duas linhas ou escolher margem (2 fontes/linhas).**
2. Quantos dispositivos suporta uma linha KNX TP sem repetidores? **R: 64.**
3. Interpreta: endereço físico 2.3.14 e endereço de grupo 1/2/5. **R: dispositivo nº 14 da linha 3 da área 2; grupo "principal 1, intermédio 2, subgrupo 5" (função definida no projeto).**
4. Cabo de bus com 400 m entre fonte e dispositivo: cumpre? **R: não, o limite é 350 m entre fonte e dispositivo (reposicionar a fonte).**
5. Qual a vantagem do DALI sobre a regulação 1-10 V? **R: endereçamento individual, feedback e controlo digital por cenas e grupos com 2 fios.**

## 12. Fontes externas sugeridas
- **KNX Association** (knx.org): documentação, cursos e lista de produtos certificados; cursos de certificação KNX Partner.
- Catálogos e guias de projeto gratuitos de fabricantes KNX (Schneider, ABB, Siemens, Gira, Jung, Hager, Legrand).
- **DALI Alliance** (dali-alliance.org): especificações e produtos certificados DALI-2.
- Guias de segurança de IoT e redes domésticas (entidades de cibersegurança nacionais e europeias).
- PDF do referencial da UC (ANQEP).
