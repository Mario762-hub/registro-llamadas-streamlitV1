from datetime import datetime, date
import pytz
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Registro de Llamadas", page_icon="📞")

# Inicializamos el DataFrame en sesión
if "llamadas" not in st.session_state:
    st.session_state.llamadas = pd.DataFrame(columns=["Fecha", "Hora", "Usuario"])

st.title("📞 Registro de llamadas")

# Nombre de usuario
usuario = st.text_input("Nombre del usuario", placeholder="Ej: Enrique")

# Selector de fecha con valor por defecto = hoy
fecha_seleccionada = st.date_input("Selecciona la fecha de la llamada", value=date.today())

# Botón
if st.button("Registrar llamada"):
    if usuario.strip() != "":
        # Hora actual en zona horaria de Chile
        tz_chile = pytz.timezone("America/Santiago")
        now = datetime.now(tz_chile)

        nueva_llamada = {
            "Fecha": fecha_seleccionada.strftime("%Y-%m-%d"),  # 👈 fecha seleccionada
            "Hora": now.strftime("%H:%M:%S"),
            "Usuario": usuario.strip()
        }

        st.session_state.llamadas = pd.concat(
            [st.session_state.llamadas, pd.DataFrame([nueva_llamada])],
            ignore_index=True
        )
        st.success(f"✅ Llamada registrada para el {nueva_llamada['Fecha']}")
    else:
        st.warning("⚠️ Ingresa un nombre antes de registrar la llamada.")

# Mostrar historial
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
