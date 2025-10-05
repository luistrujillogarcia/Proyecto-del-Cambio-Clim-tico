import discord
from discord.ext import commands
import requests
import pyttsx3
from googletrans import Translator

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

# Inicializar bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

# Guardar voz actual (por defecto masculina)
bot.voz_actual = 0

@bot.command()
async def hello(ctx):
    mensaje = "Hola, soy tu ingenioso asistente virtual, Llámame Norbot 🤖"
    await ctx.send(mensaje)
    talk(mensaje, bot.voz_actual)

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
# Clima

@bot.command()
async def clima(ctx, *, ciudad: str):
    prediccion = obtener_clima(ciudad)
    mensaje = f"El clima en {ciudad} es: {prediccion}"
    await ctx.send(mensaje)
    talk(mensaje, bot.voz_actual)

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

@bot.command()
async def climainfo(ctx, *, ciudad: str):
    mensaje = f"🌍 Información sobre cambio climático en {ciudad}:\n"
    mensaje += "- Aumento promedio de temperatura: +1.2°C en los últimos 50 años.\n"
    mensaje += "- Consejos: Reduce emisiones, usa transporte público, recicla."
    await ctx.send(mensaje)
    talk(mensaje, bot.voz_actual)

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


# Ejecutar el bot
bot.run("Token")
