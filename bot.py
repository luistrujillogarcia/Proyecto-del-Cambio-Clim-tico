import discord
from discord.ext import commands
import requests
import pyttsx3
from googletrans import Translator
import asyncio
import matplotlib.pyplot as plt
import os

# Inicializar bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Configuración de voz
def talk(text, voz_id=0):
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    engine.setProperty("volume", 0.9)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voz_id].id)
    engine.say(text)
    engine.runAndWait()

# Guardar voz actual (por defecto masculina)
bot.voz_actual = 0

# Voz
@bot.command()
async def voz(ctx, tipo: str):
    if tipo.lower() == "masculina":
        bot.voz_actual = 0
        await ctx.send("✅ Voz cambiada a masculina")
    elif tipo.lower() == "femenina":
        bot.voz_actual = 1
        await ctx.send("✅ Voz cambiada a femenina")
    else:
        await ctx.send("Por favor, elige 'masculina' o 'femenina'.")

# Presentacíon
@bot.command()
async def hello(ctx):
    mensaje = "Hola, soy tu ingenioso asistente virtual, Llámame Norbot 🤖"
    await ctx.send(mensaje)
    talk(mensaje, bot.voz_actual)

# Clima
@bot.command()
async def clima(ctx, *, ciudad: str):
    prediccion = obtener_clima(ciudad)
    mensaje = f"El clima en {ciudad} es: {prediccion}"
    await ctx.send(mensaje)
    talk(mensaje, bot.voz_actual)

# Clima en las ciudades
def obtener_clima(ciudad: str) -> str:
    url = f"https://wttr.in/{ciudad}?format=%C+%t&lang=es"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        clima = respuesta.text.strip()
        if "lluvia" in clima.lower():
            clima += " ☔ No olvides tu paraguas."
        elif "soleado" in clima.lower():
            clima += " 😎 Ponte tus gafas de sol."
        elif "nieve" in clima.lower():
            clima += " ❄️ Hora de hacer un muñeco de nieve."
        elif "nublado" in clima.lower():
            clima += " 🌥️ Parece que el sol se escondió."
        return clima
    else:
        return "No se pudo obtener información del clima."

# --- Nueva función: obtener temperatura numérica ---
def obtener_temperatura(ciudad: str) -> float:
    """
    Devuelve solo la temperatura actual en °C para una ciudad.
    Usa wttr.in y convierte la respuesta en número.
    """
    url = f"https://wttr.in/{ciudad}?format=%t"
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            temp = respuesta.text.strip()
            # Quitar símbolos y convertir a número
            return float(temp.replace("°C", "").replace("°F", "").replace("+",""))
        else:
            return None
    except:
        return None

# Información climática
@bot.command()
async def climainfo(ctx, *, ciudad: str = "el mundo"):
    """
    Muestra información sobre el clima y el cambio climático en una ciudad.
    Si no se especifica ciudad, usa 'el mundo'.
    """
    try:
        # --- Obtener clima actual desde wttr.in ---
        url_clima = f"https://wttr.in/{ciudad}?format=%C+%t&lang=es"
        respuesta = requests.get(url_clima, timeout=5)
        if respuesta.status_code == 200:
            clima = respuesta.text.strip()
        else:
            clima = "No se pudo obtener el clima actual."

        # --- Obtener temperatura numérica ---
        url_temp = f"https://wttr.in/{ciudad}?format=%t"
        temp_res = requests.get(url_temp, timeout=5)
        temperatura = temp_res.text.strip() if temp_res.status_code == 200 else "N/A"

        # --- Obtener calidad del aire (API alternativa) ---
        try:
            url_air = f"https://api.waqi.info/feed/{ciudad}/?token=demo"
            air_data = requests.get(url_air, timeout=5).json()
            if air_data.get("status") == "ok":
                aqi = air_data["data"]["aqi"]
                if aqi <= 50:
                    calidad = f"🌿 Buena ({aqi})"
                elif aqi <= 100:
                    calidad = f"🙂 Moderada ({aqi})"
                elif aqi <= 150:
                    calidad = f"😷 Dañina para sensibles ({aqi})"
                else:
                    calidad = f"☠️ Muy mala ({aqi})"
            else:
                calidad = "No disponible"
        except:
            calidad = "No disponible"

        # --- Crear mensaje ---
        mensaje = (
            f"🌍 **Información sobre el clima en {ciudad.capitalize()}**\n"
            f"- Condición: {clima}\n"
            f"- Temperatura actual: {temperatura}\n"
            f"- Calidad del aire: {calidad}\n\n"
        )

        await ctx.send(mensaje)

        # Habla el resumen (solo parte del texto)
        resumen = f"El clima en {ciudad} es {clima}. La calidad del aire es {calidad}."
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, talk, resumen, bot.voz_actual)

    except Exception as e:
        await ctx.send(f"⚠️ Error al obtener datos: {e}")

# Consejos
@bot.command()
async def consejos(ctx, *, ciudad: str = "mundo"):
    """
    Muestra consejos para minimizar el cambio climático, una imagen y un gráfico de ejemplo.
    """
    # 1. Consejos (texto)
    consejos_texto = (
        "🌱 **Consejos para ayudar al planeta**:\n"
        "- Reduce el uso del auto; usa transporte público o bicicleta.\n"
        "- Apaga luces y desconecta aparatos cuando no los uses.\n"
        "- Planta árboles o ayuda en reforestaciones.\n"
        "- Reduce, reutiliza y recicla tus residuos.\n"
        "- Consume menos carne y apoya productos locales.\n"
    )
    await ctx.send(consejos_texto)

    # 2. Mostrar una imagen ilustrativa (usa una URL o un archivo local)
    # Supongamos que tienes una carpeta "imagenes" con "climate_advice.jpg"
    if os.path.exists("imagenes/climate_advice.jpg"):
        await ctx.send(file=discord.File("imagenes/climate_advice.jpg"))
    else:
        await ctx.send("No encontré imagen ilustrativa disponible.")

    # 3. Generar un gráfico simple ejemplo
    # Por ejemplo: mostrar aumento de temperaturas promedio en los últimos años
    años = [2000, 2005, 2010, 2015, 2020, 2025]
    temp_promedio = [14.5, 14.7, 14.9, 15.2, 15.5, 15.7]  # ejemplo ficticio

    plt.figure(figsize=(6,4))
    plt.plot(años, temp_promedio, marker='o', color='orange')
    plt.title(f"Tendencia de temperatura global ({años[0]}-{años[-1]})")
    plt.xlabel("Año")
    plt.ylabel("Temperatura promedio (°C)")
    plt.grid(True)
    plt.tight_layout()

    graf_nombre = "tendencia_temp.png"
    plt.savefig(graf_nombre)
    plt.close()

    # Enviar gráfico
    await ctx.send(file=discord.File(graf_nombre))

    # Puedes limpiar el archivo si lo deseas
    try:
        os.remove(graf_nombre)
    except:
        pass

#Quizz

# --- Información y quiz de cambio climático ---
informacion_clima = """
🌍 **Cambio Climático**
- Es el aumento gradual de la temperatura media global.
- Causado principalmente por emisiones de gases de efecto invernadero (CO2, metano).
- Consecuencias: derretimiento de glaciares, aumento del nivel del mar, fenómenos meteorológicos extremos.
- Cómo ayudar: usar transporte público, reducir consumo energético, reciclar, plantar árboles.
"""

quiz = [
    {
        "pregunta": "1️⃣ ¿Qué causa principalmente el cambio climático?",
        "opciones": ["a) Emisiones de gases de efecto invernadero", 
                     "b) La gravedad", 
                     "c) La rotación de la Tierra", 
                     "d) Los volcanes"],
        "respuesta": "a"
    },
    {
        "pregunta": "2️⃣ ¿Cuál es una consecuencia del cambio climático?",
        "opciones": ["a) Ninguna de las anteriores ", 
                     "b) Aumento de la gravedad", 
                     "c) Menos luz solar", 
                     "d) Derretimiento de glaciares"],
        "respuesta": "d"
    },
    {
        "pregunta": "3️⃣ ¿Cómo podemos ayudar a combatir el cambio climático?",
        "opciones": ["a) No reciclar", 
                     "b) Consumir más energía", 
                     "c) Usar transporte público", 
                     "d) Cortar árboles"],
        "respuesta": "c"
    }
]

@bot.command()
async def enseñar(ctx):
    await ctx.send(informacion_clima)
    talk("Aquí tienes información sobre el cambio climático.", bot.voz_actual)

@bot.command()
async def quizclima(ctx):
    puntuacion = 0
    await ctx.send("Vamos a comenzar el quiz sobre cambio climático! Responde escribiendo la letra de la opción correcta (a, b, c o d).")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["a","b","c","d"]

    for pregunta in quiz:
        opciones_texto = "\n".join(pregunta["opciones"])
        await ctx.send(f"{pregunta['pregunta']}\n{opciones_texto}")
        try:
            respuesta = await bot.wait_for("message", check=check, timeout=30.0)
            if respuesta.content.lower() == pregunta["respuesta"]:
                await ctx.send("✅ Correcto!")
                puntuacion += 1
            else:
                await ctx.send(f"❌ Incorrecto. La respuesta correcta era: {pregunta['respuesta']}")
        except:
            await ctx.send(f"⏰ Tiempo agotado! La respuesta correcta era: {pregunta['respuesta']}")

# Calificación final
    await ctx.send(f"Tu puntuación final es: {puntuacion}/{len(quiz)}")
    if puntuacion == len(quiz):
        await ctx.send("🌟 ¡Excelente! Sabes mucho sobre cambio climático.")
    elif puntuacion >= len(quiz)//2:
        await ctx.send("👍 Bien hecho! Pero podrías aprender un poco más.")
    else:
        await ctx.send("💡 No te desanimes. Repasa la información y vuelve a intentarlo.")

# Hechos curiosos
def obtener_hecho():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json().get("text")
    else:
        return "No pude obtener un hecho curioso ahora mismo."

@bot.command()
async def ciencia(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    mensaje = f"🔬 Dato de ciencia: {hecho_traducido}"
    await ctx.send(mensaje)
    talk(hecho_traducido, bot.voz_actual)

@bot.command()
async def historia(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    mensaje = f"📜 Dato de historia: {hecho_traducido}"
    await ctx.send(mensaje)
    talk(hecho_traducido, bot.voz_actual)

@bot.command()
async def espacio(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    mensaje = f"🌌 Dato del espacio: {hecho_traducido}"
    await ctx.send(mensaje)
    talk(hecho_traducido, bot.voz_actual)

@bot.command()
async def animales(ctx):
    hecho = obtener_hecho()
    traductor = Translator()
    hecho_traducido = traductor.translate(hecho, src="en", dest="es").text
    mensaje = f"🐾 Dato de animales: {hecho_traducido}"
    await ctx.send(mensaje)
    talk(hecho_traducido, bot.voz_actual)

# Ejecutar el bot
bot.run("Token")
