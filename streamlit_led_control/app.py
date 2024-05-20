import streamlit as st
import paho.mqtt.client as mqtt

# Configuración del broker MQTT
mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883
mqtt_topic = "Palmadas"

# Callback de conexión al broker MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        st.write("Conectado al broker MQTT.")
    else:
        st.write(f"Falla en conexión, código de retorno: {rc}")

# Inicializa cliente MQTT
client_id = "control_led_app"
client = mqtt.Client(client_id, transport="tcp")
client.on_connect = on_connect
client._callback_api_version = 4  # Configura la versión de la API de callback

# Intentar conectar al broker MQTT
try:
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()  # Iniciar el bucle de la red en segundo plano
except Exception as e:
    st.write(f"Error al conectar al broker MQTT: {e}")

# Función para enviar mensaje de aplauso
def send_clap():
    if client.is_connected():
        client.publish(mqtt_topic, "palmada")
        st.write("Mensaje de aplauso enviado.")
    else:
        st.write("Cliente MQTT no está conectado.")

# Interfaz de usuario de Streamlit
st.title("Control de LED con Aplausos")
st.write("Presiona el botón para simular un aplauso y controlar el LED.")

if st.button("Simular Aplauso"):
    send_clap()
