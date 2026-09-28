import time
import random
import os
import json
from urllib.parse import quote
from urllib.request import urlopen
import sounddevice as sd # pyright: ignore[reportMissingImports]
import wave
try:
    import importlib
    sr = importlib.import_module("speech_recognition")
except ImportError as error:
    raise RuntimeError(
        "Falta la dependencia 'SpeechRecognition'. Instálala con: "
        "pip install SpeechRecognition"
    ) from error


class Translator:
    """Traductor sencillo que no requiere la dependencia googletrans."""

    def translate(self, texto, src="es", dest="en"):
        url = (
            "https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl={quote(src)}&tl={quote(dest)}&dt=t&q={quote(texto)}"
        )
        with urlopen(url, timeout=10) as respuesta:
            datos = json.loads(respuesta.read().decode("utf-8"))

        traduccion = "".join(segmento[0] for segmento in datos[0] if segmento[0])

        class Resultado:
            def __init__(self, text):
                self.text = text

        return Resultado(traduccion)

# Configuración base de audio
FRECUENCIA_MUESTREO = 44100
ARCHIVO_TEMPORAL = "audio_temp.wav"

# Vocabulario centrado en Cambio Climático y Sostenibilidad
VOCABULARIO = {
    "facil": ["reciclar", "planeta", "bosque", "basura", "energia", "sol"],
    "medio": ["sostenible", "contaminacion", "reciclaje", "biodiversidad", "ecosistema"],
    "dificil": ["descarbonizacion", "calentamiento global", "huella de carbono", "sustentabilidad"]
}

# Configuración de niveles de dificultad
CONFIG_DIFICULTAD = {
    "1": {"nombre": "FÁCIL 🟢", "tiempo": 4, "vidas": 3, "multiplicador": 1.0},
    "2": {"nombre": "MEDIO 🟡", "tiempo": 3, "vidas": 2, "multiplicador": 1.5},
    "3": {"nombre": "DIFÍCIL 🔴", "tiempo": 2, "vidas": 1, "multiplicador": 2.0}
}

def mostrar_banner():
    print(r"""
  =============================================================
   _____ _____ _____   _____ _____ _____  ___  _   _ 
  |  ___/  __ \  _  | /  ___|  __ \  ___|/ _ \| | | |
  | |__ | /  \/ | | | \ `--.| |  \/ |__ / /_\ \ |_| |
  |  __|| |   | | | |  `--. \ | __|  __||  _  |  _  |
  | |___| \__/\ \_/ / /\__/ / |_\ \ |___| | | | | | |
  \____/ \____/\___/  \____/ \____/\____/\_| |_\_| |_/
  =============================================================
         🌱 APRENDE INGLÉS PARA LA ACCIÓN CLIMÁTICA 🎙️
  =============================================================
    """)

def seleccionar_dificultad():
    print("🎯 SELECCIONA TU NIVEL DE DIFICULTAD CLIMÁTICA:")
    print("1. Fácil 🟢   (4 seg para hablar | 3 Vidas | Puntos x1)")
    print("2. Medio 🟡   (3 seg para hablar | 2 Vidas | Puntos x1.5)")
    print("3. Difícil 🔴 (2 seg para hablar | 1 Vida  | Puntos x2)")
    
    opcion = ""
    while opcion not in CONFIG_DIFICULTAD:
        opcion = input("\n👉 Elige una opción (1-3): ").strip()
        if opcion not in CONFIG_DIFICULTAD:
            print("⚠️ Opción no válida. Intenta de nuevo.")
            
    return CONFIG_DIFICULTAD[opcion], opcion

def traducir_palabra(palabra, translator):
    """Traduce el término ambiental de español a inglés usando googletrans."""
    try:
        resultado = translator.translate(palabra, src='es', dest='en')
        return resultado.text.lower()
    except Exception as e:
        print(f"⚠️ Error al conectar con el servicio de traducción: {e}")
        return None

def grabar_audio(duracion, fs, archivo_salida):
    """Graba el micrófono con sounddevice y guarda el archivo con scipy."""
    print("\n🔴 GRABANDO... ¡Pronuncia el término ecológico en inglés AHORA!")
    grabacion = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("⏹️ Grabación finalizada.")
    with wave.open(archivo_salida, "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(grabacion.dtype.itemsize)
        archivo.setframerate(fs)
        archivo.writeframes(grabacion.tobytes())

def procesar_audio(archivo_audio, recognizer):
    """Convierte el archivo .wav a texto mediante speech_recognition."""
    if not os.path.exists(archivo_audio):
        return None
        
    with sr.AudioFile(archivo_audio) as source:
        audio = recognizer.record(source)
        try:
            texto = recognizer.recognize_google(audio, language="en-US")
            return texto.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("❌ Error de red con el servicio de reconocimiento de voz.")
            return None

def obtener_rango(puntuacion):
    """Sistema de títulos según el grado de concientización y nivel alcanzado."""
    if puntuacion >= 80:
        return "🥇 EMBAJADOR CLIMÁTICO GLOBAL (Nivel Experto)"
    elif puntuacion >= 40:
        return "🥈 ACTIVISTA AMBIENTAL (Nivel Intermedio)"
    else:
        return "🥉 APRENDIZ ECOLÓGICO (¡Sigue practicando!)"

def jugar():
    mostrar_banner()
    translator = Translator()
    recognizer = sr.Recognizer()

    dificultad, clave = seleccionar_dificultad()
    
    if clave == "1":
        palabras = VOCABULARIO["facil"].copy()
    elif clave == "2":
        palabras = VOCABULARIO["medio"].copy()
    else:
        palabras = VOCABULARIO["dificil"].copy()
        
    random.shuffle(palabras)

    puntuacion = 0
    vidas = dificultad["vidas"]
    racha = 0
    
    print(f"\n✅ Modo seleccionado: {dificultad['nombre']}.")
    input("Presiona ENTER para iniciar la ronda...")

    for i, palabra_es in enumerate(palabras, 1):
        if vidas <= 0:
            print("\n" + "💀" * 20)
            print("  ¡GAME OVER! Te has quedado sin vidas.")
            print("💀" * 20)
            break

        ingles_correcto = traducir_palabra(palabra_es, translator)
        if not ingles_correcto:
            continue

        corazones = "❤️ " * vidas
        print("\n" + "═" * 50)
        print(f"📌 Término {i}/{len(palabras)} | Vidas: {corazones} | Puntos: {puntuacion} | Racha: 🔥x{racha}")
        print(f"👉 CONCEPTOS AMBIENTALES: 【 {palabra_es.upper()} 】")
        print("═" * 50)
        input(f"Presiona ENTER para grabar ({dificultad['tiempo']} segundos)...")

        grabar_audio(dificultad["tiempo"], FRECUENCIA_MUESTREO, ARCHIVO_TEMPORAL)

        print("⏳ Analizando pronunciación con IA...")
        respuesta_usuario = procesar_audio(ARCHIVO_TEMPORAL, recognizer)

        if respuesta_usuario:
            print(f'🔊 Se escuchó: "{respuesta_usuario}"')
            if respuesta_usuario == ingles_correcto:
                racha += 1
                puntos_ganados = int(10 * dificultad["multiplicador"]) + (racha * 2)
                puntuacion += puntos_ganados
                print(f"🎉 ¡EXCELENTE! Pronunciación correcta. (+{puntos_ganados} pts)")
            else:
                vidas -= 1
                racha = 0
                print(f'❌ Incorrecto. Dijiste "{respuesta_usuario}", pero la traducción exacta era "{ingles_correcto}".')
                print("💔 Perdiste 1 vida.")
        else:
            vidas -= 1
            racha = 0
            print(f'🤔 No se entendió el audio. La traducción correcta era: "{ingles_correcto}".')
            print("💔 Perdiste 1 vida.")

        if os.path.exists(ARCHIVO_TEMPORAL):
            os.remove(ARCHIVO_TEMPORAL)

        time.sleep(1)

    print("\n" + "=" * 55)
    print("🏁 ¡SESIÓN FINALIZADA! 🏁")
    print("=" * 55)
    print(f"📊 Puntuación Final: {puntuacion} pts")
    print(f"🏆 Rango Ambiental:  {obtener_rango(puntuacion)}")
    print("=" * 55 + "\n")

if __name__ == "__main__":
    jugar()
