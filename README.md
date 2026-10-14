# eletro-agents (repo `eletricidadeCinel`)
Software para apoiar o projeto de instalações elétricas de **moradias** (RTIEBT): a partir de uma planta, calcula circuitos, secções, quedas de tensão, quadro e DDR, tomadas ITED, e gera esquema unifilar, planta com circuitos, memória de cálculo e lista de material. Construído módulo a módulo com o curso EFA Técnico/a de Instalações Elétricas (CINEL, 2026-2028).

> **Tudo o que sai daqui é RASCUNHO NÃO ASSINADO.** Enquanto houver linhas `POR_CONFIRMAR`/`AVISO`/`NAO_CUMPRE`, o relatório e a app marcam **"NÃO UTILIZÁVEL COMO PROJETO"**. Assinatura e responsabilidade são de técnico habilitado.

## Princípios
- **Cálculos só em código** (`src/eletro/calc`); nunca por um LLM.
- **Fonte única de verdade:** `Project` (JSON). Desenhos, quadro, material e relatório são vistas geradas; revisões imutáveis, overrides com deteção de conflito, diff entre revisões.
- **Cada regra normativa cita a fonte** (diploma/artigo/norma + versão). O que não é norma (pontos por divisão, simultaneidade, curvas, poder de corte) é **convenção de projeto**, editável e rotulada.
- **Estados por linha de verificação:** `CUMPRE`, `NAO_CUMPRE`, `CONVENCAO`, `POR_CONFIRMAR`, `AVISO`.
- **Dados de PDF/foto entram `confirmed=False`**; nada segue sem confirmação humana.
- A planta de base é o **DXF do arquiteto** (ASCII; DWG não é lido) ou o **PDF do arquiteto** (vetorial, plotado do CAD com camadas): escolhe-se a página/piso, a camada das paredes e a dos caixilhos; as divisões são detetadas a partir das paredes e validadas contra o quadro de áreas do arquiteto (avisos e erros na app). Instalar `pip install -r requirements.txt`.
- **Aparelhagem na planta**: separador "Aparelhagem (planta)" com paleta de símbolos; alturas ao chão preenchidas pela tabela de alturas (`data/convencoes/simbolos_alturas.json`, editável no separador "Tabela de alturas", versionada e com fonte por valor) e verificadas contra RTIEBT 701.71.2 / 801.3.5.5; o cálculo usa a aparelhagem colocada.

## Pipeline
planta (DXF / JSON / PDF / foto) → `Project` → regras + cálculo (`engine.calcular`) → quadro, circuitos, ITED → unifilar, planta+circuitos (SVG/DXF), material, relatório HTML.

## Como correr
```
python run_tests.py                                   # 43 testes (sem dependências externas)
python run_app.py                                     # app web em http://127.0.0.1:8765 (só localhost)
PYTHONPATH=src python -m eletro.cli calc examples/moradia_t3/projeto.json
```
Projetos da app ficam em `projetos/<slug>/` (**fora do Git**: fazer cópia à parte).

## Estado e limitações
Ver `brain/ESTADO.md`. Principais: tabelas de correntes admissíveis da edição 2000 do RTIEBT (por confirmar); DXF do arquiteto só testado com um sintético; trajetos de cabo em estrela; sem preços/orçamento; trifásico e Icc/Zs não suportados.

## Para continuar noutro chat
`/retomar` (lê `brain/`). Regras do repo em `CLAUDE.md`. Roadmap: `ROADMAP.md`. Agentes: `docs/AGENTES.md`.
