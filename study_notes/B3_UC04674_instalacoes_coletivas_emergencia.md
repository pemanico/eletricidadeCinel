# UC04674 - Executar instalações coletivas e de sinalização e emergência

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Os fatores de simultaneidade, limites de queda de tensão nas colunas e as exigências de segurança contra incêndio (SCIE) são definidos por regulamentação nacional que muda: **confirmar na versão em vigor** (RTIEBT, regulamento técnico de SCIE, regras da distribuidora). O exemplo de coeficientes é o de tabelas IEC usadas como referência didática.

## 1. Instalações coletivas de edifícios
**Estrutura típica (do exterior para o fogo):**
1. **Ramal de ligação** (rede pública → edifício) e **portinhola**/caixa de entrada.
2. **Caixa de coluna / quadro de colunas**.
3. **Coluna montante** (cabos que sobem pelo edifício com derivações por piso).
4. **Caixas de coluna derivadas e quadros de contagem** (contadores por fogo e de serviços comuns).
5. **Ramais de entrada/derivações** para cada fração, até ao quadro individual (UC04673).
6. **Instalação de serviços comuns:** iluminação de escadas e garagem, elevadores, bombas, intercomunicadores, ITED/ITUR, medidores.

**Pontos práticos:**
- Os **ramais e colunas** têm requisitos de percurso (partes comuns acessíveis), proteção mecânica, identificação, e as **proteções** devem ficar acessíveis aos serviços da distribuidora.
- **Contagem:** os contadores ficam em compartimento ou armário próprio, acessível à distribuidora; ligações conforme as regras de ligação à rede (UC01788/UC01793).
- **Equipotencialidade e terra:** elétrodo de terra do edifício (anel/fundações), barra principal de terra, ligação das colunas e estruturas metálicas (UC01782).

## 2. Dimensionamento da coluna montante
**Potência de cálculo** = potência dos fogos x fator de simultaneidade (função do número de fogos) + serviços comuns.

**Coeficientes de simultaneidade de referência para edifícios de habitação (tabela IEC, ilustrativa; a regulamentação portuguesa tem o seu método: confirmar):**
| Nº de fogos | 2-4 | 5-9 | 10-14 | 15-19 | 20-24 | 25-29 | 30-34 | 35-39 | 40-49 | ≥ 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| Coeficiente | 1 | 0,78 | 0,63 | 0,53 | 0,49 | 0,46 | 0,44 | 0,42 | 0,41 | 0,38 |

### Exemplo resolvido
Edifício com **12 fogos** com potência de 10,35 kVA cada, e serviços comuns de 15 kVA (elevador, escadas, bomba). Rede trifásica 400 V.
1. Coeficiente (12 fogos) = **0,63**.
2. S_fogos = 12 · 10,35 · 0,63 = **78,2 kVA**.
3. S_total = 78,2 + 15 = **93,2 kVA** (serviços comuns normalmente somam-se com o seu próprio fator, aqui 1).
4. I = 93 246/(√3·400) = **134,6 A**.
5. Calibre da proteção da coluna: **≥ 135 A → 160 A** (próximo calibre normalizado), cabo com Iz ≥ 160 A (após fatores de correção): por exemplo Cu/XLPE de 50 mm² (referência ~180 A em tabuleiro/ar, confirmar tabela e fatores).
6. Verificar **queda de tensão** da coluna até ao último piso (a regulamentação define um limite específico para colunas: confirmar) e **curto-circuito** (poder de corte da proteção, solicitação térmica).
7. Neutro e PE: com fases de 50 mm², o PE mínimo é S_fase/2 = **25 mm²** (regra: S ≤ 16 → S; 16 < S ≤ 35 → 16 mm²; S > 35 → S/2). Neutro conforme a regra de redução (ver UC01781) e tendo em conta harmónicos.

*Nota:* com fogos de 6,9 kVA, o mesmo cálculo dá S_fogos = 52,2 kVA; S_total = 67,2 kVA; I = 97 A. Mostra como a potência contratada por fogo condiciona a coluna.

## 3. Iluminação de emergência
**Funções:** (a) **iluminação de evacuação** (vias de evacuação, saídas, pontos de risco) e (b) **iluminação anti-pânico** (grandes áreas abertas). Referências europeias: **EN 1838** (iluminação de emergência), **EN 50172** (sistemas de iluminação de segurança), **EN 60598-2-22** (luminárias de emergência). Em Portugal, as exigências por tipo de edifício estão no regulamento técnico de SCIE: confirmar.

**Valores típicos de referência (confirmar nas normas/SCIE):**
- **Vias de evacuação:** iluminância ≥ **1 lx** ao longo do eixo da via (ao nível do solo); uniformidade máx/mín ≤ 40:1.
- **Anti-pânico:** ≥ **0,5 lx** na área central (exclui margem de 0,5 m).
- **Pontos de risco (extintores, botões de alarme, quadros):** pelo menos 5 lx, conforme norma.
- **Tempo de arranque:** ≤ **5 s** a 50% do nível (≤ 0,5 s em locais de alto risco).
- **Autonomia:** tipicamente **≥ 1 h** (alguns locais exigem 2 h ou mais): confirmar a categoria do edifício.
- **Posicionamento:** junto a cada saída, mudanças de direção e de nível, cruzamentos de vias, escadas, equipamentos de combate a incêndio.

**Tipos de sistema:**
- **Luminárias autónomas** (bateria própria; manutenção/ensaios por luminária; mais simples em edifícios pequenos).
- **Alimentação centralizada** (bateria central ou grupo gerador; menos pontos de bateria, mas exige **cabos resistentes ao fogo** e proteção do circuito).
- **Permanentes** (sempre acesas) ou **não permanentes** (acendem só em falha de rede).
- **Luminárias com módulo de teste automático** (autoteste periódico e registo, recomendado).

**Instalação e ensaios:**
- Alimentação a partir de **circuito dedicado** (com o sensor de falha a montante, para detetar corte à rede normal).
- **Cabos resistentes ao fogo** (ex.: classes de resistência ao fogo E30/E60/E90 conforme o sistema e a exigência) em sistemas centralizados.
- **Ensaios periódicos:** funcional (mensal) e de autonomia (anual); manter **registo** (livro de manutenção).
- Substituir baterias no fim de vida (geralmente 4 a 5 anos, ver datasheet).

## 4. Sinalização de segurança
- **Pictogramas de saída/evacuação** (símbolo verde "homem a correr" com seta): conformes à norma (ISO 7010 e EN 1838).
- **Distância máxima de visualização do pictograma:** **d = 200 · h** (sinal iluminado internamente, mais luminoso) ou **d = 100 · h** (iluminado externamente), onde h é a altura do pictograma.
  - Exemplo: pictograma h = 0,15 m → 30 m (interno) ou 15 m (externo).
- **Sinalização de equipamento de combate a incêndio e de risco:** pictogramas conforme ISO 7010 (extintor, boca de incêndio, botão de alarme).
- **Sinalização luminosa** (indicadores de estado, lâmpadas de sinalização em painéis).
- **Sinalização sonora:** sirenes, campainhas de alarme (nível sonoro e reconhecimento da mensagem).

## 5. Sistemas de segurança associados (visão geral)
- **Deteção e alarme de incêndio** (detetores de fumo/calor convencionais ou endereçáveis, botões manuais, central; cabos resistentes ao fogo e alimentação com baterias). Projeto próprio, em regra com requisitos de homologação e manutenção (ver SCIE e normas EN 54).
- **Intercomunicadores/videoporteiros** (partes comuns): cabos de baixa tensão (ITED/ITUR/ITUR compatível), alimentações separadas, equipotencialidade.
- **Controlo de acessos e CCTV:** circuitos de baixa tensão, alimentação ininterrupta, proteção contra sobretensões.

## 6. Erros comuns
- Dimensionar a coluna pela soma das potências dos fogos (sem simultaneidade) ou, ao contrário, aplicar coeficientes sem confirmar a regulamentação.
- Esquecer a queda de tensão da coluna no último piso.
- Iluminação de emergência sem circuito dedicado ou sem deteção de falha da rede.
- Autonomia insuficiente ou ensaios nunca feitos/registados.
- Cabos de sistemas de segurança sem a resistência ao fogo exigida.
- Pictogramas fora da distância de visualização ou obstruídos.
- Ligar o neutro de várias fases ou misturar neutros entre circuitos nos serviços comuns.

## 7. Exercícios (com resultados)
1. Edifício de 20 fogos de 6,9 kVA, serviços comuns de 10 kVA: corrente na coluna (trifásica 400 V)? **R: coeficiente 0,49 → 20·6,9·0,49 = 67,6 kVA + 10 = 77,6 kVA → 112 A.**
2. Pictograma de 0,10 m iluminado internamente: distância máxima? **R: 20 m.**
3. Percurso de evacuação de 40 m, pictogramas de 0,15 m iluminados internamente: precisa de quantos pictogramas (mínimo, só por distância)? **R: 30 m de alcance cada → pelo menos 2 (confirmar posicionamento pelas regras da norma).**
4. Iluminação de emergência com autonomia exigida de 1 h e bateria de 4 Wh por luminária de 3 W: serve? **R: 4 Wh/3 W = 1,3 h → serve (com margem de envelhecimento: confirmar).**

## 8. Fontes externas sugeridas
- RTIEBT (DGEG): instalações coletivas e de ligação à rede.
- Regulamento técnico de SCIE (ANEPC) e notas técnicas: iluminação de segurança e sinalização.
- Guias de fabricantes de iluminação de emergência (Legrand, Schneider, Zumtobel, Daisalux): tabelas de espaçamento e autonomia.
- Guias de cabos resistentes ao fogo (Prysmian, Nexans).
- EN 1838, EN 50172 (pagas): usar os guias de fabricante como material público.
- PDF do referencial da UC (ANQEP).
