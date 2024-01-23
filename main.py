import streamlit as st
from PIL import Image
import plotly.express as px
import pandas as pd
import numpy as np
import os
import warnings
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

# drive
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
cliente = gspread.authorize(credenciales)
# Locaciones
salaEventos = cliente.open("Base de datos 1").get_worksheet(2)
gym = cliente.open("Base de datos 1").get_worksheet(3)
piscina = cliente.open("Base de datos 1").get_worksheet(4)
parrillas = cliente.open("Base de datos 1").get_worksheet(5)

locaciones = ('Sala de Eventos', 'GYM',
              'Piscina', 'Parrillas')
#--------------------------------------------------------------------------------------------

icono = Image.open("KIW_icono.ico")
st.set_page_config(page_title="guia de reserva", page_icon=icono, layout="wide",)

# Fecha actual
fecha_actual = datetime.now().date().strftime('%d/%m/%Y')
hora_actual = datetime.now().time().strftime('%H:%M')

st.title(f"Guia de reserva de dia {fecha_actual}",)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Horarios
horarios = [
    '7:00 AM',
    '8:00 AM',
    '9:00 AM',
    '10:00 AM',
    '11:00 AM',
    '12:00 PM',
    '1:00 PM',
    '2:00 PM',
    '3:00 PM',
    '4:00 PM',
    '5:00 PM',
    '6:00 PM',
    '7:00 PM',
    '8:00 PM',
    '9:00 PM',
    '10:00 PM'
]

df_salaEventos = pd.DataFrame()
df_gym = pd.DataFrame()
df_piscina = pd.DataFrame()
df_parrillas = pd.DataFrame()

# Agregar la columna 'Hora' con la lista de horarios a cada DataFrame
for df in [df_salaEventos, df_gym, df_piscina, df_parrillas]:
    if 'Hora' not in df.columns or df['Hora'].empty:
        df['Hora'] = horarios
        # Agregar columnas 'Nombre', 'Dpto', 'Disponibilidad' y 'Fecha' si no existen
        for col_name in ['Nombre', 'Dpto']:
            if col_name not in df.columns:
                df[col_name] = [np.nan] * len(horarios)
    if 'Disponibilidad' not in df.columns:
        df['Disponibilidad'] = ['Disponible']*len(horarios)
    if 'Fecha' not in df.columns:
        df['Fecha'] = fecha_actual

# Cuadros
local = st.selectbox("Escoge la seccion a reservar:", locaciones, key='locacion_reserva')

col1, col2 = st.columns((2))

with col1:
    if local == 'Sala de Eventos':
        df_salaEventos.fillna('', inplace=True)
        hSalaEvento = st.dataframe(df_salaEventos.loc[:, df_salaEventos.columns != 'Fecha'], width=650)

    elif local == 'GYM':
        df_gym.fillna('', inplace=True)
        hGYM = st.dataframe(df_gym.loc[:, df_gym.columns != 'Fecha'], width=650)

    elif local == 'Piscina':
        df_piscina.fillna('', inplace=True)
        hPiscina = st.dataframe(df_piscina.loc[:, df_piscina.columns != 'Fecha'], width=650)

    elif local == 'Parrillas':
        df_parrillas.fillna('', inplace=True)
        hParrillas = st.dataframe(df_parrillas.loc[:, df_parrillas.columns != 'Fecha'], width=650)

nombre_usuario = ''
departamento_usuario = ''

with col2:
    st.write("Nombre:")
    nombre_usuario = st.text_input("Ingrese su nombre")

    st.write("Departamento:")
    departamento_usuario = st.text_input("Ingrese su departamento")

    if 'Sala de Eventos' in local:
        horas_disponibles_salaEventos = df_salaEventos.loc[df_salaEventos['Disponibilidad'] == 'Disponible', 'Hora'].tolist()
        hora_SE = st.multiselect('Seleccione el horario en que desea la reserva',
                                horas_disponibles_salaEventos, key='se_disponibilidad')
        # Botón para reservar
        if st.button("Reservar"):
            # Actualizar DataFrames con información de la reserva
                if local == 'Sala de Eventos':
                    df_salaEventos.loc[df_salaEventos['Hora'].isin(hora_SE), 'Nombre'] = nombre_usuario
                    df_salaEventos.loc[df_salaEventos['Hora'].isin(hora_SE), 'Dpto'] = departamento_usuario
                    df_salaEventos.loc[df_salaEventos['Hora'].isin(hora_SE), 'Disponibilidad'] = 'Ocupado'

        salaEventos.update([df_salaEventos.columns.values.tolist()] + df_salaEventos.values.tolist())

        if local == 'Sala de Eventos':
            df_salaEventos.fillna('', inplace=True)
            hSalaEvento.dataframe(df_salaEventos.loc[:, df_salaEventos.columns != 'Fecha'], width=650)

    if 'GYM' in local:
        horas_disponibles_gym = df_gym.loc[df_gym['Disponibilidad'] == 'Disponible', 'Hora'].tolist()
        hora_gym = st.multiselect('Seleccione el horario en que desea la reserva',
                                 horas_disponibles_gym, key='se_disponibilidad')
        # Botón para reservar
        if st.button("Reservar"):
            # Actualizar DataFrames con información de la reserva
            if local == 'Sala de Eventos':
                df_gym.loc[df_gym['Hora'].isin(hora_SE), 'Nombre'] = nombre_usuario
                df_gym.loc[df_gym['Hora'].isin(hora_SE), 'Dpto'] = departamento_usuario
                df_gym.loc[df_gym['Hora'].isin(hora_SE), 'Disponibilidad'] = 'Ocupado'

        gym.update([df_gym.columns.values.tolist()] + df_gym.values.tolist())
        if local == 'GYM':
            df_gym.fillna('', inplace=True)
            hGYM.dataframe(df_gym.loc[:, df_gym.columns != 'Fecha'], width=650)


    if 'Piscina' in local:
        horas_disponibles_piscina = df_piscina.loc[df_piscina['Disponibilidad'] == 'Disponible', 'Hora'].tolist()
        hora_pis = st.multiselect('Seleccione el horario en que desea la reserva',
                                 horas_disponibles_piscina, key='se_disponibilidad')

        # Botón para reservar
        if st.button("Reservar"):
            # Actualizar DataFrames con información de la reserva
            if local == 'Sala de Eventos':
                df_piscina.loc[df_piscina['Hora'].isin(hora_SE), 'Nombre'] = nombre_usuario
                df_piscina.loc[df_piscina['Hora'].isin(hora_SE), 'Dpto'] = departamento_usuario
                df_piscina.loc[df_piscina['Hora'].isin(hora_SE), 'Disponibilidad'] = 'Ocupado'

        piscina.update([df_piscina.columns.values.tolist()] + df_piscina.values.tolist())
        if local == 'Piscina':
            df_piscina.fillna('', inplace=True)
            hPiscina.dataframe(df_piscina.loc[:, df_piscina.columns != 'Fecha'], width=650)

    if 'Parrillas' in local:
        horas_disponibles_parrillas = df_parrillas.loc[df_parrillas['Disponibilidad'] == 'Disponible', 'Hora'].tolist()
        hora_par = st.multiselect('Seleccione el horario en que desea la reserva',
                                 horas_disponibles_parrillas, key='se_disponibilidad')

        # Botón para reservar
        if st.button("Reservar"):
            # Actualizar DataFrames con información de la reserva
            if local == 'Sala de Eventos':
                df_parrillas.loc[df_parrillas['Hora'].isin(hora_SE), 'Nombre'] = nombre_usuario
                df_parrillas.loc[df_parrillas['Hora'].isin(hora_SE), 'Dpto'] = departamento_usuario
                df_parrillas.loc[df_parrillas['Hora'].isin(hora_SE), 'Disponibilidad'] = 'Ocupado'

        parrillas.update([df_parrillas.columns.values.tolist()] + df_parrillas.values.tolist())
        if local == 'Parrillas':
            df_parrillas.fillna('', inplace=True)
            hParrillas.dataframe(df_parrillas.loc[:, df_parrillas.columns != 'Fecha'], width=650)

# podria omitirce  (para la grafica de status mensual)
'''df_salaEventos = pd.DataFrame(salaEventos.get_all_records())
df_gym = pd.DataFrame(gym.get_all_records())
df_piscina = pd.DataFrame(piscina.get_all_records())
df_parrillas = pd.DataFrame(parrillas.get_all_records())
'''