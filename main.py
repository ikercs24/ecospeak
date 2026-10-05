import base64
import os
import random
from flask import Flask, jsonify, render_template, request
import googletrans
import speech_recognition as sr

app = Flask(__name__)

VOCABULARIO = {
    "facil": ["reciclar", "planeta", "bosque", "basura", "energia", "sol"],
    "medio": [
        "sostenible",
        "contaminacion",
        "reciclaje",
        "biodiversidad",
        "ecosistema",
    ],
    "dificil": [
        "descarbonizacion",
        "calentamiento global",
        "huella de carbono",
        "sustentabilidad",
    ],
}

translator = googletrans.Translator()
recognizer = sr.Recognizer()


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/obtener_palabra", methods=["POST"])
def obtener_palabra():
  datos = request.get_json()
  dificultad = datos.get("dificultad", "facil")
  palabra = random.choice(VOCABULARIO.get(dificultad, VOCABULARIO["facil"]))

  try:
    trad = translator.translate(palabra, src="es", dest="en")
    traduccion = trad.text.lower()
  except Exception:
    traduccion = palabra.lower()

  return jsonify({"palabra": palabra.upper(), "traduccion": traduccion})


@app.route("/evaluar_audio", methods=["POST"])
def evaluar_audio():
  datos = request.get_json()
  audio_b64 = datos.get("audio").split(",")[1]
  traduccion_esperada = datos.get("traduccion", "").lower()

  archivo_wav = "temp_web.wav"
  with open(archivo_wav, "wb") as f:
    f.write(base64.b64decode(audio_b64))

  texto_reconocido = ""
  try:
    with sr.AudioFile(archivo_wav) as source:
      audio_data = recognizer.record(source)
      texto_reconocido = recognizer.recognize_google(
          audio_data, language="en-US"
      ).lower()
  except Exception:
    texto_reconocido = ""

  if os.path.exists(archivo_wav):
    os.remove(archivo_wav)

  es_correcto = texto_reconocido == traduccion_esperada
  return jsonify({
      "correcto": es_correcto,
      "reconocido": texto_reconocido,
      "esperado": traduccion_esperada,
  })


if __name__ == "__main__":
  app.run(debug=True)
