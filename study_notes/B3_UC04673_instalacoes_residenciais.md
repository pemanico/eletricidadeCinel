# UC04673 - Executar projetos e instalações elétricas residenciais

> Material de estudo (explicação + exemplos). **Não é fonte normativa.** Números mínimos de pontos, alturas, volumes de casa de banho e regras de licenciamento variam com a versão em vigor do RTIEBT e da regulamentação nacional: **confirmar antes de aplicar em obra**. As tabelas deste ficheiro são "prática corrente" ou ilustrativas, não texto regulamentar.

## 1. Enquadramento (o que tens de confirmar primeiro)
- **Quem pode fazer o quê:** a execução de instalações elétricas de serviço particular em Portugal tem regime jurídico próprio (Decreto-Lei n.º 96/2017 e legislação associada; DGEG). Exige-se qualificação/inscrição adequada do responsável pela execução, e as instalações têm de cumprir regras de projeto, inspeção e certificação consoante a potência. **Não assumas que o certificado do curso, por si só, permite faturar**: confirma na DGEG e na ordem profissional aplicável.
- **Documentos típicos de obra:** projeto (quando exigido), termo de responsabilidade, esquemas, ficha de verificação/ensaios, certificação da instalação.

## 2. Potência contratada e disjuntor geral
Potências normalizadas de ligação à rede (BT):
- **Monofásicas (kVA):** 1,15; 2,3; 3,45; 4,6; 5,75; 6,9; 10,35; 13,8; 17,25; 20,7.
- **Trifásicas (kVA):** 10,35; 13,8; 17,25; 20,7; 27,6; 34,5; 41,4.

**Calibre do disjuntor de entrada** (corrente correspondente à potência):
- Monofásico (230 V): I = S/230 → 3,45 kVA = 15 A; 4,6 kVA = 20 A; 6,9 kVA = 30 A; 10,35 kVA = 45 A; 13,8 kVA = 60 A; 17,25 kVA = 75 A; 20,7 kVA = 90 A.
- Trifásico (400 V): I = S/(√3·400) → 10,35 kVA = 15 A; 13,8 kVA = 20 A; 17,25 kVA = 25 A; 20,7 kVA = 30 A; 27,6 kVA = 40 A; 34,5 kVA = 50 A; 41,4 kVA = 60 A.
- Escolher a potência a contratar é uma decisão técnico-comercial (simultaneidade e uso real), não a soma das potências instaladas.
- **Trifásico em casa:** compensa quando há cargas trifásicas (bombas de calor, carregador VE de 11 kW, aquecimento) ou potência > 20,7 kVA; permite repartir cargas pelas fases (equilíbrio).

## 3. Divisão em circuitos (prática corrente)
Separar por tipo de uso, para seletividade e para limitar o efeito de uma avaria:

| Circuito | Proteção típica | Cabo Cu (ref.) | Observações |
|---|---|---|---|
| Iluminação | C10 (ou B10) | 1,5 mm² | divide-se por pisos/zonas |
| Tomadas uso geral | C16 | 2,5 mm² | divide por zonas; diferencial 30 mA |
| Placa/forno | C32 | 6 mm² (ref.) | verificar queda de tensão e agrupamento |
| Máquinas de lavar (roupa/loiça) | C16 | 2,5 mm² | circuito dedicado |
| Termoacumulador | C20 | 4 a 6 mm² | verificar agrupamento (ver UC01781) |
| Ar condicionado/bomba calor | conforme fabricante | conforme cálculo | curva D se arranque forte |
| Tomada VE (ver UC04676) | conforme equipamento | conforme cálculo | circuito dedicado, DDR tipo A/B conforme carregador |

**A tabela é um ponto de partida**: o cabo final resulta do cálculo com Iz, agrupamento e queda de tensão (UC01781). Por exemplo, um termoacumulador de 4,6 kW (20 A) em tubo agrupado com outros circuitos pode pedir 6 mm² e não 4 mm².

## 4. Quadro elétrico de habitação
- **Ordem típica (do geral para os circuitos):** disjuntor de entrada (da potência contratada) → interruptor/diferencial geral e/ou diferenciais por grupos → disjuntores de circuito.
- **Diferencial 30 mA** em todos os circuitos de tomadas e nas zonas de risco; **repartir os circuitos por vários diferenciais** para que um disparo não deixe a casa toda sem luz.
- **Tipo do diferencial:** AC para cargas lineares; **A** quando há cargas eletrónicas, eletrodomésticos com eletrónica, tomadas VE; **F** ou **B** para variadores e certos inversores (seguir as indicações do fabricante).
- **Reserva no quadro:** deixar espaço livre para circuitos futuros (prática corrente: ~20 a 25%).
- **IP e acessibilidade:** quadro em local acessível, identificado (etiquetas por circuito), com tampa protegida.
- **Limitador de sobretensão (SPD):** frequentemente recomendado/obrigatório conforme o caso: ver UC01782.

## 5. Pontos de utilização
- O RTIEBT/guia técnico define números mínimos de pontos de luz e tomadas por divisão (sala, quarto, cozinha...). **Consultar a versão em vigor**: não os reproduzo de memória.
- **Prática corrente de alturas (confirmar regras de acessibilidade e RTIEBT):** interruptores ≈ 1,10 m; tomadas gerais ≈ 0,30 a 0,40 m do solo; tomadas de bancada de cozinha ≈ 1,00 a 1,10 m.
- **Cozinha:** pontos para placa, forno, exaustor, frigorífico, máquinas dedicadas; evitar tomadas por cima da placa/lava-loiça.
- **Exterior:** tomadas e luminárias com IP adequado (≥ IP44, conforme a zona), diferencial 30 mA, cabos próprios para exterior.

## 6. Casas de banho: volumes de proteção
Os volumes 0, 1, 2 (e fora de volume) definem que aparelhagem pode ser instalada. Esquema de referência (confirmar medidas e regras na versão em vigor):
- **Volume 0:** interior da banheira/base de duche. Apenas equipamento adequado, muito baixa tensão de segurança (SELV 12 V) e IPX7.
- **Volume 1:** acima da banheira/duche até 2,25 m. Apenas aparelhos fixos próprios (termoacumuladores, etc.), IPX4 ou superior (IPX5 se houver jatos).
- **Volume 2:** faixa em torno (≈ 0,60 m) e zona do lavatório. Luminárias e aparelhos IPX4, tomadas apenas fora dos volumes 0 a 2 (regra geral).
- **Ligação equipotencial suplementar:** todas as massas e partes condutoras estranhas ligam-se ao PE (secção mínima conforme regulamento).
- **DDR 30 mA** sempre.

## 7. Esquemas de comando de iluminação (descritos em texto)
- **Interruptor simples:** corta a fase para a lâmpada.
- **Comutador (vaivém), 2 pontos:** dois comutadores ligados por dois retornos; a lâmpada acende/apaga em qualquer um.
- **Inversor (cruzamento), 3 ou mais pontos:** um ou mais inversores entre dois comutadores.
- **Telerruptor:** comando com botões de pressão para muitos pontos (corredores, escadas), uma bobina comuta o contacto.
- **Minuteria:** acende por tempo (escadas), ligada a botões.
- **Sensores/detetores de presença:** corredores, garagens, casas de banho; atenção à carga mínima e máxima suportada.
- Fase sempre cortada no interruptor, nunca o neutro. Neutro e PE disponíveis na caixa de aparelhagem nos locais novos (para sensores e domótica futura).

## 8. Exemplo de montagem do quadro (T3 com termoacumulador e placa)
Entrada monofásica 10,35 kVA → disjuntor de 45 A.
- Diferencial 1 (30 mA, A, 40 A): iluminação 1 (C10), iluminação 2 (C10), tomadas 1 (C16), tomadas 2 (C16).
- Diferencial 2 (30 mA, A, 40 A): cozinha (placa C32), forno (C16), máquina de lavar roupa (C16), máquina de loiça (C16).
- Diferencial 3 (30 mA, A, 25 A): termoacumulador (C20), tomada exterior (C16), reserva.
- Verificar: soma das correntes nominais não tem de ser ≤ 45 A (simultaneidade), mas **cada diferencial tem de ser protegido a montante** e o calibre do diferencial ≥ calibre do disjuntor que o protege (coordenação).
- Seletividade entre geral e circuitos: calibres bem separados e/ou tabelas do fabricante.

## 9. Ensaios a efetuar antes de entregar a obra
- Continuidade dos condutores de proteção e equipotencialidade.
- Resistência de isolamento (500 V DC, mínimo de referência 1 MΩ).
- Resistência de terra (esquema TT) e diferenciais (disparo e tempo).
- Polaridade (fase no interruptor, neutro correto), funcionamento de todos os pontos.
- Registar na ficha de verificação, com número e calibração do instrumento.

## 10. Erros comuns
- Um único diferencial para a casa toda (um defeito para tudo).
- Diferencial AC onde há cargas com eletrónica (disparo/cegueira): usar tipo A (ou superior).
- Cabo dimensionado "pela tabela do quadro" sem calcular agrupamento e queda de tensão.
- Casa de banho: aparelhagem sem IP adequado no volume correspondente.
- Esquecer neutro e PE na caixa do interruptor.
- Não deixar reserva no quadro e não identificar os circuitos.

## 11. Exercícios (com resultados)
1. Contrato monofásico de 6,9 kVA: calibre do disjuntor de entrada? **R: 30 A.**
2. Contrato trifásico de 17,25 kVA: calibre? **R: 25 A.**
3. Circuito de 3,68 kW (16 A) com 2,5 mm² em B1, 30 °C, sem agrupamento: cumpre aquecimento? **R: sim (21 A); falta verificar queda de tensão e Icc mínima.**
4. Termoacumulador 4,6 kW agrupado com mais 4 circuitos, 35 °C: secção? **R: k = 0,94·0,60 = 0,564; I'z ≥ 20/0,564 = 35,5 A → 6 mm² (36 A, referência).**

## 12. Fontes externas sugeridas
- RTIEBT (DGEG): partes sobre instalações de utilização e locais com banheira/duche.
- DGEG: regime jurídico das instalações elétricas de serviço particular, qualificação de instaladores, inspeções.
- Guias de projeto gratuitos de fabricantes (Legrand, Schneider, Hager, ABB).
- PDF do referencial da UC (ANQEP).
