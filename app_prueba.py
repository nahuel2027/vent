import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(page_title="Venta de Pastelitos", layout="centered")

# Función para conectar a la base de datos en Render
def conectar_db():
    return psycopg2.connect(
        host="dpg-cvr1glre5dus7382clm0-a.virginia-postgres.render.com",
        database="bd_pastelitos",
        user="bd_pastelitos_user",
        password="vHKvMcDfNOboZR77QetT7sS72B2FHn7v",
        port="5432"
    )

# Función para insertar pedido
def insertar_pedido(nombre, cantidad, direccion, telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pastelitos (nombre, cantidad, direccion, telefono)
        VALUES (%s, %s, %s, %s)
    """, (nombre, cantidad, direccion, telefono))
    conn.commit()
    cursor.close()
    conn.close()

# Función para obtener pedidos
def obtener_pedidos():
    conn = conectar_db()
    df = pd.read_sql("SELECT nombre, cantidad, direccion, telefono FROM pastelitos ORDER BY nombre ASC", conn)
    conn.close()
    return df

# Título
st.title("🍩 Registro de Venta de Pastelitos")

# Formulario
with st.form("form_pedido"):
    nombre = st.text_input("Nombre de la persona")
    cantidad = st.selectbox("Cantidad ordenada", ["Docena", "Media docena"])
    direccion = st.text_input("Dirección de entrega")
    telefono = st.text_input("Teléfono de contacto")
    enviar = st.form_submit_button("Registrar pedido")

    if enviar:
        if nombre.strip() == "":
            st.warning("Por favor, escribí un nombre.")
        else:
            insertar_pedido(nombre, cantidad, direccion, telefono)
            st.success("✅ Pedido registrado correctamente")

# Mostrar tabla con los pedidos
df = obtener_pedidos()
if not df.empty:
    st.subheader("📋 Lista de pedidos")
    st.table(df)

    # Calcular totales
    total_personas = len(df)
    total_docenas = sum(df["cantidad"] == "Docena")
    total_medias = total_personas - total_docenas

    st.subheader("📊 Totales")
    st.write(f"👥 Total de personas: {total_personas}")
    st.write(f"🍽️ Docenas: {total_docenas}")
    st.write(f"🥄 Medias docenas: {total_medias}")
else:
    st.info("Todavía no hay pedidos registrados.")
