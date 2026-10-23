# Solar São João — São João da Madeira

Je T'aime Solar São João, casa de hóspedes na Praça Luís Ribeiro, 165, no centro
de São João da Madeira. Alojamento Local na modalidade de quartos, RNAL 113396/AL
(Branco Suave, Lda.). No site chama-se **Solar São João**, como está escrito na
fachada ("SOLAR S. JOÃO").

## Pastas

O dossiê, o arquivo e a proposta não vão para este repositório (é público): só o site, os scripts e a configuração da Netlify.

- `dossie/` — dossiê da casa (skill al-dossier). Entrada: `dossie/resumo.md`; o que o site pode dizer: `dossie/site-pronto.md`.
- `site/` — o site (a proposta A), sem build, abre com duplo clique.
  - `index.html` — a página (gerada).
  - `quartos-por-tipo.html` — a página com os quartos por tipo (4 tipos, cada um com a sua casa de banho).
  - `quartos-todos.html` — a página com todos os quartos por andar e um filtro por tipo.
  - `assets/base.css` e `assets/motor.js` — a estrutura (quartos, espaços comuns, comodidades, galeria, arredores, visor, telemóvel).
  - `assets/tema.css` e `assets/gesto.js` — a identidade A: letra, paleta e a porta.
  - `assets/series.js` — as fotos do visor e dos espaços comuns (geradas).
  - `assets/img/` — o original de cada foto (copiado sem recomprimir) e tamanhos de 800 e 1400 px (JPEG 90, 4:4:4).
- `arquivo/v1-2026-10-21-prototipos/` — as três propostas e a página de escolha, tal como foram mostradas, com o gerador delas (`monta.py`); as fotos são as de `site/assets/img` (ligação).
- `scripts/imagens.py` — gera `site/assets/img/` a partir do dossiê e das fotos da região (`python3 scripts/imagens.py`; sem `-I`, o Pillow está nos pacotes `--user`). As fotos da região ficam em cache em `scripts/_regiao/`.
- `scripts/monta.py` — gera `site/index.html` e as séries (`python3 scripts/monta.py`). Textos, legendas e listas de fotos mudam-se lá.

## Versão base: três propostas (2026-10-21)

Inspiração: Casa do Poço, Boa Nova Convento e Quinta da Malhada, sem copiar.
O conteúdo é o mesmo nas três; muda a identidade.

Enredo comum: a praça (hero, um ecrã) → a abertura → o gesto de cada proposta →
os quartos → os espaços comuns → as comodidades → a casa desde 1985 → os
arredores → «Venha visitar-nos».

| | A · Praça | B · Caminho | C · Escadaria |
|---|---|---|---|
| Letras | Forum (nome, em maiúsculas como na fachada) + Ibarra Real Nova + Instrument Sans | Sorts Mill Goudy (nome e títulos, com itálico) + Onest | Italiana (nome, maiúsculas finas) + Radley + Karla |
| Paleta | cal e pedra da fachada, grafite das grades, mel do parquet (botões) | linho, azul das mantas (quartos, comodidades), mostarda das almofadas (botões) | creme, verde do papel de parede de folhas, latão dos candeeiros (botões) |
| Nome no hero | grafite, numa linha, assente na calçada | branco, com uma sombra natural na calçada (`hero-sombra.jpg`) | verde-escuro fino, na calçada |
| Gesto | **A entrada:** uma moldura do tamanho de uma porta, com o «165» por cima, abre-se com o scroll até à sala inteira (a foto fica do mesmo tamanho) | **O Caminho:** o Caminho Português de Lisboa a Santiago desenha-se com o scroll, pára em São João da Madeira (o ponto da casa pulsa) e segue | **A escadaria:** secção presa; cada lanço entra de baixo por cima do anterior, com a frase a acompanhar |

Comum às três:
- **Hero:** a fachada na praça (3000 px), tratada como foto ao sol (meio baixado, altas luzes encolhidas, um pouco mais quente). No telemóvel, um corte ao alto com o edifício ao centro.
- **Abertura:** a almofada em grande e o cadeirão num cartão sobreposto, que sobe mais depressa; a frase sai de uma névoa com o scroll.
- **Quartos** (como na Boa Vida): Suite com vista, Suite dupla, Quarto familiar e Quarto duplo, um passo de scroll cada. Cada um tem um cartão com a sua casa de banho privativa. As fotos de cada quarto são da mesma unidade do Booking (galeria de uma só unidade). O Quarto duplo é o anúncio A 201 do Airbnb.
- **Espaços comuns:** só uma galeria: separadores (Tudo, Sala comum, Escadaria, Cozinha partilhada; no C sem a escadaria, que é o gesto) e a fila de fotos no formato original que se arrasta; carregar abre o visor só dessa divisão.
- **Comodidades:** a fita do Solar Antigo, só com o que o contrato permite (sem estacionamento nem pequeno-almoço; o ar condicionado "nas suites maiores e nos quartos familiares").
- **Na praça desde 1985:** a data do RNT e a renovação, com a foto da rua dos chapéus. A frase dos anfitriões (perfil do Airbnb) ia como subtítulo dos arredores (tirada na ronda 2).
- **Arredores:** Museu da Chapelaria, Torre da Oliva, Parque de Nossa Senhora dos Milagres (1,5 km) e Castelo da Feira (6 km), com as distâncias do Booking. Fotos do Wikimedia Commons, com a marca de água cortada.
- Botões de 42 px, .875rem, cantos de 4 px; fotos sem `will-change` fixo.
- Testado no Chromium (Playwright): PC 1440×900 e 1920×1080, telemóvel 390×844, 844×390 e 667×375 (quartos e escadaria lado a lado, fecho em duas colunas, visor sem miniaturas), tablet 820×1180; cliques do visor, espaços, cartões e separadores; CPU abrandado 4× (60 fps, nenhuma imagem acima de 50 ms).

## Ronda 2 (2026-10-21): escolhida a A

O Eduardo escolheu a proposta A em todas as secções (hero, entrada, espaços
comuns, comodidades). A A passou a `site/index.html`; as três ficam em
`arquivo/v1-2026-10-21-prototipos/`.
- **Abertura:** a almofada (mais alta do que o ecrã) e o cartão sobreposto
  escondiam-se. Agora as duas fotos estão lado a lado, desencontradas na altura,
  cada uma inteira, e o bloco cabe num ecrã; a almofada em 2:3 (cortado só o
  lençol em baixo), a sala no formato original, a subir um pouco mais depressa.
- **Na praça desde 1985:** a foto da rua dos chapéus maior (grelha 7:4).
- **Arredores:** sem a frase dos anfitriões; o subtítulo é «A cidade do chapéu
  e do calçado, entre o Porto e Aveiro.»

## Ronda 3 (2026-10-21): os quartos do Airbnb

- O anfitrião vende cada quarto num anúncio do Airbnb ("A 101" a "A 305", 21 quartos; 13 no RNT, 20 no Booking). Recolhidos para o dossiê (ver `dossie/quartos.md`, "Airbnb: um anúncio por quarto"): 52 fotos novas e 14 trocadas pela versão maior; cada foto diz de que quarto é.
- Os quartos da secção atual são o A 204 (Suite com vista), o A 305 (Suite dupla), o A 301 (Quarto familiar) e o A 201 (Quarto duplo). A casa de banho mostrada na Suite dupla (`q2-wc`) é de outros quartos (A 102, A 208, A 302): corrigir quando se escolher a proposta.
- Duas propostas para a secção, paradas (a escolhida é animada depois):
  - `quartos-por-tipo.html` **por tipo**: Quarto duplo, Suite com cama king, Quarto familiar e Quarto com casa de banho partilhada; cada um com a foto do quarto e a da sua casa de banho lado a lado, inteiras, e o visor com as fotos do tipo.
  - `quartos-todos.html` **todos os quartos**, por ordem de número e por andar (A 1.. = 1.º andar, A 2.. = 2.º, A 3.. = 3.º), com um filtro por tipo por cima (Todos, Quarto duplo, Suite com cama king, Quarto familiar, Duas ou três camas, Casa de banho partilhada; sem filtro por andar). Cada quarto tem o seu cartão; sem foto só dele, uma foto representativa do seu próprio anúncio (A 106 e A 107 partilham a mesma); casas de banho antigas fora.
- Botões e destaques: o mel do parquet (laranja) passou ao verde-escuro do papel de parede de folhas da escadaria (`--destaque` em `tema.css`), com o verde-claro da fachada nos ícones sobre o grafite.
- Pormenores: cada um na sua divisão, sem separador próprio (pedido do Eduardo): a mesa de tronco na Sala comum, a vela na Cozinha partilhada, a poltrona de veludo no visor do A 101 (é do anúncio dele). A secretária com rosas (`detalhe-05`, de uma suite sem quarto identificado) fica de fora; `detalhe-03/04` são capturas de ecrã e `detalhe-06` repete a `-05`. No telemóvel a fila de separadores desliza sozinha.
- Espaços comuns: a galeria já não esbate as outras fotos nem levanta a escolhida ao passar o cursor.

## Ronda 4 (2026-10-21): hero e abertura

- **Hero:** a praça em panorama enviada pelo Eduardo (`dossie/marketing/fotos/exterior/fachada-07.jpg`, 3168×1344; a `fachada-06` é a primeira edição, trocada a pedido dele), sem tratamento de cor (`site/assets/img/praca*.jpg`). O panorama tinha pouca calçada e o nome caía em cima das cadeiras da esplanada: o chão continua para baixo em perspetiva (+320 px; `prolonga_chao` em `scripts/imagens.py`): cada faixa nova é a de baixo ampliada por igual nos dois eixos a partir do ponto de fuga, cosida com um degradê, alternando o sentido e com o grão da foto. A 1.ª versão esticava só na vertical e o Eduardo achou que se notava («esticada», «parece IA»). No telemóvel, um corte ao alto com o letreiro ao centro. A fachada antiga (`hero*.jpg`) fica para as propostas em arquivo.
- **Abertura:** a almofada e a poltrona de ferro com a almofada florida (pormenor da sala), em vez da vista larga da sala.

## Ronda 5 (2026-10-22): fluidez

O Eduardo achou o site lento e travado. Medido no Chromium (roda do rato, CPU 4× mais lento): frames
lentos sobretudo nos quartos, na entrada e no fecho. Corrigido:
- `motor.js`: o ciclo corria duas vezes por frame (Lenis + scroll nativo); agora só no evento do Lenis.
  Mede tudo primeiro e escreve depois, e só o que mudou (`poe`). As fotos que se mexem (`data-vel`,
  `data-entra`, as dos arredores) têm camada própria só enquanto mexem (`.mexe`). As velocidades já não
  medem o próprio desvio. Lenis com `wheelMultiplier: 1`.
- A porta e a moldura dos quartos abriam com `clip-path`, que repintava a foto do ecrã inteiro a cada
  frame: agora quatro faixas na cor da página (`.vao`, em `base.css`) saem para fora com `transform`. O
  «165» e a «Praça Luís Ribeiro» vão presos às faixas.
- As palavras da névoa e as letras do nome largam o filtro quando ficam nítidas. Os traços dos quartos
  e o degradê ficam numa camada própria (já não repintam a foto).
- Telemóvel: a foto da entrada levava a versão de 800 px num ecrã ao alto (desfocada); agora o `sizes`
  conta com a altura (`cobre()` em `monta.py`). O hero ao alto declara a largura real (1331w).
- Resultado (CPU 4×): de 132 frames lentos nos quartos e 27 na entrada para ~20 nos quartos (só nas
  trocas de foto) e 0 em todas as outras secções. Telemóvel 390×844, 360×740 e 844×390: sem frames
  lentos e sem nada a transbordar.
- Depois, «o scroll vai com lag»: o Lenis suavizava também o trackpad, que já tem inércia própria, e a
  página arrastava-se atrás do dedo. Agora o trackpad e o Magic Mouse usam o scroll nativo (reconhecidos
  pelos passos pequenos, fracionários ou de lado, no `virtualScroll` do Lenis); só a roda do rato é
  suavizada, com `lerp: 0.12`. As animações seguem os dois.

## Ronda 6 (2026-10-22): os verdes da árvore

- A pedido do Eduardo (experiência): o nome do hero passou do grafite aos verdes da árvore grande da
  praça, tirados da própria foto: degradê de cima para baixo, das folhas ao sol (`--folha-sol` #7a8526)
  à meia-sombra (`--destaque` #4a5a1c) e à sombra (`--folha-sombra` #2c3a10), letra a letra.
- O mesmo verde passou a ser o `--destaque` (antes #4a5d4b, do papel de folhas): botão do topo, do
  fecho e da barra do telemóvel. O «Ver disponibilidade» do hero, que era claro com texto escuro,
  passou a verde cheio com texto branco.
- Para voltar atrás: em `site/assets/tema.css`, `--destaque: #4a5d4b; --destaque-2: #3a4a3b;` e o nome
  em `color: var(--tinta)` sem o degradê.
