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


def agrupar_proximidade(pontos: list[dict], inicio, piso_inicio: int, maximo: int) -> list[list[dict]]:
    """CONVENCAO: agrupa pontos colocados na planta em circuitos de ate 'maximo' (801.5.3). Cada circuito parte do quadro
    e segue sempre para o ponto livre mais proximo (Manhattan; pontos de outro piso so quando o piso atual acabar).
    pontos = [{id, pos, piso, ...}]. Devolve grupos pela ordem da cadeia."""
    livres = list(pontos)
    grupos = []
    while livres:
        cur, piso, g = tuple(inicio), piso_inicio, []
        while livres and len(g) < maximo:
            mesmo = [q for q in livres if q["piso"] == piso] or livres
            q = min(mesmo, key=lambda q: (abs(q["pos"][0] - cur[0]) + abs(q["pos"][1] - cur[1]), q["id"]))
            g.append(q); livres.remove(q); cur, piso = tuple(q["pos"]), q["piso"]
        grupos.append(g)
    return grupos

def ordenar_cadeia(pontos: list[dict], inicio, piso_inicio: int) -> list[dict]:
    """Ordem de ligacao de um circuito definido a mao: vizinho mais proximo a partir do quadro."""
    return agrupar_proximidade(pontos, inicio, piso_inicio, max(1, len(pontos)))[0] if pontos else []
