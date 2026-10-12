# UC04675 - Executar projetos e instalações elétricas industriais

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Valores de motores (η, cos φ, corrente de arranque), poder de corte e classes de disparo vêm de catálogos de fabricantes e das normas IEC 60947 e IEC 61439: confirmar. Trabalhos em instalações industriais com tensão exigem qualificação própria, regras de segurança e procedimentos de bloqueio (lockout/tagout): ver UC00676.

## 1. Estrutura de uma instalação industrial
- **Alimentação:** média tensão (posto de transformação, UC04679/UC03895) ou baixa tensão direta.
- **Quadro geral de baixa tensão (QGBT)** → **quadros secundários/de distribuição** → **quadros de comando de máquinas/motores (CCM)** → cargas.
- **Esquema de terra:** TN-S frequente em indústria (com PE distribuído em toda a instalação); IT onde a continuidade do serviço é crítica (com monitor de isolamento).
- **Distribuição:** calhas de cabos, tabuleiros perfurados, **canalizações pré-fabricadas (busbar trunking)** para grandes correntes, cabos enterrados.
- **Quadros:** conforme **IEC 61439** (verificação de conjuntos): grau de proteção (IP), formas de separação, ventilação/dissipação, corrente de curto-circuito suportável (Icw) e de pico (Ipk).

## 2. Corrente de curto-circuito do transformador
Estimativa (fonte à montante considerada infinita):
**Icc ≈ In_transf / u_cc**, com In_transf = S/(√3·400).

**Exemplo:** transformador 630 kVA, 400 V, u_cc = 4%.
- In = 630 000/(√3·400) = **909 A**.
- Icc aos terminais secundários ≈ 909/0,04 = **22,7 kA**.
- Os aparelhos do QGBT têm de ter **poder de corte ≥ 22,7 kA** (ou ser protegidos por filiação/limitação de corrente homologada). O cabo e a barra suportam o I²t correspondente.
- Em pontos afastados, Icc diminui com a impedância dos cabos (ver UC01781); em zonas distantes, é a **Icc mínima** que decide o disparo magnético.

## 3. Motores trifásicos de indução
### Corrente nominal
**Ib = P_veio / (√3 · U · η · cos φ)**. Usa a chapa de características; se faltar, estimativas por catálogo.

**Exemplo:** motor de 15 kW, 400 V, η = 0,92, cos φ = 0,86 (valores típicos 4 polos, confirmar chapa).
- Ib = 15 000/(√3·400·0,92·0,86) = **27,4 A**.

### Arranque
- **Direto (DOL):** simples, I_arranque ≈ 6 a 8 x In → 164 a 219 A neste motor; binário elevado; pode causar quedas de tensão e esforço mecânico.
- **Estrela-triângulo:** I_arranque ≈ 1/3 do direto → ≈ 55 A; binário também reduzido a 1/3; exige motor cujos enrolamentos funcionem em triângulo a 400 V (placa de características 400/690 V; um motor 230/400 V não serve) e comutação sequencial; ressalto no instante de comutação.
- **Arrancador suave (soft starter):** rampa de tensão, reduz corrente e binário de arranque; opcional by-pass.
- **Variador de frequência:** controlo de velocidade e binário, arranque suave, poupança de energia em bombas e ventiladores; exige cuidados com harmónicos, CEM, cabos blindados e diferenciais compatíveis (ver UC03918).

### Proteção do circuito do motor
Três funções: **seccionamento/comando**, **proteção contra curto-circuito** e **proteção contra sobrecarga**:
- **Disjuntor-motor** (curva magnética alta, com térmico regulável): solução compacta para motores pequenos e médios.
- **Fusíveis aM + contactor + relé térmico**, ou **disjuntor magnético + contactor + relé térmico**.
- **Relé térmico/eletrónico:** regulado à corrente nominal da chapa; **classe de disparo** (10A, 10, 20, 30) conforme o tempo de arranque (arranque longo → classe 20 ou 30).
- **Coordenação tipo 1 ou tipo 2** (IEC 60947-4-1): tipo 2 admite apenas soldadura leve dos contactos após curto-circuito; tipo 1 admite danos no contactor, sem perigo.
- **Proteção contra falta de fase, desequilíbrio, subtensão** (relés de controlo) onde justificado.
- **Proteção por sondas PTC/Pt100** (temperatura dos enrolamentos) em motores críticos ou com variador.

### Dimensionamento do cabo do motor (exemplo, cont.)
Cabo Cu/XLPE em tabuleiro (método E), 40 °C, 1 circuito (k1 = 0,91), L = 40 m.
- I'z ≥ Ib/k = 27,4/0,91 = 30,1 A → **4 mm² (40 A de referência)**: Iz = 40·0,91 = 36,4 A ≥ 27,4 A ✓.
- **Queda de tensão em regime:** ΔU = √3·Ib·L·(R·cos φ + X·sen φ) = **9,2 V = 2,3%** ✓.
- **Queda de tensão no arranque** (I = 6·Ib = 164 A, cos φ de arranque ≈ 0,35): ΔU = **23,2 V = 5,8%** (a regulamentação/prática exige que o arranque não perturbe outros equipamentos; muitos fabricantes aceitam até ~10 a 15% no motor, confirmar). Se for excessivo, soft starter ou aumento de secção.
- Proteção: disjuntor-motor ajustado a 27,4 A, ou fusíveis aM + térmico regulado a 27,4 A.

## 4. Compensação do fator de potência
- Cargas indutivas (motores, transformadores) reduzem o cos φ e elevam a energia reativa faturada. Corrigir com **baterias de condensadores** (fixas ou automáticas): **Qc = P·(tan φ1 − tan φ2)** (ver UC01993).
- Em redes com **harmónicos** (variadores, retificadores), usar baterias com **reatâncias de dessintonia** para evitar ressonância.
- Compensação local (junto ao motor), por grupo ou global (QGBT): compromisso entre custo e eficácia.

## 5. Seletividade e filiação
- **Seletividade:** só dispara o aparelho imediatamente a montante da avaria. Obtém-se por: calibres diferentes (limitada), temporização (disjuntores abertos com retardo), **energia** (disjuntores limitadores, tabelas do fabricante).
- **Filiação (backup):** aparelho a jusante com poder de corte inferior à Icc, protegido por um limitador a montante, conforme tabelas homologadas do fabricante. Funciona mas pode reduzir a seletividade.
- **Verificação:** Icc máxima (poder de corte), Icc mínima (disparo e contactos indiretos), I²t e seletividade, para cada ramo.

## 6. Cabos e canalizações industriais
- Escolha por ambiente: temperatura, químicos, óleos, UV, risco mecânico, roedores, fogo (cabos livres de halogéneos, LSZH, resistentes ao fogo).
- **Cabos blindados** entre variador e motor (CEM) e ligação de terra de 360° das blindagens.
- **Separação** entre cabos de potência, comando e sinal (analógico, bus); cruzamentos a 90°.
- **Identificação:** cada cabo/condutor com número e destino; esquemas atualizados (UC03077).
- **Esforços eletrodinâmicos:** em canalizações pré-fabricadas e barramentos, verificar fixações para a Icc de pico.

## 7. Segurança elétrica e manutenção (ver UC00676 e UC01792)
- **Corte, bloqueio e sinalização** antes de intervir; verificação de ausência de tensão com aparelho adequado.
- **Equipamento de proteção individual (EPI)** e distâncias de segurança.
- **Manutenção preventiva e termografia** de quadros, ligações e motores.
- **Arco elétrico:** avaliação de risco e EPI para trabalhos em quadros energizados (apenas quando estritamente necessário e com qualificação).

## 8. Erros comuns
- Poder de corte inferior à Icc no ponto de instalação.
- Relé térmico regulado ao calibre do disjuntor e não à corrente da chapa do motor.
- Classe de disparo inadequada ao arranque (disparos intempestivos ou proteção que não protege).
- Desprezar a queda de tensão no arranque.
- Cabo de motor com variador sem blindagem nem ligação adequada à terra (interferências).
- Baterias de condensadores sem avaliar harmónicos.
- Misturar cabos de potência e de sinal no mesmo caminho.

## 9. Exercícios (com resultados)
1. Transformador de 1000 kVA, u_cc = 5%, 400 V: Icc? **R: In = 1443 A; Icc ≈ 28,9 kA.**
2. Motor de 7,5 kW, η = 0,90, cos φ = 0,84: corrente nominal? **R: 7500/(1,732·400·0,90·0,84) = 14,3 A.**
3. Arranque direto do motor anterior com 7·In: corrente? **R: ≈ 100 A.** Com estrela-triângulo? **R: ≈ 33 A.**
4. Carga de 50 kW a cos φ = 0,75 → 0,95: Qc? **R: tan φ1 = 0,882; tan φ2 = 0,329; Qc = 50·(0,882−0,329) = 27,7 kvar.**

## 10. Fontes externas sugeridas
- Guias técnicos gratuitos de Schneider Electric, ABB, Siemens, Legrand: seletividade, filiação, proteção de motores, tabelas de coordenação tipo 2.
- Catálogos de motores (WEG, ABB, Siemens) para η, cos φ e corrente de arranque reais.
- RTIEBT e legislação de instalações de serviço particular (DGEG).
- IEC 60947 e IEC 61439 (pagas): usar guias de fabricantes como material público.
- PDF do referencial da UC (ANQEP).
