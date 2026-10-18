import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

# ==================================================
# KONFIGURASI
# ==================================================

st.set_page_config(
    page_title="Klasifikasi Tutupan Lahan Jawa Timur",
    page_icon="🗺️",
    layout="wide"
)

# ==================================================
# JUDUL
# ==================================================

st.title("🗺️ Klasifikasi Tutupan Lahan Jawa Timur")

st.write(
    "Pemetaan tutupan lahan Jawa Timur menggunakan "
    "citra Sentinel-2 dan algoritma Random Forest."
)

# ==================================================
# BUSINESS UNDERSTANDING
# ==================================================

st.header("1. Business Understanding")

st.subheader("Tujuan Proyek")

st.write("""
Proyek ini bertujuan untuk mengidentifikasi dan memetakan
tutupan lahan di wilayah Jawa Timur berdasarkan citra
satelit Sentinel-2 menggunakan metode klasifikasi Random Forest.

Hasil klasifikasi dibagi menjadi lima kelas, yaitu:

1. Bangunan (Built-up)
2. Lahan pertanian / sawah (Farm Land)
3. Perairan (Water Body)
4. Hutan (Forest)
5. Hutan Mangrove (Mangrove Forest)

Hasil klasifikasi digunakan untuk memperoleh informasi
mengenai persebaran dan luas masing-masing jenis tutupan
lahan di Jawa Timur.

Informasi tersebut dapat digunakan sebagai gambaran awal
kondisi permukaan bumi dan membantu proses pemantauan
serta analisis penggunaan lahan.
""")

# ==================================================
# LOAD GEOJSON
# ==================================================

geojson_path = "data/klasifikasi_jawa_timur_web_kecil.geojson"

try:

    gdf = gpd.read_file(geojson_path)

    st.success(
        f"Data klasifikasi berhasil dimuat: {len(gdf):,} area"
    )

except Exception as e:

    st.error("GeoJSON tidak dapat dibaca.")

    st.code(str(e))

    st.stop()

# ==================================================
# PASTIKAN CRS
# ==================================================

if gdf.crs is not None:
    gdf = gdf.to_crs("EPSG:4326")

# ==================================================
# FILTER KELAS
# ==================================================

st.header("2. Filter Kelas Tutupan Lahan")

st.write(
    "Centang kelas tutupan lahan yang ingin "
    "ditampilkan pada peta."
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    tampil_bangunan = st.checkbox(
        "🏢 Bangunan",
        value=True
    )

with col2:
    tampil_sawah = st.checkbox(
        "🌾 Sawah",
        value=True
    )

with col3:
    tampil_perairan = st.checkbox(
        "🌊 Perairan",
        value=True
    )

with col4:
    tampil_hutan = st.checkbox(
        "🌳 Hutan",
        value=True
    )

with col5:
    tampil_mangrove = st.checkbox(
        "🌱 Mangrove",
        value=True
    )

# ==================================================
# DAFTAR KELAS YANG DIPILIH
# ==================================================

kelas_dipilih = []

if tampil_bangunan:
    kelas_dipilih.append("bangunan")

if tampil_sawah:
    kelas_dipilih.append("sawah")

if tampil_perairan:
    kelas_dipilih.append("perairan")

if tampil_hutan:
    kelas_dipilih.append("hutan")

if tampil_mangrove:
    kelas_dipilih.append("mangrove")

# ==================================================
# PETA
# ==================================================

st.header("3. Peta Tutupan Lahan Jawa Timur")

# Ambil batas wilayah
bounds = gdf.total_bounds

minx, miny, maxx, maxy = bounds

center_lat = (miny + maxy) / 2
center_lon = (minx + maxx) / 2

# ==================================================
# BUAT PETA
# ==================================================

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=8,
    tiles=None
)

# ==================================================
# CITRA SATELIT
# ==================================================

folium.TileLayer(
    tiles=(
        "https://server.arcgisonline.com/ArcGIS/"
        "rest/services/World_Imagery/"
        "MapServer/tile/{z}/{y}/{x}"
    ),
    attr="Esri World Imagery",
    name="Citra Satelit",
    overlay=False,
    control=True
).add_to(m)

# ==================================================
# WARNA
# ==================================================

warna = {
    "bangunan": "red",
    "sawah": "yellow",
    "perairan": "blue",
    "hutan": "green",
    "mangrove": "purple"
}

# ==================================================
# LAYER KLASIFIKASI
# ==================================================

for nama_kelas in kelas_dipilih:

    data_kelas = gdf[
        gdf["class"] == nama_kelas
    ].copy()

    if data_kelas.empty:
        continue

    layer = folium.FeatureGroup(
        name=nama_kelas.capitalize(),
        show=True
    )

    folium.GeoJson(
        data_kelas.to_json(),
        style_function=lambda feature,
        warna_kelas=warna[nama_kelas]: {
            "fillColor": warna_kelas,
            "color": warna_kelas,
            "weight": 0.3,
            "fillOpacity": 0.45
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["class"],
            aliases=["Kelas:"]
        )
    ).add_to(layer)

    layer.add_to(m)

# ==================================================
# LAYER CONTROL
# ==================================================

folium.LayerControl(
    collapsed=False
).add_to(m)

# ==================================================
# LEGENDA
# ==================================================

legend_html = """
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 180px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    padding: 10px;
    font-size: 14px;
">

<b>Legenda Tutupan Lahan</b><br><br>

<span style="color:red;">■</span>
Bangunan<br>

<span style="color:#FFD700;">■</span>
Sawah<br>

<span style="color:blue;">■</span>
Perairan<br>

<span style="color:green;">■</span>
Hutan<br>

<span style="color:purple;">■</span>
Mangrove

</div>
"""

m.get_root().html.add_child(
    folium.Element(legend_html)
)

# ==================================================
# TAMPILKAN PETA
# ==================================================

st_folium(
    m,
    width=1200,
    height=650
)

# ==================================================
# INFORMASI HASIL
# ==================================================

st.header("4. Informasi Hasil Klasifikasi")

luas_path = "data/luas_klasifikasi_jawa_timur.csv"

try:

    luas = pd.read_csv(luas_path)

    st.subheader("Luas Tutupan Lahan Jawa Timur")

    st.dataframe(
        luas,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        "Data luas belum dapat ditampilkan."
    )

# ==================================================
# RINGKASAN LUAS
# ==================================================

st.subheader("Ringkasan Luas Tutupan Lahan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏢 Bangunan",
        "263.997,94 ha"
    )

with col2:
    st.metric(
        "🌾 Sawah",
        "929.885,42 ha"
    )

with col3:
    st.metric(
        "🌊 Perairan",
        "3.240.326,33 ha"
    )

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "🌳 Hutan",
        "873.192,83 ha"
    )

with col5:
    st.metric(
        "🌱 Mangrove",
        "1.299.548,65 ha"
    )

# ==================================================
# GRAFIK
# ==================================================

st.subheader("Grafik Luas Tutupan Lahan")

data_grafik = pd.DataFrame({
    "Kelas": [
        "Bangunan",
        "Sawah",
        "Perairan",
        "Hutan",
        "Mangrove"
    ],
    "Luas (ha)": [
        263997.94,
        929885.42,
        3240326.33,
        873192.83,
        1299548.65
    ]
})

st.bar_chart(
    data_grafik.set_index("Kelas")
)

# ==================================================
# EVALUASI MODEL
# ==================================================

st.header("5. Evaluasi Model")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Accuracy",
        "97,72%"
    )

with col2:
    st.metric(
        "Jumlah Kelas",
        "5"
    )

st.write("""
Model Random Forest dilatih menggunakan data training
hasil digitasi wilayah Pamekasan. Model kemudian digunakan
untuk melakukan klasifikasi tutupan lahan pada wilayah
Jawa Timur.

Berdasarkan pengujian model, diperoleh nilai accuracy
sebesar 97,72%.
""")

# ==================================================
# INFORMASI METODE
# ==================================================

st.header("6. Metode yang Digunakan")

st.write("""
**Data:** Citra Sentinel-2

**Wilayah:** Jawa Timur

**Metode klasifikasi:** Random Forest

**Jumlah kelas:** 5 kelas

**Band yang digunakan:**
B02, B03, B04, B08, B8A, B11, dan B12

**Kelas tutupan lahan:**
Bangunan, Sawah, Perairan, Hutan, dan Mangrove.
""")
