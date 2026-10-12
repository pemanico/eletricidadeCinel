# UC01788 - Instalar equipamentos de contagem inteligente e interligar redes de energia

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Quem instala, mantém e substitui aparelhos de contagem de uma instalação ligada à rede pública é, em regra, o **operador da rede de distribuição**; a intervenção de um instalador está limitada ao que a regulamentação e o operador permitem (ex.: quadros de contagem, caixas, cablagem a jusante). **Confirmar com a e-Redes e na regulamentação em vigor** o que o instalador pode e não pode fazer (selagens, ligação de contadores, TC).

## 1. Contadores inteligentes (smart meters)
- **Medem** energia ativa (kWh) e reativa (kvarh), potência, tensão e corrente; registam **curva de carga** (tipicamente em períodos de **15 minutos**) e eventos.
- **Telecomunicação:** enviam dados ao operador por **PLC (power line communication)** ou GPRS/4G e permitem **telegestão** (leituras e comandos à distância, alteração de potência contratada, corte/religação).
- **Protocolos:** DLMS/COSEM (norma de comunicação com contadores).
- **Porta do cliente (HAN/P1):** muitas implementações disponibilizam uma interface local (por exemplo, porta P1/HAN) para o cliente ligar um dispositivo de monitorização e obter dados em tempo quase real: confirmar disponibilidade e ativação com o comercializador/operador.
- **Tarifas:** simples, bi-horária, tri-horária, conforme ciclo diário/semanal (ciclo definido pela regulação).
- **Inteligência na rede:** deteção de falhas, balanços de rede, leitura de qualidade de energia.

## 2. Contagem direta e indireta
- **Direta:** o contador é percorrido pela corrente total (até corrente máxima, p. ex. 60 A a 100 A, ver contador). Para potências baixas e médias.
- **Indireta (transformadores de corrente, TC):** para correntes elevadas, a corrente é reduzida por **TC** (p. ex. 400/5 A) e lida pelo contador; a energia real = leitura x **constante de contagem K**.
  - **Exemplo:** TC 400/5 A → K = 400/5 = **80**. Leitura do contador 1 234,5 kWh → energia = 1 234,5 · 80 = **98 760 kWh**.
  - **Classes de precisão:** TC de classe 0,5 ou 0,5S (S = precisão em toda a gama de 1% a 120%).
  - **Regra de segurança:** **nunca abrir o secundário de um TC em carga** (tensão perigosamente elevada). Se for preciso trabalhar, curto-circuitar primeiro o secundário.
  - Dimensionamento do TC: corrente primária ≥ corrente máxima prevista; carga (VA) ≥ consumo do contador + cabos.
- **Contagem em MT** (média tensão): TC e TT (transformadores de tensão) e contador com compensação de perdas, em regra instalada e selada pelo operador.

## 3. Quadros e caixas de contagem
- **Localização:** acessível ao operador sem passar por locais privados (limite da propriedade ou local comum), com **grau de proteção IP** adequado e aberturas de leitura.
- **Constituição:** caixa/armário (com selos), aparelho de corte geral, aparelho de proteção (disjuntor de entrada da potência contratada), espaço para o contador e para o equipamento de telecomunicação.
- **Cablagem:** secção conforme a corrente (UC01781); ligações apertadas ao binário especificado (maus contactos aquecem); identificação das fases.
- **Selagem:** os selos de serviço da distribuidora **não podem ser violados**; qualquer intervenção que exija abrir selos requer o operador.

## 4. Interligação de redes e de produção local (autoconsumo)
- **Ligação à rede de instalações de produção (UPAC):** o operador pode exigir **contagem bidirecional** ou medição separada de produção, proteção de interligação e comunicações (UC01799).
- **Proteção de interligação:** deteção de falta de rede (anti-ilhamento), limites de tensão e frequência, religação automática temporizada. Inversores certificados incluem estas proteções; potências maiores podem exigir relé externo.
- **Ponto de ligação:** definido pelo operador (potência de ligação, nível de tensão); a **potência de injeção** é limitada pela capacidade da rede e pela regulamentação.
- **Documentação de ligação:** projeto/esquema unifilar, certificados do inversor, declaração de conformidade da instalação, termo de responsabilidade do instalador (UC01793).
- **Redes inteligentes (smart grids), comunidades de energia, autoconsumo coletivo:** partilha de produção entre vários consumidores por contagem individual e regras de repartição: consultar a regulamentação.

## 5. Medição de qualidade de energia (ligação à UC01795)
- Contadores e analisadores medem THD, desequilíbrios, cavas e sobretensões. A norma de referência é a EN 50160 (características da tensão em redes públicas): confirmar valores e intervalos.

## 6. Ensaios e verificações do instalador
- Verificar **seguimento de fases** e ordem correta, polaridade, apertos e seccionamento seguro.
- Em contagem indireta: relação do TC, sentido (P1 → P2), ligação do secundário e curto-circuito de segurança, cablagem de tensão.
- Medição de resistência de terra e de isolamento do quadro (UC01782).
- Registo fotográfico e documental da instalação antes de pedir a ligação.

## 7. Erros comuns
- TC com sentido de ligação invertido (energia lida com sinal trocado/zero).
- Secundário do TC aberto em carga.
- Apertos insuficientes nos bornes do contador (aquecimento, avaria).
- Violar ou remover selos do operador.
- Aparelho de corte geral/proteção sem o poder de corte necessário ou com calibre incoerente com a potência contratada.
- Esquecer que a injeção do excedente tem regras próprias (potência de ligação, regime e contagem).

## 8. Exercícios (com resultados)
1. TC 200/5 A e leitura de 345,6 kWh: energia real? **R: K = 40 → 13 824 kWh.**
2. Instalação com corrente máxima de 180 A: TC adequado? **R: 200/5 A (classe 0,5S), verificando carga em VA e cabos.**
3. Potência contratada de 13,8 kVA em monofásico: calibre da proteção de entrada? **R: 60 A.**
4. Contador com leitura a cada 15 min: quantas leituras por dia? **R: 96.**

## 9. Fontes externas sugeridas
- e-Redes: regras de ligação à rede, requisitos de contagem, quadros de contagem e processos de pedido.
- ERSE: regulamentação de tarifas, ciclos e comunidades de energia.
- DGEG: regime de autoconsumo e ligação de produção local.
- EN 50160 (paga): usar documentos técnicos do operador como material público.
- PDF do referencial da UC (ANQEP).
