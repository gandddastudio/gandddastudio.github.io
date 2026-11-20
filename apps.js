// ─────────────────────────────────────────────────────────────────────────────
//  apps.js · Catálogo de Ganddda Studio
//
//  Para agregar una app:
//    1. Copia uno de los bloques { ... } de APPS y pégalo donde quieras que aparezca.
//    2. Cambia sus datos. Usa siempre comillas dobles "así" en los textos.
//    3. Pon su ícono en img/<id>.png (cuadrado, 256 px o más).
//    4. Corre  python tools/generar_sitio.py  y sube los cambios.
//
//  Campos:
//    id        nombre corto sin espacios; también es el nombre del ícono y de la política
//    name      nombre en cada idioma
//    tagline   frase corta en cada idioma
//    category  una de las llaves de CATEGORIES
//    size      tamaño en el bento: "xl" (2×2) · "tall" (1×2) · "wide" (2×1) · "sm" (1×1)
//    accent    color propio de la tarjeta (brillo y detalles)
//    tags      etiquetas técnicas cortas, en mayúsculas
//    playId    ID del paquete en Google Play
//    status    "soon" (próximamente) · "new" (nuevo en Play) · "live" (en Play)
//    video     opcional: video corto en bucle para tarjetas grandes
// ─────────────────────────────────────────────────────────────────────────────

export const CATEGORIES = {
  juegos:       { es: "Juegos",            en: "Games",          color: "#C6FF3D" },
  herramientas: { es: "Herramientas",      en: "Tools",          color: "#3EF0C1" },
  misterio:     { es: "Suerte y misterio", en: "Luck & mystery", color: "#A98BFF" },
};

export const APPS = [
  {
    id: "michis-amasadores",
    name:    { es: "¡Michis Amasadores!", en: "Kneady Cats!" },
    tagline: { es: "Amasa, esculpe y colecciona michis. Cada figura que logras es un michi nuevo.",
               en: "Knead, sculpt and collect cats. Every shape you nail is a new cat." },
    category: "juegos",
    size: "xl",
    accent: "#F2A23A",
    tags: { es: ["21 MICHIS", "APTA PARA NIÑOS", "ES · EN · PT"], en: ["21 CATS", "KID FRIENDLY", "ES · EN · PT"] },
    playId: "com.ganddda.michis_amasadores",
    status: "soon",
    video: "media/michis.mp4",
  },
  {
    id: "zzzas",
    name:    { es: "Zzzás: ¡Mosquitazo!", en: "Zzzap! Mosquito Smash" },
    tagline: { es: "Caza mosquitos moviendo tu teléfono. Cuatro modos, cuatro armas, cero piedad.",
               en: "Hunt mosquitoes by moving your phone. Four modes, four weapons, zero mercy." },
    category: "juegos",
    size: "tall",
    accent: "#C6FF3D",
    tags: { es: ["GIROSCOPIO", "RACHA DE ZZZÁS"], en: ["GYROSCOPE", "ZZZAP STREAK"] },
    playId: "com.ganddda.zzzas",
    status: "soon",
  },
  {
    id: "mi-cafe-dice",
    name:    { es: "Mi Café Dice", en: "My Coffee Says" },
    tagline: { es: "Lee el fondo de tu taza y tu horóscopo del día.",
               en: "Read the bottom of your cup and your daily horoscope." },
    category: "misterio",
    size: "sm",
    accent: "#D59A5B",
    tags: { es: ["CÁMARA", "50 SÍMBOLOS"], en: ["CAMERA", "50 SYMBOLS"] },
    playId: "com.ganddda.micafedice",
    status: "soon",
  },
  {
    id: "mi-suerte-hoy",
    name:    { es: "Mi Suerte Hoy", en: "My Luck Today" },
    tagline: { es: "Tu color, tu número y tu frase de la suerte de cada día.",
               en: "Your lucky color, number and phrase, every day." },
    category: "misterio",
    size: "sm",
    accent: "#F7A8C8",
    tags: { es: ["SELFIE", "DIARIO"], en: ["SELFIE", "DAILY"] },
    playId: "com.ganddda.misuertehoy",
    status: "soon",
  },
  {
    id: "tarot-espanol",
    name:    { es: "Tarot Español", en: "Spanish Tarot" },
    tagline: { es: "Lecturas con la baraja española de 40 cartas.",
               en: "Readings with the 40-card Spanish deck." },
    category: "misterio",
    size: "sm",
    accent: "#E8C46F",
    tags: { es: ["40 CARTAS", "DIARIO"], en: ["40 CARDS", "JOURNAL"] },
    playId: "com.ganddda.tarotespanol",
    status: "soon",
  },
  {
    id: "silla-caliente",
    name:    { es: "Mi Entrevista: Silla Caliente", en: "Hot Seat: Interview Practice" },
    tagline: { es: "Ensaya tu entrevista de trabajo en voz alta.",
               en: "Practice your job interview out loud." },
    category: "herramientas",
    size: "sm",
    accent: "#FF6A3D",
    tags: { es: ["VOZ", "CALIFICACIÓN"], en: ["VOICE", "SCORING"] },
    playId: "com.ganddda.sillacaliente",
    status: "soon",
  },
  {
    id: "me-graban",
    name:    { es: "¿Me Graban?", en: "Am I on Camera?" },
    tagline: { es: "Te ayuda a buscar cámaras ocultas en tu habitación: reflejo del lente, red Wi-Fi y más.",
               en: "Helps you look for hidden cameras in your room: lens glint, Wi-Fi scan and more." },
    category: "herramientas",
    size: "wide",
    accent: "#3EF0C1",
    tags: { es: ["ESCANEO WI-FI", "REFLEJO DEL LENTE"], en: ["WI-FI SCAN", "LENS GLINT"] },
    playId: "com.ganddda.me_graban",
    status: "soon",
  },
  {
    id: "diableros",
    name:    { es: "Diableros de la Central", en: "Diableros de la Central" },
    tagline: { es: "¡Pásele, marchante!", en: "Step right up, friend!" },
    category: "juegos",
    size: "sm",
    accent: "#FF4D4D",
    tags: { es: ["SIN INTERNET", "SIN ANUNCIOS"], en: ["OFFLINE", "NO ADS"] },
    playId: "com.ganddda.diableros",
    status: "soon",
  },
];
