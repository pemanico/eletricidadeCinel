# Dúvidas abertas (resolver e mover para DECISOES)
## Legal / negócio (as mais importantes)
- [ ] Carteira de técnico: quem emite (DGEG? e-Redes não emite), requisitos além do curso (exame? experiência?), custo, prazo. O folheto do CINEL diz "preparação para requerer"; NÃO é automático.
- [ ] A carteira permite ASSINAR PROJETOS ou só executar/explorar? Limites de potência e tipo de instalação? (confirmar na DGEG e por escrito no CINEL)
- [ ] Exame "para assinar projetos": data (só no fim em jul-2028 ou intermédia?), entidade, âmbito.
- [ ] Seguro de responsabilidade civil e enquadramento da atividade (abertura de atividade, faturação) antes do primeiro cliente.
- [ ] Cláusula de exclusividade no contrato de trabalho atual (atividade paralela).
- [ ] RGPD: guardar dados de clientes e preços de fornecedores (repo é privado, mas isso não basta).
## Técnico
- [ ] Ordep: pôr o Manual ITED (ANACOM, edição em vigor) em `sources/normativas/` para confirmar tomadas RJ45/TV por divisão (quartos e outras) e dimensionar ATI/tubagem. Sala+cozinha em open space: como contar?
- [ ] Icc no ponto de ligação (e-Redes) e resistência de terra medida: campos `supply.icc_ka` e `supply.r_terra_ohm`.
- [ ] Coeficientes de simultaneidade: confirmar com formador/UC04673 o que o CINEL usa (a convenção v1 é minha).
- [ ] Obter o texto/imagens das tabelas do RTIEBT 2006/2015 (DR original ou DGEG): secções mínimas 801.5.8, Quadros 52-C, 52-D, 52-E, 52H. Até lá, valores da edição de 2000, POR CONFIRMAR.
- [ ] Fonte para nº de tomadas/pontos de luz por divisão. Pesquisa 2026-10-12: RTIEBT não o diz; nenhum documento normativo português encontrado (só blogs/imobiliárias). Perguntar ao formador da UC04673 / CINEL que referência usam. Entretanto: perfil de dotação editável, rotulado 'convenção, não normativa'. ITED tem mínimos próprios (ANACOM: 2 RJ45 + 1 TV na sala e na cozinha, a confirmar no Manual ITED).
- [ ] Confirmar o Ordep a lista de regras em `docs/REGRAS_HABITACAO_RTIEBT.md` antes de codificar.
- [ ] Ordep carregou no NotebookLM: Portaria 949-A/2006 consolidada (DR) e "RTIEBT anotada" (slideshare, ~dez/2013, comentário de terceiros, pode estar desatualizada). Falta pô-los em `sources/normativas/` (ou anexar no chat) para eu extrair regras com artigo citado.
- [ ] Confirmar data da consolidação e alterações posteriores (ex.: Portaria 252/2015 apareceu nas pesquisas; ver relação).
- [ ] Comprimentos de cabo e métodos de instalação: serão ESTIMADOS a partir da planta (distância quadro→ponto); definir margem e permitir override.
- [ ] Ordep aceita regras A VALIDAR visíveis em todas as saídas até serem confirmadas? (D12)
- [ ] Icc no ponto de ligação (e-Redes), resistividade do solo, método de instalação e temperatura: dados reais vs valores por defeito.
- [ ] Calendário real do CINEL (ordem das UC).
- [ ] Programa de CAD que o Ordep vai usar (DXF aberto em QCAD/LibreCAD/AutoCAD?).
- [ ] Validar tabelas de cabos (IZ B1 PVC 2 condutores) na norma/RTIEBT.
- [ ] Tabela de preços real de fornecedores para o motor de orçamento.
- [ ] Conteúdo mínimo legal das peças de um projeto (DGEG).
