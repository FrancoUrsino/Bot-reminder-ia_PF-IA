import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta
import re

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

st.title("SmartBot Reminder")
st.write("Tu asistente virtual de recordatorios inteligentes con notificaciones en pantalla.")

user_input = st.text_input("¿Qué recordatorio querés programar?", placeholder="Ej: Recordame estudiar mañana a las 18hs")

prompt_base = (
    "Actuá como un asistente virtual que organiza tareas personales. "
    "Cuando el usuario diga algo como 'Recordame estudiar mañana a las 19hs', "
    "extraé la fecha y hora, y confirmá el recordatorio de forma amable."
)

def extraer_hora(texto):
    coincidencia = re.search(r"(\d{1,2})[:h](\d{2})?", texto)
    if coincidencia:
        hora = int(coincidencia.group(1))
        minutos = int(coincidencia.group(2)) if coincidencia.group(2) else 0
        return hora, minutos
    return None, None

if user_input:
    with st.spinner("Pensando..."):
        try:
            full_prompt = prompt_base + "\n\nUsuario: " + user_input
            response = model.generate_content(full_prompt)
            mensaje = response.text
            st.success(mensaje)

            hora, minutos = extraer_hora(user_input)
            if hora is not None:
                ahora = datetime.now()
                recordatorio_datetime = ahora.replace(hour=hora, minute=minutos, second=0, microsecond=0)
                if recordatorio_datetime < ahora:
                    recordatorio_datetime += timedelta(days=1)

                segundos_espera = (recordatorio_datetime - ahora).total_seconds()
                st.info(f"Te recordaremos esto en {int(segundos_espera // 60)} minutos.")
                with st.spinner("Esperando el momento del recordatorio..."):
                    time.sleep(segundos_espera)
                    st.success(f"¡Es hora! {user_input}")

        except Exception as e:
            st.error(f"Error: {e}")
