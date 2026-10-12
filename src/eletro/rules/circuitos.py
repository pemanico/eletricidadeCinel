"""Agrupamento de pontos em circuitos finais. FONTE do limite: RTIEBT 801.5.3 (max. 8 pontos de utilizacao por circuito;
climatizacao em circuitos proprios, max. 5 aparelhos). O criterio de agrupamento (sequencial, por ordem das divisoes,
sem partir divisoes) e CONVENCAO."""

def agrupar_sequencial(itens: list[tuple[str, int]], maximo: int) -> list[list[tuple[str, int]]]:
    """itens = [(room_id, n_pontos)]. Junta divisoes consecutivas ate maximo; uma divisao com mais de 'maximo'
    pontos e partida em circuitos proprios."""
    grupos, atual, n = [], [], 0
    for rid, pts in itens:
        while pts > maximo:                 # divisao maior que um circuito
            if atual: grupos.append(atual); atual, n = [], 0
            grupos.append([(rid, maximo)]); pts -= maximo
        if n + pts > maximo and atual:
            grupos.append(atual); atual, n = [], 0
        atual.append((rid, pts)); n += pts
    if atual: grupos.append(atual)
    return grupos
