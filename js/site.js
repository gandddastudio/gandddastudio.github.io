// Ganddda Studio · sitio: catálogo dinámico, filtros, inclinación de tarjetas y el trueno.
import { APPS, CATEGORIES } from "../apps.js";

const lang = document.documentElement.lang === "en" ? "en" : "es";
const base = document.body.dataset.base || "";
const reducido = matchMedia("(prefers-reduced-motion: reduce)").matches;

const T = {
  es: {
    todas: "Todas", soon: "PRÓXIMAMENTE", new: "NUEVO", live: "EN PLAY",
    play: "Disponible en Google Play", pronto: "Próximamente en Google Play", privacidad: "Privacidad",
    privDir: "privacidad", acercaT: "¿Quién está detrás?", acercaP: "Un programador, un sueño de los 16 y muchos michis.",
    acercaF: "CONOCE AL CREADOR →", masT: "Siguiente app", masP: "Ya se está cocinando algo. ¿Qué crees que será?",
    trueno: "⚡ ¡Invocaste el trueno de Ganddda!", sonidoOn: "Sonido activado", sonidoOff: "Sonido desactivado",
  },
  en: {
    todas: "All", soon: "COMING SOON", new: "NEW", live: "ON PLAY",
    play: "Get it on Google Play", pronto: "Coming soon to Google Play", privacidad: "Privacy",
    privDir: "en/privacy", acercaT: "Who's behind it?", acercaP: "A programmer, a dream from age 16 and lots of cats.",
    acercaF: "MEET THE CREATOR →", masT: "Next app", masP: "Something is already cooking. Any guesses?",
    trueno: "⚡ You summoned Ganddda's thunder!", sonidoOn: "Sound on", sonidoOff: "Sound off",
  },
}[lang];

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const tx = (v) => (v && typeof v === "object" ? v[lang] ?? v.es : v);

// ── Tarjetas ────────────────────────────────────────────────
function tarjetaApp(app, i) {
  const cat = CATEGORIES[app.category] ?? { es: app.category, en: app.category, color: "#F7F1E6" };
  const estado = ["soon", "new", "live"].includes(app.status) ? app.status : "soon";
  const enPlay = estado !== "soon";
  const url = `https://play.google.com/store/apps/details?id=${encodeURIComponent(app.playId)}`;
  const tags = (tx(app.tags) ?? []).map((t) => `<li>${esc(t)}</li>`).join("");
  const grande = app.size === "xl" || app.size === "tall";
  // Tarjetas grandes: video en bucle si hay; si no, un eco gigante del ícono de fondo.
  const video = app.video && !reducido
    ? `<video class="media" src="${base}${esc(app.video)}" autoplay muted loop playsinline aria-hidden="true"></video>`
    : grande || app.size === "wide" ? `<img class="media eco" src="${base}img/${esc(app.id)}.png" alt="" aria-hidden="true" loading="lazy">` : "";
  const cuerpo = `
      <h3>${esc(tx(app.name))}</h3>
      <p>${esc(tx(app.tagline))}</p>
      <ul class="tags mono">${tags}</ul>
      <div class="acciones">
        ${enPlay ? `<a class="btn" href="${url}" rel="noopener">▶ ${T.play}</a>` : `<span class="btn off">${T.pronto}</span>`}
        <a class="pol" href="${base}${T.privDir}/${esc(app.id)}.html">${T.privacidad}</a>
      </div>`;
  return `
  <li class="s-${esc(app.size || "sm")}" data-cat="${esc(app.category)}" style="--vt: app-${i}">
    <article class="card cat-${esc(app.category)}" style="--accent:${esc(app.accent || cat.color)};--cat:${esc(cat.color)}">
      <div class="card-top">
        <span class="chip mono">${esc(tx(cat).toUpperCase())}</span>
        <span class="badge ${estado}">${T[estado]}</span>
      </div>
      <div class="icono-wrap">
        <img class="icono" src="${base}img/${esc(app.id)}.png" alt="" width="${grande ? 104 : 84}" height="${grande ? 104 : 84}" loading="lazy">
        <span class="destellos" aria-hidden="true"><i></i><i></i><i></i></span>
      </div>
      ${app.size === "wide" ? `<div class="cuerpo">${cuerpo}</div>` : cuerpo}
      ${video}
    </article>
  </li>`;
}

function tarjetasEspeciales() {
  return `
  <li class="s-wide" data-cat="*" style="--vt: acerca">
    <a class="card acerca-card especial" href="#acerca">
      <img src="${base}img/creador.webp" alt="" width="96" height="96" loading="lazy">
      <div>
        <h3>${T.acercaT}</h3>
        <p>${T.acercaP}</p>
        <span class="flecha">${T.acercaF}</span>
      </div>
    </a>
  </li>
  <li class="s-sm" data-cat="*" style="--vt: pronto">
    <div class="card pronto especial">
      <span class="mas" aria-hidden="true">+1</span>
      <h3>${T.masT}</h3>
      <p>${T.masP}</p>
    </div>
  </li>`;
}

const bento = document.getElementById("bento");
if (bento) {
  // Las especiales van después de la 7.ª app para cerrar el grid de 4 columnas.
  const partes = APPS.map(tarjetaApp);
  partes.splice(Math.min(7, partes.length), 0, tarjetasEspeciales());
  bento.innerHTML = partes.join("");
  pintarFiltros();
  activarInclinacion();
}

// ── Filtros ─────────────────────────────────────────────────
function pintarFiltros() {
  const caja = document.getElementById("filtros");
  if (!caja) return;
  const usadas = Object.keys(CATEGORIES).filter((k) => APPS.some((a) => a.category === k));
  const botones = [["*", T.todas, "#F7F1E6", APPS.length],
    ...usadas.map((k) => [k, tx(CATEGORIES[k]), CATEGORIES[k].color, APPS.filter((a) => a.category === k).length])];
  caja.innerHTML = botones.map(([k, nombre, color, n], i) =>
    `<button type="button" class="filtro" data-f="${esc(k)}" style="--c:${esc(color)}" aria-pressed="${i === 0}">${esc(nombre)}<span class="n">${n}</span></button>`).join("");
  caja.addEventListener("click", (e) => {
    const b = e.target.closest(".filtro");
    if (!b || b.getAttribute("aria-pressed") === "true") return;
    caja.querySelectorAll(".filtro").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    const f = b.dataset.f;
    const aplicar = () => bento.querySelectorAll(":scope > li").forEach((li) => {
      li.hidden = f !== "*" && li.dataset.cat !== f;
    });
    if (document.startViewTransition && !reducido && !document.hidden) document.startViewTransition(aplicar);
    else aplicar();
  });
}

// ── Inclinación 3D al mover el puntero ──────────────────────
function activarInclinacion() {
  if (reducido || !matchMedia("(hover: hover)").matches) return;
  bento.addEventListener("pointermove", (e) => {
    const card = e.target.closest(".card");
    if (!card) return;
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
    card.style.setProperty("--ry", `${(x - 0.5) * 7}deg`);
    card.style.setProperty("--rx", `${(0.5 - y) * 7}deg`);
    card.style.setProperty("--mx", `${x * 100}%`);
    card.style.setProperty("--my", `${y * 100}%`);
  });
  bento.addEventListener("pointerout", (e) => {
    const card = e.target.closest(".card");
    if (card && !card.contains(e.relatedTarget)) {
      card.style.setProperty("--rx", "0deg");
      card.style.setProperty("--ry", "0deg");
    }
  });
}

// ── Sonido (apagado por defecto) ────────────────────────────
const botonSonido = document.getElementById("sonido");
let sonido = false;
try { sonido = localStorage.getItem("ganddda-sonido") === "1"; } catch {}
function pintarSonido() {
  if (!botonSonido) return;
  botonSonido.textContent = sonido ? "🔊" : "🔇";
  botonSonido.setAttribute("aria-pressed", String(sonido));
  botonSonido.setAttribute("aria-label", sonido ? T.sonidoOn : T.sonidoOff);
  botonSonido.title = sonido ? T.sonidoOn : T.sonidoOff;
}
botonSonido?.addEventListener("click", () => {
  sonido = !sonido;
  try { localStorage.setItem("ganddda-sonido", sonido ? "1" : "0"); } catch {}
  pintarSonido();
});
pintarSonido();

// ── Easter egg: tres toques a «Ganddda» invocan el trueno ───
const marca = document.getElementById("marca");
let toques = [];
let trueno;
marca?.addEventListener("click", () => {
  const ahora = performance.now();
  toques = toques.filter((t) => ahora - t < 1200).concat(ahora);
  marca.classList.remove("cargando"); void marca.offsetWidth; marca.classList.add("cargando");
  if (toques.length >= 3) { toques = []; tormenta(); }
});

function tormenta() {
  const body = document.body;
  if (body.classList.contains("tormenta")) return;
  body.classList.add("tormenta");
  if (sonido) {
    trueno ??= new Audio(`${base}media/trueno.wav`);
    trueno.currentTime = 0;
    trueno.volume = 0.6;
    trueno.play().catch(() => {});
  }
  if (navigator.vibrate) navigator.vibrate([40, 60, 140, 80, 60]);
  const aviso = document.getElementById("aviso");
  if (aviso) { aviso.textContent = T.trueno; aviso.classList.add("ver"); }
  setTimeout(() => aviso?.classList.remove("ver"), 2600);
  setTimeout(() => body.classList.remove("tormenta"), reducido ? 2700 : 6200);
}
