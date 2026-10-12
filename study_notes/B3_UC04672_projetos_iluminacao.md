# UC04672 - Executar projetos e instalações de iluminação

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Níveis de iluminância, UGR e IRC vêm da EN 12464-1 (locais de trabalho interiores) e de outras normas por tipo de espaço: confirmar na versão em vigor. Os fatores de utilização reais vêm das tabelas fotométricas do fabricante.

## 1. Grandezas fotométricas
| Grandeza | Símbolo | Unidade | Significado |
|---|---|---|---|
| Fluxo luminoso | Φ | lúmen (lm) | luz total emitida pela fonte |
| Intensidade luminosa | I | candela (cd) | fluxo por ângulo sólido, numa direção |
| Iluminância | E | lux (lx = lm/m²) | luz que chega a uma superfície |
| Luminância | L | cd/m² | brilho percebido de uma superfície |
| Eficácia luminosa | η | lm/W | fluxo por potência elétrica |
- **IRC (Ra):** capacidade de reproduzir cores (0 a 100). Escritórios/comércio ≥ 80; indústria 60 a 80 conforme a tarefa; tarefas de cor ≥ 90.
- **Temperatura de cor (CCT, K):** 2700 a 3000 K quente (habitação), 3500 a 4000 K neutra (escritório), > 5000 K fria.
- **UGR:** índice de encandeamento unificado (valor limite típico escritórios ≤ 19).
- **Fator de manutenção (Fm):** depreciação do fluxo e sujidade ao longo do tempo (típico 0,67 a 0,8 conforme ambiente e manutenção).

## 2. Valores indicativos de iluminância média (confirmar na norma)
Habitação: corredores ≈ 100 lx; salas ≈ 100 a 200 lx (zonas de leitura mais); cozinha ≈ 300 lx (bancada ≈ 500 lx); casa de banho ≈ 200 lx. Escritórios (EN 12464-1): ≈ 500 lx. Salas de aula ≈ 300 a 500 lx. Oficinas ≈ 300 a 500 lx, trabalhos finos até 750 a 1000 lx. Armazéns ≈ 100 a 200 lx. Exterior/parques depende da norma aplicável.

## 3. Método do fluxo (lúmen), para iluminação geral uniforme
**Φ_total = E · A / (Fu · Fm)**, N = Φ_total / Φ_luminária.
- **A** = área do plano de trabalho (m²).
- **Fu** = fator de utilização: depende do **índice do local k**, da refletância de teto/paredes/plano e do tipo de luminária (tabelas do fabricante).
- **Índice do local:** **k = a·b / (h·(a+b))**, com h = altura da luminária ao plano de trabalho.

### Exemplo resolvido (escritório)
Sala 6 m x 4 m, teto a 2,7 m, plano de trabalho a 0,8 m, luminárias encastradas no teto (h ≈ 2,0 m, aproximado). Luminária LED painel 3600 lm, 32 W. Objetivo E = 500 lx.
1. k = 6·4/(2,0·(6+4)) = 24/20 = **1,2**.
2. Fu (tabela do fabricante, para k = 1,2 e refletâncias 70/50/20): assumo **0,55** (valor ilustrativo).
3. Fm = **0,80** (escritório limpo, LED, manutenção periódica).
4. Φ_total = 500·24/(0,55·0,80) = **27 273 lm**.
5. N = 27 273/3600 = 7,6 → **8 luminárias** (disposição 4 x 2).
6. Iluminância real: E = N·Φ·Fu·Fm/A = 8·3600·0,55·0,80/24 = **528 lx** ✓ (≥ 500).
7. Potência instalada: 8·32 = **256 W**, densidade **10,7 W/m²**.
8. Verificar uniformidade (U0 ≥ 0,6 típico em escritório) por espaçamento: distância entre luminárias ≤ ~1,5 x h; na dúvida, simular em DIALux ou Relux.
9. Verificar encandeamento (UGR) e reflexos em ecrãs com os dados do fabricante.

## 4. Tecnologias de fonte e eficiência
- **LED:** 100 a 160 lm/W em luminárias profissionais; vida útil L70/B10 > 50 000 h (ler no datasheet); regulável; dependem do driver. Substituíram fluorescentes tubulares e halogéneo.
- **Fluorescente/CFL e descarga (vapor de sódio, iodetos metálicos):** em fim de uso; equipamento auxiliar (balastros, ignitores) e correção do fator de potência.
- **Halogéneo/incandescente:** em desuso por ineficiência (restrições da UE).
- **Driver LED:** corrente constante (ex.: 350, 500, 700 mA) ou tensão constante (12/24 V). Fator de potência e distorção harmónica (THD) importam em grandes instalações.
- **Regulação (dimming):** 1-10 V, DALI/DALI-2, DMX, fase cortada (TRIAC). Compatibilidade driver/regulador é crítica.

## 5. Cálculo elétrico de circuitos de iluminação
- **Corrente de arranque (inrush) dos drivers LED:** pode ser dezenas de amperes durante microssegundos e pode disparar disjuntores. **Limitar o número de luminárias por disjuntor** segundo a tabela do fabricante do driver (ex.: "máx. N drivers por disjuntor B10/C10/B16") ou usar curva C/D.
- **Corrente de projeto:** Ib = P total / (U·cos φ). Para LED com cos φ ≈ 0,9 a 0,95; para cargas com PFC fraco (cos φ ≈ 0,5), a corrente é bem maior que P/U.
- **Neutro:** em iluminação com drivers (harmónicos de 3.ª ordem), o neutro pode ficar carregado; considerar S_N = S_fase e atenção em sistemas trifásicos.
- **Queda de tensão:** limite mais restrito para iluminação (3% como referência IEC; confirmar RTIEBT); em cabos longos de 12/24 V (LED em fita) a queda é muito relevante: usar alimentações distribuídas.
- **Proteção:** disjuntor B ou C conforme inrush; diferencial 30 mA nos circuitos que o exijam (casas de banho, exterior, zonas acessíveis).
- **Iluminação exterior:** IP65 (ou superior), IK adequado (impacto), proteção contra sobretensões (luminárias expostas a descargas: SPD no quadro e/ou classe II), terras e equipotencialidade em colunas metálicas.

## 6. Projeto de iluminação: passos
1. Levantar o espaço (dimensões, refletâncias, pé direito, uso, horário).
2. Definir requisitos (E, UGR, IRC, uniformidade, CCT, regulação) pela norma aplicável.
3. Escolher luminárias e disposição; calcular (fluxo) e **verificar em software** (DIALux evo e Relux são gratuitos, com ficheiros fotométricos IES/LDT dos fabricantes).
4. Estimar potência instalada e densidade (W/m²) e comparar com requisitos de eficiência aplicáveis.
5. Dimensionar circuitos e proteções (UC01781); definir comando (interruptores, sensores, DALI).
6. Prever iluminação de emergência (UC04674) e manutenção (fator Fm, acessibilidade, plano de limpeza).
7. Documentar: planta de iluminação, quadro de cargas, esquemas de comando, lista de materiais, relatório de simulação.

## 7. Controlo e poupança de energia
- **Presença/ausência:** sensores PIR ou micro-ondas em corredores, WC, salas de reunião.
- **Luz natural (daylight harvesting):** sensores de luz regulam as luminárias junto às janelas.
- **Programação horária e cenários:** DALI, KNX (ver UC03099).
- **Zonamento:** circuitos separados por zona, janelas e função.

## 8. Erros comuns
- Calcular sem Fm (a iluminância cai abaixo do projeto ao fim de alguns anos).
- Ignorar a manutenção (luminárias inacessíveis).
- Muitos drivers num só disjuntor (disparos no arranque).
- Dimmer de fase com LEDs não compatíveis (cintilação, ruído).
- Esquecer a iluminação de emergência e o seu circuito.
- Projetar só pela potência em vez de lúmen e distribuição fotométrica.

## 9. Exercícios (com resultados)
1. Sala 5 m x 5 m, E = 300 lx, Fu = 0,5, Fm = 0,8: Φ total? **R: 300·25/(0,5·0,8) = 18 750 lm.**
2. Luminárias de 2500 lm: quantas? **R: 18 750/2500 = 7,5 → 8.**
3. Local 8 m x 6 m com h = 3 m: índice do local? **R: 48/(3·14) = 1,14.**
4. LED de 24 W com 3000 lm: eficácia? **R: 125 lm/W.**
5. Corredor 10 m x 2 m, E = 100 lx, Fu = 0,45, Fm = 0,8, luminárias de 1500 lm: N? **R: 100·20/(0,45·0,8) = 5 556 lm → 3,7 → 4 luminárias.**

## 10. Fontes externas sugeridas
- DIALux evo e Relux (software gratuito, bibliotecas fotométricas de fabricantes).
- Guias de iluminação gratuitos de fabricantes (Philips/Signify, Osram/Ledvance, Zumtobel, Schréder).
- EN 12464-1 (paga: usar os guias de fabricante como referência pública).
- Para eficiência energética em edifícios: documentos da DGEG/ADENE sobre iluminação.
- PDF do referencial da UC (ANQEP).
