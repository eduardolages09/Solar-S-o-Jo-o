# Monta o site do Solar São João (o protótipo A, «Praça», escolhido a 2026-10-21;
# os três protótipos e o gerador deles estão em arquivo/v1-2026-10-21-prototipos/)
# a partir de listas de fotos e textos. Gera:
#   site/index.html          a página
#   site/assets/series.js    as séries do visor e dos espaços comuns
# O tema (letra, paleta, a porta) está em site/assets/tema.css e gesto.js.
# Uso (a partir da pasta da casa): python3 scripts/monta.py
import json
from html import escape
from pathlib import Path

CASA = Path(__file__).resolve().parent.parent
SITE = CASA / "site"
IMG = SITE / "assets" / "img"
MED = json.loads((CASA / "scripts" / "medidas.json").read_text())

BOOKING = "https://www.booking.com/hotel/pt/solar-sao-joao-sao-joao-da-madeira.pt-pt.html"
AIRBNB = "https://www.airbnb.pt/rooms/926787010266736200"
TEL = "+351918030000"
TEL_VER = "+351 918 030 000"
EMAIL = "portojetaime2@gmail.com"
MAPA = "https://www.google.com/maps/dir/?api=1&amp;destination=40.899349,-8.492242"
RNT = "https://rnt.turismodeportugal.pt/RNT/RNAL.aspx?nr=113396"


def tam(nome):
    return MED[nome]


def srcset(nome, pre="assets/img/"):
    w, _ = tam(nome)
    partes = [f"{pre}{nome}-{x}.jpg {x}w" for x in (800, 1400) if (IMG / f"{nome}-{x}.jpg").exists()]
    partes.append(f"{pre}{nome}.jpg {w}w")
    return ", ".join(partes)


def medio(nome, pre="assets/img/"):
    for x in (1400, 800):
        if (IMG / f"{nome}-{x}.jpg").exists():
            return f"{pre}{nome}-{x}.jpg"
    return f"{pre}{nome}.jpg"


def mini(nome, pre="assets/img/"):
    return f"{pre}{nome}-800.jpg" if (IMG / f"{nome}-800.jpg").exists() else f"{pre}{nome}.jpg"


def cobre(nome):
    """sizes de uma foto que enche o ecrã (object-fit: cover): num ecrã mais estreito do que a foto,
    a largura mostrada é a altura do ecrã × o formato (com 100vw, o telemóvel ao alto levava a de 800 px
    e a foto ficava desfocada)."""
    w, h = tam(nome)
    r = round(100 * w / h)
    return f"(max-aspect-ratio: {r}/100) {r}vh, 100vw"


def img(nome, alt, sizes, lazy=True, extra=""):
    w, h = tam(nome)
    carga = ' loading="lazy"' if lazy else ""
    return (f'<img src="{medio(nome)}" srcset="{srcset(nome)}" sizes="{sizes}" alt="{escape(alt)}" '
            f'width="{w}" height="{h}"{carga} decoding="async"{extra}>')


# ---------------------------------------------------------------- séries
QUARTOS = [
    {"k": "q1", "nome": ("Suite com", "vista"), "tab": "Suite com vista", "camas": "Cama de casal extragrande",
     "fotos": [("q1-quarto", "Suite com vista: cama de casal, papel de parede de folhas e roupeiro aberto", "O quarto"),
               ("q1-b", "A mesma suite, com a secretária e a janela", "A secretária"),
               ("q1-wc", "Casa de banho privativa da suite, com duche", "Casa de banho privativa")],
     "wc": 2},
    {"k": "q2", "nome": ("Suite", "dupla"), "tab": "Suite dupla", "camas": "Três camas de casal",
     "fotos": [("q2-quarto", "Suite dupla com camas de casal lado a lado e quadros por cima", "O quarto"),
               ("q2-b", "A suite dupla vista da porta, com o roupeiro aberto", "Vista da porta"),
               ("q2-c", "A suite dupla com a cómoda e as camas feitas", "As camas"),
               ("q2-wc", "Casa de banho privativa da suite dupla", "Casa de banho privativa")],
     "wc": 3},
    {"k": "q3", "nome": ("Quarto", "familiar"), "tab": "Quarto familiar", "camas": "Duas camas de casal",
     "fotos": [("q3-quarto", "Quarto familiar com duas camas de casal e duas janelas", "O quarto"),
               ("q3-b", "Cabeceira com luz e papel de parede geométrico", "A cabeceira"),
               ("q3-c", "A cama do quarto familiar junto à janela", "Junto à janela"),
               ("q3-d", "O quarto familiar visto da entrada", "Da entrada"),
               ("q3-wc", "Casa de banho privativa com espelho iluminado e escada-toalheiro", "Casa de banho privativa"),
               ("q3-wc2", "O duche da casa de banho privativa", "O duche")],
     "wc": 4},
    {"k": "q4", "nome": ("Quarto", "duplo"), "tab": "Quarto duplo", "camas": "Cama de casal",
     "fotos": [("q4-quarto", "Quarto duplo com cama de casal e casa de banho ao fundo", "O quarto"),
               ("q4-b", "O quarto duplo com roupeiro, toucador e espelho redondo", "O toucador"),
               ("q4-wc", "Casa de banho privativa com chão de mosaico preto e branco", "Casa de banho privativa")],
     "wc": 2},
]

ESPACOS = {
    "sala": ("Sala comum", "Sofás e poltronas, ao pé da escadaria.", [
        ("sala-alta", "A sala comum à entrada, com a escadaria e a luz do sol no parquet", "A sala, à entrada"),
        ("sala-sofas", "Sofá, poltrona de ferro e a escadaria ao fundo", "Sofá e poltrona"),
        ("sala-escada", "A escadaria vista da sala, com o papel de parede de folhas", "A escadaria, vista da sala")]),
    "escada": ("Escadaria", "Madeira, ferro e papel de parede de folhas.", [
        ("escada-sobe", "A escadaria com o corrimão de ferro e o papel de parede de folhas", "Os degraus"),
        ("escada-ferro", "O corrimão de ferro a subir entre os andares", "O corrimão"),
        ("escada-cima", "A escadaria vista de cima, com a sala lá em baixo", "Vista de cima")]),
    "cozinha": ("Cozinha partilhada", "Equipada, para todos os hóspedes.", [
        ("cozinha", "Cozinha partilhada com bancadas em L e móveis de madeira clara", "A cozinha"),
        ("cozinha-bancada", "Bancada da cozinha com a ilha ao centro", "A bancada"),
        ("cozinha-janela", "A cozinha com a janela e a máquina de café", "Junto à janela"),
        ("cozinha-ilha", "Ilha da cozinha posta para o pequeno-almoço", "A ilha")]),
}

GALERIA = {
    "suites": ("Suites", [("suite-candeeiros", "Suite com candeeiros suspensos de cada lado da cama", "Candeeiros de cada lado"),
                          ("suite-verde", "Suite com manta verde e espelho alto", "A manta verde"),
                          ("suite-luz", "Suite com cama de casal, poltrona e casa de banho ao fundo", "A poltrona")]),
    "quartos": ("Quartos", [("familiar-verde", "Quarto familiar com duas camas e mantas verdes", "Mantas verdes"),
                            ("dupla-b", "Quarto com duas camas de casal e mantas castanhas", "Duas camas de casal"),
                            ("dupla-c", "Quarto com duas camas e uma cama individual", "Três camas")]),
}


def foto_serie(nome, alt, leg):
    w, h = tam(nome)
    return {"src": f"assets/img/{nome}.jpg", "medio": medio(nome), "mini": mini(nome), "alt": alt, "leg": leg, "w": w, "h": h}


def series(espacos):
    s = {}
    for q in QUARTOS:
        s[q["k"]] = {"chave": q["k"], "titulo": " ".join(q["nome"]).capitalize(), "fotos": [foto_serie(*f) for f in q["fotos"]]}
    for k, (tit, _, fotos) in espacos.items():
        s[k] = {"chave": k, "titulo": tit, "fotos": [foto_serie(*f) for f in fotos]}
    for k, (tit, fotos) in GALERIA.items():
        s["g-" + k] = {"chave": "g-" + k, "titulo": tit, "fotos": [foto_serie(*f) for f in fotos]}
    return s


# ---------------------------------------------------------------- blocos comuns
SETA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'


def topo(nav):
    links = "\n    ".join(f'<a href="#{i}">{t}</a>' for i, t in nav)
    return f'''<header class="topo" id="topo">
  <a class="topo__marca" href="#inicio" aria-label="Solar São João, início">Solar São João</a>
  <nav class="topo__nav" aria-label="Secções">
    {links}
  </nav>
  <a class="botao botao--topo" href="#reservar">Reservar</a>
</header>'''


def hero(linhas, base="hero"):
    nome = " ".join(f"<span>{x}</span>" for x in linhas)
    w, h = tam(base)
    alto = f"{base}-alto"
    return f'''<section class="hero" id="inicio" data-sem-folga aria-labelledby="hero-titulo">
  <picture class="hero__foto">
    <source media="(max-width: 760px) and (orientation: portrait)" srcset="assets/img/{alto}-800.jpg 800w, assets/img/{alto}.jpg {tam(alto)[0]}w" sizes="100vw">
    <img src="assets/img/{base}-2000.jpg" srcset="assets/img/{base}-1400.jpg 1400w, assets/img/{base}-2000.jpg 2000w, assets/img/{base}.jpg {w}w" sizes="100vw" alt="A fachada do Solar São João na praça, com as esplanadas no rés-do-chão" width="{w}" height="{h}" fetchpriority="high">
  </picture>
  <div class="hero__ecra">
    <div class="hero__texto">
      <h1 class="hero__titulo" id="hero-titulo">{nome}</h1>
      <p class="hero__onde">Casa de hóspedes na praça · São João da Madeira</p>
    </div>
    <a class="hero__reservar" href="#reservar">Ver disponibilidade</a>
  </div>
</section>'''


def abertura(grande, cartao):
    return f'''<section class="abertura" id="abertura">
  <div class="abertura__grelha largura">
    <div class="abertura__fotos">
      <figure class="abertura__grande" data-entra>{img(grande[0], grande[1], "(max-width: 760px) 60vw, 30vw")}</figure>
      <figure class="abertura__cartao" data-entra data-vel="-0.08">{img(cartao[0], cartao[1], "(max-width: 760px) 50vw, 26vw")}</figure>
    </div>
    <p class="abertura__frase" data-palavras>Na praça central de São João da Madeira, uma casa de hóspedes que recebe desde 1985 e tem vindo a ser renovada, quarto a quarto.</p>
  </div>
</section>'''


def quartos():
    fotos, textos, tabs, wcs = [], [], [], []
    for i, q in enumerate(QUARTOS):
        n0 = q["fotos"][0]
        fotos.append(f'<figure class="qp__foto{" ativo" if i == 0 else ""}">{img(n0[0], n0[1], "100vw", lazy=False)}</figure>')
        a, b = q["nome"]
        n = len(q["fotos"])
        textos.append(f'''<article class="qp__quarto{" ativo" if i == 0 else ""}">
              <h3 class="qp__nome"><span><span>{a}</span></span><span><span>{b}</span></span></h3>
              <button type="button" class="qp__ver" data-visor="{q["k"]}" data-indice="0">Ver as {n} fotografias {SETA}</button>
            </article>''')
        tabs.append(f'<li><button type="button" aria-pressed="{"true" if i == 0 else "false"}"><span class="qp__traco" aria-hidden="true"><span></span></span><span class="qp__linha-nome">{q["tab"]}</span><span class="qp__linha-camas">{q["camas"]}</span></button></li>')
        wn = q["fotos"][q["wc"]]
        w, h = tam(wn[0])
        wcs.append(f'<button type="button" class="qp__wc{" ativo" if i == 0 else ""}" data-q="{i}" data-visor="{q["k"]}" data-indice="{q["wc"]}"><img src="{mini(wn[0])}" alt="{escape(wn[1])}" width="{w}" height="{h}" decoding="async"><span>Casa de banho privativa</span></button>')
    return f'''<section class="quartos" id="quartos" aria-labelledby="quartos-titulo">
  <div class="qp" data-qp>
    <div class="qp__palco">
      <div class="qp__moldura">
        <div class="qp__fotos">
          {chr(10).join("          " + f for f in fotos).strip()}
        </div>
        <div class="qp__veu" aria-hidden="true"></div>
        <h2 class="qp__titulo" id="quartos-titulo">Quartos</h2>
        <i class="vao" aria-hidden="true"><b></b><b></b><b></b><b></b></i>
        {chr(10).join("        " + w for w in wcs).strip()}
        <div class="qp__legenda" aria-live="polite">
          <div class="qp__textos">
            {chr(10).join("            " + t for t in textos).strip()}
          </div>
        </div>
        <ol class="qp__linha" aria-label="Escolher quarto">
          {chr(10).join("          " + t for t in tabs).strip()}
        </ol>
      </div>
    </div>
  </div>
</section>'''


def espacos_comuns(espacos, frase):
    total = sum(len(f) for _, _, f in espacos.values())
    seps = [f'<button type="button" role="tab" aria-selected="true" data-div="tudo">Tudo<sup>{total}</sup></button>']
    itens = []
    for k, (tit, _, fotos) in espacos.items():
        curto = tit.split(" ")[0] + (f'<span class="longo"> {" ".join(tit.split(" ")[1:])}</span>' if " " in tit else "")
        seps.append(f'<button type="button" role="tab" aria-selected="false" data-div="{k}">{curto}<sup>{len(fotos)}</sup></button>')
        for i, (n, alt, leg) in enumerate(fotos):
            w, h = tam(n)
            itens.append(f'''      <li class="gf" data-div="{k}" style="--ar:{w / h:.4f}">
        <button type="button" class="gf__foto" data-serie="{k}" data-indice="{i}" aria-label="Ver em grande: {escape(tit)}, {escape(leg)}">{img(n, alt, "(max-width: 760px) 92vw, 62vw")}</button>
        <p class="gf__leg"><span>{tit}</span> {leg}</p>
      </li>''')
    return f'''<section class="fotos" id="espacos" aria-labelledby="ec-titulo">
  <div class="fotos__cabeca largura">
    <h2 class="titulo" id="ec-titulo">Espaços comuns</h2>
    <div class="separadores" role="tablist" aria-label="Divisões">
      {chr(10).join("      " + x for x in seps).strip()}
      <span class="separadores__filete" aria-hidden="true"></span>
    </div>
  </div>
  <div class="galeria" data-entra>
    <ul class="galeria__fila" aria-label="Fotografias dos espaços comuns">
{chr(10).join(itens)}
    </ul>
    <div class="galeria__barra largura" aria-hidden="true"><i></i></div>
  </div>
</section>'''


COMODIDADES = [
    ('<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.2a9.5 9.5 0 0 1 13 0M8.6 15.4a5 5 0 0 1 6.8 0"/><path d="M12 18.6h.01"/>', "Wi-Fi gratuito", "Em toda a casa"),
    ('<path d="M5 11h14v6.5A3.5 3.5 0 0 1 15.5 21h-7A3.5 3.5 0 0 1 5 17.5z"/><path d="M3 11h18M9 7.5c0-1.5 1-1.5 1-3M14 7.5c0-1.5 1-1.5 1-3"/>', "Cozinha partilhada", "Equipada, para os hóspedes"),
    ('<path d="M6 19v-6.5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2V19"/><path d="M4 13.5a2 2 0 0 1 4 0V17h8v-3.5a2 2 0 0 1 4 0V19H4zM7.5 10.5V7a4.5 4.5 0 0 1 9 0v3.5"/>', "Sala comum", "Ao pé da escadaria"),
    ('<path d="M4 12h16v3.5a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z"/><path d="M6 12V5.5A2 2 0 0 1 8 3.5h.5a2 2 0 0 1 2 2"/><path d="M8.5 7.5l1-1M7 21l1-1.6M17 21l-1-1.6"/>', "Casa de banho privativa", "Na maioria dos quartos"),
    ('<path d="M12 2.5v19M4 7l16 10M20 7L4 17"/><path d="M9.5 3.8L12 6l2.5-2.2M9.5 20.2L12 18l2.5 2.2"/>', "Ar condicionado", "Nas suites maiores e nos quartos familiares"),
    ('<path d="M3.5 5.5h17v11h-17z"/><path d="M8.5 20h7M12 16.5V20"/>', "Televisão", "Ecrã plano, canais por satélite"),
    ('<path d="M3.5 8.5h17v9.5h-17z"/><path d="M3.5 12.5h17M7 8.5V6h10v2.5"/>', "Roupa de cama e toalhas", "Com produtos de higiene"),
    ('<path d="M14 9.5a5 5 0 1 1-5-5h5z"/><path d="M14 4.5h3.5l3 2.5-3 2.5H14M8 14l-1.5 6.5h3"/>', "Secador de cabelo", "Na casa de banho"),
    ('<path d="M5 3.5h14v17H5z"/><circle cx="12" cy="13" r="4.2"/><path d="M8 6.5h1.5M11.5 6.5H13"/>', "Lavar e secar roupa", "Máquinas na casa"),
    ('<path d="M2.5 14.5l7-1 5-7.5 2 .5-2.5 7 5.5-1 1.5-2.5 1.5.3-1 4.5-16 3z"/><path d="M3 20.5h18"/>', "Transfer do aeroporto", "Com custo adicional"),
    ('<path d="M8.5 14c-2 0-4 2-4 4 0 1.4 1 2 2.2 2 1.6 0 2.4-1 5.3-1s3.7 1 5.3 1c1.2 0 2.2-.6 2.2-2 0-2-2-4-4-4-1.3 0-2.2-1-3.5-1s-2.2 1-3.5 1z"/><circle cx="5.5" cy="10" r="1.6"/><circle cx="9.5" cy="6.5" r="1.6"/><circle cx="14.5" cy="6.5" r="1.6"/><circle cx="18.5" cy="10" r="1.6"/>', "Animais de estimação", "Mediante pedido"),
    ('<path d="M4 5.5h10v8H8.5L5 16.5v-3H4z"/><path d="M14 9h6v7.5h-1v3l-3.5-3H10v-3"/>', "Quatro línguas", "Português, inglês, espanhol e francês"),
    ('<path d="M3 14h13v3.5H3zM18.5 14v3.5M21 14v3.5M18.5 11c0-1.6 2.5-1.6 2.5-3.5"/><path d="M4 4l16 16"/>', "Casa sem fumo", "Em todos os espaços"),
]


def comodidades():
    itens = "\n".join(f'      <li class="comod__item"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg><div><b>{n}</b><span>{t}</span></div></li>' for p, n, t in COMODIDADES)
    return f'''<section class="comod" id="comodidades" aria-labelledby="comod-titulo">
  <div class="largura comod__cabeca">
    <h2 class="comod__titulo" id="comod-titulo">Comodidades</h2>
  </div>
  <div class="comod__pista" data-comod tabindex="0" role="group" aria-label="Comodidades, lista horizontal">
    <ul class="comod__lista">
{itens}
    </ul>
  </div>
</section>'''


def historia(foto_sizes="(max-width: 760px) 90vw, 54vw"):
    return f'''<section class="historia" aria-label="A casa e quem recebe">
  <div class="historia__corpo largura">
    <figure class="historia__foto">
      <div data-entra>{img("regiao-chapeus", "Rua de São João da Madeira enfeitada com chapéus de cores pendurados por cima", foto_sizes)}</div>
      <figcaption>São João da Madeira, a cidade do chapéu.</figcaption>
    </figure>
    <div class="historia__texto">
      <p class="historia__grande" data-palavras>Na praça desde 1985.</p>
      <p class="historia__nota">A casa abriu ao público em 1985, no centro da cidade, e tem vindo a ser renovada, andar a andar e quarto a quarto.</p>
    </div>
  </div>
</section>'''


def galeria():
    seps = ['<button type="button" role="tab" aria-selected="true" data-div="tudo">Tudo<sup>%d</sup></button>' % sum(len(f) for _, f in GALERIA.values())]
    itens = []
    for k, (tit, fotos) in GALERIA.items():
        seps.append(f'<button type="button" role="tab" aria-selected="false" data-div="{k}">{tit}<sup>{len(fotos)}</sup></button>')
        for i, (n, alt, leg) in enumerate(fotos):
            w, h = tam(n)
            itens.append(f'''      <li class="gf" data-div="{k}" style="--ar:{w / h:.4f}">
        <button type="button" class="gf__foto" data-serie="g-{k}" data-indice="{i}" aria-label="Ver em grande: {escape(leg)}">{img(n, alt, "(max-width: 760px) 92vw, 62vw")}</button>
        <p class="gf__leg">{leg}</p>
      </li>''')
    return f'''<section class="fotos" id="fotografias" aria-labelledby="fotos-titulo">
  <div class="fotos__cabeca largura">
    <h2 class="titulo" id="fotos-titulo">Mais quartos</h2>
    <div class="separadores" role="tablist" aria-label="Escolher">
      {chr(10).join("      " + s for s in seps).strip()}
      <span class="separadores__filete" aria-hidden="true"></span>
    </div>
  </div>
  <div class="galeria" data-entra>
    <ul class="galeria__fila" aria-label="Fotografias">
{chr(10).join(itens)}
    </ul>
    <div class="galeria__barra largura" aria-hidden="true"><i></i></div>
  </div>
</section>'''


LUGARES = [
    ("regiao-chapelaria", "Na cidade", "Museu da Chapelaria", "Numa antiga fábrica de chapéus, a história da indústria que fez a cidade.",
     "O Museu da Chapelaria, de paredes amarelas, com a estátua de bronze dos chapeleiros à frente"),
    ("regiao-oliva", "Na cidade", "Torre da Oliva", "Na antiga fábrica das máquinas de costura Oliva: arte, design e o Museu do Calçado.",
     "A Torre da Oliva, com a estátua de um sapateiro no relvado"),
    ("regiao-milagres", "1,5 km", "Parque de Nossa Senhora dos Milagres", "Um parque arborizado à volta do santuário, para caminhar à sombra.",
     "O santuário de Nossa Senhora dos Milagres, branco, entre árvores"),
    ("regiao-castelo", "6 km", "Castelo de Santa Maria da Feira", "Um castelo medieval no alto de um monte; no verão, a Viagem Medieval.",
     "As muralhas e as torres do Castelo de Santa Maria da Feira"),
]


def arredores(frase):
    lis, afs = [], []
    for n, km, nome, txt, alt in LUGARES:
        lis.append(f'''      <li class="lugar">
        <figure class="lugar__foto">{img(n, alt, "92vw")}</figure>
        <span class="lugar__km">{km}</span>
        <h3 class="lugar__nome">{nome}</h3>
        <p class="lugar__texto">{txt}</p>
      </li>''')
        afs.append(f'        <figure class="af">{img(n, alt, "min(56vw, 114vh)")}</figure>')
    return f'''<section class="arredores" id="arredores" aria-labelledby="arredores-titulo">
  <header class="cabeca largura">
    <h2 class="titulo" id="arredores-titulo">Arredores</h2>
    <p class="cabeca__frase">{frase}</p>
  </header>
  <div class="arredores__corpo largura">
    <ol class="lugares">
{chr(10).join(lis)}
    </ol>
    <div class="arredores__palco" aria-hidden="true">
      <div class="arredores__preso">
{chr(10).join(afs)}
      </div>
    </div>
  </div>
</section>'''


def fecho(foto, alt):
    return f'''<section class="fecho" id="reservar" data-sem-folga aria-labelledby="fecho-titulo">
  <div class="fecho__foto" data-vel="0.1">{img(foto, alt, "(orientation: portrait) 180vh, 100vw")}</div>
  <div class="fecho__texto">
    <h2 class="fecho__titulo" id="fecho-titulo">Venha visitar-nos</h2>
    <p>Na Praça Luís Ribeiro, no centro de São João da Madeira.</p>
    <div class="fecho__botoes">
      <a class="botao botao--seta" href="{BOOKING}" target="_blank" rel="noopener">Ver disponibilidade</a>
      <a class="botao botao--fosco" href="tel:{TEL}">Ligar {TEL_VER[5:]}</a>
    </div>
  </div>
</section>'''


def rodape():
    return f'''<footer class="rodape">
  <div class="largura rodape__linha">
    <div class="rodape__casa">
      <a href="#inicio" class="rodape__marca">Solar São João</a>
      <p class="rodape__sub">Je T'aime Solar São João · casa de hóspedes</p>
    </div>
    <div class="rodape__onde">
      <h3>Onde</h3>
      <address>Praça Luís Ribeiro, 165<br>3700-172 São João da Madeira</address>
      <a class="mapa" href="{MAPA}" target="_blank" rel="noopener">
        <span class="mapa__icone" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 1.5c-4.4 0-8 3.5-8 7.9 0 5.6 6.6 12.1 7.4 12.8.3.3.9.3 1.2 0 .8-.7 7.4-7.2 7.4-12.8 0-4.4-3.6-7.9-8-7.9Z" fill="#ea4335"/><path d="M12 1.5c-4.4 0-8 3.5-8 7.9 0 1.8.7 3.7 1.7 5.5L12 9.4Z" fill="#4285f4" opacity=".9"/><path d="M5.7 14.9c1.6 3 4.6 6.1 5.7 7.3.3.3.9.3 1.2 0 .6-.6 1.8-1.8 3-3.4L12 9.4Z" fill="#34a853"/><path d="M12 9.4l3.6 9.4c1.9-2.6 4.4-6.1 4.4-9.4 0-1.1-.2-2.2-.6-3.1Z" fill="#fbbc04"/><circle cx="12" cy="9.4" r="3" fill="#fff"/></svg></span>
        <span>Como chegar</span>
      </a>
    </div>
    <address class="rodape__contacto">
      <h3>Contacto</h3>
      <a class="rodape__tel" href="tel:{TEL}">{TEL_VER}</a>
      <small>Chamada para a rede móvel nacional</small>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </address>
    <div class="rodape__reservas">
      <h3>Reservas</h3>
      <a href="{BOOKING}" target="_blank" rel="noopener">Booking.com</a>
      <a href="{AIRBNB}" target="_blank" rel="noopener">Airbnb</a>
    </div>
  </div>
  <div class="largura rodape__legal">
    <div>
      <p>Je T'aime Solar São João — Alojamento Local na modalidade de quartos, <a href="{RNT}" target="_blank" rel="noopener">RNAL n.º 113396/AL</a>. Explorado por Branco Suave, Lda., NIPC 518804950.</p>
      <p>Em caso de litígio de consumo, pode recorrer ao <a href="https://www.cicap.pt" target="_blank" rel="noopener">CICAP — Centro de Informação de Consumo e Arbitragem do Porto</a>. Mais informação no <a href="https://www.consumidor.gov.pt" target="_blank" rel="noopener">Portal do Consumidor</a>.</p>
    </div>
    <div>
      <p><a href="https://www.livroreclamacoes.pt" target="_blank" rel="noopener">Livro de Reclamações Eletrónico</a></p>
      <p>Fotografias da região no Wikimedia Commons:
        <a href="https://commons.wikimedia.org/wiki/File:Museu_da_Chapelaria_e_Monumento_Unhas_Negras.jpg" target="_blank" rel="noopener">Museu da Chapelaria</a> (Trotz, domínio público),
        <a href="https://commons.wikimedia.org/wiki/File:S%C3%A2o_Jo%C3%A3o_da_Madeira_-_Portugal_(49749908533).jpg" target="_blank" rel="noopener">rua dos chapéus</a>,
        <a href="https://commons.wikimedia.org/wiki/File:Torre_da_Oliva_-_S%C3%A3o_Jo%C3%A3o_da_Madeira_-_Portugal_(49750446236).jpg" target="_blank" rel="noopener">Torre da Oliva</a> e
        <a href="https://commons.wikimedia.org/wiki/File:Santu%C3%A1rio_de_Nossa_Senhora_dos_Milagres_-_S%C3%A3o_Jo%C3%A3o_da_Madeira_-_Portugal_(49257629458).jpg" target="_blank" rel="noopener">santuário dos Milagres</a> (Vitor Oliveira, CC BY-SA 2.0),
        <a href="https://commons.wikimedia.org/wiki/File:Castelo_St._Maria_Feira_(1).jpg" target="_blank" rel="noopener">castelo da Feira</a> (Jorge Lobo, CC BY-SA 4.0).</p>
      <p>© 2026 Solar São João</p>
    </div>
  </div>
</footer>

<nav class="barra" aria-label="Reservar">
  <a href="tel:{TEL}">Ligar</a>
  <a class="barra__principal" href="{BOOKING}" target="_blank" rel="noopener">Ver disponibilidade</a>
</nav>

<div class="visor" id="visor" role="dialog" aria-modal="true" aria-label="Fotografias" hidden>
  <p class="visor__titulo"></p>
  <p class="visor__conta"></p>
  <button type="button" class="visor__fechar" aria-label="Fechar"><svg viewBox="0 0 24 24"><path d="M5 5l14 14M19 5L5 19"/></svg></button>
  <button type="button" class="visor__seta visor__seta--ant" aria-label="Anterior"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
  <figure class="visor__palco"><img alt=""></figure>
  <button type="button" class="visor__seta visor__seta--seg" aria-label="Seguinte"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>
  <ol class="visor__minis" aria-label="Escolher fotografia"></ol>
</div>'''


# ---------------------------------------------------------------- gestos de cada protótipo
def gesto_porta():
    return f'''<section class="porta" id="entrada" aria-labelledby="porta-titulo" data-presa>
  <div class="porta__preso">
    <figure class="porta__foto">{img("sala-alta", "A sala à entrada da casa, alta, com a escadaria ao fundo e o sol no parquet", cobre("sala-alta"))}</figure>
    <i class="vao" aria-hidden="true"><b></b><b></b><b></b><b></b></i>
    <div class="porta__texto">
      <h2 class="porta__titulo" id="porta-titulo">A entrada</h2>
      <p>Da praça, entra-se numa sala alta, com a escadaria ao fundo.</p>
    </div>
  </div>
</section>'''


# o Caminho Português Central, de Lisboa a Santiago (lat, lon) — traçado esquemático pelas cidades de etapa
CAMINHO = [("Lisboa", 38.722, -9.139), ("Santarém", 39.236, -8.687), ("Tomar", 39.602, -8.410), ("Coimbra", 40.211, -8.429),
           ("Águeda", 40.575, -8.448), ("Albergaria-a-Velha", 40.692, -8.481), ("Oliveira de Azeméis", 40.840, -8.477),
           ("São João da Madeira", 40.899, -8.492), ("Porto", 41.150, -8.611), ("Barcelos", 41.531, -8.619),
           ("Ponte de Lima", 41.767, -8.583), ("Valença", 42.028, -8.643), ("Pontevedra", 42.433, -8.648),
           ("Padrón", 42.739, -8.661), ("Santiago de Compostela", 42.880, -8.545)]
ROTULOS = {"Lisboa", "Coimbra", "São João da Madeira", "Porto", "Valença", "Santiago de Compostela"}


def gesto_caminho():
    import math
    H, W = 1000, 420
    lat0, lat1 = 38.62, 42.98
    lons = [c[2] for c in CAMINHO]
    lonm = (min(lons) + max(lons)) / 2
    k = H / (lat1 - lat0)
    pts = []
    for nome, la, lo in CAMINHO:
        x = W / 2 + (lo - lonm) * k * math.cos(math.radians(40.8)) * 1.0
        y = H - (la - lat0) * k
        pts.append((nome, x, y))
    # comprimento acumulado (fração de cada ponto ao longo do traçado)
    comp = [0.0]
    for a, b in zip(pts, pts[1:]):
        comp.append(comp[-1] + math.hypot(b[1] - a[1], b[2] - a[2]))
    total = comp[-1]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for _, x, y in pts)
    marcas = []
    for (nome, x, y), c in zip(pts, comp):
        f = c / total
        aqui = nome == "São João da Madeira"
        cls = "caminho__ponto" + (" caminho__ponto--aqui" if aqui else "")
        rot = ""
        if nome in ROTULOS:
            lado = "end" if aqui else "start"
            dx = -16 if aqui else 16
            texto = "Solar São João" if aqui else nome
            rot = f'<text x="{x + dx:.1f}" y="{y + 5:.1f}" text-anchor="{lado}">{texto}</text>'
            if aqui:
                rot += f'<text class="caminho__sub" x="{x + dx:.1f}" y="{y + 28:.1f}" text-anchor="end">São João da Madeira</text>'
        marcas.append(f'<g class="{cls}" data-f="{f:.4f}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{9 if aqui else 4.5}"/>{rot}</g>')
    f_aqui = comp[[p[0] for p in pts].index("São João da Madeira")] / total
    return f'''<section class="caminho" id="caminho" aria-labelledby="caminho-titulo" data-presa data-aqui="{f_aqui:.4f}">
  <div class="caminho__preso largura">
    <div class="caminho__texto">
      <h2 class="titulo" id="caminho-titulo">O Caminho</h2>
      <p class="caminho__linha" data-passo>O Caminho Português de Santiago sobe de Lisboa pelo interior, por Coimbra, até ao Porto.</p>
      <p class="caminho__linha" data-passo>Pelo meio, passa por São João da Madeira.</p>
      <p class="caminho__linha" data-passo>A casa fica na praça, no centro da cidade.</p>
    </div>
    <svg class="caminho__mapa" viewBox="-170 -30 {W + 340} {H + 60}" role="img" aria-label="Traçado do Caminho Português de Lisboa a Santiago de Compostela, com São João da Madeira assinalado">
      <path class="caminho__fundo" d="{d}"/>
      <path class="caminho__traco" d="{d}" pathLength="1"/>
      {"".join(marcas)}
    </svg>
  </div>
</section>'''


ESCADA = [("sala-escada", "A escadaria vista da sala, com o papel de parede de folhas", "Ao fundo da sala, a escadaria."),
          ("escada-sobe", "Degraus de madeira e corrimão de ferro", "Degraus de madeira, corrimão de ferro,"),
          ("escada-ferro", "A escada a subir entre paredes de papel de folhas", "entre paredes de folhas,"),
          ("escada-cima", "A escadaria vista de cima, com a sala lá em baixo", "até aos quartos.")]


def gesto_escada():
    fotos = "\n".join(f'        <figure class="escada__foto" data-passo>{img(n, a, "(max-width: 760px) 70vw, 34vw", lazy=False)}</figure>' for n, a, _ in ESCADA)
    linhas = "\n".join(f'      <p class="escada__linha">{t}</p>' for _, _, t in ESCADA)
    return f'''<section class="escada" id="escadaria" aria-labelledby="escada-titulo" data-presa data-topo-claro>
  <div class="escada__preso">
    <div class="escada__texto">
      <h2 class="escada__titulo" id="escada-titulo">A escadaria</h2>
{linhas}
    </div>
    <div class="escada__moldura" role="button" tabindex="0" data-visor="escada" data-indice="0" aria-label="Ver as fotografias da escadaria">
{fotos}
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- os três protótipos
PROTOTIPOS = {
    "a": {
        "titulo": "Praça",
        "fontes": "family=Forum&family=Ibarra+Real+Nova:ital,wght@0,400;0,500;1,400&family=Instrument+Sans:wght@400;500;600",
        "nome": ["Solar", "São João"],
        "nav": [("entrada", "A entrada"), ("quartos", "Quartos"), ("espacos", "Espaços comuns"), ("arredores", "Arredores")],
        "abertura": (("almofada", "Almofada de padrão geométrico na cama, com o candeeiro de latão"), ("porm-cadeira", "Poltrona de ferro com almofada florida, ao pé do espelho e do papel de parede de folhas")),
        "hero": "praca",
        "gesto": gesto_porta,
        "espacos": {"sala": ("Sala comum", "Sofás e poltronas, ao pé da escadaria.", ESPACOS["sala"][2][1:]
                             + [("porm-mesa", "Mesa de tronco com velas, diante do papel de parede de folhas", "A mesa de tronco")]),
                    "escada": ESPACOS["escada"],
                    "cozinha": ("Cozinha partilhada", ESPACOS["cozinha"][1], ESPACOS["cozinha"][2]
                                + [("porm-vela", "Vela acesa e fruta na mesa da cozinha", "Na mesa")])},
        "ec_frase": "A sala, a escadaria e a cozinha, para todos os hóspedes.",
        "fecho": ("suite-quente", "Suite de luz quente, com candeeiros suspensos e almofadas de padrão"),
        "arred": "A cidade do chapéu e do calçado, entre o Porto e Aveiro.",
        "cor": "#f3efe7",
    },
    "b": {
        "titulo": "Caminho",
        "fontes": "family=Sorts+Mill+Goudy:ital@0;1&family=Onest:wght@400;500;600",
        "nome": ["Solar", "São João"],
        "nav": [("caminho", "O Caminho"), ("quartos", "Quartos"), ("espacos", "Espaços comuns"), ("arredores", "Arredores")],
        "abertura": (("almofada", "Almofada de padrão geométrico na cama, com o candeeiro de latão"), ("sala-cadeira", "Cadeirão, espelho e papel de parede de folhas")),
        "gesto": gesto_caminho,
        "hero": "hero-sombra",
        "espacos": {"sala": ESPACOS["sala"], "escada": ESPACOS["escada"], "cozinha": ESPACOS["cozinha"]},
        "ec_frase": "A sala, a escadaria e a cozinha, para todos os hóspedes.",
        "fecho": ("suite-quente", "Suite de luz quente, com candeeiros suspensos e almofadas de padrão"),
        "arred": "A cidade do chapéu e do calçado, no Caminho de Santiago.",
        "cor": "#f1ebe0",
    },
    "c": {
        "titulo": "Escadaria",
        "fontes": "family=Italiana&family=Radley:ital@0;1&family=Karla:wght@400;500;600",
        "nome": ["Solar", "São João"],
        "nav": [("escadaria", "A escadaria"), ("quartos", "Quartos"), ("espacos", "Espaços comuns"), ("arredores", "Arredores")],
        "abertura": (("almofada", "Almofada de padrão geométrico na cama, com o candeeiro de latão"), ("sala-cadeira", "Cadeirão, espelho e papel de parede de folhas")),
        "gesto": gesto_escada,
        "espacos": {"sala": ("Sala comum", "Sofás e poltronas, ao pé da escadaria.", ESPACOS["sala"][2][:2]),
                    "cozinha": ESPACOS["cozinha"]},
        "ec_frase": "A sala e a cozinha, para todos os hóspedes.",
        "fecho": ("suite-quente", "Suite de luz quente, com candeeiros suspensos e almofadas de padrão"),
        "arred": "A cidade do chapéu e do calçado, entre o Porto e Aveiro.",
        "cor": "#f6f1e6",
    },
}


# ---------------------------------------------------------------- propostas de quartos (2026-10-21)
# Duas maneiras de mostrar os quartos, para o Eduardo escolher (paradas, sem animação; a escolhida
# é animada depois): por tipo (quartos-por-tipo.html) e todos os quartos (quartos-todos.html).
# Quartos e casas de banho de cada um: dossie/quartos.md, "Airbnb: um anúncio por quarto".
PRIV, PART = "Casa de banho privativa", "Casa de banho partilhada"
TIPOS = [
    {"k": "t1", "nome": "Quarto duplo", "camas": "Cama de casal", "wc": PRIV,
     "fotos": [("f-quarto-06", "Quarto duplo com cama de casal, cabeceira de veludo e candeeiros suspensos", "O quarto"),
               ("f-quarto-68", "Quarto duplo com cama de casal, toucador e espelho redondo", "Outro quarto duplo"),
               ("f-quarto-30", "Cama de casal com almofadas de padrão e candeeiros de latão", "A cama"),
               ("f-casa-de-banho-13", "Casa de banho privativa em mármore, com duche e espelho iluminado", PRIV),
               ("f-casa-de-banho-16", "Casa de banho privativa com chão de mosaico preto e branco", PRIV)], "wc_i": 3},
    {"k": "t2", "nome": "Suite com cama king", "camas": "Cama king", "wc": PRIV,
     "fotos": [("f-quarto-15", "Suite com cama king e papel de parede de folhas", "O quarto"),
               ("f-quarto-05", "A suite com a secretária e a janela", "A secretária"),
               ("f-casa-de-banho-09", "Casa de banho privativa da suite, com duche", PRIV)], "wc_i": 2},
    {"k": "t3", "nome": "Quarto familiar", "camas": "Duas camas de casal", "wc": PRIV,
     "fotos": [("f-quarto-12", "Quarto familiar com duas camas de casal e parede geométrica escura", "O quarto"),
               ("f-quarto-46", "Quarto familiar com duas camas de casal e quadros por cima", "Outro quarto familiar"),
               ("f-quarto-43", "Quarto familiar com duas camas de casal e chão de parquet", "Outro quarto familiar"),
               ("f-casa-de-banho-14", "Casa de banho privativa com espelho iluminado e escada-toalheiro", PRIV)], "wc_i": 3},
    {"k": "t4", "nome": "Quarto com casa de banho partilhada", "camas": "Cama de casal ou duas camas", "wc": PART,
     "fotos": [("f-quarto-82", "Quarto com duas camas e papel de parede dourado", "Duas camas"),
               ("f-quarto-23", "Quarto com cama de casal e almofada cor de laranja", "Cama de casal"),
               ("f-casa-de-banho-12", "Casa de banho partilhada com chão de mosaico preto e branco", PART)], "wc_i": 2},
]
CASAL, DUAS, KING, DUAS_C, TRES = "Cama de casal", "Duas camas", "Cama king", "Duas camas de casal", "Três camas"
# Todos os quartos por ordem de número, por andar (A 1.. = 1.º andar; confirmado por duas avaliações do
# Booking, ver dossie/quartos.md), com um filtro por tipo por cima. O anfitrião repete fotos entre anúncios:
# quando um quarto não tem foto só dele, usa-se uma foto representativa do seu próprio anúncio (A 105–A 107
# têm as mesmas duas fotos; A 208 a do quarto que o anúncio mostra); as casas de banho antigas (A 203,
# A 208, A 210, A 303, A 304, A 305) ficam de fora.
TIPOS_Q = {"duplo": "Quarto duplo", "suite": "Suite com cama king", "familiar": "Quarto familiar",
           "camas": "Duas ou três camas", "partilhada": "Casa de banho partilhada"}
TODOS = [  # quartos, tipo, camas, fotos do quarto, foto da casa de banho ou None
    (["A 101"], "duplo", CASAL, ["quarto-27", "detalhe-02"], "casa-de-banho-15"),
    (["A 102"], "partilhada", CASAL, ["quarto-23"], "casa-de-banho-02"),
    (["A 103"], "partilhada", DUAS, ["quarto-38"], None),
    (["A 104"], "duplo", CASAL, ["quarto-06", "quarto-30", "quarto-31", "quarto-60"], "casa-de-banho-13"),
    (["A 105"], "duplo", CASAL, ["quarto-14"], "casa-de-banho-01"),
    (["A 106"], "duplo", CASAL, ["quarto-63"], "casa-de-banho-17"),
    (["A 107"], "duplo", CASAL, ["quarto-63", "quarto-14"], "casa-de-banho-17"),
    (["A 201"], "duplo", CASAL, ["quarto-68", "quarto-69"], "casa-de-banho-16"),
    (["A 203"], "camas", TRES, ["quarto-70", "quarto-36", "quarto-37", "quarto-71"], None),
    (["A 204"], "suite", KING, ["quarto-15", "quarto-05"], "casa-de-banho-09"),
    (["A 205"], "duplo", CASAL, ["quarto-48"], None),
    (["A 206"], "camas", DUAS, ["quarto-72"], None),
    (["A 207"], "partilhada", DUAS, ["quarto-74"], "casa-de-banho-19"),
    (["A 208"], "partilhada", DUAS, ["quarto-29"], "casa-de-banho-20"),
    (["A 209"], "partilhada", DUAS, ["quarto-82", "quarto-83"], "casa-de-banho-12"),
    (["A 210"], "duplo", CASAL, ["quarto-84"], None),
    (["A 301"], "familiar", DUAS_C, ["quarto-12", "quarto-87", "quarto-09", "quarto-04"], "casa-de-banho-14"),
    (["A 302"], "familiar", DUAS_C, ["quarto-41"], "casa-de-banho-04"),
    (["A 303"], "duplo", CASAL, ["quarto-88"], None),
    (["A 304"], "familiar", DUAS_C, ["quarto-43", "quarto-44"], None),
    (["A 305"], "familiar", DUAS_C, ["quarto-46", "quarto-45", "quarto-47", "quarto-02"], None),
]
ANDAR = {"1": "1.º andar", "2": "2.º andar", "3": "3.º andar"}


def nome_q(qs):
    if len(qs) > 2:
        return f"{qs[0]} a {qs[-1]}"
    return qs[0] if len(qs) == 1 else " e ".join(qs)


def chave_q(qs):
    return "r" + qs[0].replace("A ", "")


def series_propostas():
    s = {}
    for t in TIPOS:
        s[t["k"]] = {"chave": t["k"], "titulo": t["nome"], "fotos": [foto_serie(*f) for f in t["fotos"]]}
    for qs, tipo, camas, fotos, f_wc in TODOS:
        if not fotos:
            continue
        n = nome_q(qs)
        wc = PART if tipo == "partilhada" else PRIV
        s[chave_q(qs)] = {"chave": chave_q(qs), "titulo": ("Quartos " if len(qs) > 1 else "Quarto ") + n.replace("A ", ""),
                          "fotos": [foto_serie("f-" + f, f"Quarto {n}: {camas.lower()}", "O quarto") for f in fotos]
                                   + ([foto_serie("f-" + f_wc, f"{wc} do quarto {n}", wc)] if f_wc else [])}
    return s


def cabeca_quartos(frase=""):
    f = f'\n    <p class="cabeca__frase">{frase}</p>' if frase else ""
    return f'''  <header class="cabeca largura">
    <h2 class="titulo" id="quartos-titulo">Quartos</h2>{f}
  </header>'''


def quartos_tipos():
    fichas = []
    for t in TIPOS:
        q, wc = t["fotos"][0], t["fotos"][t["wc_i"]]
        n = len(t["fotos"])
        fichas.append(f'''    <article class="tq">
      <div class="tq__texto">
        <h3 class="tq__nome">{t["nome"]}</h3>
        <p class="tq__linha">{t["camas"]}</p>
        <p class="tq__linha">{t["wc"]}</p>
        <button type="button" class="tq__ver" data-visor="{t["k"]}" data-indice="0">Ver as {n} fotografias {SETA}</button>
      </div>
      <button type="button" class="tq__foto" data-visor="{t["k"]}" data-indice="0" aria-label="Ver em grande: {escape(q[1])}">{img(q[0], q[1], "(max-width: 760px) 92vw, 46vw")}</button>
      <button type="button" class="tq__wc" data-visor="{t["k"]}" data-indice="{t["wc_i"]}" aria-label="Ver em grande: {escape(wc[1])}">{img(wc[0], wc[1], "(max-width: 760px) 40vw, 18vw")}<span>{t["wc"]}</span></button>
    </article>''')
    return f'''<section class="quartos quartos--tipos" id="quartos" aria-labelledby="quartos-titulo">
{cabeca_quartos()}
  <div class="tipos largura">
{chr(10).join(fichas)}
  </div>
</section>'''


def quartos_todos():
    seps = [f'<button type="button" aria-pressed="true" data-tipo="todos">Todos<sup>{sum(len(q[0]) for q in TODOS)}</sup></button>']
    for k, nome in TIPOS_Q.items():
        n = sum(len(q[0]) for q in TODOS if q[1] == k)
        seps.append(f'<button type="button" aria-pressed="false" data-tipo="{k}">{nome}<sup>{n}</sup></button>')
    andares = []
    for a in "123":
        cartoes = []
        for qs, tipo, camas, fotos, f_wc in TODOS:
            if qs[0][2] != a:
                continue
            n, k = nome_q(qs), chave_q(qs)
            wc = PART if tipo == "partilhada" else PRIV
            linha = TIPOS_Q[tipo] if tipo != "partilhada" else f"{camas} · {PART.lower()}"
            if tipo == "camas":
                linha = camas
            if fotos:
                foto = f'<button type="button" class="qq__foto" data-visor="{k}" data-indice="0" aria-label="Ver as fotografias do quarto {n}">{img("f-" + fotos[0], f"Quarto {n}: {camas.lower()}", "(max-width: 760px) 46vw, 23vw")}</button>'
            else:
                foto = f'<div class="qq__foto qq__foto--vazia" aria-hidden="true"><span>{n.replace("A ", "")}</span></div>'
            mini_wc = (f'<button type="button" class="qq__wc" data-visor="{k}" data-indice="{len(fotos)}" aria-label="Ver a casa de banho do quarto {n}">'
                       f'{img("f-" + f_wc, f"{wc} do quarto {n}", "90px")}</button>') if f_wc else ""
            cartoes.append(f'''        <li class="qq" data-tipo="{tipo}">
          {foto}
          <div class="qq__baixo">
            <div class="qq__texto"><h4 class="qq__nome">{n}</h4><p>{linha}</p></div>
            {mini_wc}
          </div>
        </li>''')
        andares.append(f'''    <div class="qq-andar">
      <h3 class="qq-andar__nome">{ANDAR[a]}</h3>
      <ol class="qq-grelha">
{chr(10).join(cartoes)}
      </ol>
    </div>''')
    return f'''<section class="quartos quartos--todos" id="quartos" aria-labelledby="quartos-titulo">
{cabeca_quartos()}
  <div class="todos largura" data-filtro>
    <div class="filtro" role="group" aria-label="Escolher o tipo de quarto">
      {chr(10).join("      " + b for b in seps).strip()}
    </div>
{chr(10).join(andares)}
  </div>
</section>'''

todas = {}
for chave, p in [("a", PROTOTIPOS["a"])]:
    s = series(p["espacos"])
    if chave == "c":
        s["escada"] = {"chave": "escada", "titulo": "A escadaria", "fotos": [foto_serie(n, a, t.rstrip(",.")) for n, a, t in ESCADA]}
    todas[chave] = s
    corpo = "\n\n".join([
        hero(p["nome"], p.get("hero", "hero")),
        abertura(*p["abertura"]),
        p["gesto"](),
        quartos(),
        espacos_comuns(p["espacos"], p["ec_frase"]),
        comodidades(),
        historia(),
        arredores(p["arred"]),
        fecho(*p["fecho"]),
    ])
    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Solar São João — Casa de hóspedes em São João da Madeira</title>
<meta name="description" content="Casa de hóspedes na Praça Luís Ribeiro, no centro de São João da Madeira: suites e quartos renovados, cozinha partilhada e sala comum.">
<meta property="og:title" content="Solar São João — São João da Madeira">
<meta property="og:description" content="Casa de hóspedes na praça central de São João da Madeira.">
<meta property="og:image" content="assets/img/{p.get("hero", "hero")}-1400.jpg">
<meta name="theme-color" content="{p["cor"]}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23262522'/%3E%3Ctext x='16' y='22' font-family='Georgia' font-size='17' fill='%23f4f0e8' text-anchor='middle'%3ES%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{p["fontes"]}&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="assets/img/{p.get("hero", "hero")}-2000.jpg" media="(min-width: 761px)">
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" href="assets/tema.css">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LodgingBusiness","name":"Solar São João","alternateName":"Je T'aime Solar São João",
"address":{{"@type":"PostalAddress","streetAddress":"Praça Luís Ribeiro, 165","postalCode":"3700-172","addressLocality":"São João da Madeira","addressCountry":"PT"}},
"geo":{{"@type":"GeoCoordinates","latitude":40.899349,"longitude":-8.492242}},"telephone":"{TEL}"}}
</script>
</head>
<body class="prototipo-{chave}">

<a class="saltar" href="#abertura">Saltar para o conteúdo</a>

{topo(p["nav"])}

<main>

{corpo}

</main>

{rodape()}

<script src="assets/series.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.min.js"></script>
<script src="assets/gesto.js"></script>
<script src="assets/motor.js"></script>
</body>
</html>
'''
    (SITE / "index.html").write_text(html, encoding="utf-8")
    # as duas propostas de quartos: a mesma página, só com a secção dos quartos trocada
    s.update(series_propostas())
    for nome, bloco in (("quartos-por-tipo", quartos_tipos()), ("quartos-todos", quartos_todos())):
        (SITE / f"{nome}.html").write_text(html.replace(quartos(), bloco), encoding="utf-8")
    (SITE / "assets" / "series.js").write_text("window.SERIES = " + json.dumps(s, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print("site", len(html) // 1024, "KB")
