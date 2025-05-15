# -*- coding: utf-8 -*-
"""
Created on Wed May 14 21:55:18 2025

@author: matorresm
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz  # 👈 importar pytz

st.set_page_config(page_title="Registro de Llamadas", page_icon="📞")

# Inicializamos el DataFrame en sesión
if "llamadas" not in st.session_state:
    st.session_state.llamadas = pd.DataFrame(columns=["Fecha", "Hora", "Usuario"])

st.title("📞 Registro de llamadas")

usuario = st.text_input("Nombre del usuario", placeholder="Ej: Enrique")

if st.button("Registrar llamada"):
    if usuario.strip() != "":
        # Establecer la hora con zona horaria de Chile
        tz_chile = pytz.timezone("America/Santiago")
        now = datetime.now(tz_chile)

        nueva_llamada = {
            "Fecha": now.strftime("%Y-%m-%d %H:%M:%S"),
            "Hora": now.strftime("%H:%M:%S"),
            "Usuario": usuario.strip()
        }

        st.session_state.llamadas = pd.concat(
            [st.session_state.llamadas, pd.DataFrame([nueva_llamada])],
            ignore_index=True
        )
        st.success("✅ Llamada registrada correctamente")
    else:
        st.warning("⚠️ Ingresa un nombre antes de registrar la llamada.")

st.subheader("📋 Historial de llamadas")
st.dataframe(st.session_state.llamadas, use_container_width=True)

# Botón para descargar como CSV
csv = st.session_state.llamadas.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Descargar historial",
    data=csv,
    file_name="llamadas.csv",
    mime="text/csv"
)

