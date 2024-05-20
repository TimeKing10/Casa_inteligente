import paho.mqtt.client as mqtt
import streamlit as st
import numpy as np
from PIL import Image
from keras.models import load_model
import json
import time

# Callback de publicación
def on_publish(client, userdata, result):
    st.write("El dato ha sido publicado")

# Callback de mensaje
def on_message(client, userdata, message):
    st.write(f"Mensaje recibido: {str(message.payload.decode('utf-8'))}")

# Configuración del broker MQTT
broker = "broker.mqttdashboard.com"
port = 1883

# Función para inicializar el cliente MQTT
def initialize_mqtt_client():
    client = mqtt.Client("APP_CERR")
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect(broker, port)
    client.loop_start()
    return client

client = initialize_mqtt_client()

# Función para publicar mensajes
def publish_message(client, topic, message):
    try:
        client.publish(topic, json.dumps(message), qos=0, retain=False)
    except Exception as e:
        st.write(f"Error al publicar mensaje MQTT: {e}")

# Cargar el modelo de Keras
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Interfaz de usuario de Streamlit
st.title("Casa Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    try:
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
            publish_message(client, "IMIA", {"gesto": "Abre"})
            time.sleep(0.2)
        elif prediction[0][1] > 0.3:
            st.header('Cerrando')
            publish_message(client, "IMIA", {"gesto": "Cierra"})
            time.sleep(0.2)
    except Exception as e:
        st.write(f"Error durante la predicción: {e}")
