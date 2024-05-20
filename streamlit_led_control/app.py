# Inicialización del cliente MQTT
def initialize_mqtt_client():
    client = paho.Client("APP_CERR")
    client.on_message = on_message
    client.on_publish = on_publish
    try:
        client.connect(broker, port)
        client.loop_start()  # Iniciar el bucle de la red en segundo plano
        return client
    except Exception as e:
        st.write(f"Error al inicializar el cliente MQTT: {e}")
        return None

client1 = initialize_mqtt_client()

def publish_message(client, topic, message):
    if client is not None:
        try:
            client.publish(topic, json.dumps(message), qos=0, retain=False)
        except Exception as e:
            st.write(f"Error al publicar mensaje MQTT: {e}")
            client.disconnect()
            client = initialize_mqtt_client()

# En tu bloque de predicción
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
            publish_message(client1, "IMIA", {"gesto": "Abre"})
            time.sleep(0.2)
        elif prediction[0][1] > 0.3:
            st.header('Cerrando')
            publish_message(client1, "IMIA", {"gesto": "Cierra"})
            time.sleep(0.2)
    except Exception as e:
        st.write(f"Error durante la predicción: {e}")
