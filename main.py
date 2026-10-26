from deep_translator import GoogleTranslator
import discord
from discord.ext import commands
import os
import uuid
import time, random
import asyncio
import requests
from deep_translator import GoogleTranslator

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot conectado:", bot.user)

@bot.event
async def on_message(message):
    print("Mensaje recibido:", message.content)
    await bot.process_commands(message)

@bot.command()
async def recommendation(ctx):
    lista = [
                    "Selecciona electrodomésticos y accesorios que ahorren energía y agua",
                    "Apaga los aparatos electrónicos cuando no los estés utilizando",
                    "Utiliza bombillas LED para ahorrar energía",
                    "Cierra el grifo mientras te lavas los dientes",
                    "Toma duchas cortas para ahorrar agua",
                    "Recicla los materiales que puedas",
                    "Suministra energía renovable a tu hogar siempre que puedas",
                    "Climatiza tu hogar de forma inteligente con un aislamiento adecuado y un mantenimiento correcto de los equipos. ",
                    "Minimiza los residuos reduciendo, reutilizando, reparando y reciclando.",
                    "Considera opciones de transporte más ecológicas, como usar el transporte público, caminar, andar en bicicleta y compartir el coche.",
                    "Minimiza los viajes innecesarios y opta por una mayor eficiencia en el consumo de combustible.",
                    "Evita el uso de productos químicos y pesticidas que puedan dañar el medio ambiente.",
                    "Planta árboles y vegetación para mejorar la calidad del aire y reducir la contaminación.",
                    "Apoya a empresas y productos que sean sostenibles y respetuosos con el medio ambiente.",
                    "Participa en programas de limpieza y conservación del medio ambiente en tu comunidad.",
                    "Educa a otros sobre la importancia de cuidar el medio ambiente y cómo pueden contribuir.",
                    "Reduce el consumo de carne y productos de origen animal, ya que la producción de estos alimentos tiene un impacto ambiental significativo.",
                    "Compra productos locales y de temporada para reducir la huella de carbono asociada al transporte de alimentos."
                ]
    choice = random.choice(lista)
    await ctx.send(choice)

@bot.command()
async def facts(ctx):
    datos = [
                        "El calentamiento global a largo plazo está causado principalmente por actividades humanas.",
                        "Los océanos absorben gran parte del exceso de calor del sistema climático."
                        "La temperatura media global ha aumentado debido principalmente a las actividades humanas.",
                        "Los océanos absorben más del 90% del exceso de calor acumulado en el sistema climático.",
                        "Los glaciares están perdiendo masa en muchas regiones del planeta.",
                        "El dióxido de carbono se libera al quemar carbón, petróleo y gas natural.",
                        "Los bosques absorben CO2 y almacenan carbono.",
                        "La pérdida de hielo marino amenaza el hábitat de los osos polares.",
                        "El cambio climático aumenta el riesgo y la intensidad de algunos episodios de calor extremo.",
                        "El calentamiento global puede intensificar las lluvias extremas en muchas regiones.",
                        "El océano absorbe CO2, lo que provoca su acidificación.",
                        "El deshielo de glaciares contribuye al aumento del nivel del mar.",
                        "Las sequías y las olas de calor pueden perjudicar los cultivos.",
                        "Las energías solar y eólica generan electricidad con bajas emisiones durante su funcionamiento.",
                        "Caminar, ir en bicicleta y usar transporte público puede reducir las emisiones del transporte.",
                        "Mejorar la eficiencia energética ayuda a reducir el consumo de electricidad.",
                        "Reducir las emisiones de gases de efecto invernadero es fundamental para limitar el calentamiento global."
                                            ]
    choice = random.choice(datos)
    await ctx.send(choice)
def traducir_texto(texto: str) -> str:
    """Traduce texto de inglés a español usando la API de MyMemory"""
    if not texto or texto == "Sin descripción disponible.":
        return texto
    url = "https://api.mymemory.translated.net/get"
    parametros = { "q": texto, "langpair": "en|es" }
    try:
        response = requests.get(url, params=parametros, timeout=10)
        if response.status_code == 200:
            datos = response.json()
            # La traducción se encuentra en responseData -> translatedText
            traduccion = datos.get("responseData", {}).get("translatedText")
            if traduccion:
                return traduccion
    except Exception:
        pass
    # Si falla por cualquier motivo, devuelve el texto original sin tumbar el bot
    return texto

@bot.command()
async def evento_m(ctx):
    def obtener_evento():
        url = "https://eonet.gsfc.nasa.gov/api/v3/events"
        parametros = {
            "status": "open",
            "limit": 100
        }

        respuesta = requests.get(url, params=parametros, timeout=15)
        respuesta.raise_for_status()

        eventos = respuesta.json()["events"]

        if not eventos:
            return "No hay eventos disponibles."

        evento = random.choice(eventos)

        nombre_en = evento["title"]
        descripcion_en = evento.get("description") or "Sin descripción disponible."
        enlace = evento["link"]

        # Traducimos usando MyMemory 
        nombre_es = traducir_texto(nombre_en)
        descripcion_es = traducir_texto(descripcion_en)

        return f"🌍 **{nombre_es}**\n{descripcion_es}\n\nMás información: {enlace}"
    print(obtener_evento())

@bot.command() #intento (miserable) de implementar nueva funcion para obtener el clima de una ciudad
async def clima(ctx, city: str):
    def get_weather(city: str) -> str:
        base_url = f"https://wttr.in/{city}?format=%c+%t"
        response = requests.get(base_url)

        if response.status_code == 200:
            return response.text.strip()
        else:
            return "No se pudo obtener la información del clima. Por favor, inténtalo más tarde."
    await ctx.send(get_weather(city))

bot.run("YOUR_BOT_TOKEN")
