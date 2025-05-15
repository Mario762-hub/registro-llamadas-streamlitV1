import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import pytz

st.set_page_config(page_title="Registro de Llamadas", page_icon="📞")

if "llamadas" not in st.session_state:
    st.session_state.llamadas = pd.DataFrame(columns=[
        "Fecha Llamada", "Hora Llamada", "Usuario", "Caso", 
        "Fecha Creación Caso", "Hora Creación Caso", "Tiempo hasta llamada (mm:ss)"
    ])

st.title("📞 Registro de llamadas")

# Inputs
usuario = st.text_input("👤 Nombre del usuario", placeholder="Ej: Enrique")
caso = st.text_input("🧾 Número de caso", placeholder="Ej: 12345678")
fecha_creacion = st.date_input("📅 Fecha de creación del caso", value=date.today())
hora_creacion_str = st.text_input("🕒 Hora de creación del caso (formato HH:MM o HH:MM:SS)", value="08:00")

# Botón
if st.button("Registrar llamada"):
    if usuario.strip() != "" and caso.strip() != "":
        try:
            # Validar hora ingresada
            hora_creacion = datetime.strptime(hora_creacion_str.strip(), "%H:%M:%S").time() \
                if len(hora_creacion_str.strip().split(":")) == 3 \
                else datetime.strptime(hora_creacion_str.strip(), "%H:%M").time()

            # Hora actual en zona horaria Chile
            tz_cl = pytz.timezone("America/Santiago")
            now = datetime.now(tz_cl)

            # Fecha + hora de creación
            dt_creacion = datetime.combine(fecha_creacion, hora_creacion)
            dt_creacion = tz_cl.localize(dt_creacion)

            # Calcular diferencia
            diferencia = now - dt_creacion
            if diferencia.total_seconds() < 0:
                minutos = 0
                segundos = 0
            else:
                total_segundos = int(diferencia.total_seconds())
                minutos = total_segundos // 60
                segundos = total_segundos % 60

            tiempo_str = f"{minutos:02}:{segundos:02}"

            nueva_llamada = {
                "Fecha Llamada": now.strftime("%Y-%m-%d"),
                "Hora Llamada": now.strftime("%H:%M:%S"),
                "Usuario": usuario.strip(),
                "Caso": caso.strip(),
                "Fecha Creación Caso": fecha_creacion.strftime("%Y-%m-%d"),
                "Hora Creación Caso": hora_creacion.strftime("%H:%M:%S"),
                "Tiempo hasta llamada (mm:ss)": tiempo_str
            }

            st.session_state.llamadas = pd.concat(
                [st.session_state.llamadas, pd.DataFrame([nueva_llamada])],
                ignore_index=True
            )

            st.success(f"✅ Llamada registrada. Tiempo desde creación: {tiempo_str} minutos")

        except Exception as e:
            st.error(f"❌ Hora inválida. Usa formato HH:MM o HH:MM:SS — Error: {e}")
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

