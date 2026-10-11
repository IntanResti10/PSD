
import streamlit as st
import rasterio
import geopandas as gpd
import numpy as np
import folium

from folium.raster_layers import ImageOverlay
from streamlit_folium import st_folium
from matplotlib.colors import to_rgb
from rasterio.warp import transform_bounds

# =========================
# 1. PENGATURAN APLIKASI
# =========================
st.set_page_config(
    page_title="Klasifikasi Tutupan Lahan Pamekasan",
    page_icon="🌍",
    layout="wide"
)

st.title("Klasifikasi Tutupan Lahan Pamekasan")
st.write(
    "Pemetaan tutupan lahan menggunakan citra Sentinel-2 "
    "dan algoritma Random Forest."
)

RASTER_PATH = "hasil_klasifikasi_pamekasan.tif"
GEOJSON_PATH = "polygon.geojson"

KELAS = {
    1: "building",
    2: "farmland",
    3: "water_body",
    4: "forest",
    5: "mangrove"
}

WARNA = {
    1: "#d73027",
    2: "#fdae61",
    3: "#4575b4",
    4: "#1a9850",
    5: "#66c2a5"
}

# =========================
# 2. MEMBACA DATA
# =========================
@st.cache_data
def baca_raster(path):
    with rasterio.open(path) as src:
        data = src.read(1)
        batas = src.bounds
        crs = src.crs
        transformasi = src.transform
        nodata = src.nodata

    if crs is None:
        raise ValueError("CRS raster tidak ditemukan.")

    # Mengubah batas raster ke koordinat geografis
    # yang diperlukan untuk peta Folium.
    batas_geo = transform_bounds(
        crs,
        "EPSG:4326",
        batas.left,
        batas.bottom,
        batas.right,
        batas.top
    )

    return data, batas_geo, nodata


@st.cache_data
def baca_geojson(path):
    data = gpd.read_file(path)

    if data.crs is None:
        raise ValueError(
            "CRS GeoJSON tidak ditemukan. "
            "Pastikan file GeoJSON memiliki informasi CRS."
        )

    return data.to_crs("EPSG:4326")


try:
    hasil, batas_geo, nodata = baca_raster(RASTER_PATH)
    poligon = baca_geojson(GEOJSON_PATH)

except Exception as e:
    st.error("Data belum berhasil dibaca.")
    st.code(str(e))
    st.info(
        "Pastikan app.py, file GeoTIFF, dan polygon.geojson "
        "berada di folder proyek yang sama."
    )
    st.stop()

# =========================
# 3. FILTER KELAS
# =========================
st.subheader("Pilih Kelas Tutupan Lahan")

pilihan = st.multiselect(
    "Pilih kelas yang ingin ditampilkan pada peta:",
    options=list(KELAS.values()),
    default=list(KELAS.values())
)

# =========================
# 4. MEMBUAT OVERLAY
# =========================
# Raster hasil klasifikasi diasumsikan memakai:
# 1=building, 2=farmland, 3=water_body,
# 4=forest, 5=mangrove.
# Nilai 0 dianggap sebagai area tanpa klasifikasi.

rgba = np.zeros(
    (hasil.shape[0], hasil.shape[1], 4),
    dtype=np.uint8
)

for kode, nama in KELAS.items():
    if nama not in pilihan:
        continue

    mask = hasil == kode
    rgb = np.array(to_rgb(WARNA[kode])) * 255

    rgba[mask, 0] = int(rgb[0])
    rgba[mask, 1] = int(rgb[1])
    rgba[mask, 2] = int(rgb[2])
    rgba[mask, 3] = 180

# Kosongkan piksel NoData jika memang ditentukan di GeoTIFF.
if nodata is not None:
    rgba[hasil == nodata, 3] = 0

# =========================
# 5. MEMBUAT PETA
# =========================
left, bottom, right, top = batas_geo

tengah = [
    (bottom + top) / 2,
    (left + right) / 2
]

peta = folium.Map(
    location=tengah,
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True
)

# Layer citra satelit.
folium.TileLayer(
    tiles=(
        "https://server.arcgisonline.com/ArcGIS/rest/services/"
        "World_Imagery/MapServer/tile/{z}/{y}/{x}"
    ),
    attr="Tiles © Esri",
    name="Citra Satelit",
    overlay=False,
    control=True
).add_to(peta)

# Layer hasil klasifikasi.
ImageOverlay(
    image=rgba,
    bounds=[[bottom, left], [top, right]],
    opacity=1,
    name="Hasil Klasifikasi",
    interactive=False,
    cross_origin=False,
    zindex=2
).add_to(peta)

# =========================
# 6. LAYER POLIGON SAMPEL
# =========================
kolom_kelas = None

for nama_kolom in ["kelas", "class", "label", "Class", "Kelas"]:
    if nama_kolom in poligon.columns:
        kolom_kelas = nama_kolom
        break

if kolom_kelas is not None:
    poligon_tampil = poligon[
        poligon[kolom_kelas].astype(str).isin(pilihan)
    ]

    if not poligon_tampil.empty:
        folium.GeoJson(
            poligon_tampil,
            name="Poligon Sampel",
            tooltip=folium.GeoJsonTooltip(
                fields=[kolom_kelas],
                aliases=["Kelas:"]
            ),
            style_function=lambda feature: {
                "color": "#ffffff",
                "weight": 2,
                "fillOpacity": 0.08
            }
        ).add_to(peta)

folium.LayerControl(collapsed=False).add_to(peta)

# Sesuaikan tampilan peta dengan area raster.
peta.fit_bounds([
    [bottom, left],
    [top, right]
])

# =========================
# 7. MENAMPILKAN PETA
# =========================
st.subheader("Peta Interaktif")

st_folium(
    peta,
    key="peta_pamekasan",
    height=600,
    use_container_width=True,
    returned_objects=[]
)

# =========================
# 8. LEGENDA
# =========================
st.subheader("Legenda Kelas")

kolom = st.columns(5)

for i, (kode, nama) in enumerate(KELAS.items()):
    if nama in pilihan:
        with kolom[i]:
            st.markdown(
                f"<span style='color:{WARNA[kode]};"
                f"font-size:24px'>■</span> **{nama}**",
                unsafe_allow_html=True
            )

# =========================
# 9. RINGKASAN DATA
# =========================
st.subheader("Ringkasan Hasil Klasifikasi")

total = int(np.count_nonzero(np.isin(hasil, list(KELAS.keys()))))
st.metric("Total piksel terklasifikasi", f"{total:,}")

for kode, nama in KELAS.items():
    if nama in pilihan:
        jumlah = int(np.count_nonzero(hasil == kode))
        st.write(f"**{nama}:** {jumlah:,} piksel")

st.caption(
    "Peta menampilkan hasil klasifikasi dari file GeoTIFF. "
    "Akurasi model perlu dinilai menggunakan hasil testing."
)
