# UC00676 - Implementar as normas de segurança e saúde no trabalho no setor da eletricidade e eletrónica

> Material de estudo (explicação). **Não é fonte normativa.** Os valores abaixo (correntes e tempos de risco, distâncias, requisitos de EPI) são ordens de grandeza de referência. A regulamentação aplicável (segurança e saúde no trabalho, regras de trabalho em instalações elétricas, procedimentos do empregador e do operador de rede) tem de ser consultada e cumprida: **confirmar nos documentos oficiais**.

## 1. Enquadramento
- **Lei-quadro em Portugal:** regime jurídico da promoção da segurança e saúde no trabalho (Lei n.º 102/2009 e alterações), com obrigações do empregador (avaliação de riscos, formação, vigilância da saúde, equipamentos de proteção) e dos trabalhadores (cumprir regras e usar EPI).
- **Regras específicas para trabalhos em instalações elétricas:** norma europeia **EN 50110-1** (exploração de instalações elétricas) e regulamentos aplicáveis, com procedimentos de **corte, bloqueio, verificação de ausência de tensão e colocação à terra**.
- **Qualificação do pessoal:** classificação de pessoas (comum, instruída, qualificada: classificações BA em instalações) conforme a regulamentação: **só pessoal qualificado e autorizado** executa trabalhos elétricos.
- **Empreitadas/obras:** plano de segurança e saúde, coordenação de segurança, sinalização de estaleiro; no caso de várias empresas, regras de coordenação.

## 2. Efeitos da corrente elétrica no corpo (referência IEC/TS 60479-1)
Os efeitos dependem da **corrente**, do **tempo de passagem**, do **trajeto** (mão-mão, mão-pé atravessa o coração) e da **frequência**. Ordens de grandeza para 50 Hz:
- **~0,5 a 1 mA:** limiar de percepção.
- **~10 mA:** contrações musculares; risco de não conseguir largar o condutor ("let-go").
- **> ~30 mA** durante tempo prolongado: dificuldades respiratórias e risco de **fibrilhação ventricular** (por isso os diferenciais de 30 mA).
- **Centenas de mA a vários A:** paragem cardíaca, queimaduras graves.
- **Tensão de contacto limite convencional: 50 V CA** (25 V em locais húmidos ou agrícolas, conforme regulamentação) e **120 V DC sem ondulação**.
- A **resistência do corpo** varia muito (pele seca vs húmida): a mesma tensão pode ser inofensiva ou mortal.
- **Arco elétrico:** além do choque, queimaduras graves por radiação, projeção de metal fundido e onda de pressão, mesmo sem contacto direto.

## 3. As 5 regras de ouro (corte para trabalhos sem tensão)
1. **Seccionar completamente** (cortar todas as fontes possíveis de alimentação, incluindo retornos e geradores).
2. **Impedir qualquer religação** (bloqueio com cadeado, etiqueta de segurança, bloqueio mecânico).
3. **Verificar a ausência de tensão** com instrumento adequado, testando-o antes e depois ("test before touch"; usar detetor bipolar/medidor categoria adequada).
4. **Colocar à terra e em curto-circuito** (quando aplicável, por exemplo, em MT/AT ou onde possa haver retorno de tensão).
5. **Proteger contra elementos em tensão na vizinhança** e **sinalizar a zona de trabalho**.
- **Reposição em serviço:** só depois de verificar que ninguém trabalha, retirar bloqueios (por quem os colocou), repor sinalização e avisar os envolvidos.
- **Procedimento LOTO (lockout/tagout):** cada pessoa que trabalha coloca o seu cadeado; o equipamento só é religado quando **todos** os cadeados forem retirados.

## 4. Trabalhos sob tensão e na vizinhança de tensão
- **Trabalhos sob tensão (TST):** em BT, só por pessoal especificamente formado, com procedimentos aprovados, ferramentas isoladas e EPI. Em regra, **evitar**: preferir trabalhar sem tensão.
- **Distâncias de segurança** a partes em tensão (zonas de perigo e de vizinhança): dependem da tensão nominal; consultar tabelas oficiais.
- **Ferramentas isoladas (VDE/1000 V)** certificadas e inspecionadas; **instrumentos de medida** com categoria CAT III/IV adequada ao ponto da instalação, pontas de prova em bom estado e fusíveis corretos.
- **Instalações com condensadores** (UPS, variadores, baterias de condensadores): **descarregar** e esperar o tempo indicado pelo fabricante antes de intervir.
- **Baterias e fotovoltaico:** tensão DC mesmo com a rede desligada (módulos produzem com luz); procedimentos próprios.

## 5. EPI (equipamento de proteção individual)
- **Cabeça:** capacete dielétrico com viseira para arco quando aplicável.
- **Olhos/rosto:** óculos e viseiras de proteção (também contra projeções e radiação de arco).
- **Mãos:** luvas isolantes com classe de tensão adequada, ensaiadas periodicamente, usadas com sobreluvas de proteção mecânica; inspecionar antes de cada uso.
- **Corpo:** vestuário de proteção contra arco elétrico (classificado) quando exigido; **calçado isolante** e antiestático conforme o local.
- **Altura:** arnês, linha de vida, ancoragens.
- **Ruído/poeiras:** proteção auditiva e máscara, conforme a tarefa.
- **Manutenção do EPI:** guardar, inspecionar, testar periodicamente; **substituir** o que está danificado. EPI não substitui o corte e o bloqueio.

## 6. Avaliação de riscos (método simples)
**Risco = Probabilidade x Gravidade.** Exemplo de matriz 3x3:
| | Gravidade baixa | Média | Alta |
|---|---|---|---|
| **Probabilidade alta** | médio | alto | muito alto |
| **média** | baixo | médio | alto |
| **baixa** | baixo | baixo | médio |
**Hierarquia de medidas:** eliminar o perigo → substituir → proteções coletivas → procedimentos/formação → EPI (último recurso).
**Exemplo (substituição de quadro de habitação):** perigo = tensão no quadro. Medida = corte no disjuntor geral, bloqueio, verificação de ausência de tensão, aviso aos ocupantes; cuidado com a **entrada do contador, que pode ficar em tensão a montante** (só o operador pode intervir nessa parte).

## 7. Trabalhos em altura, espaços confinados e outras áreas
- **Altura:** acessos seguros (andaimes, plataformas, escadas fixas e seguras); a regulamentação aplica requisitos a partir de determinadas alturas (referência corrente: cerca de 2 m, confirmar). Nunca trabalhar em tensão em altura.
- **Escadas portáteis:** apoio estável, ângulo adequado (cerca de 75°), ferramenta isolada, não usar escadas condutoras perto de partes em tensão.
- **Espaços confinados** (caixas de visita, PT, galerias): avaliar atmosfera (gases, oxigénio), ventilação, vigilância, plano de resgate.
- **Manuseamento de cargas** (cabos, quadros, baterias): técnica correta, ajudas mecânicas, trabalho em equipa.
- **Ruído, poeiras (amianto em obras antigas!), químicos e fumos de soldadura:** identificar, extrair e proteger.
- **Amianto:** em edifícios antigos, cabos e quadros podem ter materiais com amianto. Não perfurar nem partir sem avaliação e sem procedimentos próprios.

## 8. Resposta a emergências e primeiros socorros
**Acidente elétrico:**
1. **Garantir a segurança de quem socorre:** cortar a alimentação ou afastar a vítima com material isolante seco (nunca tocar a vítima enquanto ela estiver em contacto com a tensão).
2. **Ligar 112.**
3. **Avaliar** consciência e respiração.
4. **Sem respiração normal:** iniciar **suporte básico de vida (SBV)**: compressões torácicas de **30:2** (30 compressões, 2 ventilações), ritmo **100 a 120/min**, profundidade **5 a 6 cm**; usar **DAE** (desfibrilhador) assim que disponível.
5. **Queimaduras:** arrefecer com água corrente (queimaduras térmicas), cobrir com penso limpo, não furar bolhas. Mesmo que pareça "bem", **encaminhar sempre para avaliação médica** (efeitos cardíacos podem aparecer mais tarde).
**Incêndio em instalação elétrica:**
- **Cortar a alimentação** se possível e seguro.
- **Extintor de CO₂ ou de pó** para fogos em equipamento elétrico; **nunca água** em equipamento sob tensão.
- Dar o alerta, evacuar, ligar 112.
**Acidentes e incidentes:** comunicar, registar, investigar causas e atualizar a avaliação de riscos.

## 9. Sinalização de segurança
- **Cores e formas:** proibição (círculo vermelho), obrigação (círculo azul), aviso (triângulo amarelo), emergência/salvamento (verde), equipamento de combate a incêndio (vermelho).
- **Sinais elétricos típicos:** "Perigo: eletricidade", "Proibido religar", "Trabalhos em curso", sinais de EPI obrigatório.
- A **prescrição mínima de sinalização** está definida em regulamentação nacional: consultar.

## 10. Cultura de segurança
- **Planear o trabalho:** objetivo, riscos, passos, material, comunicação, plano de emergência.
- **Briefing** antes de cada intervenção e **pausa de segurança** se algo mudar.
- **Autoridade para parar o trabalho** quando algo parece inseguro.
- **Nunca trabalhar sozinho** em tarefas de risco elevado sem procedimento de vigilância.
- **Pressão do cliente ou do prazo não justifica saltar o procedimento**: a causa mais comum de acidentes graves é "só vai demorar um minuto".

## 11. Erros comuns
- Confiar no esquema ou no disjuntor sem **verificar a ausência de tensão** no ponto de trabalho.
- Esquecer que o **neutro** e o **PE** também podem estar em tensão (retornos, cargas ligadas).
- Cortar só o diferencial/disjuntor do circuito, sem identificar todos os circuitos do quadro e a entrada.
- Bloquear sem etiquetar e sem avisar.
- Usar instrumento de medida sem categoria adequada, ou com pontas deterioradas.
- Subestimar o **arco elétrico** em quadros com correntes de curto-circuito elevadas.
- Trabalhar com luvas ou ferramentas fora do prazo de ensaio.
- Não ter plano de emergência nem kit de primeiros socorros.

## 12. Exercícios (com resultados)
1. Quais são as 5 regras de ouro por ordem? **R: seccionar; impedir religação; verificar ausência de tensão; terra e curto-circuito; proteger vizinhança e sinalizar.**
2. Porque se testa o instrumento antes e depois de verificar ausência de tensão? **R: para garantir que o instrumento funciona e que "tensão zero" não foi uma leitura falsa.**
3. Qual é o ritmo e profundidade das compressões no SBV? **R: 100 a 120/min, 5 a 6 cm, com 30 compressões para 2 ventilações.**
4. Pode usar-se água num fogo de um quadro elétrico em tensão? **R: não; usar CO₂ ou pó e cortar a alimentação quando possível.**
5. Por que 30 mA nos diferenciais? **R: valor a partir do qual há risco de fibrilhação ventricular em exposição prolongada.**

## 13. Fontes externas sugeridas
- **ACT (Autoridade para as Condições do Trabalho):** legislação, guias e publicações sobre segurança e saúde no trabalho.
- **DGEG:** regulamentação sobre instalações elétricas e trabalhos em instalações.
- **EDP/e-Redes:** manuais e procedimentos de segurança em trabalhos junto da rede.
- Guias gratuitos de segurança elétrica de fabricantes e entidades europeias (EU-OSHA); EN 50110-1 (paga): usar guias públicos como material de apoio.
- Documento de avaliação de riscos e procedimentos da tua entidade formadora ou empregadora.
- PDF do referencial da UC (ANQEP).
