# UC04681 - Efetuar uma instalação em fibra ótica em ITED

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Limites de atenuação por componente, tipos de fibra e conectores exigidos em ITED vêm do **Manual ITED** (ANACOM): confirmar na edição em vigor. Valores típicos abaixo são de referência e dependem do fabricante.

## 1. Princípios da fibra ótica
- A luz propaga-se no **núcleo** por reflexão total interna. Estrutura: núcleo, bainha (cladding), revestimento primário (coating) de 250 µm, buffer/tubo e capa do cabo.
- **Monomodo (OS2, G.652/G.657):** núcleo ≈ 9 µm; longas distâncias; é a que se usa em FTTH e na maioria das ITED atuais. **Multimodo (OM1 a OM5):** núcleo 50 ou 62,5 µm; curtas distâncias e redes locais.
- **Janelas de comprimento de onda (monomodo):** 1310 nm e 1550 nm (FTTH/GPON usa 1310 nm para subida e 1490 nm para descida, mais 1550 nm para vídeo em alguns casos).
- **Atenuação típica OS2:** ≈ 0,35 dB/km a 1310 nm e ≈ 0,21 dB/km a 1550 nm (ver datasheet).
- **G.657A:** fibra insensível a curvaturas, adequada para instalação em edifícios (raios de curvatura reduzidos).

## 2. Cabos e código de cores
- **Cabos para interior/exterior, para tubagem, "drop" para fração, e cabos aéreos**: escolher por ambiente (retardantes de chama, LSZH em interior, proteção contra roedores/humidade no exterior).
- **Código de cores das fibras (12 cores, em ordem):** azul, laranja, verde, castanho, cinzento, branco, vermelho, preto, amarelo, violeta, rosa, turquesa (aqua). Em cabos com mais de 12 fibras, os tubos usam o mesmo código.
- **Raio de curvatura:** respeitar o datasheet; valores típicos para cabos: ≥ 10 x diâmetro do cabo sem tensão, ≥ 20 x durante o puxamento.
- **Tensão de puxamento máxima:** nunca ultrapassar o valor do datasheet (por exemplo, algumas centenas de N para cabos de interior); usar guias e lubrificantes apropriados.

## 3. Conectores e componentes passivos
- **SC/APC (verde):** polimento angulado (8°) para minimizar reflexões; **norma em FTTH/GPON**.
- **SC/UPC (azul):** polimento reto; usado em alguns equipamentos e redes de dados (**nunca ligar APC com UPC**: danifica os conectores e causa perdas elevadas).
- **LC e outros:** em equipamentos de dados e multimodo.
- **Caixas de emenda e de distribuição, organizadores, bandejas de fusão**, pigtails (cordão com um conector e fibra solta para fundir), patch cords.
- **Acopladores (adaptadores) e divisores (splitters):** 1:2, 1:4, 1:8, 1:16, 1:32 em redes PON; **perda do splitter ≈ 3,5 dB (1:2), 7 dB (1:4), 10,5 dB (1:8), 14 dB (1:16), 17,5 dB (1:32)** (valores típicos, confirmar).
- **ONT/ONU:** terminal ótico do cliente (ligado ao ATI).

## 4. Emendas e conectorização
- **Emenda por fusão:** alinhamento e fusão por arco elétrico, **atenuação típica ≤ 0,05 a 0,1 dB**; proteção da emenda com manga termorretrátil e arrumação na bandeja.
- **Emenda mecânica:** mais rápida e menos fiável a longo prazo (atenuação ≈ 0,2 a 0,5 dB); usada em reparações e instalações rápidas.
- **Conectorização de campo:** conectores de montagem rápida (fast connectors) em fibras de acesso; resultados dependem do operador e da qualidade do corte.
- **Pigtail com fusão:** solução mais fiável para terminar fibras em ATI/ATE.

**Passos de uma emenda por fusão:**
1. Retirar a capa e o revestimento (strip) com ferramenta de precisão (sem arranhar a fibra).
2. **Limpar** com álcool isopropílico e panos sem fiapos.
3. **Cortar (cleave)** com a cliver, com ângulo < 1°.
4. **Posicionar** na fusionadora e fundir; ler a atenuação estimada.
5. **Proteger** a emenda (manga termorretrátil) e colocar na bandeja.
6. Registar e etiquetar.

## 5. Atenuação e balanço ótico (power budget)
**Atenuação total do canal = α·L + N_conectores·a_c + N_emendas·a_e + perdas dos splitters.**
- Referência de valores máximos por elemento (confirmar valores do Manual ITED): conector ≈ 0,5 dB; emenda ≈ 0,1 dB.

### Exemplo 1: cabo de 100 m para uma fração (sem splitter)
- Fibra: 0,1 km x 0,35 dB/km = **0,035 dB**.
- 2 conectores (um em cada ponta): 2 x 0,5 = **1,0 dB**.
- 1 emenda: **0,1 dB**.
- **Total ≈ 1,14 dB.** Qualquer valor medido muito acima (ex.: 3 dB) aponta para conector sujo, curva apertada ou emenda má.

### Exemplo 2: ligação GPON do OLT ao cliente (referência)
- 5 km de fibra: 5 x 0,35 = **1,75 dB**.
- Splitter 1:32: **17,7 dB** (típico).
- 4 conectores: **2,0 dB**; 6 emendas: **0,6 dB**.
- **Total ≈ 22,1 dB.** Com orçamento de potência de **28 dB** (classe B+, referência), a **margem é ≈ 5,9 dB** ✓ (margem para envelhecimento, reparações e curvas).

## 6. Ensaios
- **Medidor de potência e fonte (OLTS):** mede a atenuação **total** do canal (inclui conectores e emendas) a 1310/1550 nm; é o ensaio de aceitação principal. Procedimento: referenciar o medidor com a fonte (cordões de referência), medir o canal e comparar com o valor máximo calculado.
- **OTDR (reflectómetro):** mostra o trajeto da luz, a posição e a perda de eventos (emendas, conectores, curvas) e permite **localizar avarias**. Usa-se **cabo de lançamento (launch cable)** e de receção para ver o primeiro e o último conector; tem **zonas mortas** (dead zones) perto de eventos.
- **Microscópio de inspeção** (ou videoscópio): inspecionar as ferrules **antes de ligar**. Limpar com cassete/caneta de limpeza ou álcool isopropílico.
- **Registo:** guardar curvas/relatórios por fibra (ficheiros .sor, relatórios PDF) para a ficha de ensaios.

## 7. Segurança
- **Laser invisível (infravermelho):** nunca olhar diretamente para uma fibra ou conector ligado, nem para instrumentos com fonte ativa.
- **Fragmentos de fibra:** são vidro muito fino e perfurante; usar óculos, recolher em recipiente próprio e **nunca** deixar no chão ou na roupa.
- **Produtos químicos** (álcool isopropílico): ventilação, longe de fontes de ignição.
- **Trabalhos em altura e em caixas de visita:** segurança nos acessos, gases e canalizações (UC00676).

## 8. Erros comuns
- Conectores sujos (a causa nº 1 de perdas elevadas).
- Ligar APC com UPC.
- Curvas apertadas (microcurvaturas) em ATI/ATE e nas caixas.
- Cortes mal feitos (cleave com ângulo grande) e emendas com bolhas.
- Medir sem referenciar o instrumento ou com cordões gastos.
- Cabos puxados com tensão excessiva (danos invisíveis que aparecem depois).
- Não registar e etiquetar fibras e tomadas.

## 9. Exercícios (com resultados)
1. Cabo OS2 de 300 m a 1310 nm (0,35 dB/km), 2 conectores de 0,5 dB, 2 emendas de 0,1 dB: atenuação total? **R: 0,105 + 1,0 + 0,2 = 1,305 dB.**
2. Orçamento GPON de 28 dB, perdas totais de 25 dB: margem? **R: 3 dB (margem curta; rever a instalação).**
3. Splitter 1:8 e 1:32 em cascata: perda aproximada? **R: ≈ 10,5 + 17,5 = 28 dB (inviável sem outras condições, o que mostra porque as redes PON têm topologias definidas).**
4. Conector SC/APC verde ligado a um SC/UPC azul: o que acontece? **R: acoplamento defeituoso, perdas elevadas e risco de danificar as ferrules.**

## 10. Fontes externas sugeridas
- **ANACOM, Manual ITED:** requisitos de fibra, atenuações máximas, conectores e ensaios.
- Guias de instalação e de ensaio de fabricantes de instrumentos (EXFO, VIAVI, Fluke Networks, Sumitomo, Fujikura): procedimentos de OLTS, OTDR e fusão.
- Documentação de fabricantes de cabos e passivos (Corning, Prysmian, CommScope).
- Documentos técnicos gratuitos do **FOA (Fiber Optic Association)** sobre ensaios e instalação.
- PDF do referencial da UC (ANQEP).
