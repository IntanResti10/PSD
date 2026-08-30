
# Crawling Data
## Bussiness Understanding

### Mengamati Kualitas Udara
Kualitas udara merupakan salah satu elemen penting dalam menjaga keberlanjutan lingkungan hidup dan kesehatan masyarakat. Seiring meningkatnya aktivitas industri, transportasi, dan perubahan tata guna lahan, emisi zat pencemar ke atmosfer mengalami peningkatan. Oleh karena itu, pengamatan kualitas udara secara berkala menjadi krusial untuk mendeteksi risiko pemaparan zat berbahaya sejak dini.

Indeks Kualitas Udara (Air Quality Index / AQI) adalah indikator terstandarisasi yang digunakan untuk mengomunikasikan tingkat kebersihan atau pencemaran udara di suatu area kepada publik. Nilai AQI mengodekan konsentrasi berbagai polutan atmosfer menjadi skala numerik yang intuitif, umumnya dilengkapi dengan kategori tingkat risiko kesehatan (seperti Baik, Sedang, Tidak Sehat, Sangat Tidak Sehat, hingga Berbahaya).

### Unsur-Unsur Polutan Udara
Kualitas udara ditentukan oleh keberadaan senyawa kimia gas dan partikulat tersuspensi. Dalam studi ini, pengamatan difokuskan pada beberapa polutan utama hasil ekstraksi data satelit Copernicus:
- **Nitrogen Dioksida (NO2)**: Gas pembentukan utama emisi pembakaran bahan bakar fosil dari kendaraan bermotor dan pembangkit listrik. Konsentrasi NO2 yang tinggi berpotensi memicu penyakit saluran pernapasan, bronkitis, serta berperan dalam pembentukan hujan asam dan ozon troposferik.
- **Karbon Monoksida (CO)**: Gas yang dihasilkan dari proses pembakaran tidak sempurna bahan bakar karbon (misalnya pada mesin kendaraan dan kebakaran vegetasi). CO berikatan kuat dengan hemoglobin darah, mengurangi pengangkutan oksigen ke jaringan tubuh.
- **Sulfur Dioksida (SO2)**: Gas berbau tajam yang utamanya dihasilkan dari pembakaran batu bara, pengolahan bijih logam, atau aktivitas vulkanik. SO2 dapat menyebabkan penyempitan saluran napas dan kerusakan ekosistem tanah/air.
- **Metana (CH4)**: Gas rumah kaca kuat yang dihasilkan dari proses penguraian bahan organik secara anaerobik (seperti pada sektor pertanian, peternakan, sawah tergenang, dan tempat pemrosesan akhir sampah) serta kebocoran distribusi gas alam. CH4 memiliki potensi pemanasan global (Global Warming Potential) jauh lebih tinggi dibanding CO2 dan berperan penting dalam pembentukan ozon di tingkat permukaan (ground-level ozone).


## Data Understanding
### Mengumpulkan Data dari Copernicus Data Space Ecosystem (CDSE)
Data kualitas udara dikumpulkan dari platform Copernicus Data Space Ecosystem (CDSE) dengan memanfaatkan sensor TROPOMI yang terpasang pada satelit Sentinel-5P. Satelit ini memiliki kapabilitas penginderaan jauh resolusi tinggi untuk memantau gas trace dan konsentrasi polutan atmosfer secara global setiap hari.

#### Pengambilan Data:
- **Lokasi Pengamatan**: Kecamatan Kadur, Kabupaten Pamekasan, Jawa Timur.
- **Titik Koordinat & Luas**: Latitude $-7.0365^\circ$, Longitude $113.6175^\circ$ (Luas area polygon $\approx 55.28\text{ km}^2$).
- **Rentang Waktu**: 24 Agustus 2025 – 24 Agustus 2026.
- **Sumber Data**: Satelit Sentinel-5P (Sensor TROPOMI Level-2/Level-3) dari portal Copernicus Data Space Ecosystem.
- **Parameter Pencemar**: Gas Nitrogen Dioksida (NO2) Troposferik dalam satuan mol/m2.
- **Format Output**: File .csv yang diekstraksi via fitur Statistical Info / Chart Copernicus Browser.

### Eksplorasi Data (EDA)
##### Deskripsi Pengambilan Data
Pengambilan data kualitas udara ini dilakukan untuk mengamati fluktuasi konsentrasi polutan udara di wilayah Kecamatan Kadur, Kabupaten Pamekasan, Provinsi Jawa Timur. Penentuan lokasi ini difokuskan pada area pemukiman dan agraris dengan titik koordinat pusat berada pada Latitude $-7.0365^\circ$ dan Longitude $113.6175^\circ$, serta mencakup batas wilayah dalam bentuk polygon dengan total luas area pengamatan sebesar $\approx 55.28\text{ km}^2$.

Pengamatan dilakukan secara time-series harian dalam rentang waktu 24 Agustus 2025 sampai dengan 24 Agustus 2026 (1 tahun penuh). Periode satu tahun ini dipilih secara khusus untuk menangkap pola perubahan kualitas udara antarmusim, baik saat musim kemarau maupun musim hujan, serta mengidentifikasi faktor lingkungan dan meteorologis yang memengaruhi tingkat polusi udara di wilayah Kecamatan Kadur.

Data diperoleh dari Copernicus Data Space Ecosystem, yaitu platform penyedia data observasi bumi milik European Space Agency (ESA), menggunakan instrumen sensor TROPOMI (TROPOspheric Monitoring Instrument) yang terpasang pada satelit Sentinel-5P. Parameter utama yang diekstraksi adalah Tropospheric NO2 Column Density (konsentrasi gas Nitrogen Dioksida pada lapisan troposfer) yang diukur dalam satuan $\text{mol/m}^2$.

#### Visualisasi Data Peta
Visualisasi peta interaktif digunakan untuk memastikan bahwa cakupan wilayah pengamatan sudah sesuai secara geografis di wilayah Kecamatan Kadur, Pamekasan.

```
import io
import folium
import matplotlib.pyplot as plt
import pandas as pd
from google.colab import files

print("upload file CSV)
uploaded = files.upload()

file_name = list(uploaded.keys())[0]

try:
    df = pd.read_csv(
        io.BytesIO(uploaded[file_name]), sep=None, engine="python"
    )
except Exception:
    
    df = pd.read_csv(
        io.BytesIO(uploaded[file_name]), sep=";", on_bad_lines="skip"
    )

print(f"\nBerhasil mengunggah: {file_name}")
print("\n5 Baris Pertama Data:")
display(df.head())


print("menampilkan peta wilayah kecamatan kadur")
m = folium.Map(
    location=[-7.0365, 113.6175], zoom_start=13, tiles="OpenStreetMap"
)
folium.Marker(
    [-7.0365, 113.6175],
    popup="Kecamatan Kadur, Pamekasan",
    tooltip="Lokasi Pengamatan NO2",
).add_to(m)
display(m)


print("grafik Tren konsentrasi NO2")
col_date = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()][
    0
]
col_val = [
    c
    for c in df.columns
    if "mean" in c.lower() or "val" in c.lower() or "no2" in c.lower()
]
col_val = col_val[0] if col_val else df.columns[1]

df[col_date] = pd.to_datetime(df[col_date])

plt.figure(figsize=(12, 5))
plt.plot(
    df[col_date],
    df[col_val],
    color="crimson",
    linewidth=1.5,
    label="Konsentrasi NO2",
)
plt.title(
    "Tren Konsentrasi NO2 di Kecamatan Kadur, Pamekasan (24 Agst 2025 - 24 Agst"
    " 2026)"
)
plt.xlabel("Tanggal Pengamatan")
plt.ylabel("Konsentrasi NO2 (mol/m²)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
```

###### 1. Visualisasi Peta (folium):
![peta1](images/peta1.png)

###### 2. Visualisasi Grafik (matplotlib):
![grafikkonsentrasiNO2](images/grafikkonsentrasiNO2.png)

###### 3. Visualisasi Peta wilayah kecamatan kadur(Copernicus):
![peta2](images/peta2.png)

##### Missing Value
Terdeteksi beberapa baris data bernilai kosong/0 yang disebabkan oleh gangguan tutupan awan (cloud cover) saat satelit Sentinel-5P melakukan pemindaian harian.
##### Noises
Terdapat noise skala pengukuran bawaan satelit karena nilai konsentrasi $\text{NO}_2$ berada pada orde yang sangat kecil ($10^{-5}\text{ mol/m}^2$), sehingga berpotensi menimbulkan rounding error pada pemrosesan awal.
##### Outliers
Terdeteksi beberapa titik pencilan (outliers) berupa lonjakan nilai konsentrasi $\text{NO}_2$ pada bulan September–Oktober 2025. Lonjakan ini dipengaruhi faktor meteorologis (musim kemarau panjang) dan bukan merupakan kesalahan input data.



