import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
import pyaudio
import struct
import math

#from PIL import Image
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

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

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Cerradura Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # Run the inference
    prediction = model.predict(data)
    print(prediction)
    if prediction[0][0] > 0.3:
        st.header('Abriendo')
        client1.publish("Gestos", "Abre", qos=0, retain=False)
        time.sleep(0.2)
    if prediction[0][1] > 0.3:
        st.header('Cerrando')
        client1.publish("Gestos", "Cierra", qos=0, retain=False)
        time.sleep(0.2)  

FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

def get_rms(block):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

try:
    while True:
        block = stream.read(INPUT_FRAMES_PER_BLOCK, exception_on_overflow=False)
        amplitude = get_rms(block)
        print(amplitude)
        if amplitude > 0.02:  # Adjust this threshold according to your environment
            st.header('Detectada una palmada')
            client1.publish("Palmadas", "Palmada", qos=0, retain=False)
            time.sleep(0.2)

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
