# 🎙️ EcoSpeak — Aplicación Web de Acción Climática

**EcoSpeak** es una aplicación web interactiva desarrollada con **Flask, HTML5, CSS3 y Python**. Está diseñada para enseñar vocabulario clave sobre el cambio climático y la sustentabilidad en inglés, evaluando la pronunciación de los usuarios en tiempo real mediante el uso de reconocimiento de voz.

---

## 🚀 Características

* **Estructura Web:** Basada en la arquitectura Model-View-Controller (MVC) utilizando Flask para el backend y HTML/CSS/JavaScript para el frontend.
* **Evaluación en Tiempo Real:** Captura el audio desde el micrófono del navegador y lo procesa en el servidor con bibliotecas de reconocimiento de voz.
* **Sistema de Dificultad y Vidas:** Diferentes niveles de vocabulario (Fácil, Medio y Difícil) con contadores de vidas y puntaje.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API / Web Audio API)
* **Reconocimiento de Voz & Traducción:** `SpeechRecognition`, `googletrans`

---

## 📂 Estructura del Proyecto

```text
ecospeak/
├── templates/
│   └── index.html      # Interfaz de usuario (HTML + JS)
├── static/
│   └── style.css       # Estilos visuales de la aplicación
├── ecospeak.py         # Servidor principal y rutas en Flask
├── README.md           # Documentación del proyecto
└── requirements.txt    # Dependencias de Python necesarias
