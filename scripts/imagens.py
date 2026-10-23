# Prepara site/assets/img/ a partir do dossiê e das fotos da região (Wikimedia Commons).
# Uso (a partir da pasta da casa): python3 scripts/imagens.py  (sem -I: o Pillow está nos pacotes --user)
# - fotos da casa: o maior tamanho é o ficheiro original, copiado sem recomprimir;
#   os menores (800, 1400) em JPEG 90 com cor 4:4:4, nunca maiores do que o original.
# - hero: a fachada tirada ao sol, com o meio baixado e as altas luzes encolhidas
#   (a calçada vinha quase branca); mais um corte ao alto para o telemóvel.
# - região: corte da marca de água em baixo, reduzidas a 2400 px de largura.
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

CASA = Path(__file__).resolve().parent.parent
FOTOS = CASA / "dossie" / "marketing" / "fotos"
REGIAO = CASA / "scripts" / "_regiao"
SAIDA = CASA / "site" / "assets" / "img"
SAIDA.mkdir(parents=True, exist_ok=True)

CASA_FOTOS = {
    # quartos
    "q1-quarto": "interior/quarto-15.jpg", "q1-b": "interior/quarto-05.jpg", "q1-wc": "interior/casa-de-banho-09.jpg",
    "q2-quarto": "interior/quarto-46.jpg", "q2-b": "interior/quarto-45.jpg", "q2-c": "interior/quarto-47.jpg", "q2-wc": "interior/casa-de-banho-12.jpg",
    "q3-quarto": "interior/quarto-48.jpg", "q3-b": "interior/quarto-12.jpg", "q3-c": "interior/quarto-11.jpg", "q3-d": "interior/quarto-04.jpg",
    "q3-wc": "interior/casa-de-banho-14.jpg", "q3-wc2": "interior/casa-de-banho-13.jpg",
    "q4-quarto": "interior/quarto-68.jpg", "q4-b": "interior/quarto-69.jpg", "q4-wc": "interior/casa-de-banho-16.jpg",
    # espaços comuns
    "sala-alta": "interior/sala-10.jpg", "sala-sofas": "interior/sala-12.jpg", "sala-escada": "interior/sala-03.jpg",
    "sala-luz": "interior/sala-11.jpg", "sala-longa": "interior/sala-06.jpg", "sala-cadeira": "interior/sala-04.jpg",
    "escada-sobe": "interior/escada-01.jpg", "escada-ferro": "interior/escada-02.jpg", "escada-cima": "interior/escada-03.jpg",
    "escada-poco": "interior/escada-04.jpg",
    "cozinha": "interior/cozinha-02.jpg", "cozinha-bancada": "interior/cozinha-03.jpg", "cozinha-janela": "interior/cozinha-04.jpg",
    "cozinha-ilha": "interior/cozinha-05.jpg",
    # pormenores e outros quartos (galeria, fecho)
    "almofada": "interior/detalhe-01.jpg",
    "porm-cadeira": "interior/sala-01.jpg", "porm-mesa": "interior/sala-02.jpg", "porm-vela": "interior/detalhe-07.jpg",
    "suite-quente": "interior/quarto-06.jpg", "suite-candeeiros": "interior/quarto-30.jpg", "suite-verde": "interior/quarto-13.jpg",
    "suite-noite": "interior/quarto-34.jpg", "familiar-verde": "interior/quarto-41.jpg", "dupla-b": "interior/quarto-43.jpg",
    "dupla-c": "interior/quarto-02.jpg", "suite-luz": "interior/quarto-66.jpg",
}

REGIAO_FOTOS = {
    # nome: (ficheiro em _regiao, fração a cortar em baixo por causa da marca de água)
    "chapelaria": ("chapelaria4.jpg", 0.0),
    "chapeus": ("chapeus.jpg", 0.05),
    "oliva": ("oliva.jpg", 0.05),
    "milagres": ("milagres.jpg", 0.045),
    "castelo": ("castelo.jpg", 0.0),
}


def guarda(im, destino, largura):
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    im.convert("RGB").save(destino, quality=90, subsampling=0, optimize=True, progressive=True)


medidas = {}
# fotos das propostas de quartos (por tipo e quarto a quarto), com a chave f-<ficheiro>
PROPOSTAS = ["quarto-%02d" % n for n in (2, 4, 5, 6, 9, 12, 14, 15, 23, 24, 27, 29, 30, 31, 36, 37, 38, 41, 43, 44, 45, 46, 47, 48, 60, 63,
                                         68, 69, 70, 71, 72, 74, 82, 83, 84, 87, 88)] + ["detalhe-02"] + \
            ["casa-de-banho-%02d" % n for n in (1, 2, 4, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24)]
for f in PROPOSTAS:
    CASA_FOTOS.setdefault("f-" + f, f"interior/{f}.jpg")

for nome, rel in CASA_FOTOS.items():
    origem = FOTOS / rel
    shutil.copyfile(origem, SAIDA / f"{nome}.jpg")
    im = Image.open(origem)
    medidas[nome] = im.size
    for w in (800, 1400):
        if im.width > w * 1.15:
            guarda(im, SAIDA / f"{nome}-{w}.jpg", w)

# hero: a fachada ao sol
fachada = Image.open(FOTOS / "exterior" / "fachada-01.jpg").convert("RGB")
lut = []
for i in range(256):
    v = i / 255
    v = v ** 1.18                       # baixa o meio
    if v > 0.78:                        # encolhe as altas luzes
        v = 0.78 + (v - 0.78) * 0.62
    lut.append(round(v * 255))
heroi = fachada.point(lut * 3)
heroi = ImageEnhance.Color(heroi).enhance(1.04)
r, g, b = heroi.split()                 # um pouco mais quente
r = r.point(lambda x: min(255, round(x * 1.02)))
b = b.point(lambda x: round(x * 0.97))
heroi = Image.merge("RGB", (r, g, b))
heroi.save(SAIDA / "hero.jpg", quality=93, subsampling=0, optimize=True, progressive=True)
# variante com uma sombra natural na calçada (para um nome branco por cima): escurece
# devagar a partir de 60% da altura, sem véu na página
W0, H0 = heroi.size
mascara = Image.new("L", (1, H0))
for y in range(H0):
    t = max(0.0, (y / H0 - 0.6) / 0.4)
    mascara.putpixel((0, y), round(255 * (1 - 0.34 * t * t * (3 - 2 * t))))
mascara = mascara.resize((W0, H0))
sombra = Image.composite(heroi, Image.new("RGB", heroi.size, (40, 34, 28)), mascara)
sombra.save(SAIDA / "hero-sombra.jpg", quality=93, subsampling=0, optimize=True, progressive=True)
for w in (1400, 2000):
    guarda(sombra, SAIDA / f"hero-sombra-{w}.jpg", w)
for w in (1400, 2000):
    guarda(heroi, SAIDA / f"hero-{w}.jpg", w)
# corte ao alto para o telemóvel: o edifício ao centro, a calçada em baixo para o nome
W, H = heroi.size
cw = round(H * 0.8)
x0 = round(W * 0.47 - cw / 2)
alto = heroi.crop((x0, 0, x0 + cw, H))
alto.save(SAIDA / "hero-alto.jpg", quality=92, subsampling=0, optimize=True, progressive=True)
guarda(alto, SAIDA / "hero-alto-800.jpg", 800)
alto_s = sombra.crop((x0, 0, x0 + cw, H))
alto_s.save(SAIDA / "hero-sombra-alto.jpg", quality=92, subsampling=0, optimize=True, progressive=True)
guarda(alto_s, SAIDA / "hero-sombra-alto-800.jpg", 800)
medidas["hero"] = heroi.size
medidas["hero-alto"] = alto.size

# hero da proposta escolhida: a praça em panorama (enviada pelo Eduardo), sem tratamento de cor.
# O panorama tem pouca calçada para o nome, que caía nas cadeiras da esplanada: o chão continua
# para baixo em perspetiva (+320 px). Cada faixa nova é a faixa de baixo ampliada por igual nos
# dois eixos a partir do ponto de fuga, como chão mais perto da câmara (nunca esticada só na
# vertical: as pedras ficavam compridas e desfocadas), cosida com um degradê e com o grão da foto.
def prolonga_chao(im, extra, horizonte, a0, costura=14):
    W, H = im.size
    cx = W / 2
    tela = Image.new("RGB", (W, H + extra))
    tela.paste(im, (0, 0))
    k = (H - horizonte) / (a0 - horizonte)
    B, passo = H, 0
    while B < H + extra:
        B2 = round(horizonte + k * (B - horizonte))
        topo = B - costura
        A = horizonte + (topo - horizonte) / k
        faixa = tela.crop((round(cx - cx / k), round(A), round(cx + (W - cx) / k), B)).resize((W, B2 - topo), Image.LANCZOS)
        if passo % 2:
            faixa = ImageOps.mirror(faixa)       # alterna o sentido, para as manchas não se repetirem em fila
        mascara = Image.new("L", faixa.size, 255)
        for y in range(costura):
            mascara.paste(round(255 * y / costura), (0, y, W, y + 1))
        tela.paste(faixa, (0, topo), mascara)
        B, passo = B2, passo + 1
    chao = tela.crop((0, H, W, H + extra)).filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    grao = Image.effect_noise(chao.size, 6).filter(ImageFilter.GaussianBlur(0.5))
    chao = ImageChops.add(chao, Image.merge("RGB", (grao, grao, grao)), scale=1, offset=-128)
    tela.paste(chao, (0, H))
    return tela


praca = prolonga_chao(Image.open(FOTOS / "exterior" / "fachada-07.jpg").convert("RGB"), 320, 1060, 1285)
praca.save(SAIDA / "praca.jpg", quality=93, subsampling=0, optimize=True, progressive=True)
for w in (1400, 2000):
    guarda(praca, SAIDA / f"praca-{w}.jpg", w)
W, H = praca.size
cw = round(H * 0.8)                     # telemóvel: o corte ao alto com o letreiro ao centro
x0 = round(W * 0.485 - cw / 2)
alto = praca.crop((x0, 0, x0 + cw, H))
alto.save(SAIDA / "praca-alto.jpg", quality=92, subsampling=0, optimize=True, progressive=True)
guarda(alto, SAIDA / "praca-alto-800.jpg", 800)
medidas["praca"] = praca.size
medidas["praca-alto"] = alto.size

for nome, (ficheiro, corte) in REGIAO_FOTOS.items():
    im = Image.open(REGIAO / ficheiro).convert("RGB")
    if corte:
        im = im.crop((0, 0, im.width, round(im.height * (1 - corte))))
    guarda(im, SAIDA / f"regiao-{nome}.jpg", 2400)
    guarda(im, SAIDA / f"regiao-{nome}-1400.jpg", 1400)
    guarda(im, SAIDA / f"regiao-{nome}-800.jpg", 800)
    medidas[f"regiao-{nome}"] = Image.open(SAIDA / f"regiao-{nome}.jpg").size

(CASA / "scripts" / "medidas.json").write_text(json.dumps(medidas, indent=1))
print(len(medidas), "imagens")
