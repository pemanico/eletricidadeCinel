# UC03088 - Instalar sistemas de conversão de corrente elétrica

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Dimensionar sempre com os datasheets do equipamento (potência em VA e W, fator de potência, rendimento, tensões).

## 1. Tipos de conversão
- **AC → DC: retificadores e carregadores** (fontes de alimentação, carregadores de baterias).
- **DC → AC: inversores** (alimentam cargas AC a partir de baterias ou FV).
- **DC → DC: conversores** (buck, boost, buck-boost; fontes isoladas).
- **AC → AC: transformadores, autotransformadores, reguladores de tensão, conversores de frequência (variadores).**
- **UPS (sistemas de alimentação ininterrupta):** retificador + bateria + inversor; mantêm a carga ligada durante cortes e perturbações da rede.

## 2. Inversores
- **Onda sinusoidal pura:** adequada a quase todas as cargas (motores, eletrónica sensível). **Onda modificada/quadrada:** só cargas simples, pode causar ruído e aquecimento em motores.
- **Potência nominal vs potência de pico:** motores e compressores têm corrente de arranque de 3 a 7 vezes a nominal; o inversor deve suportar o pico (ler "surge power").
- **Rendimento:** 90 a 97%, menor a baixa carga. **Consumo em vazio** (stand-by) conta em sistemas isolados.
- **Tensão do barramento DC:** 12/24/48 V (baixa tensão) ou mais elevada; potências altas pedem tensões altas (menor corrente).
- **Inversor de rede (grid-tie):** sincroniza com a rede e inclui proteções de anti-ilhamento (UC01799).
- **Inversor off-grid/híbrido:** forma a sua própria tensão ou comuta com a rede.

### Exemplo: dimensionar um inversor de 12 V para ferramentas
- Carga: 2 ferramentas a 600 W cada (simultâneas) e um motor de 400 W com arranque a 3x.
- Potência contínua: 600 + 600 + 400 = **1 600 W**. Pico: 600 + 600 + 3·400 = **2 400 W**.
- Escolher inversor sinusoidal de **≥ 2 000 W contínuos** com pico ≥ 2 400 W; corrente DC em 12 V ≈ 2 000/(12·0,9) ≈ **185 A** (cabos grossos, fusível DC: fica claro que 24 V ou 48 V seriam preferíveis para esta potência).

## 3. UPS
- **Off-line (standby):** a carga está ligada à rede; em falha, comuta para a bateria (tempo de comutação ~5 a 10 ms). Para PCs simples.
- **Line-interactive:** com regulação de tensão (AVR) sem usar a bateria; comuta em falha; uso em escritório e pequenos servidores.
- **Online (dupla conversão):** a carga é sempre alimentada pelo inversor; sem tempo de comutação e com isolamento das perturbações da rede; para servidores, equipamentos críticos e médicos.
- **Dimensionamento:**
  - **Potência aparente:** S = P/cos φ (UPS indica kVA e kW). Carga de 2 kW com cos φ = 0,8 → **2,5 kVA** (+ margem de 20 a 30%).
  - **Autonomia:** E_bateria = P·t/(η_inversor·DoD).
  - **Exemplo resolvido:** carga 800 W, autonomia 30 min, η = 0,9, DoD 0,8: E = 800·0,5/(0,9·0,8) = **556 Wh** → em baterias de 12 V: 556/12 = **46,3 Ah** → 1 bateria 12 V/50 Ah (ou 2 de 12 V em série a 24 V com 23,1 Ah → 2 x 12 V/25 Ah). A capacidade real das baterias de chumbo cai com descargas rápidas (efeito Peukert): aplicar margem (20 a 30%) ou consultar as tabelas do fabricante.
- **Bypass manual** de manutenção para trabalhar na UPS sem desligar a carga.
- **Ligação à terra e neutro:** respeitar o esquema de ligação à terra (TN/TT/IT) e a existência de transformador de isolamento, com diferenciais compatíveis.
- **Normas:** EN/IEC 62040 (UPS).

## 4. Carregadores de baterias
- **Perfil de carga:** corrente constante (CC) → tensão constante (CV) → flutuação; lítio e chumbo têm tensões diferentes (p. ex., chumbo 12 V: absorção ≈ 14,4 V; flutuação ≈ 13,6 V, confirmar fabricante).
- **Compensação de temperatura** em chumbo-ácido.
- **Corrente de carga:** típica **C/10 a C/5** em chumbo (C/10 de uma bateria 100 Ah = 10 A); lítio aceita correntes mais altas conforme o BMS.
- **Proteção:** fusível no cabo da bateria o mais perto possível do terminal positivo.

## 5. Retificadores e fontes de alimentação industriais
- **Fonte de alimentação DC (24 V)** para comando e automação: potência com margem (≥ 120% da carga), tensão, ripple e **corrente de arranque**; instalar em quadro com ventilação e fusíveis a jusante.
- **Redundância (N+1)** e módulos de diodos de redundância em sistemas críticos.
- **Conversores DC-DC isolados** para sinais e proteção.

## 6. Instalação e proteções
- **Secções de cabos DC** para correntes elevadas (queda de tensão baixa), comprimentos curtos e **fusível/disjuntor DC** com poder de corte DC adequado.
- **Seccionador** do lado DC e do lado AC.
- **Terra e equipotencialidade** da carcaça dos conversores.
- **Ventilação e dissipação:** inversores e UPS dissipam 3 a 10% da potência em calor; espaço livre e temperatura ambiente do fabricante.
- **Harmónicos e CEM:** conversores eletrónicos injetam harmónicos e ruído; usar filtros e cablagem blindada quando indicado (UC01795).
- **Diferencial:** cargas eletrónicas com fugas DC podem exigir diferencial tipo A ou B (ver ficha técnica).

## 7. Erros comuns
- Dimensionar o inversor só pela potência nominal, sem pico de arranque.
- Cabos DC de baixa tensão subdimensionados.
- UPS dimensionada em W e não em VA (cos φ).
- Ignorar a degradação e o efeito Peukert nas baterias de chumbo.
- Sem fusível DC junto da bateria.
- Ligar carga indutiva a inversor de onda modificada.

## 8. Exercícios (com resultados)
1. Carga de 1 500 W, cos φ = 0,75: potência aparente da UPS (com 25% de margem)? **R: S = 2 000 VA; com margem ≈ 2,5 kVA.**
2. Inversor de 3 000 W em 48 V (η = 0,92): corrente DC? **R: 3 000/(48·0,92) ≈ 67,9 A.**
3. Carregador para bateria de chumbo de 120 Ah a C/10: corrente? **R: 12 A.**
4. UPS com bateria de 24 V/40 Ah (DoD 0,8, η = 0,9) para carga de 300 W: autonomia aproximada? **R: E útil = 24·40·0,8·0,9 = 691 Wh → 691/300 ≈ 2,3 h (ideal; na prática menos).**

## 9. Fontes externas sugeridas
- Guias de projeto de fabricantes (Victron Energy, Eaton, APC/Schneider, Riello, Mean Well).
- EN/IEC 62040 (paga): usar documentação de fabricante como material público.
- PDF do referencial da UC (ANQEP).
