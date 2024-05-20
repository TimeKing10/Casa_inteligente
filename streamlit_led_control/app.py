import streamlit as st
import paho.mqtt.client as mqtt

# Configuración de MQTT
mqtt_broker = "broker.mqttdashboard.com"
mqtt_topic_palmadas = "Palmadas"
client_id = "StreamlitLedControl"

# Configuración de Streamlit
st.title("Control de LED con Aplausos")
st.write("Presiona el botón para simular un aplauso y controlar el LED.")

# Función de callback para conexión MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        st.write("Conectado al broker MQTT.")
    else:
        st.write("Falla en conexión, código de retorno: ", rc)

# Inicializa cliente MQTT
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.connect(mqtt_broker)

# Botón para controlar LED con aplausos (Simulación)
if st.button("Simular Aplauso"):
    st.write("Simulando aplauso...")
    client.publish(mqtt_topic_palmadas, "Palmada")
