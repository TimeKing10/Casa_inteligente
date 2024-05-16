import streamlit as st
import pyaudio
import numpy as np

# Función para detectar palmadas en el audio
def detectar_palmadas(stream):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 2000  # Umbral de detección de palmadas

    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)
        if max(audio_data) > THRESHOLD:
            return True

# Interfaz de usuario con Streamlit
st.title("Detector de Palmadas")

# Configuración del dispositivo de audio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

st.write("Haga una palmada para iniciar la detección.")

if st.button("Iniciar Detección"):
    st.write("Detección iniciada. Haga una palmada para detener.")
    palmada_detectada = detectar_palmadas(stream)
    if palmada_detectada:
        st.write("Palmada detectada. ¡Bien hecho!")
    else:
        st.write("No se detectó ninguna palmada.")

# Cierre del stream de audio
stream.stop_stream()
stream.close()
audio.terminate()
