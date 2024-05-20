import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps
from keras.models import load_model

# Callback de publicación
def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")
    pass

# Callback de mensaje
def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Configuración del broker MQTT
broker = "broker.mqttdashboard.com"
port = 1883

# Inicialización del cliente MQTT
try:
    client1 = paho.Client("APP_CERR")
    client1.on_message = on_message
    client1.on_publish = on_publish
    client1.connect(broker, port)
    client1.loop_start()  # Iniciar el bucle de la red en segundo plano
except Exception as e:
    st.write(f"Error al inicializar el cliente MQTT: {e}")

# Cargar el modelo de Keras
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Interfaz de usuario de Streamlit
st.title("Cerradura Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    img = img.resize((224, 224))
    img_array = np.array(img)
    
    # Normalizar la imagen
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    # Realizar la inferencia
    prediction = model.predict(data)
    if prediction[0][0] > 0.3:
        st.header('Abriendo')
        client1.publish("IMIA", json.dumps({"gesto": "Abre"}), qos=0, retain=False)
        time.sleep(0.2)
    elif prediction[0][1] > 0.3:
        st.header('Cerrando')
        client1.publish("IMIA", json.dumps({"gesto": "Cierra"}), qos=0, retain=False)
        time.sleep(0.2)
