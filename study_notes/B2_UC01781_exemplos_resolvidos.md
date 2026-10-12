> **ERRATA (2026-10-12):** nesta nota, a 'correção' do exemplo do termoacumulador usou capacidades de corrente da tabela IEC 60364-5-52:2009 (método B1: 4 mm² = 28 A). O **RTIEBT, Quadro 52-C1, método B** (tubo embebido em alvenaria), dá **32 A para 4 mm²**. Com os fatores k1 = 0,94 e k2 = 0,70, Iz = 21,06 A ≥ In = 20 A: **4 mm² cumpre sob o RTIEBT** (3G4 + C20 + DDR 30 mA). A tabela a usar em Portugal é a do RTIEBT. Todos os valores de capacidade de corrente desta nota são IEC 2009 B1, não RTIEBT, e por rever. Ver `src/eletro/calc/cabos.py` e `docs/REGRAS_HABITACAO_RTIEBT.md`.

# UC01781 - Exemplos resolvidos de dimensionamento (complemento)

> Material de estudo. **Valores de tabela são de referência (IEC 60364-5-52) e têm de ser confirmados na norma/RTIEBT e nos catálogos dos fabricantes.** Resistividade usada: Cu 0,0225 Ω·mm²/m (≈ 90 °C), X = 0,08 mΩ/m. Os cálculos foram verificados por código.

---

## Exemplo 1 - Termoacumulador (versão corrigida do exemplo do chat)
Circuito monofásico 230 V, carga 4,6 kW resistiva, L = 25 m, Cu/PVC em tubo embebido (B1), ambiente 35 °C, agrupado com mais 2 circuitos, Icc presumida 3 kA, disjuntor 6 kA curva C.

1. Ib = 4600/230 = **20 A**; In = **20 A**.
2. k1 (35 °C, PVC) = 0,94; k2 (3 circuitos) = 0,70; **k = 0,658**.
3. I'z ≥ In/k = 20/0,658 = **30,4 A**.
4. Tabela B1 PVC 2 carr.: 2,5 mm² → 21 A; 4 mm² → 28 A (**não chega**); 6 mm² → 36 A ✓.
5. Iz = 36 · 0,658 = **23,7 A**. Verificação: Ib (20) ≤ In (20) ≤ Iz (23,7) ✓.
6. Queda de tensão: ΔU = 2·0,0225·25·20/6 = 3,75 V = **1,6%** ✓.
7. Curto-circuito: poder de corte 6 kA ≥ 3 kA ✓. Térmico: k²S² = 115²·6² = 476 100 A²s, muito acima do I²t passante de um C20 limitador (ordem de 50 000 A²s a 6 kA; confirmar curva do fabricante) ✓.
8. Contactos indiretos: C20, Ia = 10·20 = 200 A; Zs máx = 230/200 = 1,15 Ω. Impedância do circuito (fase + PE 6 mm²): 0,0225·25·(1/6+1/6) = 0,19 Ω; com 0,4 Ω a montante, Zs ≈ 0,59 Ω ≤ 1,15 Ω ✓.

**Resultado: 3G6 mm² Cu/PVC + C20 6 kA + DDR 30 mA.**

---

## Exemplo 2 - Circuito trifásico em tabuleiro, XLPE, onde a queda de tensão decide
Carga trifásica 18 kW, 400 V, cos φ = 0,9, L = 60 m, cabo Cu/XLPE multicondutor em tabuleiro perfurado (método E), ambiente 40 °C, 2 circuitos juntos no tabuleiro (camada única, encostados).

1. Ib = 18 000 / (√3·400·0,9) = **28,9 A**; In = **32 A**.
2. k1 (40 °C, XLPE) = 0,91; k2 (2 circuitos, tabuleiro perfurado) = 0,88; **k = 0,801**.
3. I'z ≥ 32/0,801 = **39,96 A**.
4. Tabela E XLPE 3 carr.: 4 mm² → 40 A (passa **por 0,04 A**); 6 mm² → 51 A; 10 mm² → 70 A.
5. Iz: 4 mm² → 32,03 A; 6 mm² → 40,8 A; 10 mm² → 56,1 A.
6. Queda de tensão (trifásica, R·cos φ + X·sen φ):

| S | R (Ω/m) | ΔU (V) | ΔU (%) |
|---|---|---|---|
| 4 mm² | 0,005625 | 15,3 | **3,82%** |
| 6 mm² | 0,00375 | 10,2 | **2,56%** |
| 10 mm² | 0,00225 | 6,2 | **1,54%** |

7. **Decisão:**
   - Se o limite aplicável fosse 3%, 4 mm² não serve (3,82%) e escolhe-se **6 mm²** (2,56%).
   - Se o limite for 5%, 4 mm² cumpre a queda de tensão, mas com margem térmica de 0,03 A: qualquer alteração (um terceiro circuito no tabuleiro, 45 °C no verão) invalida-o. **Boa prática: 6 mm²**.
8. Com 6 mm²: Iz = 40,8 A ≥ In = 32 A ✓; I2 = 1,45·32 = 46,4 A ≤ 1,45·40,8 = 59,2 A ✓.
9. Térmico a curto-circuito: k²S² = 143²·6² = 736 164 A²s (Cu/XLPE); confirmar I²t do disjuntor.
10. Neutro: S_fase 6 mm² ≤ 16 → S_N = 6 mm²; PE = 6 mm².

**Resultado: 5G6 mm² Cu/XLPE (ou 4G6 + PE conforme o caso) + disjuntor 32 A.** Lição: o critério térmico dava 4 mm², o decisivo foi a queda de tensão/robustez.

---

## Exemplo 3 - Cabo longo monofásico: queda de tensão e Icc mínima
Iluminação exterior monofásica 2,3 kW (Ib = 10 A, cos φ = 1) a 90 m do quadro, Cu/PVC, 230 V. Proteção disjuntor C10 (Im máx = 10·10 = 100 A). Impedância a montante do quadro (fase+neutro) presumida em 0,4 Ω.

1. Secção mínima pela queda de tensão (limite 3% = 6,9 V): S ≥ 2·ρ·L·Ib/ΔU = 2·0,0225·90·10/6,9 = **5,87 mm²** → **6 mm²**.

| S | ΔU (V) | ΔU (%) | Zs (Ω) | Icc mín (A) | Dispara C10 (≥ 100 A)? |
|---|---|---|---|---|---|
| 1,5 mm² | 27,0 | 11,7% | 3,10 | 74 | **Não** |
| 2,5 mm² | 16,2 | 7,0% | 2,02 | 114 | Sim (margem curta) |
| 4 mm² | 10,1 | 4,4% | 1,41 | 163 | Sim |
| 6 mm² | 6,75 | 2,93% | 1,08 | 214 | Sim |
| 10 mm² | 4,05 | 1,76% | 0,81 | 286 | Sim |

   (Zs = 0,0225·90·(1/S+1/S_PE) + 0,4 com S_PE = S; Icc mín = 230/Zs.)

2. **Leituras importantes:**
   - O aquecimento permitiria 1,5 mm² (a corrente é só 10 A): o critério decisivo é a **queda de tensão** (6 mm²).
   - Com 1,5 mm² a Icc mínima (74 A) fica abaixo do disparo magnético do C10 (100 A): **o disjuntor pode não disparar num curto no extremo**. O mesmo critério aplica-se à proteção contra contactos indiretos (Zs ≤ 230/100 = 2,3 Ω → 1,5 mm² não cumpre, 2,5 mm² cumpre).
   - Em cabos longos: usar curva B (disparo 3-5·In) ou reduzir o calibre da proteção, e/ou aumentar a secção.
3. Com 6 mm²: ΔU = 2,93% (apenas dentro de 3%): se houver mais carga futura, subir para 10 mm². Caso a queda de tensão total contasse desde a origem, somar a parte do circuito a montante.

**Resultado: 3G6 mm² + C10 (ou B10) + DDR 30 mA.**

---

## Exemplo 4 - Fatores de agrupamento: o erro clássico
O Exemplo 1 com 6 circuitos no mesmo tubo/calha embebida (k2 = 0,57) a 35 °C (k1 = 0,94): k = 0,536.
- I'z ≥ 20/0,536 = 37,3 A → 6 mm² (36 A) já **não chega**: passa a 10 mm² (50 A).
- Mesma carga, mesmo cabo, só por juntar circuitos no mesmo tubo: a secção sobe um escalão. Evita-se separando circuitos ou aumentando secção cedo no projeto.

## Exercícios propostos
1. Repete o Exemplo 2 com L = 100 m. Qual a secção mínima (limite 3%)? **R: 4 mm² → 6,37%; 6 mm² → 4,26%; 10 mm² → 2,57%. Com limite de 3% a secção mínima é 10 mm² (com limite de 5%, 6 mm² bastaria).**
2. Exemplo 3 com disjuntor C16 em vez de C10: a Icc mínima de 6 mm² (214 A) dispara? **R: Im máx = 10·16 = 160 A < 214 A → sim; mas rever Iz (6 mm² B1 PVC 2 carr.: 36 A) e a queda de tensão.**
3. Monofásico 230 V, motor de 2,2 kW, cos φ = 0,8, η = 0,85: Ib? **R: Ib = 2200/(230·0,8·0,85) = 14,1 A (confirmar com a chapa).**

## Fontes externas sugeridas
- RTIEBT (DGEG), versão em vigor.
- Catálogos de cabos (queda de tensão em mV/A/m por secção) e guias de proteção de fabricantes (Schneider, Legrand, ABB).
- Calculadores de fabricantes (Schneider EcoStruxure, ABB DOC, Legrand XL Pro) para comparar os teus resultados manuais.
