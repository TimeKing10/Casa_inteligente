import streamlit as st
import speech_recognition as sr

# Función para el reconocimiento de voz
def reconocer_voz(audio_file):
    # Inicializamos el reconocedor
    recognizer = sr.Recognizer()

    # Cargamos el archivo de audio
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    # Realizamos la transcripción del audio a texto
    try:
        text = recognizer.recognize_google(audio_data, language="es-ES")
        return text
    except sr.UnknownValueError:
        return "No se pudo reconocer el audio"
    except sr.RequestError as e:
        return f"No se pudo completar la solicitud: {e}"

# Interfaz de usuario con Streamlit
st.title("Reconocimiento de Voz")

uploaded_audio = st.file_uploader("Subir archivo de audio", type=["wav"])

if uploaded_audio:
    # Realizamos el reconocimiento de voz
    transcription = reconocer_voz(uploaded_audio)

    # Mostramos la transcripción
    st.write(f"Transcripción: {transcription}")
