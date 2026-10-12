# Analisis Data Time Series Kualitas Udara CO Kecamatan Kadur Menggunakan Ekstraksi Fitur TSFEL

## 1. Pendahuluan

Kualitas udara merupakan salah satu aspek lingkungan yang perlu diperhatikan karena dapat memberikan dampak terhadap kesehatan manusia dan lingkungan. Salah satu parameter yang dapat digunakan untuk menggambarkan kualitas udara adalah Carbon Monoxide (CO).

Pada tugas ini dilakukan pengolahan data kualitas udara pada tingkat Kecamatan Kadur menggunakan data pengamatan selama 365 hari.

Tahapan pengolahan data meliputi:

1. Identifikasi Area of Interest (AOI).
2. Data understanding.
3. Pembentukan data time series selama 365 hari.
4. Penanganan missing value.
5. Identifikasi dan perbaikan outlier.
6. Perbandingan hasil deteksi outlier menggunakan metode IQR dan Z-Score.
7. Ekstraksi 68 fitur menggunakan TSFEL.
8. Penggabungan hasil ekstraksi fitur dari empat polutan.
9. Clustering menggunakan K-Means.
10. Evaluasi hasil clustering menggunakan Silhouette Score.

Setelah preprocessing, data CO diekstraksi menggunakan kumpulan fitur yang mengacu pada Time Series Feature Extraction Library (TSFEL). Sebanyak 68 fitur digunakan untuk memperoleh karakteristik statistik, temporal, spektral, fractal, wavelet, dan kompleksitas dari data CO.


## 2. Identifikasi Area of Interest (AOI)

Area of Interest (AOI) merupakan wilayah yang menjadi fokus dalam penelitian.

Wilayah yang digunakan adalah:

| Informasi   | Keterangan                        |
| ----------- | --------------------------------- |
| Kecamatan   | Kadur                             |
| Kabupaten   | Pamekasan                         |
| Provinsi    | Jawa Timur                        |
| Parameter   | Carbon Monoxide (CO)              |
| Periode     | 24 Agustus 2025 – 23 Agustus 2026 |
| Jumlah hari | 365 hari                          |

Identifikasi AOI dilakukan menggunakan Folium untuk menampilkan lokasi wilayah penelitian pada peta.

Visualisasi AOI dilakukan pada tahap data understanding agar lokasi geografis data yang dianalisis dapat diketahui dengan jelas.

Peta AOI Folium
[images](images/petakadur1.png)



## 3. Dataset

Data yang digunakan merupakan data kualitas udara parameter Carbon Monoxide (CO) pada wilayah Kecamatan Kadur.

Periode data yang digunakan adalah:

* **Tanggal awal:** 24 Agustus 2025
* **Tanggal akhir:** 23 Agustus 2026
* **Jumlah hari:** 365 hari
* **Wilayah:** Kecamatan Kadur
* **Parameter:** Carbon Monoxide (CO)

Data awal dari hasil pengolahan Copernicus memiliki beberapa tanggal yang tidak mempunyai nilai pengamatan. Oleh karena itu, data disusun kembali berdasarkan tanggal kalender sehingga diperoleh deret waktu lengkap selama 365 hari.

## 4. Persiapan dan Data Understanding

Data awal memiliki beberapa kolom statistik, antara lain:

| Kolom            | Keterangan                      |
| ---------------- | ------------------------------- |
| `C0/date`        | Tanggal pengamatan              |
| `C0/min`         | Nilai minimum CO                |
| `C0/max`         | Nilai maksimum CO               |
| `C0/mean`        | Nilai rata-rata CO              |
| `C0/stDev`       | Standar deviasi                 |
| `C0/sampleCount` | Jumlah sampel                   |
| `C0/noDataCount` | Jumlah data yang tidak tersedia |
| `C0/median`      | Nilai median                    |
| `C0/p10`         | Persentil ke-10                 |
| `C0/p90`         | Persentil ke-90                 |

Dalam analisis ini, **`C0/mean`** digunakan sebagai nilai utama CO karena merepresentasikan nilai rata-rata konsentrasi CO pada setiap tanggal.

### Screenshot 2 – Data CO

> **Masukkan screenshot data CSV CO yang menunjukkan kolom tanggal dan nilai CO.**

**Gambar 2.** Data kualitas udara CO Kecamatan Kadur.


# 5. Pembentukan Data 365 Hari

Data disusun berdasarkan tanggal kalender mulai dari 24 Agustus 2025 sampai 23 Agustus 2026.

Periode tersebut terdiri dari tepat:

**365 hari**

Beberapa tanggal tidak memiliki hasil pengamatan dari sumber data. Tanggal tersebut tetap dipertahankan agar struktur time series tidak terputus.

Dengan demikian, jumlah baris akhir adalah:

**365 baris data**

Hal ini penting karena penghapusan tanggal yang tidak memiliki data akan menyebabkan jarak waktu antar-pengamatan menjadi tidak konsisten.

### contoh grafik folium



## 6. Penanganan Missing Value

### 6.1 Identifikasi Missing Value

Setelah data disusun menjadi 365 hari, ditemukan beberapa tanggal yang tidak mempunyai nilai CO.

Missing value terutama terdapat pada kolom:

```text
C0/mean
```

Berdasarkan data awal:

| Kondisi       | Jumlah |
| ------------- | -----: |
| Total hari    |    365 |
| Data tersedia |    216 |
| Missing value |    149 |

Missing value tidak dihapus karena setiap tanggal tetap diperlukan dalam analisis time series.

### 6.2 Metode Imputasi

Metode yang digunakan adalah:

**Linear Interpolation**

Pada KNIME digunakan node:

```text
Missing Value
```

dengan pengaturan:

```text
Column : C0/mean
Method : Linear Interpolation
```

Linear interpolation memperkirakan nilai yang hilang berdasarkan nilai sebelum dan sesudahnya.

Rumus umum:

```math
y = y_1 + \frac{(x-x_1)}{(x_2-x_1)}(y_2-y_1)
```

Kolom tanggal tidak dilakukan interpolasi karena tanggal merupakan informasi waktu, bukan nilai numerik yang perlu diperkirakan.


## 7. Identifikasi dan Perbaikan Outlier

Setelah missing value ditangani, dilakukan identifikasi terhadap nilai CO yang dianggap sebagai pencilan (*outlier*).

Deteksi outlier dilakukan menggunakan metode **Interquartile Range (IQR)**.

Pada KNIME digunakan node:

```text
Numeric Outliers
```

Pengaturan yang digunakan:

* Column: `Mean`
* IQR multiplier: **1.5**
* Quartile calculation: **Full data estimate**
* Estimation type: **R6**
* Apply to: **All outliers**
* Treatment: **Replace outlier values**
* Replacement strategy: **Missing values**

---

## 7.1 Rumus IQR

Interquartile Range dihitung dengan:

```math
IQR = Q_3-Q_1
```

Batas bawah:

```math
Lower = Q_1-1.5(IQR)
```

Batas atas:

```math
Upper = Q_3+1.5(IQR)
```

Nilai yang berada di luar batas tersebut dianggap sebagai outlier.


## 7.2 Hasil Identifikasi Outlier

Berdasarkan pemeriksaan terhadap data CO, terdapat **3 nilai outlier utama** pada data awal, yaitu:

| No | Hari ke- | Tanggal    | Nilai `C0/mean` | Posisi |
| -: | -------: | ---------- | --------------: | ------ |
|  1 |        6 | 29-08-2025 |        0.017807 | Lower  |
|  2 |       45 | 07-10-2025 |        0.036308 | Upper  |
|  3 |      253 | 03-05-2026 |        0.017449 | Lower  |

Dengan demikian terdapat:

* **2 lower outlier**
* **1 upper outlier**
* **3 outlier utama**

Outlier tidak dihapus karena penghapusan baris dapat menyebabkan jumlah hari dalam time series berkurang.

Sebagai gantinya, nilai outlier diubah menjadi Missing Value.

Setelah itu dilakukan interpolasi kembali menggunakan node:

```
Missing Value
```

dengan:

```
Column : Mean
Method : Linear Interpolation
```

Dengan cara tersebut, jumlah data tetap:

**365 hari**

dan nilai pencilan digantikan dengan nilai yang diperkirakan berdasarkan pola data di sekitarnya.

## 8. Perbandingan IQR dan Z-Score

Selain metode IQR, digunakan metode **Z-Score** sebagai metode pembanding dalam identifikasi outlier.

Rumus Z-Score:

```math
Z = \frac{x-\mu}{\sigma}
```

dengan:

* `x` = nilai pengamatan
* `μ` = rata-rata data
* `σ` = standar deviasi

Kriteria yang digunakan adalah:

```text
|Z| > 3
```

Hasil perbandingan menunjukkan:

| Metode  | Jumlah Outlier | Tanggal                            |
| ------- | -------------: | ---------------------------------- |
| IQR     |              3 | 29-08-2025, 07-10-2025, 03-05-2026 |
| Z-Score |              3 | 29-08-2025, 07-10-2025, 03-05-2026 |

Kedua metode menghasilkan tanggal outlier yang sama pada data yang dibandingkan.

Hal tersebut menunjukkan bahwa tiga nilai tersebut merupakan nilai yang cukup menyimpang dari pola umum data CO.


## 9. Alur Preprocessing

Alur preprocessing yang digunakan pada KNIME adalah:

```text
CSV Reader
     ↓
String to Date&Time
     ↓
Missing Value
     ↓
Numeric Outliers
     ↓
Missing Value
     ↓
Statistics
```

Penjelasan:

1. **CSV Reader**
   Membaca dataset CO.

2. **String to Date&Time**
   Mengubah kolom tanggal menjadi format tanggal/time series.

3. **Missing Value**
   Mengisi data CO yang hilang menggunakan Linear Interpolation.

4. **Numeric Outliers**
   Mendeteksi nilai pencilan menggunakan metode IQR.

5. **Missing Value**
   Mengisi kembali nilai outlier yang telah diubah menjadi missing value.

6. **Statistics**
   Digunakan untuk memeriksa kondisi data setelah preprocessing.

### Screenshot 8 – Workflow KNIME

> **Masukkan screenshot keseluruhan workflow KNIME.**

**Gambar 8.** Workflow preprocessing data CO Kecamatan Kadur.

## 10. Hasil Preprocessing

Setelah preprocessing diperoleh dataset dengan karakteristik:

| Kondisi           | Hasil     |
| ----------------- | --------- |
| Periode           | 365 hari  |
| Missing `C0/date` | 0         |
| Missing `C0/mean` | 0         |
| Data CO           | Lengkap   |
| Outlier           | Ditangani |
| Jumlah baris      | 365       |

Kolom lain seperti `C0/stDev` dapat tetap memiliki missing value karena kolom tersebut bukan variabel utama yang digunakan dalam ekstraksi fitur CO.

Variabel utama yang digunakan untuk proses selanjutnya adalah:

```
C0/mean
```

## 11. Ekstraksi Fitur Time Series Menggunakan TSFEL

Setelah preprocessing selesai, dilakukan ekstraksi fitur dari sinyal CO selama 365 hari.

Sebanyak **68 fungsi fitur** digunakan. Fitur tersebut mencakup:

* fitur statistik
* fitur temporal
* fitur probabilistik
* fitur spektral
* fitur fractal
* fitur wavelet
* fitur kompleksitas

Hasil ekstraksi disusun menjadi:

```
F1, F2, F3, ..., F68
```

## 12. Daftar 68 Fitur TSFEL

|  No | Fitur                       |
| --: | --------------------------- |
|  F1 | abs_energy                  |
|  F2 | auc                         |
|  F3 | autocorr                    |
|  F4 | average_power               |
|  F5 | calc_centroid               |
|  F6 | calc_max                    |
|  F7 | calc_mean                   |
|  F8 | calc_median                 |
|  F9 | calc_min                    |
| F10 | calc_std                    |
| F11 | calc_var                    |
| F12 | dfa                         |
| F13 | distance                    |
| F14 | ecdf                        |
| F15 | ecdf_percentile             |
| F16 | ecdf_percentile_count       |
| F17 | ecdf_slope                  |
| F18 | entropy                     |
| F19 | fundamental_frequency       |
| F20 | higuchi_fractal_dimension   |
| F21 | hist_mode                   |
| F22 | human_range_energy          |
| F23 | hurst_exponent              |
| F24 | interq_range                |
| F25 | kurtosis                    |
| F26 | lempel_ziv                  |
| F27 | lpcc                        |
| F28 | max_frequency               |
| F29 | max_power_spectrum          |
| F30 | maximum_fractal_length      |
| F31 | mean_abs_deviation          |
| F32 | mean_abs_diff               |
| F33 | mean_diff                   |
| F34 | median_abs_deviation        |
| F35 | median_abs_diff             |
| F36 | median_diff                 |
| F37 | median_frequency            |
| F38 | mfcc                        |
| F39 | mse                         |
| F40 | negative_turning            |
| F41 | neighbourhood_peaks         |
| F42 | petrosian_fractal_dimension |
| F43 | pk_pk_distance              |
| F44 | positive_turning            |
| F45 | power_bandwidth             |
| F46 | rms                         |
| F47 | skewness                    |
| F48 | slope                       |
| F49 | spectral_centroid           |
| F50 | spectral_decrease           |
| F51 | spectral_distance           |
| F52 | spectral_entropy            |
| F53 | spectral_kurtosis           |
| F54 | spectral_positive_turning   |
| F55 | spectral_roll_off           |
| F56 | spectral_roll_on            |
| F57 | spectral_skewness           |
| F58 | spectral_slope              |
| F59 | spectral_spread             |
| F60 | spectral_variation          |
| F61 | spectrogram_mean_coeff      |
| F62 | sum_abs_diff                |
| F63 | wavelet_abs_mean            |
| F64 | wavelet_energy              |
| F65 | wavelet_entropy             |
| F66 | wavelet_std                 |
| F67 | wavelet_var                 |
| F68 | zero_cross                  |

### Screenshot 9 – Hasil F1–F68

> **Masukkan screenshot file `CO_Kadur_TSFEL_F1_F68_FINAL.csv` yang menunjukkan kolom F1 sampai F68.**

**Gambar 9.** Hasil ekstraksi 68 fitur TSFEL.

# 13. Hasil Ekstraksi F1–F68

Hasil ekstraksi menghasilkan satu vektor karakteristik yang menggambarkan keseluruhan pola CO selama 365 hari.

File hasil ekstraksi:

```
CO_Kadur_TSFEL_F1_F68_FINAL.csv
```

Representasi F1–F68 kemudian dapat digunakan untuk analisis karakteristik, similarity, serta proses analisis lanjutan.

---

# 14. Pemahaman Fitur

Beberapa contoh fitur yang digunakan adalah:

| Fitur               | Fungsi                                              |
| ------------------- | --------------------------------------------------- |
| `abs_energy`        | Mengukur energi absolut sinyal                      |
| `auc`               | Menghitung luas di bawah kurva                      |
| `calc_mean`         | Menghasilkan nilai rata-rata                        |
| `calc_median`       | Menghasilkan nilai tengah                           |
| `calc_max`          | Menghasilkan nilai maksimum                         |
| `calc_min`          | Menghasilkan nilai minimum                          |
| `calc_std`          | Mengukur penyebaran data                            |
| `calc_var`          | Mengukur variansi                                   |
| `entropy`           | Mengukur tingkat ketidakaturan                      |
| `kurtosis`          | Menggambarkan bentuk distribusi dan nilai ekstrem   |
| `skewness`          | Menggambarkan kemencengan distribusi                |
| `rms`               | Mengukur nilai efektif sinyal                       |
| `slope`             | Menunjukkan kecenderungan perubahan data            |
| `spectral_centroid` | Menunjukkan pusat distribusi energi pada frekuensi  |
| `spectral_entropy`  | Mengukur ketidakaturan distribusi energi spektrum   |
| `zero_cross`        | Menghitung perubahan sinyal yang melewati nilai nol |

Penjelasan lengkap F1–F68 tersedia pada file:

```
CO_Kadur_TSFEL_F1_F68_Keterangan.csv
```


## 15. Analisis Similarity CO

### 15.1 Konsep Similarity

Similarity digunakan untuk mengetahui seberapa mirip pola atau karakteristik suatu data dengan data lainnya.

Salah satu metode yang dapat digunakan adalah Cosine Similarity:

```math
Similarity(A,B)=
\frac{A\cdot B}
{\|A\|\|B\|}
```

Nilai similarity semakin mendekati **1** menunjukkan bahwa kedua data semakin mirip.

Sebaliknya, nilai yang semakin mendekati **0** menunjukkan bahwa pola kedua data semakin berbeda.



