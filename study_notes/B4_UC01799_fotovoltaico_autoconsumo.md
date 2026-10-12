# UC01799 - Instalar kit de sistema fotovoltaico para autoconsumo

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Os dados dos módulos e inversores do exemplo são ilustrativos: usar sempre os datasheets reais. Os **limiares de potência e os procedimentos de registo/licenciamento de UPAC** (unidades de produção para autoconsumo) mudam com a legislação: consultar a DGEG, o portal de autoconsumo e a distribuidora (e-Redes) antes de instalar.

## 1. Conceitos
- **UPAC:** unidade de produção para autoconsumo; a energia produzida é consumida no local e o excedente pode ser injetado na rede (conforme o regime aplicável).
- **kWp:** potência de pico dos módulos (condições STC: 1000 W/m², 25 °C, AM 1,5).
- **Produtividade específica** (kWh/kWp/ano): depende da localização, orientação e inclinação. Em Portugal continental, valores típicos em torno de **1 400 a 1 700 kWh/kWp/ano**; **usar o PVGIS** (ferramenta gratuita da Comissão Europeia) para o local, inclinação e azimute reais.
- **Autoconsumo vs autossuficiência:** autoconsumo = % da produção consumida no local; autossuficiência = % do consumo coberta pela produção própria.
- **Orientação e inclinação:** sul (azimute 0°) com inclinação ≈ 30° a 35° maximiza a produção anual em Portugal; este/oeste dá menos energia total, mas curva de produção mais larga (útil para autoconsumo).

## 2. Componentes do sistema
- **Módulos fotovoltaicos** (monocristalinos, tipicamente 400 a 450 W; ler Voc, Isc, Vmpp, Impp, coeficientes de temperatura).
- **Inversor:** string (ligado à rede) ou híbrido (com bateria); com 1 ou mais MPPT; certificado para ligação à rede (anti-ilhamento e comportamento conforme a norma aplicável, p. ex. EN 50549).
- **Estrutura de fixação** (cobertura inclinada, plana com suportes, solo): cálculo de cargas de vento/neve e fixações adequadas à cobertura.
- **Cablagem DC** (cabo solar fotovoltaico, duplo isolamento, resistente a UV, ex.: H1Z2Z2-K, 4 mm² ou 6 mm²) e **conectores** (da mesma marca/modelo: misturar marcas é causa frequente de incêndio).
- **Proteções DC:** interruptor-seccionador DC, limitador de sobretensão DC, fusíveis de string quando exigidos (tipicamente quando há 3 ou mais strings em paralelo, conforme as indicações do fabricante).
- **Proteções AC:** disjuntor, diferencial (tipo conforme o inversor, ver datasheet), limitador de sobretensão AC.
- **Contador** (bidirecional ou com medição separada da produção, conforme o regime) e **monitorização** (Wi-Fi/Ethernet).
- **Terras e equipotencialidade:** estrutura metálica e módulos ligados ao sistema de terra (UC01782).

## 3. Dimensionamento (passos)
1. **Consumo anual** (kWh) e **perfil horário** (quando é consumido).
2. **Potência FV:** P_pico ≈ E_alvo / produtividade específica. Limitar pela área disponível e pela potência de ligação à rede.
3. **Escolha do inversor:** potência AC ≈ 0,8 a 1,2 x P_pico (rácio DC/AC), conforme a tecnologia e a estratégia.
4. **Configuração de strings** (módulos em série) com base na janela de tensão do MPPT.
5. **Cabos e proteções DC e AC.**
6. **Ligação ao quadro e ao contador, terra e SPD.**
7. **Ensaios e comissionamento.**

### Exemplo resolvido: moradia com consumo de 5 000 kWh/ano
1. Produtividade específica de referência (confirmar no PVGIS): **1 500 kWh/kWp/ano**.
2. P_pico ≈ 5 000/1 500 = 3,33 kWp. Com módulos de 415 W: **8 módulos = 3,32 kWp**; produção anual estimada ≈ 3,32 · 1 500 ≈ **4 980 kWh** (ordem de grandeza).
3. Inversor monofásico de 3 kW a 3,6 kW (rácio DC/AC ≈ 1,0 a 1,1).
4. **Dados do módulo (ilustrativos):** Voc = 37,5 V, Vmpp = 31,5 V, Isc = 13,9 A; coeficiente de Voc = −0,27 %/°C; de Vmpp ≈ −0,34 %/°C.
5. **String de 8 módulos em série:**
   - **Voc máxima** (temperatura de célula mínima, ex.: −10 °C): Voc = 37,5·(1 + 0,0027·35) = 41,0 V por módulo → **328 V** na string. Tem de ser **menor que a tensão máxima DC do inversor** (ex.: 600 V ou 1 000 V; ler no datasheet) ✓.
   - **Vmpp mínima** (célula a ~70 °C): Vmpp = 31,5·(1 − 0,0034·45) = 26,7 V por módulo → **213 V** na string. Tem de ficar **dentro da janela MPPT** do inversor (ex.: 90 a 550 V) ✓.
   - **Corrente:** Isc = 13,9 A deve ser ≤ corrente máxima de entrada do MPPT (ler datasheet).
   - 9 módulos em série: Voc a −10 °C seria 369 V (continua dentro de 600 V), mas fora do exemplo de potência.
6. **Cabo DC:** Iz ≥ 1,25 · Isc = 17,4 A → cabo solar de **4 mm²** (confirmar capacidade de corrente do cabo ao ar/fixo, fatores de temperatura de cobertura que pode atingir 60 a 70 °C). Queda de tensão no lado DC: manter < 1 a 2%.
7. **Lado AC:** I = 3 300/230 = **14,3 A** → disjuntor **C16** (confirmar com o datasheet do inversor), cabo 2,5 mm² (verificar queda de tensão e agrupamento), diferencial 30 mA (tipo A ou conforme indicação do fabricante: inversores sem transformador podem exigir tipo B ou terem monitorização de corrente residual integrada).

## 4. Ligação à rede e enquadramento (confirmar)
- **Injeção e regimes:** consoante a potência da UPAC e a potência contratada, aplicam-se regras diferentes de registo, comunicação prévia ou licença. **Verifica no portal oficial de autoconsumo (DGEG/e-Redes)** o regime e os procedimentos para o teu caso.
- **Proteção de interligação:** o inversor deve cumprir a norma de ligação (anti-ilhamento, limites de tensão e frequência); para potências maiores pode exigir proteção de interligação externa.
- **Contador:** a ligação do contador e a eventual troca por contador bidirecional é feita pela distribuidora (UC01788).
- **Potência de ligação à rede e potência contratada:** a potência de injeção está limitada pelos regulamentos e pela capacidade da ligação.

## 5. Instalação em cobertura: segurança
- **Trabalhos em altura:** linhas de vida, EPI, plano de segurança (UC00676).
- **DC com tensão sempre que há luz:** não se corta a produção desligando só o lado AC; usar o seccionador DC e cobrir módulos para intervenções.
- **Distâncias a respeitar** e acesso dos bombeiros: seccionamento de emergência acessível e sinalizado conforme as regras aplicáveis; verificar requisitos de SCIE para edifícios de maior risco.
- **Ligações MC4 (ou equivalente):** crimpagem correta com a ferramenta do fabricante; nunca misturar fabricantes; confirmar tração e estanquidade.
- **Equipotencial e terra** da estrutura; **SPD** DC e AC onde o risco o justifique.

## 6. Ensaios de comissionamento (IEC 62446-1, referência)
- Continuidade dos condutores de proteção e equipotencialidade.
- **Polaridade** dos cabos DC.
- **Voc e Isc por string** (comparar com o esperado: desvios entre strings iguais devem ser pequenos).
- **Resistência de isolamento DC** (strings e estrutura).
- **Funcionamento do inversor** (arranque, potência, comunicação) e da proteção diferencial.
- Registo dos resultados (ficha de comissionamento) e entrega de documentação ao cliente (esquemas, datasheets, manual).

## 7. Erros comuns
- String com Voc a baixa temperatura acima do limite do inversor (risco de danificar).
- Vmpp a alta temperatura abaixo da janela MPPT (o inversor desliga em dias quentes).
- Conectores de marcas diferentes (maus contactos, aquecimento, incêndios).
- Sombreamentos (chaminés, árvores, antenas) sem avaliação: uma sombra num módulo pode reduzir toda a string (usar otimizadores/micro-inversores nesses casos).
- Cabos DC mal dimensionados ou expostos a sol e calor sem as proteções adequadas.
- Dimensionar só pela potência sem olhar para o perfil de consumo (excedentes injetados valem muito menos do que a energia que se deixa de comprar).
- Prometer ao cliente produção/poupança sem simulação (PVGIS) e sem condições tarifárias atuais.

## 8. Exercícios (com resultados)
1. Consumo 3 500 kWh/ano, produtividade 1 450 kWh/kWp: P_pico? **R: ≈ 2,4 kWp → 6 módulos de 400 W = 2,4 kWp.**
2. String com 10 módulos, Voc = 40 V (a −10 °C: 43,5 V): Voc máx da string? **R: 435 V; confirmar se < Vmáx do inversor.**
3. Inversor de 5 kW monofásico: corrente AC? **R: 5 000/230 = 21,7 A → disjuntor C25 e cabo conforme cálculo.**
4. Isc = 11,5 A: corrente de dimensionamento do cabo? **R: 1,25·11,5 = 14,4 A.**

## 9. Fontes externas sugeridas
- **PVGIS** (re.jrc.ec.europa.eu/pvg_tools): simulação gratuita de produção.
- DGEG e portal de autoconsumo, e-Redes: regimes, formulários e requisitos de ligação.
- Guias de instalação gratuitos de fabricantes de inversores (SMA, Fronius, Huawei, Sungrow, SolarEdge).
- RTIEBT (secção de instalações fotovoltaicas, IEC 60364-7-712) e IEC 62446-1 (paga): usar guias de fabricante como material público.
- PDF do referencial da UC (ANQEP).
