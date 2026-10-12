# UC01793 - Elaborar documentação relativa a ligações à rede de distribuição em BT e MT

> Material de estudo (método + modelos). **Não é fonte normativa.** Os **procedimentos, formulários, prazos, nomes de documentos, limiares de potência e regimes (comunicação prévia, certificação, inspeção, certificado de exploração)** são definidos pela legislação e pelo operador da rede de distribuição (e-Redes) e **mudam**: **confirmar nos sites oficiais** (DGEG, e-Redes, ERSE) e nos formulários em vigor antes de preparar um processo. Os modelos abaixo servem para perceberes a estrutura e a lógica; **não são formulários oficiais**.

## 1. Níveis de tensão e tipos de ligação (referência)
- **BTN (baixa tensão normal):** habitualmente instalações com **potência até 41,4 kVA** (trifásico) (confirmar).
- **BTE (baixa tensão especial):** **acima de 41,4 kVA**, em BT (confirmar).
- **MT (média tensão):** instalações de maior potência, com **posto de transformação (PT) de serviço particular** do cliente, ou ligadas a PT do operador, conforme o caso.
- **Ligações de produção (autoconsumo, UPAC):** têm requisitos próprios de **registo/comunicação/licenciamento** e de **ligação** (UC01799, UC01788).
- **Cada tipo implica documentação diferente**; a potência a requisitar e o tipo de ligação definem o que é exigido.

## 2. Visão geral do processo de ligação (genérica)
1. **Definir as necessidades:** tipo de instalação (habitação, comércio, indústria, produção), potência, tensão, fases.
2. **Projeto ou ficha técnica** (conforme exigência legal): memória descritiva, cálculos, esquemas, termos de responsabilidade.
3. **Requisição de ligação/alteração de potência** ao operador (por intermédio do comercializador ou diretamente, conforme o caso).
4. **Estudo e orçamento do operador:** ponto de ligação, ramal, equipamentos, **encargos de ligação** e prazos.
5. **Aceitação e pagamento**, execução do **ramal** e da **ligação** pelo operador.
6. **Execução da instalação de utilização** (pelo instalador habilitado).
7. **Ensaios, certificação ou inspeção** (consoante a potência e o tipo) e **comunicação/licença de exploração** (quando aplicável).
8. **Contagem e ativação** (contador instalado e ligado pelo operador, UC01788).
- **Atenção:** as fases, os documentos e os prazos variam por **tipo de instalação** e por **potência**; **consultar sempre o enquadramento atual**.

## 3. Documentos habituais (checklist)
### a) Identificação e enquadramento
- Identificação do **requerente** (nome/denominação, NIF, contactos) e do **local** (morada, artigo matricial, coordenadas).
- **Planta de localização** (escala adequada) e **planta de implantação**.
- **Autorização do proprietário/condomínio** (quando necessária).
- **Potência pretendida, tensão, nº de fases, tipo de uso, tarifa/ciclo**.

### b) Projeto técnico (quando exigido) ou ficha técnica simplificada
- **Memória descritiva e justificativa:** descrição da instalação, regimes de neutro, soluções adotadas, conformidade com a regulamentação.
- **Quadro de cargas** e **cálculo da potência**: instalada, de cálculo (com simultaneidade) e a requisitar.
- **Cálculos justificativos:** dimensionamento de condutores, proteções, queda de tensão, curto-circuito (Icc e poder de corte), selectividade, **terras** (UC01781, UC01782).
- **Esquema unifilar** completo (aparelhagem, calibres, secções, poder de corte, diferenciais).
- **Plantas** (pontos de luz, tomadas, quadros, caminhos de cabos), **esquema de terras**.
- **Medições e orçamento** (se aplicável).
- **Termo de responsabilidade do projetista** e do **técnico responsável pela execução**.

### c) Ensaios, certificação e exploração
- **Protocolo/ficha de ensaios e verificação:** continuidade, isolamento, terra, diferenciais, polaridade, etc. (UC04673, UC01792).
- **Certificação ou inspeção por entidade reconhecida** (conforme o regime aplicável).
- **Declaração/certificado de conformidade** e, nos casos aplicáveis, **licença/certificado de exploração**.
- **Plantas "como construído"** e **manuais** (quadros, equipamentos) entregues ao cliente.

### d) Para MT e PT de serviço particular (adicional)
- **Projeto de PT** (cabina, celas, transformador, terras, ventilação, contagem), com **cálculos de Icc**, seleção de **proteções (fusíveis/relés)**, **terras de proteção e de serviço**, **tensões de passo e de toque**.
- **Termos de responsabilidade** específicos para MT e **técnico responsável pela exploração**.
- **Aprovação do projeto** (quando exigida) e **vistorias/ensaios** antes da entrada em serviço.
- **Esquemas unifilares MT e BT**, **regulações das proteções**, **plano de manutenção** (UC04679, UC01792).

### e) Para instalações de produção (autoconsumo)
- **Ficha técnica da UPAC**, **datasheets** de módulos e inversores, **certificados** (por exemplo, conformidade com a norma de ligação à rede), **esquema unifilar** com proteção de interligação, **registo/comunicação** na plataforma oficial.

## 4. Exemplo: quadro de cargas e potência a requisitar (pequeno estabelecimento)
| Grupo de cargas | Potência instalada (kW) | Fator de simultaneidade (ilustrativo) | Potência de cálculo (kW) |
|---|---|---|---|
| Iluminação | 3,0 | 0,9 | 2,70 |
| Tomadas | 4,0 | 0,4 | 1,60 |
| AVAC | 6,0 | 0,8 | 4,80 |
| Equipamentos de cozinha | 8,0 | 0,6 | 4,80 |
| Outros | 2,0 | 0,5 | 1,00 |
| **Total** | **23,0** | | **14,9** |
- **Potência aparente:** S = 14,9/0,9 (cos φ médio) = **16,6 kVA**.
- **Potência normalizada a requisitar:** **17,25 kVA trifásico** (próxima potência normalizada ≥ 16,6 kVA).
- **Corrente do disjuntor de entrada:** I = 17 250/(√3·400) = **24,9 A → 25 A** (UC04673).
- **Verificar:** poder de corte ≥ Icc no ponto de ligação (**informação a pedir ao operador**), seletividade, queda de tensão do ramal, secção do ramal (do operador) e da instalação de utilização.
- **Os fatores de simultaneidade do exemplo são ilustrativos**: usar os que a regulamentação, o projeto ou a experiência justificarem e **explicar o critério** na memória.

## 5. Memória descritiva e justificativa: estrutura recomendada
1. **Objeto e âmbito.**
2. **Enquadramento regulamentar** (diplomas e normas aplicáveis, com data/versão).
3. **Descrição do local e da instalação** (área, uso, regime de neutro/terra).
4. **Alimentação e ligação à rede:** tensão, potência, ponto de ligação, ramal.
5. **Quadros e circuitos:** divisão, proteções, diferenciais.
6. **Cabos e canalizações:** tipos, métodos de instalação.
7. **Terras e equipotencialidade.**
8. **Proteção contra sobretensões e descargas atmosféricas** (UC01782).
9. **Iluminação e emergência** (UC04672, UC04674) e outros sistemas (AVAC, FV, VE, ITED).
10. **Cálculos justificativos** (resumo e anexos).
11. **Ensaios previstos.**
12. **Manutenção e exploração** (instruções ao utilizador).
13. **Anexos:** quadro de cargas, esquemas, datasheets.

## 6. Esquema unifilar: o que deve conter
- **Origem** (ligação à rede/contador/PT) e **tensão**.
- **Aparelhagem de corte e proteção** com **calibre, curva, poder de corte e tipo de diferencial** (por exemplo, "C16, 6 kA; DDR 30 mA tipo A").
- **Cabos:** tipo, número de condutores, secção e comprimento aproximado (por exemplo, "H07V-K 3G2,5 mm²").
- **Circuitos** identificados por **designação** e **função** (UC03077).
- **Terras:** condutor de terra, barra principal, equipotencial.
- **Legenda de símbolos, data, revisão e autor.**

## 7. Boas práticas de documentação
- **Coerência:** potências, calibres e secções iguais na memória, no esquema, nas plantas e na ficha de ensaios.
- **Rastreabilidade:** versões, datas, quem assinou, **cópias entregues**.
- **Clareza:** linguagem técnica precisa, tabelas, esquemas legíveis.
- **Atualização:** no fim da obra, **plantas "como construído"** e esquemas finais.
- **Arquivo:** guardar processo completo (**contratos, comunicações, certificados, relatórios**) por **prazo legal** de retenção (confirmar).
- **Protocolo de dados pessoais (RGPD):** dados de clientes tratados com cuidado; **não** partilhar além do necessário.
- **Direitos de autor:** projetos e esquemas são trabalhos intelectuais; **não** copiar projetos de terceiros.

## 8. Erros comuns
- **Requisitar potência** sem quadro de cargas nem critério.
- **Documentos incoerentes** entre si (calibres, potências, secções).
- **Faltar o termo de responsabilidade**, certificado ou ensaio exigido, o que atrasa a ligação.
- **Usar formulários ou versões desatualizados.**
- **Não pedir ao operador** a **Icc no ponto de ligação** (essencial para escolher o poder de corte).
- **Ignorar prazos** de resposta e de validade de orçamentos do operador.
- **Não guardar o processo** nem entregar a documentação ao cliente.
- **Assinar termos de responsabilidade sem estar habilitado** ou sem ter executado/verificado o trabalho.

## 9. Exercícios (com resultados)
1. Potência instalada de 12 kW, simultaneidade média de 0,6, cos φ = 0,9: potência aparente de cálculo e potência normalizada a requisitar (monofásico)? **R: 12·0,6 = 7,2 kW; S = 8,0 kVA; potência normalizada 10,35 kVA (a seguinte ≥ 8,0 kVA; 6,9 kVA não chega).**
2. Corrente do disjuntor de entrada para 13,8 kVA monofásico? **R: 60 A.**
3. Corrente do disjuntor de entrada para 27,6 kVA trifásico? **R: 27 600/(√3·400) = 39,8 A → 40 A.**
4. Porque se pede ao operador a Icc no ponto de ligação? **R: para escolher o poder de corte da aparelhagem e verificar a proteção/selectividade.**
5. Que documentos mostram coerência na obra? **R: quadro de cargas, esquema unifilar, memória, plantas, ficha de ensaios: todos com os mesmos calibres, secções e potências.**

## 10. Fontes externas sugeridas
- **e-Redes:** requisitos de ligação à rede (BT, BTE, MT), formulários, prazos, normas técnicas de ramais e contagem.
- **DGEG:** regime das instalações elétricas de serviço particular (projeto, certificação, inspeção, exploração, responsáveis técnicos), autoconsumo.
- **ERSE:** regras de tarifas, potência contratada e ligações.
- Guias de projeto de fabricantes e modelos de memória descritiva disponibilizados por associações do setor (como material de apoio, não oficial).
- PDF do referencial da UC (ANQEP).
