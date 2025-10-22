import os
import streamlit as st
import base64
from openai import OpenAI
import openai
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
from streamlit_drawable_canvas import st_canvas

# 💖 CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title='🎨 Tablero Inteligente',
    page_icon='🌸',
    layout='centered'
)

# 🌈 ESTILOS PERSONALIZADOS
st.markdown("""
    <style>
        body {
            background-color: #fdeef4; /* Fondo rosado claro */
            font-family: "Poppins", sans-serif;
            color: #4a4a4a;
        }
        .main {
            background-color: #fff;
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(255, 182, 193, 0.4);
        }
        h1 {
            text-align: center;
            color: #d81b60;
            font-size: 2.5em;
            font-weight: 800;
        }
        h2, h3, h4 {
            color: #ad1457;
            text-align: center;
        }
        .stSidebar {
            background: #f8bbd0;
        }
        .stSidebar > div {
            background-color: #f8bbd0 !important;
        }
        .stButton>button {
            background: linear-gradient(135deg, #f48fb1, #ce93d8);
            color: white;
            border: none;
            border-radius: 15px;
            height: 50px;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(233, 30, 99, 0.3);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #f06292, #ba68c8);
            transform: scale(1.05);
            box-shadow: 0 6px 18px rgba(233, 30, 99, 0.4);
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 1.5px solid #f48fb1;
            padding: 10px;
            font-size: 1em;
        }
        .stSlider>div>div>div>div {
            background-color: #ec407a !important;
        }
        .css-1d391kg {
            background-color: #fdeef4 !important;
        }
        .stAlert {
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

# 🌸 INTERFAZ PRINCIPAL
st.title('💗 Tablero Inteligente')
st.subheader("Dibuja tu idea y deja que la IA te diga qué ve 🎀")

with st.sidebar:
    st.markdown("## 🌷 Acerca de")
    st.markdown("Esta aplicación muestra cómo una **máquina puede interpretar un boceto**. "
                "Explora, dibuja y deja que la IA describa lo que ve. 💡✨")

st.markdown("---")
st.subheader("🎨 Dibuja en el lienzo y presiona el botón para analizarlo")

# 🎀 LIENZO DE DIBUJO
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('✏️ Grosor de línea', 1, 30, 5)
stroke_color = "#8e24aa"  # Lila fuerte
bg_color = "#ffffff"

canvas_result = st_canvas(
    fill_color="rgba(255, 182, 193, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

# 🔐 API KEY
ke = st.text_input('🔑 Ingresa tu clave API', type="password")
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

# 💌 FUNCIÓN PARA ENCODEAR LA IMAGEN
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró en la ruta especificada."

# 🚀 CONFIGURAR CLIENTE OPENAI
client = OpenAI(api_key=api_key)
analyze_button = st.button("💞 Analizar imagen")

# 🧠 PROCESAMIENTO
if canvas_result.image_data is not None and api_key and analyze_button:
    with st.spinner("✨ Analizando tu dibujo..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')

        base64_image = encode_image_to_base64("img.png")
        prompt_text = "Describe brevemente en español la imagen"

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {"type": "image_url",
                             "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=400
            )

            description = response.choices[0].message.content
            st.success("🌸 Resultado del análisis:")
            st.write(description)

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
else:
    if not api_key:
        st.warning("🔔 Por favor ingresa tu clave API antes de continuar.")
