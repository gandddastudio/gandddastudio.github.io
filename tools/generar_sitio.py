"""Genera el sitio estático de Ganddda Studio para GitHub Pages.

Uso (desde la carpeta ganddda_web):
    python tools/generar_sitio.py

El catálogo (nombres, categorías, tamaños, estado en Play) vive en apps.js.
Aquí solo están los textos de las políticas de privacidad de cada app (lista APPS,
unida a apps.js por el campo slug = id). Al agregar una app a apps.js, agrega
también su bloque aquí con lo que usa la app.
"""
import json
import re
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
APPS_DIR = RAIZ.parent

CONTACTO = "gandddastudio@gmail.com"
ACTUALIZADO = {"es": "21 de noviembre de 2026", "en": "November 21, 2026"}

# Política común de anuncios y compras (se activa por app).
ADS = "ads"
IAP = "iap"

APPS = [
    dict(slug="mi-cafe-dice", carpeta="mi_cafe_dice", id="com.ganddda.micafedice",
         nombre={"es": "Mi Café Dice", "en": "My Coffee Says"},
         lema={"es": "Lee el fondo de tu taza y tu horóscopo del día.",
               "en": "Read the bottom of your cup and your daily horoscope."},
         extras=[ADS, IAP],
         datos={"es": [
             "<b>Cámara:</b> para fotografiar el fondo de tu taza. La imagen se analiza en tu teléfono (incluido el reconocimiento de imágenes de Google ML Kit, que funciona sin conexión) y no se sube a ningún servidor.",
             "<b>Sensores de movimiento:</b> solo para comprobar que la foto se tomó en vivo.",
             "<b>Notificaciones:</b> para los recordatorios que tú activas (café y horóscopo).",
             "<b>Preferencias y signo zodiacal:</b> se guardan solo en tu teléfono.",
         ], "en": [
             "<b>Camera:</b> to photograph the bottom of your cup. The image is analyzed on your phone (including Google ML Kit image labeling, which works offline) and is never uploaded to a server.",
             "<b>Motion sensors:</b> only to check that the photo was taken live.",
             "<b>Notifications:</b> for the reminders you turn on (coffee and horoscope).",
             "<b>Preferences and zodiac sign:</b> stored only on your phone.",
         ]}),
    dict(slug="mi-suerte-hoy", carpeta="mi_suerte_hoy", id="com.ganddda.misuertehoy",
         nombre={"es": "Mi Suerte Hoy", "en": "My Luck Today"},
         lema={"es": "Tu color, tu número y tu frase de la suerte de cada día.",
               "en": "Your lucky color, number and phrase for every day."},
         extras=[ADS, IAP],
         datos={"es": [
             "<b>Cámara:</b> para tomarte una selfie con marco y filtro. La foto se procesa en tu teléfono y no se sube a ningún servidor.",
             "<b>Notificaciones:</b> para el recordatorio diario, si lo activas.",
             "<b>Preferencias:</b> se guardan solo en tu teléfono.",
         ], "en": [
             "<b>Camera:</b> to take a selfie with a frame and filter. The photo is processed on your phone and is never uploaded to a server.",
             "<b>Notifications:</b> for the daily reminder, if you turn it on.",
             "<b>Preferences:</b> stored only on your phone.",
         ]}),
    dict(slug="tarot-espanol", carpeta="tarot_baraja", id="com.ganddda.tarotespanol",
         nombre={"es": "Tarot Español", "en": "Spanish Tarot"},
         lema={"es": "Lecturas con la baraja española de 40 cartas.",
               "en": "Readings with the 40-card Spanish deck."},
         extras=[ADS, IAP],
         datos={"es": [
             "<b>Diario de lecturas:</b> se guarda solo en tu teléfono. Puedes borrar una lectura o todo el diario desde la app.",
             "<b>Lectura profunda:</b> si la activas, la app descarga un modelo de lenguaje que funciona en tu teléfono. Tus preguntas y lecturas no se envían a ningún servidor.",
             "<b>Notificaciones:</b> para el recordatorio diario de los suscriptores, si lo activan.",
         ], "en": [
             "<b>Reading journal:</b> stored only on your phone. You can delete one reading or the whole journal from the app.",
             "<b>Deep reading:</b> if you turn it on, the app downloads a language model that runs on your phone. Your questions and readings are never sent to a server.",
             "<b>Notifications:</b> for the subscribers' daily reminder, if turned on.",
         ]}),
    dict(slug="silla-caliente", carpeta="ensayo_entrevistas", id="com.ganddda.sillacaliente",
         nombre={"es": "Mi Entrevista: Silla Caliente", "en": "My Interview: Hot Seat"},
         lema={"es": "Ensaya tu entrevista de trabajo en voz alta.",
               "en": "Practice your job interview out loud."},
         extras=[ADS, IAP],
         datos={"es": [
             "<b>Micrófono:</b> para escuchar tus respuestas. La transcripción la hace el servicio de reconocimiento de voz de tu teléfono (por ejemplo, el de Google), que puede procesar el audio según su propia política de privacidad. Ganddda Studio no guarda ni recibe tu audio.",
             "<b>Cámara:</b> para que te veas mientras respondes. La imagen no se graba ni se envía.",
             "<b>Respuestas y calificaciones:</b> se guardan solo en tu teléfono.",
         ], "en": [
             "<b>Microphone:</b> to hear your answers. Transcription is done by your phone's speech recognition service (for example, Google's), which may process the audio under its own privacy policy. Ganddda Studio never stores or receives your audio.",
             "<b>Camera:</b> so you can see yourself while answering. The image is not recorded or sent.",
             "<b>Answers and scores:</b> stored only on your phone.",
         ]}),
    dict(slug="zzzas", carpeta="zzzas_mosquitazo", id="com.ganddda.zzzas",
         nombre={"es": "Zzzás: ¡Mosquitazo!", "en": "Zzzap! Mosquito Smash"},
         lema={"es": "Caza mosquitos moviendo tu teléfono. ¡Zzzás!",
               "en": "Hunt mosquitoes by moving your phone. Zzzap!"},
         extras=[ADS, IAP],
         datos={"es": [
             "<b>Micrófono (modo Leyenda):</b> solo mide el volumen en el momento para el juego. No se graba, no se guarda y no se envía audio.",
             "<b>Sensores de movimiento:</b> para apuntar con el teléfono.",
             "<b>Notificaciones:</b> para el zumbido diario, si lo activas.",
             "<b>Récords, monedas y aspectos:</b> se guardan solo en tu teléfono.",
         ], "en": [
             "<b>Microphone (Legend mode):</b> only measures loudness in the moment for gameplay. No audio is recorded, stored or sent.",
             "<b>Motion sensors:</b> to aim with your phone.",
             "<b>Notifications:</b> for the daily buzz, if you turn it on.",
             "<b>Records, coins and skins:</b> stored only on your phone.",
         ]}),
    dict(slug="me-graban", carpeta="me_graban", id="com.ganddda.me_graban",
         nombre={"es": "¿Me Graban?", "en": "Am I Being Recorded?"},
         lema={"es": "Te ayuda a buscar cámaras ocultas en tu habitación.",
               "en": "Helps you look for hidden cameras in your room."},
         extras=[ADS, IAP],
         datos={"es": [
             "<b>Cámara y linterna:</b> para detectar el reflejo de lentes. La imagen se analiza en tu teléfono y no se graba ni se envía.",
             "<b>Red Wi-Fi local:</b> el escaneo busca dispositivos conectados a tu misma red (por ejemplo, cámaras). Los resultados se quedan en tu teléfono y no se envían a ningún servidor.",
             "<b>Sensores:</b> el magnetómetro sirve como apoyo para la búsqueda.",
             "<b>Historial de habitaciones:</b> se guarda solo en tu teléfono.",
         ], "en": [
             "<b>Camera and flashlight:</b> to detect lens reflections. The image is analyzed on your phone and is not recorded or sent.",
             "<b>Local Wi-Fi network:</b> the scan looks for devices on your same network (for example, cameras). Results stay on your phone and are never sent to a server.",
             "<b>Sensors:</b> the magnetometer helps the search.",
             "<b>Room history:</b> stored only on your phone.",
         ]}),
    dict(slug="michis-amasadores", carpeta="michis_amasadores", id="com.ganddda.michis_amasadores",
         nombre={"es": "¡Michis Amasadores!", "en": "Kneady Cats!"},
         lema={"es": "Amasa, esculpe y colecciona michis.",
               "en": "Knead, sculpt and collect cats."},
         extras=[ADS, IAP],
         datos={"es": [
             "<b>Foto de tu michi:</b> si agregas a tu gato, eliges la foto de tu galería. Se guarda solo en tu teléfono.",
             "<b>Notificaciones:</b> para avisarte de tus vidas o del reto, si las activas.",
             "<b>Progreso y colección:</b> se guardan solo en tu teléfono.",
         ], "kids": {
             "es": "¡Michis Amasadores! es apta para niños y cumple la política de Familias de Google Play. Todos los anuncios se piden como contenido para menores: no son personalizados, son aptos para todo público y no usan el identificador de publicidad para crear perfiles. No pedimos nombre, correo ni ubicación. La foto de tu michi se queda en el teléfono. Las compras requieren la autorización de la cuenta de Google Play del dispositivo; te recomendamos activar la aprobación de compras en Google Family Link. Madres, padres o tutores pueden escribirnos en cualquier momento.",
             "en": "Kneady Cats! is suitable for children and follows the Google Play Families policy. All ads are requested as child-directed: they are not personalized, are rated for all audiences and do not use the advertising ID to build profiles. We don't ask for a name, email or location. Your cat's photo stays on the phone. Purchases require authorization from the device's Google Play account; we recommend turning on purchase approval in Google Family Link. Parents or guardians can write to us at any time.",
         }, "en": [
             "<b>Your cat's photo:</b> if you add your cat, you pick the photo from your gallery. It is stored only on your phone.",
             "<b>Notifications:</b> to let you know about lives or challenges, if you turn them on.",
             "<b>Progress and collection:</b> stored only on your phone.",
         ]}),
    dict(slug="diableros", carpeta="diableros_central", id="com.ganddda.diableros",
         nombre={"es": "Diableros de la Central", "en": "Diableros de la Central"},
         lema={"es": "¡Pásele, marchante!",
               "en": "Step right up, friend!"},
         extras=[IAP],
         datos={"es": [
             "<b>Sensores de movimiento:</b> para controlar el juego.",
             "<b>Progreso:</b> se guarda solo en tu teléfono.",
             "Esta app no tiene anuncios. Solo se conecta a internet para las compras opcionales con Google Play.",
         ], "en": [
             "<b>Motion sensors:</b> to control the game.",
             "<b>Progress:</b> stored only on your phone.",
             "This app has no ads. It only connects to the internet for optional Google Play purchases.",
         ]}),
]


T = {
    "es": dict(
        lang="es", home="index.html", support="soporte.html", pol_dir="privacidad",
        title="Ganddda Studio", tagline="Apps pequeñas, hechas con cariño, desde México.",
        apps="Nuestras apps", privacy="Privacidad", support_t="Soporte",
        soon="Próximamente en Google Play", play="Disponible en Google Play",
        other="English", other_href="en/index.html",
        pol_title="Política de privacidad", updated="Última actualización",
        who_t="Quién la publica",
        who="{app} es una app de <b>Ganddda Studio</b>, desarrollador independiente en México. Si tienes dudas sobre esta política, escríbenos a <a href='mailto:{mail}'>{mail}</a>.",
        sum_t="En resumen",
        sum="No pedimos que te registres, no tenemos servidores propios y no vendemos tus datos. Lo que usa la app se queda en tu teléfono, salvo lo que procesan los servicios de Google que se indican abajo.",
        data_t="Qué usa la app y para qué",
        ads_t="Anuncios (Google AdMob)",
        ads="La versión gratuita muestra anuncios de Google AdMob. Para mostrarlos y medirlos, Google puede recopilar el identificador de publicidad de tu dispositivo, tu dirección IP, el modelo del teléfono e información de uso de los anuncios, según la <a href='https://policies.google.com/technologies/ads'>política de publicidad de Google</a>. En los ajustes de Android puedes restablecer o borrar tu ID de publicidad. Cuando la ley lo exige (por ejemplo, en la Unión Europea y el Reino Unido), la app te pide tu consentimiento antes de mostrar anuncios personalizados.",
        iap_t="Compras dentro de la app",
        iap="Los pagos los procesa Google Play. Ganddda Studio no recibe tu nombre ni los datos de tu tarjeta; la app solo recibe la confirmación de que la compra o suscripción está activa. Las suscripciones se administran y cancelan desde Google Play.",
        share_t="Compartir",
        share="Las imágenes o tarjetas solo se comparten cuando tú tocas «Compartir», con la app que elijas.",
        kids_t="Menores de edad",
        kids="La app no está dirigida a menores de 13 años y no recopila a sabiendas datos de menores. Si crees que un menor nos envió datos, escríbenos y los borraremos.",
        del_t="Cómo borrar tus datos",
        dele="Como tus datos están en tu teléfono, se borran al desinstalar la app o al borrar sus datos desde los ajustes de Android. Para los datos de anuncios, consulta la <a href='https://policies.google.com/privacy'>política de privacidad de Google</a>.",
        chg_t="Cambios",
        chg="Si cambia esta política, publicaremos la nueva versión en esta página con su fecha de actualización.",
        sup_title="Soporte",
        sup="¿Encontraste un error, tienes una idea o necesitas ayuda con una compra? Escríbenos e indica el nombre de la app y el modelo de tu teléfono.",
        sup_buy="Las compras y suscripciones se administran desde Google Play (Perfil → Pagos y suscripciones).",
        foot="© 2026 Ganddda Studio",
    ),
    "en": dict(
        lang="en", home="index.html", support="support.html", pol_dir="privacy",
        title="Ganddda Studio", tagline="Small apps, made with care, from Mexico.",
        apps="Our apps", privacy="Privacy", support_t="Support",
        soon="Coming soon to Google Play", play="Get it on Google Play",
        other="Español", other_href="../index.html",
        pol_title="Privacy policy", updated="Last updated",
        who_t="Who publishes it",
        who="{app} is an app by <b>Ganddda Studio</b>, an independent developer based in Mexico. If you have questions about this policy, write to <a href='mailto:{mail}'>{mail}</a>.",
        sum_t="In short",
        sum="We don't ask you to sign up, we don't run our own servers and we don't sell your data. What the app uses stays on your phone, except what the Google services listed below process.",
        data_t="What the app uses and why",
        ads_t="Ads (Google AdMob)",
        ads="The free version shows ads from Google AdMob. To show and measure them, Google may collect your device's advertising ID, IP address, phone model and ad interaction data, as described in <a href='https://policies.google.com/technologies/ads'>Google's advertising policy</a>. You can reset or delete your advertising ID in Android settings. Where the law requires it (for example, in the EU and UK), the app asks for your consent before showing personalized ads.",
        iap_t="In-app purchases",
        iap="Payments are processed by Google Play. Ganddda Studio never receives your name or card details; the app only receives confirmation that the purchase or subscription is active. Subscriptions are managed and canceled in Google Play.",
        share_t="Sharing",
        share="Images or cards are only shared when you tap “Share”, with the app you choose.",
        kids_t="Children",
        kids="The app is not directed at children under 13 and does not knowingly collect data from children. If you believe a child sent us data, write to us and we will delete it.",
        del_t="How to delete your data",
        dele="Because your data lives on your phone, it is deleted when you uninstall the app or clear its data in Android settings. For ad data, see <a href='https://policies.google.com/privacy'>Google's privacy policy</a>.",
        chg_t="Changes",
        chg="If this policy changes, we will post the new version on this page with its update date.",
        sup_title="Support",
        sup="Found a bug, have an idea or need help with a purchase? Write to us and include the app name and your phone model.",
        sup_buy="Purchases and subscriptions are managed in Google Play (Profile → Payments & subscriptions).",
        foot="© 2026 Ganddda Studio",
    ),
}


SITIO = "https://gandddastudio.github.io"
FUENTES = ("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700"
           "&family=Playfair+Display:ital,wght@1,600&family=Space+Grotesk:wght@400;500;700"
           "&family=Syne:wght@700;800&display=swap")

# Redes sociales (mismo usuario en todas). Para agregar otra, suma una tupla aquí.
REDES = [
    ("Instagram", "https://www.instagram.com/gandddastudio/", "ig",
     '<rect x="3" y="3" width="18" height="18" rx="5.5" fill="none" stroke="currentColor" stroke-width="2"/>'
     '<circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/>'
     '<circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/>'),
    ("TikTok", "https://www.tiktok.com/@gandddastudio", "tt",
     '<path d="M14 3h3.2c.3 2.3 1.8 3.9 4 4.1v3.2c-1.5 0-2.9-.4-4-1.2v6.4A5.6 5.6 0 1 1 11.6 10v3.3'
     'a2.4 2.4 0 1 0 2.4 2.3z" fill="currentColor"/>'),
    ("Facebook", "https://www.facebook.com/gandddastudio", "fb",
     '<circle cx="12" cy="12" r="10" fill="currentColor"/>'
     '<path d="M13.2 21v-6.6h2.3l.4-2.8h-2.7V9.9c0-.8.3-1.4 1.4-1.4H16V6.1c-.3 0-1.1-.1-2-.1-2 0-3.4 1.2-3.4 3.5v2.1H8.4v2.8h2.2V21z" fill="var(--noche)"/>'),
    ("YouTube", "https://www.youtube.com/@gandddastudio", "yt",
     '<rect x="2" y="5" width="20" height="14" rx="4.5" fill="currentColor"/>'
     '<path d="M10 9l5.2 3L10 15z" fill="var(--noche)"/>'),
]


def icono_red(svg, tam=22):
    return f'<svg viewBox="0 0 24 24" width="{tam}" height="{tam}" aria-hidden="true">{svg}</svg>'


def enlaces_redes(clase):
    return "".join(f'<a class="{clase} red-{k}" href="{url}" target="_blank" rel="noopener me" aria-label="{n} @gandddastudio">'
                   f'{icono_red(svg)}<span>{n}</span></a>' for n, url, k, svg in REDES)


UI = {
    "es": dict(home="index.html", support="soporte.html", pol_dir="privacidad",
               nav_apps="Apps", nav_about="Acerca de", nav_support="Soporte", other="EN", other_lang="en",
               skip="Saltar al contenido", sound="Sonido", made="Hecho en México", social="Redes sociales",
               desc="Ganddda Studio: apps y juegos divertidos para todos, hechos en México. Michis, mosquitos, suerte, tarot y más."),
    "en": dict(home="index.html", support="support.html", pol_dir="privacy",
               nav_apps="Apps", nav_about="About", nav_support="Support", other="ES", other_lang="es",
               skip="Skip to content", sound="Sound", made="Made in Mexico", social="Social media",
               desc="Ganddda Studio: fun apps and games for everyone, made in Mexico. Cats, mosquitoes, luck, tarot and more."),
}

MICHI_SVG = """<svg viewBox="0 0 130 72" xmlns="http://www.w3.org/2000/svg"><g fill="currentColor">
<path d="M30 40c-9-2-16-9-17-19-1-6 2-11 6-13-3 6-2 13 3 18 3 3 7 5 11 6z"/>
<path d="M28 34c4-9 16-14 34-14h26c5 0 9-2 12-6l5-9 3 9 6-8 1 11c5 4 7 10 5 16-2 7-8 10-15 11l-2 19h-7l-2-15H62l-5 15h-7l1-16c-11-2-19-6-23-13z"/>
</g><circle cx="108" cy="25" r="2.2" fill="#0E0B1F"/></svg>"""


def leer_catalogo():
    """Lee apps.js (sintaxis de JavaScript) y lo convierte a datos de Python."""
    src = (RAIZ / "apps.js").read_text(encoding="utf-8")
    limpio, i, en_str = [], 0, False
    while i < len(src):
        c = src[i]
        if en_str:
            limpio.append(c)
            if c == "\\":
                limpio.append(src[i + 1])
                i += 1
            elif c == '"':
                en_str = False
        elif c == '"':
            en_str = True
            limpio.append(c)
        elif src.startswith("//", i):
            while i < len(src) and src[i] != "\n":
                i += 1
            continue
        else:
            limpio.append(c)
        i += 1
    js = "".join(limpio)

    def a_json(texto):
        partes = re.split(r'("(?:[^"\\]|\\.)*")', texto)
        for k in range(0, len(partes), 2):  # solo fuera de las cadenas
            partes[k] = re.sub(r"([A-Za-z_]\w*)\s*:", r'"\1":', partes[k])
            partes[k] = re.sub(r",(\s*[\]}])", r"\1", partes[k])
        return "".join(partes)

    def bloque(nombre):
        m = re.search(rf"export\s+const\s+{nombre}\s*=\s*", js)
        if not m:
            raise SystemExit(f"apps.js: falta «export const {nombre} = ...»")
        resto = js[m.end():]
        fin = resto.index(";\n") if ";\n" in resto else len(resto)
        try:
            return json.loads(a_json(resto[:fin]))
        except json.JSONDecodeError as e:
            raise SystemExit(f"apps.js: error de formato en {nombre} ({e}). Revisa comas y comillas dobles.")

    return bloque("CATEGORIES"), bloque("APPS")


CATEGORIAS, CATALOGO = leer_catalogo()
POLITICAS = {a["slug"]: a for a in APPS}
for _app in CATALOGO:
    if _app["id"] not in POLITICAS:
        raise SystemExit(f"Falta la política de privacidad de «{_app['id']}» en la lista APPS de este script.")
    if _app["category"] not in CATEGORIAS:
        raise SystemExit(f"«{_app['id']}» usa la categoría «{_app['category']}», que no está en CATEGORIES.")
    POLITICAS[_app["id"]]["nombre"] = _app["name"]
APPS = [POLITICAS[a["id"]] for a in CATALOGO]


def pagina(lang, titulo, cuerpo, prof, otro_href, inicio=False):
    u = UI[lang]
    base = "../" * prof
    home = base + ("" if lang == "es" else "en/") + u["home"]
    sup = base + ("" if lang == "es" else "en/") + u["support"]
    anc = "" if inicio else home
    if inicio:
        marca = ('<button class="wordmark" id="marca" type="button" aria-label="Ganddda Studio">'
                 '<span class="wm-g">Ganddda</span><span class="wm-s">Studio</span></button>')
        sonido = f'<button class="sonido" id="sonido" type="button" aria-pressed="false" aria-label="{u["sound"]}">🔇</button>'
        script = f'<script type="module" src="{base}js/site.js"></script>\n'
        extras = (f'<div class="relampago" aria-hidden="true"></div>\n'
                  f'<div class="michi" aria-hidden="true">{MICHI_SVG}</div>\n'
                  f'<div class="aviso" id="aviso" role="status" aria-live="polite"></div>\n')
    else:
        marca = (f'<a class="wordmark" href="{home}" aria-label="Ganddda Studio">'
                 '<span class="wm-g">Ganddda</span><span class="wm-s">Studio</span></a>')
        sonido = script = extras = ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{u['desc']}">
<meta name="theme-color" content="#0E0B1F">
<meta property="og:type" content="website">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{u['desc']}">
<meta property="og:image" content="{SITIO}/img/creador-og.jpg">
<link rel="icon" href="{base}img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FUENTES}" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css">
{script}</head>
<body data-base="{base}">
<a class="skip" href="#contenido">{u['skip']}</a>
<header class="top"><div class="wrap">
  {marca}
  <nav class="nav" aria-label="Ganddda Studio">
    <a href="{anc}#apps">{u['nav_apps']}</a><a href="{anc}#acerca">{u['nav_about']}</a><a href="{sup}">{u['nav_support']}</a>
    <a class="idioma" href="{otro_href}" hreflang="{u['other_lang']}" lang="{u['other_lang']}">{u['other']}</a>{sonido}
  </nav>
</div></header>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie"><div class="wrap">
  <span>© 2026 Ganddda Studio · {u['made']}</span>
  <nav class="pie-redes" aria-label="{u['social']}">{enlaces_redes("pie-red")}</nav>
  <span class="mono"><a href="mailto:{CONTACTO}">{CONTACTO}</a> · <a href="{sup}">{u['nav_support']}</a></span>
</div></footer>
{extras}</body>
</html>
"""


INICIO = {
    "es": dict(
        titulo="Ganddda Studio · Apps divertidas para todos",
        kicker="estudio indie · hecho en México",
        h1='Apps divertidas <span class="hl">para todos.</span>',
        lead="Juegos, herramientas y un poquito de suerte. Hechas con cariño, en tres idiomas y sin cuentas obligatorias.",
        stats=["<b>{n}</b> APPS", "<b>3</b> IDIOMAS", "<b>0</b> CUENTAS OBLIGATORIAS", "<b>∞</b> MICHIS"],
        catalogo="Catálogo", filtrar="Filtrar por categoría",
        alt="El creador de Ganddda Studio con un gato Maine Coon en brazos",
        caption="// el Doctor Molina + michi",
        kicker2="el creador", h2="Detrás de Ganddda",
        kicker3="@gandddastudio", h3="Síguenos",
        redes_txt="Adelantos, michis amasando y avisos de lanzamiento. Te esperamos en Instagram, TikTok, Facebook y YouTube.",
        bio=[
            "A los 16 años soñaba con ser programador y crear mis propios videojuegos. El camino dio una vuelta: primero aprendí arreglando <strong>software financiero</strong>, donde cada error cuesta dinero real y cada detalle importa.",
            "En el mundo profesional me conocen como <strong>«el Doctor» Molina</strong>; en los juegos, como <strong>Ganddda</strong>. Ganddda Studio junta las dos cosas: el oficio de quien arregla sistemas críticos y las ganas de aquel chavo de 16 de hacer <strong>apps divertidas para todos</strong>.",
        ],
        ficha=[("alias.profesional", '<span class="str">"el Doctor" Molina</span>'),
               ("gamertag", '<span class="str">"Ganddda"</span>'),
               ("hecho.en", "México"),
               ("sueño.desde", "los 16 años"),
               ("apps", '{n} → ∞ <span class="cursor"></span>')],
    ),
    "en": dict(
        titulo="Ganddda Studio · Fun apps for everyone",
        kicker="indie studio · made in Mexico",
        h1='Fun apps <span class="hl">for everyone.</span>',
        lead="Games, tools and a little bit of luck. Made with care, in three languages, no sign-up required.",
        stats=["<b>{n}</b> APPS", "<b>3</b> LANGUAGES", "<b>0</b> REQUIRED ACCOUNTS", "<b>∞</b> CATS"],
        catalogo="Catalog", filtrar="Filter by category",
        alt="The creator of Ganddda Studio holding a Maine Coon cat",
        caption="// Doctor Molina + cat",
        kicker2="the creator", h2="Behind Ganddda",
        kicker3="@gandddastudio", h3="Follow us",
        redes_txt="Sneak peeks, kneading cats and launch news. Find us on Instagram, TikTok, Facebook and YouTube.",
        bio=[
            "At 16 I dreamed of becoming a programmer and making my own video games. The road took a detour: I first learned by fixing <strong>financial software</strong>, where every bug costs real money and every detail matters.",
            "Professionally I'm known as <strong>“the Doctor” Molina</strong>; in games, as <strong>Ganddda</strong>. Ganddda Studio brings both together: the craft of someone who fixes critical systems and that 16-year-old's drive to make <strong>fun apps for everyone</strong>.",
        ],
        ficha=[("alias.professional", '<span class="str">"the Doctor" Molina</span>'),
               ("gamertag", '<span class="str">"Ganddda"</span>'),
               ("made.in", "Mexico"),
               ("dreaming.since", "age 16"),
               ("apps", '{n} → ∞ <span class="cursor"></span>')],
    ),
}


def escribir(ruta, texto):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


def iconos():
    for a in APPS:
        src = APPS_DIR / a.get("carpeta", "-") / "assets" / "icon" / "icon.png"
        if not src.exists():
            continue
        im = Image.open(src).convert("RGBA")
        im.thumbnail((256, 256), Image.LANCZOS)
        im.save(RAIZ / "img" / f"{a['slug']}.png", optimize=True)
    for a in CATALOGO:
        if not (RAIZ / "img" / f"{a['id']}.png").exists():
            print(f"Aviso: falta el ícono img/{a['id']}.png")
    Image.open(RAIZ / "img" / "mi-suerte-hoy.png").resize((64, 64), Image.LANCZOS).save(RAIZ / "img" / "favicon.png")


def generar(lang):
    t, u, h = T[lang], UI[lang], INICIO[lang]
    pre = RAIZ if lang == "es" else RAIZ / "en"
    prof0 = 0 if lang == "es" else 1
    n = len(CATALOGO)

    # Inicio
    sin_js = "\n".join(
        f'    <li><a href="{u["pol_dir"]}/{a["id"]}.html">{a["name"][lang]}</a> · {a["tagline"][lang]}</li>'
        for a in CATALOGO)
    stats = "".join(f"<li>{s.format(n=n)}</li>" for s in h["stats"])
    bio = "\n".join(f"      <p>{p}</p>" for p in h["bio"])
    ficha = "\n".join(f"        <div><dt>{k}</dt><dd>{v.format(n=n)}</dd></div>" for k, v in h["ficha"])
    img = "../img" if lang == "en" else "img"
    cuerpo = f"""<section class="hero wrap">
  <p class="kicker mono">{h['kicker']}</p>
  <h1>{h['h1']}</h1>
  <p class="lead">{h['lead']}</p>
  <ul class="stats mono">{stats}</ul>
</section>
<section class="catalogo wrap" id="apps" aria-labelledby="t-apps">
  <div class="barra">
    <h2 id="t-apps">{h['catalogo']}</h2>
    <div class="filtros" id="filtros" role="group" aria-label="{h['filtrar']}"></div>
  </div>
  <ul class="bento" id="bento"></ul>
  <noscript><ul class="lista-simple">
{sin_js}
  </ul></noscript>
</section>
<section class="acerca" id="acerca" aria-labelledby="t-acerca">
  <div class="wrap grid">
    <figure class="retrato">
      <img src="{img}/creador.webp" alt="{h['alt']}" width="760" height="760" loading="lazy">
      <figcaption>{h['caption']}</figcaption>
    </figure>
    <div>
      <p class="kicker mono">{h['kicker2']}</p>
      <h2 id="t-acerca">{h['h2']}</h2>
{bio}
      <dl class="ficha">
{ficha}
      </dl>
    </div>
  </div>
</section>
<section class="siguenos wrap" id="redes" aria-labelledby="t-redes">
  <p class="kicker mono">{h['kicker3']}</p>
  <h2 id="t-redes">{h['h3']}</h2>
  <p>{h['redes_txt']}</p>
  <div class="redes">{enlaces_redes("red")}</div>
</section>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Ganddda Studio","url":"{SITIO}/","email":"{CONTACTO}","sameAs":[{",".join('"' + r[1] + '"' for r in REDES)}]}}</script>"""
    otro = "en/index.html" if lang == "es" else "../index.html"
    escribir(pre / "index.html", pagina(lang, h["titulo"], cuerpo, prof0, otro, inicio=True))

    # Soporte
    otro_sup = "en/support.html" if lang == "es" else "../soporte.html"
    cuerpo = (f'<article class="doc wrap"><p class="kicker mono">ganddda studio</p><h1>{t["sup_title"]}</h1>'
              f'<p>{t["sup"]}</p>\n<p class="mail"><a href="mailto:{CONTACTO}">{CONTACTO}</a></p>'
              f'<p>{t["sup_buy"]}</p></article>')
    escribir(pre / t["support"], pagina(lang, f"{t['sup_title']} · Ganddda Studio", cuerpo, prof0, otro_sup))

    # Políticas
    for a in APPS:
        nombre = a["nombre"][lang]
        secs = [f"<h2>{t['sum_t']}</h2><p>{t['sum']}</p>",
                f"<h2>{t['who_t']}</h2><p>{t['who'].format(app=nombre, mail=CONTACTO)}</p>",
                f"<h2>{t['data_t']}</h2><ul>" + "".join(f"<li>{d}</li>" for d in a["datos"][lang]) + "</ul>"]
        if ADS in a["extras"] and "kids" not in a["datos"]:
            secs.append(f"<h2>{t['ads_t']}</h2><p>{t['ads']}</p>")
        if IAP in a["extras"]:
            secs.append(f"<h2>{t['iap_t']}</h2><p>{t['iap']}</p>")
        for k in ("share", "kids", "del", "chg"):
            body = t["dele"] if k == "del" else t[k]
            if k == "kids" and "kids" in a["datos"]:
                body = a["datos"]["kids"][lang]
            secs.append(f"<h2>{t[k + '_t']}</h2><p>{body}</p>")
        cuerpo = f"""<article class="doc wrap">
<img class="mini" src="{'../' * (prof0 + 1)}img/{a['slug']}.png" alt="" width="72" height="72">
<h1>{t['pol_title']} · {nombre}</h1>
<p class="fecha">{t['updated']}: {ACTUALIZADO[lang]}</p>
{chr(10).join(secs)}
</article>"""
        otro_pol = (f"../en/privacy/{a['slug']}.html" if lang == "es"
                    else f"../../privacidad/{a['slug']}.html")
        escribir(pre / t["pol_dir"] / f"{a['slug']}.html",
                 pagina(lang, f"{t['pol_title']} · {nombre}", cuerpo, prof0 + 1, otro_pol))


if __name__ == "__main__":
    iconos()
    generar("es")
    generar("en")
    print(f"Sitio generado en {RAIZ} con {len(CATALOGO)} apps.")
