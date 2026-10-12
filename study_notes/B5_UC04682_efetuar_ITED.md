# UC04682 - Efetuar uma ITED

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** As quantidades mínimas (tomadas, tubos, fibras, dimensões de armários), ocupações máximas de tubagem e distâncias de separação vêm do **Manual ITED** (ANACOM): confirmar na edição em vigor. Os valores aqui são exemplos didáticos.

## 1. Sequência de execução de uma ITED (visão geral)
1. **Receber e ler o projeto ITED** (memória descritiva, plantas, esquemas, lista de materiais) e verificar a compatibilidade com a obra (RTIEBT, estrutura, prumadas).
2. **Tubagens e caixas** (durante a obra de construção, antes dos rebocos): caixas de entrada e de visita, tubos horizontais e verticais, caixas de aparelhagem e de passagem, armários (ATE e ATI).
3. **Cablagem**: puxamento de cabos de pares, coaxiais e fibra, seguindo percursos e separações do manual.
4. **Terminações**: conectorização nas tomadas, nos painéis de distribuição, ligação dos cabos coaxiais e emendas de fibra.
5. **Redes de terra e equipotencialidade**.
6. **Ensaios** e **registo** (ficha de ensaios por cabo e tomada).
7. **Documentação final**: plantas "como construído", etiquetagem, termo de responsabilidade, manual do utilizador, e interface com a entidade certificadora quando aplicável.

## 2. Tubagens
- **Tipos:** tubos PVC/PEAD flexíveis ou rígidos, corrugados para embeber; diâmetros normalizados (Ø20, Ø25, Ø32, Ø40, Ø50, Ø63 mm...).
- **Regras gerais:** tubagens **exclusivas de telecomunicações** (separadas das de energia), com **guias** (fio guia) de reserva; curvas amplas (raios de curvatura adequados, evitar mais de duas curvas de 90° entre caixas); caixas de passagem em trajetos longos.
- **Ocupação máxima:** o manual define a taxa de ocupação de cada tubo (ordem de grandeza: 40% a 50% da secção interior). Garante o puxamento e o crescimento futuro.

### Exemplo: quantos cabos Cat 6 cabem num tubo Ø25?
- Diâmetro interior aproximado: 20 mm → secção ≈ 314 mm².
- Cabo Cat 6 com Ø exterior 6,5 mm → secção ≈ 33,2 mm².
- Com ocupação de 40%: 0,4·314/33,2 = 3,8 → **3 cabos**; com 50%: 4,7 → **4 cabos** (confirmar a taxa do manual e o diâmetro real do tubo).

## 3. Armários (ATE e ATI)
- **ATI (individual):** armário na fração, em local acessível e arejado, com espaço para distribuidores, terminação de fibra (ONT), router/ switch, ligações coaxiais e alimentação (tomada de energia dedicada ao armário).
- **ATE (de edifício):** ponto de ligação das redes de operadores com as prumadas; maior, normalmente no piso de entrada, também com alimentação e terra.
- **Alimentação:** circuito de energia **exclusivo** e identificado para os armários (com proteção dedicada e, quando aplicável, SPD).
- **Organização:** separar potência de telecomunicações, identificar todos os cabos e tomadas.
- **Ventilação e dissipação:** evitar sobreaquecimento com muitos equipamentos ativos.

## 4. Cabos de pares (cobre)
- **Categoria:** Cat 6 (ou superior, conforme o manual); **blindados (FTP/S/FTP) ou não blindados (UTP)**, conforme a edição do manual e o ambiente.
- **Terminação:** tomadas RJ45 (keystone) e painéis de distribuição, esquema **T568A ou T568B** (um único esquema em toda a instalação; o mais comum em Portugal é T568B).
- **Boas práticas:**
  - Manter os pares torcidos o mais possível até ao ponto de terminação (destorcer < 13 mm em Cat 6).
  - Raio de curvatura ≥ 4 x diâmetro do cabo.
  - Não apertar abraçadeiras ao ponto de deformar o cabo.
  - Reservar folga (service loop) no ATI e na tomada.
- **Comprimento:** cabo horizontal ≤ **90 m** (ligação permanente) mais 10 m de cordões até aos 100 m do canal.

## 5. Cabo coaxial e distribuição de TV
- **Cabo coaxial 75 Ω** (classe adequada ao manual), terminado em **conectores F** com crimpagem correta (a blindagem não pode tocar o condutor central).
- **Componentes:** derivadores (taps), distribuidores (splitters), tomadas de TV, cargas de terminação de 75 Ω onde necessário.
- **Balanço de sinal** (método): Nível na tomada = nível à entrada − atenuação do cabo − perdas dos componentes.

### Exemplo (ilustrativo)
- Nível à entrada do ATI: 70 dBµV.
- Cabo coaxial de 30 m com atenuação de 20 dB/100 m (a 862 MHz, ver datasheet) → **6 dB**.
- Distribuidor 1:4 (≈ 7,5 dB) + tomada (≈ 1 dB) → **8,5 dB**.
- Nível na tomada ≈ 70 − 6 − 8,5 = **55,5 dBµV**, que se compara com a **gama de níveis exigida no manual** (e com a sensibilidade dos recetores).

## 6. Fibra ótica (resumo; ver UC04681)
- Cabos de fibra de acesso à fração, emendados com pigtails em caixas, e terminados em **SC/APC** (verde) no ATI.
- Limpar, inspecionar e ensaiar antes de fechar o armário.

## 7. Tomadas e posições
- **Quantidade e localização** (ex.: salas, quartos, cozinha) conforme o manual e o projeto; as tomadas combinam normalmente RJ45 e coaxial, com acesso a ambos nas divisões principais.
- **Alturas e afastamentos** em relação às tomadas de energia (confirmar no manual).
- **Identificação:** cada tomada com número e destino no ATI.

## 8. Terra e equipotencialidade
- **Armários (ATE/ATI)** e massas metálicas da infraestrutura ligados à **barra de terra**.
- Secções e percursos do condutor de ligação conforme o manual (confirmar; a regra de equipotencial do edifício aplica-se também: ver UC01782).
- **Proteção contra sobretensões** em cabos de entrada de operadores e em antenas: em coordenação com a instalação elétrica.

## 9. Ensaios de aceitação (ver UC04680)
- **Cobre:** certificador de cabos (wiremap, comprimento, atenuação, NEXT, return loss).
- **Coaxial:** continuidade, curto, medição de níveis nas tomadas.
- **Fibra:** OLTS e, se necessário, OTDR, com inspeção dos conectores.
- **Terra:** continuidade e resistência.
- **Entregar:** ficha de ensaios por tomada, plantas as-built, termo de responsabilidade, manual do utilizador.

## 10. Erros comuns
- Tubagem de telecomunicações partilhada com energia ou com ocupação acima do limite.
- Caixas inacessíveis depois dos rebocos (não se consegue puxar nem reparar).
- Cabos de cobre puxados com tensão excessiva (alteram o desempenho em Cat 6).
- Destorcer pares demais, apertar abraçadeiras em excesso.
- Conectores F mal crimpados (perdas e interferências).
- Armário sem alimentação nem terra, ou sem espaço para equipamentos ativos.
- Não etiquetar e não entregar plantas "como construído".

## 11. Exercícios (com resultados)
1. Quantos cabos de 6 mm de diâmetro cabem num tubo de 20 mm interior com 40% de ocupação? **R: secção do tubo 314 mm²; cabo 28,3 mm²; 0,4·314/28,3 = 4,4 → 4 cabos.**
2. Cabo horizontal de 85 m mais 2 cordões de 4 m: o canal cumpre o limite de 100 m? **R: 85 + 8 = 93 m ✓.**
3. Nível de entrada 75 dBµV, cabo de 40 m a 18 dB/100 m, distribuidor 1:8 (11 dB) e tomada (1 dB): nível na tomada? **R: 75 − 7,2 − 12 = 55,8 dBµV.**
4. Para que serve o fio guia deixado nos tubos? **R: para futuros puxamentos de cabos sem partir paredes.**

## 12. Fontes externas sugeridas
- **ANACOM, Manual ITED**: tabelas de materiais, quantidades, ocupações, distâncias e esquemas tipo.
- Manuais de instalação de fabricantes (Cat 6 e 6A, tomadas, painéis, fibra): Legrand, Schneider, Nexans, Prysmian, CommScope.
- Vídeos de instalação práticos de fabricantes (terminação RJ45 e F, emendas de fibra).
- PDF do referencial da UC (ANQEP).
