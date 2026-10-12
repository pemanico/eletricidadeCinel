# UC03077 - Executar desenho técnico de esquemas elétricos

> Material de estudo (explicação). Não é fonte normativa. Simbologia e regras de designação devem ser confirmadas nas normas IEC/EN indicadas.

## 1. Tipos de esquemas
- **Unifilar**: representa o circuito trifásico ou monofásico com um único traço por circuito; usa-se em quadros elétricos e projetos (aparelhagem, calibres, secções de cabo).
- **Multifilar**: todos os condutores representados; usado em montagem e deteção de avarias.
- **Funcional (de comando e potência)**: separa o circuito de potência do circuito de comando, e mostra a lógica de funcionamento (ex.: marcha-paragem de um motor).
- **De implantação (planta)**: posição física de tomadas, pontos de luz, quadros, caminhos de cabos sobre a planta da habitação ou fração.
- **De bornes / de ligações**: como se liga cada fio a cada borne.

## 2. Normas de referência (a confirmar nas versões em vigor)
- **IEC 60617** (simbologia gráfica).
- **IEC 61082** (regras de elaboração de documentação) e **IEC 81346 / EN 81346** (designação de equipamentos por letras).
- Em Portugal, para instalações de utilização: RTIEBT e as regras técnicas da DGEG exigem elementos de projeto, incluindo esquema unifilar e planta.

## 3. Designação dos aparelhos (letras)
A convenção tradicional (ainda comum em escolas e catálogos) e a da EN 81346-2 diferem; convém saber ambas.

| Aparelho | Tradicional | EN 81346-2 (letra de classe) |
|---|---|---|
| Disjuntor / interruptor de potência | QM, Q | Q |
| Contactor de potência | KM | Q |
| Relé de comando | KA | K |
| Fusível, relé térmico, proteção | F, FR | F |
| Botão, seletor, fim-de-curso | S | S |
| Motor | M | M |
| Sinalização (lâmpada/buzzer) | H | P |
| Transformador | T | T |

## 4. Numeração de bornes (contactores e relés)
- Bobina: **A1 / A2**.
- Contactos de potência: **1-2, 3-4, 5-6** (ou L1-T1, L2-T2, L3-T3).
- Contactos auxiliares normalmente abertos (NA): terminam em **3-4** (13-14, 23-24, ...). Normalmente fechados (NF): terminam em **1-2** (21-22, 31-32, ...).
- Relé térmico: potência 1-2, 3-4, 5-6; contacto auxiliar NF **95-96**, NA **97-98**.

## 5. Exemplo: esquema de arranque direto de motor trifásico (marcha-paragem)
**Potência:** L1/L2/L3 → disjuntor-motor ou fusíveis (F1) → contactor (KM1, contactos 1-2, 3-4, 5-6) → relé térmico (F2) → motor (M1).

**Comando:** de fase (L1) ou de transformador de comando → botão de paragem S0 (NF) → botão de marcha S1 (NA), em paralelo com o **contacto de selo** KM1 (13-14) → bobina KM1 (A1-A2) → neutro. O contacto auxiliar NF do relé térmico (95-96) entra em série no comando, antes da bobina.

**Funcionamento:** S1 energiza KM1; KM1 fecha os contactos de potência e o contacto de selo 13-14, que mantém a bobina energizada depois de largar S1. S0 ou o disparo do térmico interrompem o comando e o motor pára.
**Erros comuns:** botão de paragem em NA em vez de NF (não pára em caso de fio solto), e esquecer o contacto de selo.

## 6. Regras de boa apresentação
- Formato A4 ou A3, margens e moldura normalizadas; legenda com título, escala, data, autor, revisão.
- Cada esquema com legenda de símbolos; calibres e secções escritos junto dos símbolos no unifilar (ex.: "Q3 C16 6 kA, H07V-K 3G2,5").
- Linhas de potência mais grossas do que as de comando; cruzamentos sem ligação indicados sem ponto, e ligações com ponto.
- Planta: legenda de símbolos de tomadas e pontos de luz e cotas essenciais.

## 7. Exercícios práticos
1. Desenha o unifilar de um quadro de apartamento T2: geral, diferencial 30 mA, disjuntores para iluminação (C10), tomadas (C16), fogão (C32), termoacumulador (C20).
2. Desenha o esquema funcional de um motor com inversão de sentido (2 contactores, intertravamento mecânico e elétrico).
3. Refaz o esquema de marcha-paragem com sinalização (H1 em marcha, H2 em avaria térmica).

## 8. Ferramentas e fontes externas
- QElectroTech (gratuito, simbologia IEC) e LibreCAD; AutoCAD Electrical (pago) se for requisito do curso.
- Manuais de aparelhagem Schneider/Siemens/Legrand/ABB: contêm esquemas tipo gratuitos.
- RTIEBT (DGEG) e referencial da UC (ANQEP).
- Nota: o NotebookLM lê texto; esquemas desenhados em imagem ficam pobres como fonte. Descreve sempre o esquema em texto (como na secção 5).
