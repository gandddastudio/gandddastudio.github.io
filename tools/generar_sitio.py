"""Genera el sitio estático de Ganddda Studio para GitHub Pages.

Uso (desde la carpeta ganddda_web):
    python tools/generar_sitio.py

Edita CONTACTO, PUBLICADO y la lista APPS; vuelve a correr el script y sube los cambios.
"""
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
APPS_DIR = RAIZ.parent

CONTACTO = "gandddastudio@gmail.com"
ACTUALIZADO = {"es": "19 de noviembre de 2026", "en": "November 19, 2026"}

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
         ], "en": [
             "<b>Your cat's photo:</b> if you add your cat, you pick the photo from your gallery. It is stored only on your phone.",
             "<b>Notifications:</b> to let you know about lives or challenges, if you turn them on.",
             "<b>Progress and collection:</b> stored only on your phone.",
         ]}),
    dict(slug="diableros", carpeta="diableros_central", id="com.ganddda.diableros",
         nombre={"es": "Diableros de la Central", "en": "Diableros de la Central"},
         lema={"es": "Reparte en diablito con los michis de la Central.",
               "en": "Deliver by hand truck with the cats of the Central market."},
         extras=[],
         datos={"es": [
             "<b>Sensores de movimiento:</b> para controlar el juego.",
             "<b>Progreso:</b> se guarda solo en tu teléfono.",
             "Esta app no tiene anuncios ni compras y no se conecta a internet.",
         ], "en": [
             "<b>Motion sensors:</b> to control the game.",
             "<b>Progress:</b> stored only on your phone.",
             "This app has no ads or purchases and does not connect to the internet.",
         ]}),
]

# Cambia a True cada app cuando ya esté publicada en Google Play.
PUBLICADO = {a["slug"]: False for a in APPS}

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


def pagina(lang, titulo, cuerpo, prof, otro_href):
    t = T[lang]
    base = "../" * prof
    home = base + ("" if lang == "es" else "en/") + t["home"]
    sup = base + ("" if lang == "es" else "en/") + t["support"]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<link rel="icon" href="{base}img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css">
</head>
<body>
<header>
  <a class="marca" href="{home}"><span>Ganddda</span><small>Studio</small></a>
  <nav><a href="{home}">{t['apps']}</a><a href="{sup}">{t['support_t']}</a><a href="{otro_href}">{t['other']}</a></nav>
</header>
<main>
{cuerpo}
</main>
<footer>{t['foot']} · <a href="mailto:{CONTACTO}">{CONTACTO}</a></footer>
</body>
</html>
"""


def escribir(ruta, texto):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


def iconos():
    for a in APPS:
        src = APPS_DIR / a["carpeta"] / "assets" / "icon" / "icon.png"
        if not src.exists():
            continue
        im = Image.open(src).convert("RGBA")
        im.thumbnail((256, 256), Image.LANCZOS)
        im.save(RAIZ / "img" / f"{a['slug']}.png", optimize=True)
    fav = Image.open(RAIZ / "img" / "mi-suerte-hoy.png")
    fav.resize((64, 64), Image.LANCZOS).save(RAIZ / "img" / "favicon.png")


def generar(lang):
    t = T[lang]
    pre = RAIZ if lang == "es" else RAIZ / "en"
    prof0 = 0 if lang == "es" else 1
    base = "../" * prof0

    # Inicio
    tarjetas = []
    for a in APPS:
        n = a["nombre"][lang]
        url = f"https://play.google.com/store/apps/details?id={a['id']}"
        boton = (f"<a class='btn' href='{url}'>{t['play']}</a>" if PUBLICADO[a['slug']]
                 else f"<span class='btn off'>{t['soon']}</span>")
        tarjetas.append(f"""<article class="app">
  <img src="{base}img/{a['slug']}.png" alt="" width="96" height="96">
  <div><h3>{n}</h3><p>{a['lema'][lang]}</p>
  <div class="acciones">{boton}<a href="{t['pol_dir']}/{a['slug']}.html">{t['privacy']}</a></div></div>
</article>""")
    cuerpo = f"""<section class="hero"><h1><span>Ganddda</span><small>Studio</small></h1><p>{t['tagline']}</p></section>
<h2>{t['apps']}</h2>
<div class="grid">
{chr(10).join(tarjetas)}
</div>"""
    otro = "en/index.html" if lang == "es" else "../index.html"
    escribir(pre / "index.html", pagina(lang, t["title"], cuerpo, prof0, otro))

    # Soporte
    otro_sup = "en/support.html" if lang == "es" else "../soporte.html"
    cuerpo = f"""<article class="doc"><h1>{t['sup_title']}</h1><p>{t['sup']}</p>
<p class="mail"><a href="mailto:{CONTACTO}">{CONTACTO}</a></p><p>{t['sup_buy']}</p></article>"""
    escribir(pre / t["support"], pagina(lang, f"{t['sup_title']} · Ganddda Studio", cuerpo, prof0, otro_sup))

    # Políticas
    for a in APPS:
        n = a["nombre"][lang]
        secs = [f"<h2>{t['sum_t']}</h2><p>{t['sum']}</p>",
                f"<h2>{t['who_t']}</h2><p>{t['who'].format(app=n, mail=CONTACTO)}</p>",
                f"<h2>{t['data_t']}</h2><ul>" + "".join(f"<li>{d}</li>" for d in a["datos"][lang]) + "</ul>"]
        if ADS in a["extras"]:
            secs.append(f"<h2>{t['ads_t']}</h2><p>{t['ads']}</p>")
        if IAP in a["extras"]:
            secs.append(f"<h2>{t['iap_t']}</h2><p>{t['iap']}</p>")
        for k in ("share", "kids", "del", "chg"):
            body = t["dele"] if k == "del" else t[k]
            secs.append(f"<h2>{t[k + '_t']}</h2><p>{body}</p>")
        cuerpo = f"""<article class="doc">
<img class="mini" src="{'../' * (prof0 + 1)}img/{a['slug']}.png" alt="" width="64" height="64">
<h1>{t['pol_title']} · {n}</h1>
<p class="fecha">{t['updated']}: {ACTUALIZADO[lang]}</p>
{chr(10).join(secs)}
</article>"""
        otro_pol = (f"../en/privacy/{a['slug']}.html" if lang == "es"
                    else f"../../privacidad/{a['slug']}.html")
        escribir(pre / t["pol_dir"] / f"{a['slug']}.html",
                 pagina(lang, f"{t['pol_title']} · {n}", cuerpo, prof0 + 1, otro_pol))


if __name__ == "__main__":
    iconos()
    generar("es")
    generar("en")
    print("Sitio generado en", RAIZ)
