import streamlit as st
import cv2
import numpy as np
import face_recognition

# Función para el reconocimiento facial
def reconocer_cara(image):
    # Cargamos la imagen y convertimos a RGB (ya que face_recognition requiere imágenes en RGB)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Encontramos todas las caras en la imagen
    face_locations = face_recognition.face_locations(img)
    
    # Iteramos sobre todas las caras encontradas y las marcamos con un rectángulo
    for (top, right, bottom, left) in face_locations:
        # Dibujamos un rectángulo alrededor de la cara
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    
    return image

# Interfaz de usuario con Streamlit
st.title("Reconocimiento Facial")

uploaded_image = st.file_uploader("Subir imagen de cámara", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Convertimos la imagen subida a un arreglo numpy
    image = np.array(uploaded_image)
    
    # Mostramos la imagen original
    st.image(image, caption='Imagen subida', use_column_width=True)
    
    # Realizamos el reconocimiento facial
    image_with_faces = reconocer_cara(image)
    
    # Mostramos la imagen con las caras reconocidas
    st.image(image_with_faces, caption='Caras reconocidas', use_column_width=True)
