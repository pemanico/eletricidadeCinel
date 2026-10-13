"""Gera um PDF vetorial SINTETICO ao estilo de um plot de AutoCAD (camadas OCG, escala 1:50) para testes.
NAO e um ficheiro real. Medidas verificaveis a mao (interiores):
  Sala     x 0.30-4.30, y 0.30-3.30 -> 4.00 x 3.00 = 12.00 m2
  Quarto 1 x 4.40-7.40, y 0.30-3.30 -> 3.00 x 3.00 =  9.00 m2
Paredes exteriores 0.30 m, interior 0.10 m com porta de 0.90 m (y 1.00-1.90).
Janela na Sala (x 1.50-2.70, parede de baixo) com caixilho na camada de vistas; porta exterior no Quarto (x 5.00-5.90,
parede de cima) com aro; frente de roupeiro no Quarto (paralela a parede, a 0.60 m) que NAO pode roubar area;
sanita encostada a parede (so a linha das costas fica na faixa da parede)."""

ESCALA = 50
PT = 72 / 25.4 * 1000 / ESCALA          # pontos PDF por metro real (56.69...)
OX, OY = 40.0, 60.0                     # origem do desenho na folha (pt)

def _p(x, y):
    return f"{OX + x * PT:.3f} {OY + y * PT:.3f}"

def _rect(x0, y0, x1, y1):
    return f"{_p(x0, y0)} m {_p(x1, y0)} l {_p(x1, y1)} l {_p(x0, y1)} l h S\n"

def _linha(x0, y0, x1, y1):
    return f"{_p(x0, y0)} m {_p(x1, y1)} l S\n"

def paredes(com_interior=True):
    s = ""
    # exterior: baixo (com janela 1.50-2.70), cima (com porta 5.00-5.90), esquerda, direita
    s += _rect(0, 0, 1.50, 0.30) + _rect(2.70, 0, 7.70, 0.30)
    s += _rect(0, 3.30, 5.00, 3.60) + _rect(5.90, 3.30, 7.70, 3.60)
    s += _rect(0, 0.30, 0.30, 3.30) + _rect(7.40, 0.30, 7.70, 3.30)
    if com_interior:   # parede interior com porta (1.00-1.90)
        s += _rect(4.30, 0.30, 4.40, 1.00) + _rect(4.30, 1.90, 4.40, 3.30)
    return s

def vistas():
    s = _linha(1.50, 0.10, 2.70, 0.10) + _linha(1.50, 0.20, 2.70, 0.20)    # caixilho da janela (dentro da parede)
    s += _linha(5.00, 3.45, 5.90, 3.45)                                     # aro da porta exterior
    s += _linha(4.40, 2.70, 7.40, 2.70)                                     # frente de roupeiro (a 0.60 m): ignorar
    s += _rect(6.80, 3.25, 7.20, 3.30) + _rect(6.85, 2.60, 7.15, 3.25)      # sanita encostada (so as costas contam)
    return s

def _txt(x, y, t, tam=6):
    return f"BT /F1 {tam} Tf {_p(x, y)} Td ({t}) Tj ET\n"

def pdf(com_camadas=True, com_interior=True, quadro=(("Sala", "12.00"), ("Quarto 1", "9.00")), titulo="PLANTA DO PISO 0"):
    oc = (lambda tag, corpo: f"/OC /{tag} BDC\n{corpo}EMC\n") if com_camadas else (lambda tag, corpo: corpo)
    conteudo = "0 0 0 RG 0.2 w\n" + oc("oc1", paredes(com_interior)) + oc("oc2", vistas())
    conteudo += _txt(1.9, 1.7, "Sala") + _txt(5.4, 1.7, "Quarto 1")
    y = 330.0
    leg = "BT /F1 7 Tf 470 360 Td (Areas uteis do piso 0) Tj ET\n"
    for nome, a in quadro:
        leg += f"BT /F1 7 Tf 470 {y:.0f} Td ({nome}: {a}m\\262) Tj ET\n"; y -= 12
    leg += f"BT /F1 7 Tf 470 120 Td ({titulo}) Tj ET\nBT /F1 7 Tf 470 100 Td (ESCALA 1:{ESCALA}) Tj ET\n"
    conteudo += leg
    c = conteudo.encode("latin-1")
    props = "/Properties << /oc1 5 0 R /oc2 6 0 R >>" if com_camadas else ""
    ocprops = "/OCProperties << /OCGs [5 0 R 6 0 R] /D << /ON [5 0 R 6 0 R] >> >>" if com_camadas else ""
    objs = [
        f"<< /Type /Catalog /Pages 2 0 R {ocprops} >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 400] /Contents 4 0 R /Resources << /Font << /F1 7 0 R >> {props} >> >>",
        None,
        "<< /Type /OCG /Name (PAREDES) >>",
        "<< /Type /OCG /Name (VISTA) >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    out = b"%PDF-1.5\n"
    offs = []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        if o is None:
            out += f"{i} 0 obj\n<< /Length {len(c)} >>\nstream\n".encode() + c + b"\nendstream\nendobj\n"
        else:
            out += f"{i} 0 obj\n{o}\nendobj\n".encode("latin-1")
    x = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    out += "".join(f"{o:010d} 00000 n \n" for o in offs).encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n".encode()
    return out
