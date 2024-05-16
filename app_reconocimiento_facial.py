import paho.mqtt.client as paho
import time
import json
import streamlit as st
import face_recognition
from PIL import Image

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

st.title("Cerradura Inteligente")

img_file_buffer = st.file_uploader("Subir imagen de cámara", type=["jpg", "jpeg", "png"])

if img_file_buffer is not None:
    # Convertir la imagen en un arreglo numpy
    image = np.array(Image.open(img_file_buffer))
    
    # Reconocimiento facial
    face_locations = face_recognition.face_locations(image)
    
    if face_locations:
        st.success("Cara detectada. Abriendo la cerradura.")
        client1.publish("IMIA", "{'gesto': 'Abre'}", qos=0, retain=False)
    else:
        st.error("No se detectó ninguna cara.")
