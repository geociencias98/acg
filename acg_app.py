
# URL del archivo CSV
url = "https://gist.githubusercontent.com/geociencias98/4698f49cc870bfc70415bac5d5e11a6c/raw/cbf979bcd6f4809d03ba40b4d2ffbf6521449909/gistfile1.txt"

# Cargar los datos
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# Cargar los datos
data = load_data(url)

# Configuración de la página
st.set_page_config(page_title="Avistamientos de Especies", layout="wide")

# Título
st.title("Avistamientos de Especies")

# Lista de selección
species = st.selectbox(
    "Selecciona una especie (nombre común):",
    options=data["common_name"].unique()
)

# Filtrar datos por especie seleccionada
filtered_data = data[data["common_name"] == species]

# Mostrar tabla filtrada
st.subheader(f"Datos Filtrados: {species}")
st.dataframe(filtered_data)

# Gráfico interactivo con Plotly
st.subheader("Gráfico Estadístico Interactivo")
fig = px.histogram(
    filtered_data,
    x="observed_on",
    title=f"Distribución de Avistamientos para {species}",
    labels={"observed_on": "Fecha de Observación"},
    nbins=20
)
st.plotly_chart(fig)

# Mapa interactivo con Folium
st.subheader("Mapa Interactivo de Avistamientos")
map_center = [filtered_data["latitude"].mean(), filtered_data["longitude"].mean()]

m = folium.Map(location=map_center, zoom_start=6)

# Agregar marcadores al mapa
for _, row in filtered_data.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['common_name']}<br>{row['observed_on']}"
    ).add_to(m)

# Mostrar el mapa
st_folium(m, width=700, height=500)
