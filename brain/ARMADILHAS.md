# Armadilhas conhecidas
## Erros de conteúdo já cometidos
- **(2026-10-12, grave)** Fiz uma "correção" errada: 4 mm² B1 = 28 A é IEC 60364-5-52:2009; o RTIEBT (Quadro 52-C1, método B) dá 32 A. Sob RTIEBT o termoacumulador 4,6 kW/25 m/35 °C/3 circuitos fica em 4 mm² (Iz 21,06 A), não 6 mm². As notas de estudo B2 têm errata no topo; as restantes tabelas das notas (IEC 2009) estão por rever. Lição: tabela só do texto normativo, com artigo citado.
- O PDF consolidado do DR não traz o texto das tabelas ("ver documento original", 193 vezes); a anotada é a Edição de 2000.
- (SUPERADO pela entrada acima) a "correção" 4→6 mm² estava errada para o RTIEBT.
- Resistências em paralelo e outros exercícios do bloco 1 foram corrigidos; as notas continuam a ser material de estudo por validar.
## Ambiente (sessão em contentor na nuvem)
- `pip` não chega ao PyPI (sem ezdxf, sem pytest): usar `python run_tests.py` e o escritor DXF próprio.
- `rsync` não existe: usar `cp -r`. Verificar sempre o resultado de uma cópia/commit (`git show --stat`).
- Ficheiros com acentos no nome causam problemas: usar nomes ASCII.
## Processo
- Entregar sempre os ficheiros que peço ao Ordep para abrir (SendUserFile) e guardá-los no repo se forem exemplos; `saida/` está no .gitignore e só existe no contentor.
- Não confiar em texto de marketing do curso para direitos legais (assinar projetos).
- Texto no DXF R12 sai sem acentos (ASCII).
- Cada correção de números: verificar em Python antes de escrever em nota.
- (2026-10-12) Ambiente: sem PyPI (sem ezdxf/FastAPI/pytest). Testes: `python run_tests.py`. Chromium+Playwright existem para verificar UI/SVG. `pkill -f` com parênteses no padrão rebenta; arrancar o servidor em background com porta fixa e matar por `pkill -f <porta>`.
- (2026-10-12) Importar DXF renumera divisões r1..rN: equipamentos/quadro ligados a ids antigos podem ficar na divisão errada. Rever sempre após importar.
- (2026-10-13) **Acentos em DXF do arquiteto (risco, ainda não observado):** `app.js` lê o ficheiro com `File.text()` (sempre UTF-8) e o servidor descodifica UTF-8 com `errors="replace"`. Um DXF em ANSI_1252 perde "ç/ã/á" antes de chegar ao servidor (irrecuperável). Correção provável: enviar bytes e descodificar segundo `$DWGCODEPAGE`. Só mexer depois de ver o DXF real.
- (2026-10-13) Windows: `mimetypes` lê o registo e pode dar `.js` = `text/plain`. No PC do Ordep deu `text/javascript` (OK). Se a página aparecer vazia noutra máquina, é a primeira suspeita.
- (2026-10-13) Os botões "Novo"/"Exemplo T3" usam `prompt()`, que bloqueia o browser automatizado. Para testar, chamar `api("/api/projetos", {slug, exemplo:true}); listar(slug); abrir(slug)` pela consola JS.
- (2026-10-13) Nuvem: um venv novo não chega ao PyPI (nem com o CA do proxy); o `python3` do sistema já tem pydantic 2.13 → correr os testes com ele.
- (2026-10-13) `pkill -f <porta>` mata o próprio shell se a porta aparecer na linha de comando corrente: arrancar o servidor de teste numa porta e NÃO correr pkill no mesmo comando.
- (2026-10-13) pdfplumber é lento em plantas (interpreta toda a geometria só para tirar texto: 26 s para 23 págs.); para o texto de todas as páginas usar pypdfium2 (0,35 s). pdfplumber só na página escolhida.
- (2026-10-13) Verificar a escala pelas cotas do PDF falhou: cadeias de cotas sobrepostas, marcas intermédias não desenhadas como linhas. A escala valida-se pelas ÁREAS contra o quadro do arquiteto.
- (2026-10-13) Bugs meus apanhados pelos testes: traçado de contorno Moore errado (só 4 pixeis), Douglas-Peucker num contorno fechado colapsa (início = fim → linha de comprimento 0), amostragem do lado das portas ao longo da parede em vez de através. Sempre testar funções geométricas com formas conhecidas antes do caso real.
- (2026-10-13) A camada de "vistas" mistura caixilharia com loiças, bancadas e roupeiros: usar só linhas no prolongamento de uma parede (paralelas, dentro da espessura); senão as divisões perdem 10–40% de área.
- (2026-10-13) O PDF "regravado" (Creator=PDFium) perdeu as camadas; o plot direto do AutoCAD (Creator=AutoCAD LT) mantém-nas. Pedir sempre o plot direto.
- (2026-10-14) Testar a UI com um servidor arrancado ANTES de mudar o código dá resultados do código antigo (aconteceu: posições "erradas" eram do processo antigo). Reiniciar o servidor de teste depois de cada alteração em Python.
- (2026-10-14) Playwright considera linhas SVG finas "não visíveis": esperar com wait_for_function (contagem de elementos), não wait_for_selector.
