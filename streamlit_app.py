import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import pytz

st.set_page_config(page_title="Registro de Llamadas", page_icon="📞")

if "llamadas" not in st.session_state:
    st.session_state.llamadas = pd.DataFrame(columns=[
        "Fecha Llamada", "Hora Llamada", "Usuario", "Caso", "Fecha Creación Caso", 
        "Hora Creación Caso", "Tiempo hasta llamada"
    ])

st.title("📞 Registro de llamadas")

# Inputs
usuario = st.text_input("👤 Nombre del usuario", placeholder="Ej: Ingresar nombre de usuario")
caso = st.text_input("🧾 Número de caso", placeholder="Ej: 12345678")

fecha_creacion = st.date_input("📅 Fecha de creación del caso", value=date.today())
hora_creacion = st.time_input("⏰ Hora de creación del caso", value=datetime.now().time())

# Botón
if st.button("Registrar llamada"):
    if usuario.strip() != "" and caso.strip() != "":
        # Hora actual de la llamada en zona horaria Chile
        tz_cl = pytz.timezone("America/Santiago")
        now = datetime.now(tz_cl)

        # Fecha y hora creación del caso combinadas
        dt_creacion = datetime.combine(fecha_creacion, hora_creacion)
        dt_creacion = tz_cl.localize(dt_creacion)  # asegurar timezone

        # Calcular diferencia
        diferencia = now - dt_creacion
        tiempo_str = str(diferencia).split(".")[0]  # sin microsegundos

        nueva_llamada = {
            "Fecha Llamada": now.strftime("%Y-%m-%d"),
            "Hora Llamada": now.strftime("%H:%M:%S"),
            "Usuario": usuario.strip(),
            "Caso": caso.strip(),
            "Fecha Creación Caso": fecha_creacion.strftime("%Y-%m-%d"),
            "Hora Creación Caso": hora_creacion.strftime("%H:%M:%S"),
            "Tiempo hasta llamada": tiempo_str
        }

        st.session_state.llamadas = pd.concat(
            [st.session_state.llamadas, pd.DataFrame([nueva_llamada])],
            ignore_index=True
        )

        st.success(f"✅ Llamada registrada ({tiempo_str} desde la creación del caso)")

    else:
        st.warning("⚠️ Ingresa el nombre del usuario y el número de caso.")

# Mostrar tabla
st.subheader("📋 Historial de llamadas")
st.dataframe(st.session_state.llamadas, use_container_width=True)

# Descargar CSV
csv = st.session_state.llamadas.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Descargar historial",
    data=csv,
    file_name="llamadas.csv",
    mime="text/csv"
)

