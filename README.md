# eletricidadeCinel
Projecto elétrico 
# eletro-agents
Sistema para apoiar projetos, orçamentos e propostas de instalações elétricas, construído módulo a módulo com o curso (CINEL, 2026-2028).

## Pipeline
entrada (JSON | DXF | PDF vetorial | foto) → `Project` (schema) → regras + cálculo determinístico → rascunhos (quadro de cargas, unifilar, memória, orçamento) → revisão humana

## Prioridade de entradas
1. JSON manual (já) 2. DXF (converter DWG→DXF) 3. PDF vetorial (extração + confirmação) 4. Fotos só para contexto qualitativo, nunca para cotas.

## Estado
Ver ROADMAP.md. Executar testes: `PYTHONPATH=src python -m pytest tests/golden` (ou pytest com pythonpath).
