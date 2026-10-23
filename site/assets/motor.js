/* Solar São João — motor comum aos três protótipos. Sem build: abre por duplo-clique.
   Tudo o que mexe com o scroll é calculado num só ciclo, no evento do Lenis.
   Cada protótipo usa as peças que tem na página:
   - [data-palavras]  frase que sai de uma névoa, palavra a palavra, com o scroll
   - [data-entra]     fotos que se abrem ao entrar e sobem e se esvaem ao sair
   - [data-vel]       velocidades diferentes no scroll
   - [data-presa]     secção presa: recebe --p (0 → 1) e os [data-passo] lá dentro recebem --a
   - [data-qp]        quartos (como na Boa Vida): um passo de scroll por quarto
   - [data-ec]        espaços comuns: lista das divisões + moldura que toma a forma de cada foto
   - [data-comod]     comodidades: a fila que anda sozinha, pára com o rato e se arrasta
   - .galeria         separadores + fila de fotos que se arrasta
   - .lugar / .af     arredores: o texto corre e a foto presa troca
   - #visor           visor por espaço, sempre com o ficheiro original */
(() => {
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const limita = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const suave = (t) => t * t * (3 - 2 * t);
  let vh = innerHeight;
  // escreve só o que mudou (cada escrita igual à anterior ainda custava um recálculo de estilos)
  const poe = (el, k, v) => { const c = el._c || (el._c = {}); if (c[k] !== v) { c[k] = v; el.style.setProperty(k, v); } };
  // camada própria só enquanto mexe (sem will-change fixo: tira nitidez); parada, volta a ser pintada nítida
  const camada = (el, sim, cls = 'mexe') => { const m = el._m || (el._m = {}); if (m[cls] !== sim) { m[cls] = sim; el.classList.toggle(cls, sim); } };

  /* ---------- scroll suave ---------- */
  let lenis = null;
  if (!reduz && window.Lenis) {
    /* O trackpad (e o Magic Mouse) já tem inércia própria: suavizá-lo outra vez punha a página a
       arrastar-se atrás do dedo («vai com lag»). Esses gestos ficam com o scroll nativo; só a roda do
       rato, aos saltos, é suavizada. Reconhece-se o trackpad pelos passos pequenos ou fracionários e
       pelo movimento de lado; fica assim enquanto o gesto (e a inércia dele) durar. */
    let tpAte = 0;
    const eTrackpad = (e) => {
      if (e.deltaMode !== 0) return false;
      const y = Math.abs(e.deltaY);
      return e.deltaX !== 0 || y < 4 || !Number.isInteger(e.deltaY);
    };
    lenis = new Lenis({
      lerp: 0.12, wheelMultiplier: 1, smoothWheel: true,
      virtualScroll: ({ event }) => {
        if (event.type !== 'wheel') return true;
        const agora = performance.now();
        const era = agora < tpAte;
        if (eTrackpad(event) || era) {
          tpAte = agora + 250;
          // se a roda ainda estava a deslizar, pára onde está (sem salto) e deixa seguir o nativo
          if (!era && lenis.isScrolling === 'smooth') lenis.scrollTo(lenis.animatedScroll, { immediate: true, force: true });
          return false;
        }
        return true;
      },
    });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  const irPara = (y, imediato = false) => {
    if (lenis) lenis.scrollTo(y, { immediate: imediato, force: true, duration: 1.4 });
    else scrollTo({ top: y, behavior: imediato || reduz ? 'auto' : 'smooth' });
  };
  const topoDe = (el) => el.getBoundingClientRect().top + scrollY;

  /* ---------- palavras (névoa ligada ao scroll) e letras do nome ---------- */
  const nevoas = $$('[data-palavras]');
  nevoas.forEach((el) => {
    let i = 0;
    el.innerHTML = el.textContent.trim().split(/\s+/).map((p) => `<span class="p" style="--i:${i++}">${p}</span>`).join(' ');
    el.style.setProperty('--np', i);
  });
  const titulo = $('.hero__titulo');
  let li = 0;
  if (titulo) $$(':scope > span', titulo).forEach((pal) => {
    pal.innerHTML = [...pal.textContent].map((c) => `<span class="l" style="--i:${li++}">${c === ' ' ? '&nbsp;' : c}</span>`).join('');
  });

  /* ---------- hero pronto ---------- */
  const hero = $('.hero');
  const heroImg = $('.hero__foto img');
  const pronto = () => requestAnimationFrame(() => hero.classList.add('pronto'));
  if (heroImg.complete) pronto(); else { heroImg.addEventListener('load', pronto); setTimeout(pronto, 1600); }

  /* ---------- elementos ---------- */
  const topo = $('.topo');
  const barra = $('.barra');
  const fecho = $('.fecho');
  const vels = $$('[data-vel]');
  const entram = $$('[data-entra]');
  const presas = $$('[data-presa]').map((el) => ({ el, passos: $$('[data-passo]', el) }));
  const escuros = $$('[data-topo-claro]');   // secções a ecrã inteiro onde o topo fica transparente

  /* ---------- QUARTOS: um passo de scroll por quarto ---------- */
  const qp = $('[data-qp]');
  let pintaQuartos = () => {};
  if (qp) {
    const qMoldura = $('.qp__moldura', qp);
    const qFotos = $$('.qp__foto', qp);
    const qTextos = $$('.qp__quarto', qp);
    const qTabs = $$('.qp__linha button', qp);
    const qTracos = qTabs.map((b) => $('.qp__traco span', b) || b);   // o --b no próprio traço: no botão repintava a fila
    const qWcs = $$('.qp__wc', qp);
    const qN = qFotos.length;
    qp.style.setProperty('--n', qN);
    let qAtual = 0;
    const qPronta = (f) => { const im = $('img', f); return im.complete ? Promise.resolve() : im.decode().catch(() => {}); };
    const mostraQuarto = (q) => {
      if (q === qAtual) return;
      const nova = qFotos[q];
      qAtual = q;
      qTextos.forEach((t, i) => t.classList.toggle('ativo', i === q));
      qWcs.forEach((w) => w.classList.toggle('ativo', +w.dataset.q === q));
      qTabs.forEach((b, i) => b.setAttribute('aria-pressed', i === q ? 'true' : 'false'));
      qPronta(nova).then(() => {
        if (qAtual !== q) return;
        qFotos.forEach((f) => { if (f !== nova && f.classList.contains('ativo')) { f.classList.remove('ativo'); f.classList.add('sai'); clearTimeout(f._t); f._t = setTimeout(() => f.classList.remove('sai'), 1300); } });
        clearTimeout(nova._t); nova.classList.remove('sai'); nova.classList.add('ativo');
      });
    };
    pintaQuartos = (r) => {
      if (r.top > vh || r.bottom < 0) return;
      const p = limita(-r.top / (r.height - vh));
      mostraQuarto(Math.min(qN - 1, Math.floor(p * qN)));
      qTracos.forEach((b, i) => poe(b, '--b', (reduz ? (i <= qAtual ? 1 : 0) : limita(p * qN - i)).toFixed(3)));
      const q = reduz ? 1 : suave(limita((vh - r.top) / (vh * 0.85)));
      poe(qMoldura, '--q', q.toFixed(4));
    };
    qTabs.forEach((b, i) => b.addEventListener('click', () => irPara(topoDe(qp) + (i + 0.5) / qN * (qp.offsetHeight - vh))));
  }

  /* ---------- arredores: a foto presa troca quando o texto seguinte chega ---------- */
  const lugares = $$('.lugar');
  const afs = $$('.af');

  /* ---------- GALERIA: separadores + fila que se arrasta ---------- */
  const gFila = $('.galeria__fila');
  if (gFila) {
    const gSeps = $$('.separadores [role="tab"]');
    const gFilete = $('.separadores__filete');
    const gFotos = $$('.gf', gFila);
    const gBarra = $('.galeria__barra');
    const gPolegar = $('i', gBarra);
    let gDiv = 'tudo', gPedido = 0;
    const poeFilete = () => {
      const b = gSeps.find((x) => x.dataset.div === gDiv);
      gFilete.style.width = `${b.offsetWidth}px`;
      gFilete.style.transform = `translate3d(${b.offsetLeft}px, 0, 0)`;
    };
    const pintaBarra = () => {
      const w = gFila.scrollWidth, c = gFila.clientWidth;
      gBarra.hidden = c / w > 0.995;
      gPolegar.style.width = `${(c / w * 100).toFixed(2)}%`;
      gPolegar.style.left = `${(gFila.scrollLeft / w * 100).toFixed(2)}%`;
    };
    const numera = () => { let k = 0; gFotos.forEach((g) => { if (!g.hidden) g.style.setProperty('--k', k++); }); };
    const escolheDiv = (d) => {
      if (d === gDiv) return;
      gDiv = d; const meu = ++gPedido;
      gSeps.forEach((x) => { const sim = x.dataset.div === d; x.setAttribute('aria-selected', sim ? 'true' : 'false'); x.tabIndex = sim ? 0 : -1; });
      poeFilete();
      gFila.classList.remove('chega'); gFila.classList.add('sai');
      setTimeout(() => {
        if (meu !== gPedido) return;
        gFotos.forEach((g) => { g.hidden = d !== 'tudo' && g.dataset.div !== d; });
        numera();
        gFila.scrollLeft = 0;
        gFila.classList.remove('sai'); void gFila.offsetWidth; gFila.classList.add('chega');
        pintaBarra();
      }, reduz ? 0 : 260);
    };
    gSeps.forEach((x, i) => {
      x.tabIndex = i ? -1 : 0;
      x.addEventListener('click', () => escolheDiv(x.dataset.div));
      x.addEventListener('keydown', (e) => {
        const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!d) return;
        const n = gSeps[(i + d + gSeps.length) % gSeps.length];
        n.focus(); escolheDiv(n.dataset.div);
      });
    });
    let gAgarra = null, gArrastou = false;
    gFila.addEventListener('pointerdown', (e) => {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      gAgarra = { x: e.clientX, s: gFila.scrollLeft, id: e.pointerId }; gArrastou = false;
    });
    gFila.addEventListener('pointermove', (e) => {
      if (!gAgarra) return;
      const dx = e.clientX - gAgarra.x;
      if (!gArrastou && Math.abs(dx) > 6) { gArrastou = true; gFila.classList.add('agarrada'); gFila.setPointerCapture(gAgarra.id); }
      if (gArrastou) gFila.scrollLeft = gAgarra.s - dx;
    });
    const gLarga = () => { if (!gAgarra) return; gAgarra = null; gFila.classList.remove('agarrada'); };
    gFila.addEventListener('pointerup', gLarga);
    gFila.addEventListener('pointercancel', gLarga);
    gFila.addEventListener('click', (e) => { if (gArrastou) { e.preventDefault(); e.stopPropagation(); gArrastou = false; } }, true);
    gFila.addEventListener('dragstart', (e) => e.preventDefault());
    gFila.addEventListener('scroll', pintaBarra, { passive: true });
    numera(); poeFilete(); pintaBarra();
    addEventListener('resize', () => { poeFilete(); pintaBarra(); });
    if (document.fonts) document.fonts.ready.then(() => { poeFilete(); pintaBarra(); });
    addEventListener('load', pintaBarra);
  }

  /* ---------- ESPAÇOS COMUNS: escolhe-se a divisão; a moldura toma a forma de cada foto ----------
     A foto nova entra por cima e assenta; numa ao alto a moldura estreita-se
     devagar. Legenda por baixo, contador e miniaturas da divisão. Carregar na
     foto abre o visor só dessa divisão. */
  const ec = $('[data-ec]');
  if (ec) {
    const divs = $$('.ec__div', ec);
    const moldura = $('.ec__moldura', ec);
    const leg = $('.ec__leg', ec);
    const conta = $('.ec__conta', ec);
    const minis = $('.ec__minis', ec);
    let serieEc = null, iEc = 0, pedidoEc = 0;
    const altura = () => moldura.getBoundingClientRect().height;
    const forma = (f) => {
      // a moldura tem altura fixa; a largura segue a foto, sem passar a largura disponível
      const max = moldura.parentNode.clientWidth;
      const w = Math.min(max, altura() * f.w / f.h);
      moldura.style.width = `${w.toFixed(1)}px`;
    };
    const poeFoto = (i, primeira = false) => {
      iEc = i; const f = serieEc.fotos[i]; const meu = ++pedidoEc;
      forma(f);
      const fig = document.createElement('figure');
      fig.className = 'ec__foto';
      fig.innerHTML = `<img src="${f.medio || f.src}" alt="${f.alt}" decoding="async">`;
      const im = $('img', fig);
      const entra = () => {
        if (meu !== pedidoEc) return;
        moldura.appendChild(fig);
        requestAnimationFrame(() => requestAnimationFrame(() => fig.classList.add('ativo')));
        $$('.ec__foto', moldura).forEach((v) => { if (v !== fig) { v.classList.add('sai'); setTimeout(() => v.remove(), 1400); } });
      };
      if (im.complete) entra(); else im.decode().then(entra, entra);
      leg.textContent = f.leg || '';
      conta.textContent = `${i + 1} / ${serieEc.fotos.length}`;
      $$('button', minis).forEach((b, j) => b.setAttribute('aria-pressed', j === i ? 'true' : 'false'));
      if (primeira) fig.classList.add('ativo');
    };
    const escolhe = (k, primeira = false) => {
      serieEc = window.SERIES[k];
      divs.forEach((d) => d.setAttribute('aria-pressed', d.dataset.serie === k ? 'true' : 'false'));
      minis.innerHTML = serieEc.fotos.map((f, j) => `<li><button type="button" aria-label="${f.leg || 'Fotografia ' + (j + 1)}"><img src="${f.mini}" alt="" decoding="async"></button></li>`).join('');
      $$('button', minis).forEach((b, j) => b.addEventListener('click', () => poeFoto(j)));
      poeFoto(0, primeira);
    };
    divs.forEach((d) => d.addEventListener('click', () => { if (d.getAttribute('aria-pressed') !== 'true') escolhe(d.dataset.serie); }));
    moldura.addEventListener('click', () => abre(serieEc.chave, iEc));
    moldura.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abre(serieEc.chave, iEc); } });
    escolhe(divs[0].dataset.serie, true);
    addEventListener('resize', () => forma(serieEc.fotos[iEc]));
  }

  /* ---------- ciclo ---------- */
  /* Primeiro mede-se tudo, depois escreve-se tudo: medir a seguir a escrever obrigava o
     browser a recalcular a página a meio do frame, uma vez por elemento. */
  const mede = (el) => el.getBoundingClientRect();
  const ciclo = () => {
    // 1. medir
    const y = scrollY;
    const hh = hero.offsetHeight;
    const rf = mede(fecho);
    const rq = qp ? mede(qp) : null;
    const rEsc = escuros.map(mede);
    const rNev = nevoas.map(mede);
    const rVel = reduz ? [] : vels.map(mede);
    const rEnt = entram.map(mede);
    const rPre = presas.map(({ el }) => mede(el));
    const rLug = lugares.map(mede);

    // 2. escrever
    poe(hero, '--hs', limita(y / hh).toFixed(4));

    // topo: transparente sobre o hero, os quartos presos, as secções a ecrã inteiro e o fecho
    let sobreFoto = y < hh - 70 || (rf.top <= 34 && rf.bottom > 70);
    if (rq && rq.top <= 34 && rq.bottom >= vh - 2) sobreFoto = true;
    rEsc.forEach((r) => { if (r.top <= 34 && r.bottom >= vh - 2) sobreFoto = true; });
    topo.classList.toggle('solido', !sobreFoto);
    if (barra) barra.classList.toggle('visivel', y > hh * 0.7 && rf.top > vh * 0.9);

    // a névoa: cada palavra sai do desfoque, em onda, conforme a frase sobe no ecrã;
    // nítida inteira, larga o filtro (um desfoque de 0 px ainda custa a cada frame)
    nevoas.forEach((el, k) => {
      const r = rNev[k];
      if (r.bottom < -100 || r.top > vh + 100) return;
      const n = el._np || (el._np = +el.style.getPropertyValue('--np') || 1);
      const t = reduz ? 1 : limita((vh * 0.95 - r.top) / (vh * 0.42));   // nítida inteira antes de chegar ao meio do ecrã
      poe(el, '--n', (t * (n + 4)).toFixed(2));
      if (el._limpa !== (t >= 1)) { el._limpa = t >= 1; el.classList.toggle('limpa', t >= 1); }
    });

    // velocidades: a posição natural é a medida menos o desvio já aplicado
    vels.forEach((el, k) => {
      const r = rVel[k];
      if (!r) return;
      const d0 = el._d || 0;
      const topo0 = r.top - d0;
      if (r.bottom - d0 < -200 || topo0 > vh + 200) { camada(el, false, 'mexe-v'); return; }
      const d = Math.round((topo0 + r.height / 2 - vh / 2) * parseFloat(el.dataset.vel) * 2) / 2;
      el._d = d;
      poe(el, 'translate', `0 ${d}px`);
      camada(el, true, 'mexe-v');
    });

    entram.forEach((el, k) => {
      const r = rEnt[k];
      if (!r.height) { poe(el, '--e', '1'); return; }
      if (r.bottom < -50 || r.top > vh + 50) { camada(el, false); return; }
      const e = reduz ? 1 : suave(limita((vh - r.top) / (vh * 0.55)));
      const s = reduz ? 0 : limita(1 - r.bottom / (vh * 0.4));
      poe(el, '--e', e.toFixed(4));
      poe(el, '--s', s.toFixed(4));
      camada(el, e < 1 || s > 0);
    });

    // secções presas: --p de 0 a 1 no percurso; cada passo recebe o seu --a
    presas.forEach(({ el, passos }, k) => {
      const r = rPre[k];
      if (r.top > vh * 1.2 || r.bottom < -vh * 0.2) return;
      const curso = Math.max(1, r.height - vh);
      const p = reduz ? 1 : limita(-r.top / curso);
      poe(el, '--p', p.toFixed(4));
      poe(el, '--in', (reduz ? 1 : limita((vh - r.top) / vh)).toFixed(4));
      const n = passos.length;
      passos.forEach((ps, i) => poe(ps, '--a', limita(p * n - i).toFixed(4)));
      if (el._pinta) el._pinta(p);
    });

    if (rq) pintaQuartos(rq);

    let ativo = 0, melhor = Infinity;
    lugares.forEach((l, i) => {
      const r = rLug[i];
      const d = Math.abs(r.top + r.height / 2 - vh / 2);
      if (d < melhor) { melhor = d; ativo = i; }
      if (i > 0 && afs[i]) {
        const a = suave(limita((vh * 0.88 - r.top) / (vh * 0.38)));
        poe(afs[i], '--a', a.toFixed(4));
        camada(afs[i], a > 0 && a < 1);
      }
    });
    lugares.forEach((l, i) => { if (l._a !== (i === ativo)) { l._a = i === ativo; l.classList.toggle('ativo', l._a); } });
  };
  window.Motor = { limita, suave, reduz, agenda: () => agenda() };

  let pedido = false;
  const agenda = () => { if (!pedido) { pedido = true; requestAnimationFrame(() => { pedido = false; ciclo(); }); } };
  // com o Lenis, só no evento dele (no mesmo frame do scroll); antes corria também no scroll nativo: duas vezes por frame
  if (lenis) lenis.on('scroll', ciclo);
  else addEventListener('scroll', agenda, { passive: true });
  addEventListener('resize', () => { vh = innerHeight; agenda(); });
  addEventListener('load', agenda);
  requestAnimationFrame(ciclo);

  /* ---------- ligações internas ---------- */
  $$('a[href^="#"]').forEach((a) => a.addEventListener('click', (e) => {
    const alvo = $(a.getAttribute('href'));
    if (!alvo) return;
    e.preventDefault();
    const extra = alvo.matches('[data-sem-folga]') ? 0 : 70;
    irPara(topoDe(alvo) - extra);
  }));

  /* ---------- COMODIDADES: a fila anda sozinha, devagar, e não acaba ---------- */
  const pista = $('[data-comod]');
  if (pista) {
    const lista = $('.comod__lista', pista);
    $$(':scope > li', lista).forEach((c) => { const k = c.cloneNode(true); k.setAttribute('aria-hidden', 'true'); lista.appendChild(k); });
    if (!reduz) {
      const VEL = 24;
      let pos = 0, anterior = null, pausa = 0, sobre = false, visivel = true, aCorrer = false;
      let volta = lista.scrollWidth / 2;
      const andar = (agora) => {
        if (!visivel) { aCorrer = false; return; }
        if (anterior === null) anterior = agora;
        const ms = Math.min(agora - anterior, 100); anterior = agora;
        if (sobre || pausa > 0) { if (pausa > 0) pausa -= ms; pos = pista.scrollLeft; }
        else {
          pos += VEL * ms / 1000;
          if (volta > 0) { if (pos >= volta) pos -= volta; else if (pos < 0) pos += volta; }
          pista.scrollLeft = pos;
        }
        requestAnimationFrame(andar);
      };
      const liga = () => { if (aCorrer) return; aCorrer = true; anterior = null; requestAnimationFrame(andar); };
      new IntersectionObserver((e) => { visivel = e[0].isIntersecting; if (visivel) { volta = lista.scrollWidth / 2; liga(); } }).observe(pista);
      addEventListener('resize', () => { volta = lista.scrollWidth / 2; });
      const suspende = () => { pausa = 1500; };
      pista.addEventListener('wheel', suspende, { passive: true });
      pista.addEventListener('touchstart', suspende, { passive: true });
      pista.addEventListener('touchmove', suspende, { passive: true });
      pista.addEventListener('touchend', () => { pausa = 2500; }, { passive: true });
      pista.addEventListener('mouseenter', () => { sobre = true; });
      pista.addEventListener('mouseleave', () => { sobre = false; });
      addEventListener('blur', () => { sobre = false; });
      let agarrado = false, x0 = 0, s0 = 0;
      pista.addEventListener('pointerdown', (e) => {
        if (e.pointerType === 'touch') return;
        agarrado = true; x0 = e.clientX; s0 = pista.scrollLeft;
        pista.classList.add('agarrada'); pista.setPointerCapture(e.pointerId);
      });
      pista.addEventListener('pointermove', (e) => { if (agarrado) { e.preventDefault(); pista.scrollLeft = s0 - (e.clientX - x0); } });
      const larga = (e) => { if (!agarrado) return; agarrado = false; pista.classList.remove('agarrada'); try { pista.releasePointerCapture(e.pointerId); } catch (_) {} };
      pista.addEventListener('pointerup', larga);
      pista.addEventListener('pointercancel', larga);
      liga();
    }
  }

  /* ---------- VISOR: abre só o espaço clicado ----------
     Carrega sempre o ficheiro original e nunca o mostra maior do que ele é. */
  const visor = $('#visor');
  const vImg = $('.visor__palco img');
  const vTit = $('.visor__titulo');
  const vConta = $('.visor__conta');
  const vMinis = $('.visor__minis');
  let serie = null, vi = 0, ultimoFoco = null, pedidoV = 0;
  const pinta = () => {
    const f = serie.fotos[vi], meu = ++pedidoV;
    const tinha = !!vImg.getAttribute('src');
    vImg.classList.add('troca');
    const im = new Image();
    im.onload = () => setTimeout(() => {
      if (meu !== pedidoV) return;
      vImg.src = im.src; vImg.alt = f.alt;
      vImg.style.maxWidth = `min(100%, ${f.w}px)`; vImg.style.maxHeight = `min(100%, ${f.h}px)`;
      requestAnimationFrame(() => vImg.classList.remove('troca'));
    }, tinha ? 180 : 0);
    im.src = f.src;
    vConta.textContent = `${vi + 1} / ${serie.fotos.length}`;
    $$('button', vMinis).forEach((b, i) => {
      b.classList.toggle('ativo', i === vi);
      if (i === vi) vMinis.scrollTo({ left: b.parentNode.offsetLeft - (vMinis.clientWidth - b.offsetWidth) / 2, behavior: 'smooth' });
    });
  };
  const abre = (k, i) => {
    serie = window.SERIES[k]; if (!serie) return;
    vi = i || 0; ultimoFoco = document.activeElement;
    vTit.textContent = serie.titulo;
    vImg.removeAttribute('src');
    vMinis.innerHTML = serie.fotos.map((f, j) => `<li><button type="button" aria-label="Fotografia ${j + 1}"><img src="${f.mini}" alt="" decoding="async"></button></li>`).join('');
    $$('button', vMinis).forEach((b, j) => b.addEventListener('click', () => { vi = j; pinta(); }));
    visor.hidden = false; requestAnimationFrame(() => visor.classList.add('aberto'));
    if (lenis) lenis.stop(); document.body.style.overflow = 'hidden'; document.body.classList.add('com-visor');
    pinta(); $('.visor__fechar').focus();
  };
  const fecha = () => {
    visor.classList.remove('aberto');
    setTimeout(() => { visor.hidden = true; }, 350);
    if (lenis) lenis.start(); document.body.style.overflow = ''; document.body.classList.remove('com-visor');
    if (ultimoFoco) ultimoFoco.focus({ preventScroll: true });
  };
  const anda = (d) => { vi = (vi + d + serie.fotos.length) % serie.fotos.length; pinta(); };
  $$('[data-visor]').forEach((b) => b.addEventListener('click', () => abre(b.dataset.visor, +b.dataset.indice || 0)));

  /* ---------- FILTRO DOS QUARTOS (quartos-todos.html): mostra só o tipo escolhido, sem animação ---------- */
  const filtro = $('[data-filtro]');
  if (filtro) {
    const botoes = [...filtro.querySelectorAll('.filtro button')];
    botoes.forEach((b) => b.addEventListener('click', () => {
      const t = b.dataset.tipo;
      botoes.forEach((x) => x.setAttribute('aria-pressed', x === b ? 'true' : 'false'));
      filtro.querySelectorAll('.qq').forEach((q) => { q.hidden = t !== 'todos' && q.dataset.tipo !== t; });
      filtro.querySelectorAll('.qq-andar').forEach((a) => { a.hidden = !a.querySelector('.qq:not([hidden])'); });
      if (lenis) lenis.resize();
    }));
  }
  $$('.gf__foto').forEach((b) => b.addEventListener('click', () => abre(b.dataset.serie, +b.dataset.indice)));
  $('.visor__fechar').addEventListener('click', fecha);
  $('.visor__seta--ant').addEventListener('click', () => anda(-1));
  $('.visor__seta--seg').addEventListener('click', () => anda(1));
  visor.addEventListener('click', (e) => { if (e.target === visor || e.target.classList.contains('visor__palco')) fecha(); });
  addEventListener('keydown', (e) => {
    if (visor.hidden) return;
    if (e.key === 'Escape') fecha();
    if (e.key === 'ArrowLeft') anda(-1);
    if (e.key === 'ArrowRight') anda(1);
  });
  let vx = null;
  $('.visor__palco').addEventListener('touchstart', (e) => { vx = e.touches[0].clientX; }, { passive: true });
  $('.visor__palco').addEventListener('touchend', (e) => {
    if (vx === null) return;
    const dx = e.changedTouches[0].clientX - vx; vx = null;
    if (Math.abs(dx) > 40) anda(dx < 0 ? 1 : -1);
  });
})();
