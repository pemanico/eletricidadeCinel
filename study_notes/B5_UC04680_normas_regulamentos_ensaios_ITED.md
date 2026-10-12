# UC04680 - Implementar normas, regulamentos e ensaios em ITED

> Material de estudo (explicação). **Não é fonte normativa.** O regime ITED/ITUR e o **Manual ITED** são publicados pela **ANACOM** e são revistos periodicamente. Designações, tabelas, limites de atenuação, ocupações de tubagem e requisitos de qualificação dependem da edição em vigor: **confirmar sempre no site da ANACOM**. Onde dou números, são ordens de grandeza ou práticas correntes.

## 1. O que é o ITED
- **ITED** = Infraestruturas de Telecomunicações em Edifícios. **ITUR** = Infraestruturas de Telecomunicações em Urbanizações, Loteamentos e Conjuntos de Edifícios (a parte exterior aos edifícios).
- **Objetivo:** garantir que cada edifício e cada fração tem infraestrutura de telecomunicações (cabos, tubagens, armários, tomadas) que permita aceder a serviços de qualquer operador (telefone, internet, televisão), com **qualidade e neutralidade**.
- **Enquadramento legal:** regime jurídico das infraestruturas de telecomunicações em edifícios (decreto-lei, com alterações) e o **Manual ITED** (especificações técnicas) aprovado pela ANACOM. Confirmar o diploma e a edição do manual em vigor.
- **Edifícios abrangidos:** novos e com obras de alteração significativa; as regras variam consoante o tipo (habitação, comércio, escritórios, edifícios existentes). Confirmar no manual.

## 2. Intervenientes e qualificações (confirmar)
- **Técnico de projeto ITED** e **empresa/entidade instaladora ITED**: têm de estar **inscritos/registados na ANACOM** e cumprir requisitos de formação e habilitações. **Esta é a barreira de entrada principal**: sem registo, não podes assinar projeto nem termo de responsabilidade ITED nem ser a entidade instaladora.
- **Entidade certificadora:** verifica a conformidade e emite o **certificado ITED** nos casos em que a lei o exige (confirmar quais).
- **Promotor/dono de obra:** responsável por encomendar projeto e instalação e por entregar a documentação.
- **Operadores:** podem ligar-se à infraestrutura de forma neutra; a informação do projeto e dos ensaios é entregue ao proprietário/condomínio.
- **Importante:** as UC do curso (UC04680, 04681, 04682, 04685) estão alinhadas com a formação para esta atividade, mas **o certificado do curso, por si só, pode não bastar** para o registo na ANACOM. Verifica os requisitos atuais.

## 3. Documentação ITED
- **Projeto ITED** (quando exigido): memória descritiva, cálculos, peças desenhadas, medições/estimativa orçamental e **termo de responsabilidade** do técnico de projeto.
- **Termo de responsabilidade da instalação**, assinado por técnico habilitado.
- **Ficha de ensaios:** resultados dos ensaios por cabo e por tomada (cobre, coaxial, fibra), com os instrumentos usados.
- **Certificado ITED** (entidade certificadora) e **plantas "como construído"** (as-built).
- **Manual do utilizador** para o proprietário/condomínio (diagramas, armários, contactos).

## 4. Constituição geral de uma ITED (visão)
- **Entrada no edifício:** caixa de entrada e ligação às redes de operadores (exterior).
- **ATE** (armário de telecomunicações de edifício): ponto de distribuição principal do edifício.
- **Rede de cabos e tubagens** verticais (prumadas) e horizontais.
- **ATI** (armário de telecomunicações individual): em cada fração.
- **Tomadas de telecomunicações** nas divisões, ligadas ao ATI por cabos de pares de cobre, coaxial e fibra ótica.
- **Rede de terras e equipotencialidade** dos armários e infraestrutura.
- **Redes:** pares de cobre (voz/dados, Ethernet), cabo coaxial (TV por distribuição de RF), fibra ótica (FTTH), e interligação aos operadores. (Designações e topologias exatas: ver manual.)

## 5. Ensaios (visão geral, com objetivos)
Os ensaios provam que a infraestrutura cumpre o manual. Cada rede tem os seus.

### Pares de cobre (cabos UTP/FTP Cat 6 ou superior)
- **Mapa de fios (wiremap):** continuidade, inversões, curtos, pares trocados.
- **Comprimento** e **atenuação (insertion loss)**.
- **Diafonia** (NEXT/PS-NEXT) e **perda de retorno (return loss)**.
- **Canal/ligação:** o comprimento máximo do canal em Cat 6 é **100 m** (90 m de ligação permanente + 10 m de cordões).
- Instrumento: **certificador de cabos** (Fluke DSX, etc.) com relatório por tomada.

### Cabo coaxial (75 Ω)
- **Continuidade, curto-circuitos, impedância/adaptação**.
- **Atenuação** por lance e níveis de sinal nas tomadas (medidor de campo ou analisador de espectro).
- **Blindagem e ligação à terra** onde aplicável.
- Limites dos níveis de sinal nas tomadas (em dBµV) vêm do manual.

### Fibra ótica
- **Atenuação do canal** com medidor de potência e fonte (OLTS), a 1310 nm e/ou 1550 nm.
- **Reflectometria (OTDR):** localiza eventos (emendas, conectores, curvas), útil para diagnóstico e para trechos longos.
- **Inspeção e limpeza das extremidades dos conectores** (microscópio): sujidade é a maior causa de perdas e reflexões.
- Detalhes na UC04681.

### Terra e equipotencialidade
- **Continuidade** e **resistência** da ligação de terra dos armários e das massas metálicas.
- Equipotencial entre armários, condutas metálicas e a terra de proteção do edifício (UC01782).

## 6. Segurança e boas práticas
- **Separação entre cabos de telecomunicações e cabos de energia:** respeitar as distâncias do manual e da norma de cablagem (evitar paralelismos longos e cruzamentos a 90° quando inevitáveis).
- **Raios de curvatura:** UTP ≥ 4 x diâmetro do cabo; coaxial e fibra, ver datasheet (fibra em cabos: tipicamente ≥ 10 x diâmetro do cabo instalado, ≥ 20 x durante o puxamento).
- **Tensão de puxamento máxima** do cabo (não exceder; usar guias e lubrificantes adequados).
- **Etiquetagem:** cada cabo e tomada identificados nas duas extremidades, e documentados no ATI/ATE.
- **EPI:** óculos para trabalho com fibra (fragmentos), cuidado com laser infravermelho (invisível) e nunca olhar para um conector com fonte ligada.

## 7. Erros comuns
- Fazer o registo ou assinar documentos ITED sem estar inscrito na ANACOM.
- Usar uma edição desatualizada do manual.
- Ensaios apenas "funcionais" (ver se há internet) em vez de ensaios certificados e registados.
- Cabos de telecomunicações encostados a cabos de energia em longos trechos.
- Conectores de fibra sem inspeção e limpeza antes do ensaio.
- Não deixar a documentação e as plantas "como construído" ao proprietário.

## 8. Exercícios
1. Qual o comprimento máximo do canal de cabo de pares Cat 6? **R: 100 m (90 m de permanent link + 10 m de patch cords).**
2. Porque é crítico limpar os conectores de fibra antes do ensaio? **R: a sujidade aumenta a atenuação e a reflexão, mascarando a qualidade real da ligação.**
3. Quem pode assinar o termo de responsabilidade de um projeto ITED? **R: técnico de projeto inscrito na ANACOM (confirmar requisitos atuais).**
4. Porquê separar os cabos de telecomunicações dos de energia? **R: para reduzir interferências eletromagnéticas (ruído, diafonia) e riscos de segurança.**

## 9. Fontes externas sugeridas (as fontes principais)
- **ANACOM:** Manual ITED em vigor, perguntas frequentes, listas de entidades certificadoras e requisitos de registo de técnicos e empresas.
- Guias de ensaios de fabricantes de instrumentos (Fluke Networks, EXFO, VIAVI): procedimentos práticos de certificação e OTDR.
- Guias de cablagem estruturada e de fibra de fabricantes (Corning, CommScope, Prysmian).
- PDF do referencial da UC (ANQEP).
