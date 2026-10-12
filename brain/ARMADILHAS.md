# Armadilhas conhecidas
## Erros de conteúdo já cometidos
- 4 mm² B1 PVC 2 condutores: 28 A (não 32 A). Termoacumulador 4,6 kW/25 m/35 °C/3 circuitos: 4 mm² dá Iz 18,4 A, falha; 6 mm² dá 23,7 A, cumpre (3G6 + C20 + DDR 30 mA).
- Resistências em paralelo e outros exercícios do bloco 1 foram corrigidos; as notas continuam a ser material de estudo por validar.
## Ambiente (sessão em contentor na nuvem)
- `pip` não chega ao PyPI (sem ezdxf, sem pytest): usar `python run_tests.py` e o escritor DXF próprio.
- `rsync` não existe: usar `cp -r`. Verificar sempre o resultado de uma cópia/commit (`git show --stat`).
- Ficheiros com acentos no nome causam problemas: usar nomes ASCII.
## Processo
- Não confiar em texto de marketing do curso para direitos legais (assinar projetos).
- Texto no DXF R12 sai sem acentos (ASCII).
- Cada correção de números: verificar em Python antes de escrever em nota.
