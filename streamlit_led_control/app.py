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

# Callback de mensaje
def on_message(client, userdata, msg):
    st.write(f"Mensaje recibido: {msg.topic} {msg.payload.decode()}")

# Inicializa cliente MQTT
def initialize_mqtt():
    try:
        client_id = "control_led_app"
        client = mqtt.Client(client_id)
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(mqtt_broker, mqtt_port, 60)
        client.loop_start()  # Iniciar el bucle de la red en segundo plano
        return client
    except Exception as e:
        st.write(f"Error al inicializar el cliente MQTT: {e}")
        return None

client = initialize_mqtt()

# Función para enviar mensaje de aplauso
def send_clap():
    if client:
        try:
            client.publish(mqtt_topic, "Palmada")
            st.write("Mensaje de aplauso enviado.")
        except Exception as e:
            st.write(f"Error al enviar el mensaje: {e}")
    else:
        st.write("Cliente MQTT no está inicializado.")

# Interfaz de usuario de Streamlit
st.title("Control de LED con Aplausos")
st.write("Presiona el botón para simular un aplauso y controlar el LED.")

if st.button("Simular Aplauso"):
    send_clap()
