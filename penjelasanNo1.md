Tantangan yang dihadapi Desa Medang Kamulan sangat umum terjadi di banyak desa di Indonesia. Transformasi dari sistem manual berbasis kertas ke sistem basis data digital akan sangat membantu mempercepat pelayanan dan meningkatkan transparansi.

Untuk memenuhi tugas **Pekerjaan 1**, kita akan memilih tiga manajemen yang saling berkaitan erat agar sistem basis data yang terbentuk menjadi solid dan terintegrasi:

1. **Manajemen Pendataan Penduduk (Poin B):** Sebagai fondasi utama (master data), karena pelayanan dan pengaduan pasti membutuhkan data warga yang valid.
2. **Manajemen Pelayanan Warga (Poin A):** Mengelola proses permohonan surat dokumen warga (KTP, KK, SKTM, dll.).
3. **Pengaduan Masyarakat (Poin E):** Memberikan wadah bagi warga untuk memberikan umpan balik terhadap pelayanan desa.

Berikut adalah rancangan **Conceptual Data Model (CDM)** dan **Physical Data Model (PDM)** untuk ketiga manajemen tersebut.

---

## 1. Conceptual Data Model (CDM)

CDM berfokus pada entitas bisnis, atribut, dan hubungan (*relationship*) antar entitas tanpa memperhatikan detail teknis penyimpanan (seperti tipe data spesifik DBMS).

### Daftar Entitas dan Atribut

* **WARGA** (Entitas Master Penduduk)
* `NIK` (Identifier/PK)
* `No_KK`
* `Nama_Lengkap`
* `Tempat_Lahir`
* `Tanggal_Lahir`
* `Jenis_Kelamin`
* `Alamat`
* `Pendidikan_Terakhir`
* `Pekerjaan`
* `Status_Ekonomi` (Misal: Mampu, Kurang Mampu)


* **JENIS_SURAT** (Master Jenis Dokumen)
* `ID_Jenis_Surat` (Identifier/PK)
* `Nama_Surat` (Contoh: KTP, KK, SKTM, Domisili)
* `Syarat_Dokumen`


* **PERMOHONAN_SURAT** (Transaksi Pelayanan)
* `No_Permohonanan` (Identifier/PK)
* `Tanggal_Pengajuan`
* `Status_Pengajuan` (Contoh: Diproses, Selesai, Ditolak)
* `Keterangan`


* **PENGADUAN** (Transaksi Pengaduan)
* `ID_Pengaduan` (Identifier/PK)
* `Tanggal_Pengaduan`
* `Isi_Pengaduan`
* `Kategori` (Contoh: Pelayanan, Fasilitas, Infrastruktur)
* `Status_Tindak_Lanjut` (Contoh: Pending, Diproses, Selesai)



### Hubungan Antar Entitas (Relationships)

1. **WARGA mengajukan PERMOHONAN_SURAT**
* Kardinalitas: **1 to Many (1:N)**. Satu warga dapat mengajukan banyak permohonan surat seiring waktu, tetapi satu permohonan surat hanya dimiliki oleh satu warga.


2. **JENIS_SURAT mencakup PERMOHONAN_SURAT**
* Kardinalitas: **1 to Many (1:N)**. Satu jenis surat (misal: SKTM) bisa diajukan dalam banyak permohonan, tetapi satu permohonan hanya untuk satu jenis surat spesifik.


3. **WARGA menyampaikan PENGADUAN**
* Kardinalitas: **1 to Many (1:N)**. Satu warga dapat membuat banyak pengaduan, dan setiap pengaduan dicatat atas nama warga yang bersangkutan.



---

## 2. Physical Data Model (PDM)

PDM adalah representasi teknis yang siap diimplementasikan ke dalam DBMS (seperti MySQL atau PostgreSQL). Di sini, hubungan *1:N* akan menghasilkan *Foreign Key (FK)* pada tabel anak (*child table*).

### Struktur Tabel (Skema Relasi)

#### 1. Tabel `tabel_warga`

| Nama Kolom | Tipe Data | Keterangan |
| --- | --- | --- |
| `nik` **(PK)** | VARCHAR(16) | Nomor Induk Kependudukan |
| `no_kk` | VARCHAR(16) | Nomor Kartu Keluarga |
| `nama_lengkap` | VARCHAR(100) |  |
| `tempat_lahir` | VARCHAR(50) |  |
| `tanggal_lahir` | DATE |  |
| `jenis_kelamin` | ENUM('L', 'P') |  |
| `alamat` | TEXT |  |
| `pendidikan_terakhir` | VARCHAR(30) |  |
| `pekerjaan` | VARCHAR(50) |  |
| `status_ekonomi` | VARCHAR(20) | Mampu / Kurang Mampu (untuk filter bansos/SKTM) |

#### 2. Tabel `tabel_jenis_surat`

| Nama Kolom | Tipe Data | Keterangan |
| --- | --- | --- |
| `id_jenis_surat` **(PK)** | INT (Auto Increment) |  |
| `nama_surat` | VARCHAR(50) | KTP, KK, SKTM, dll. |
| `syarat_dokumen` | TEXT | Persyaratan berkas |

#### 3. Tabel `tabel_permohonan_surat`

| Nama Kolom | Tipe Data | Keterangan |
| --- | --- | --- |
| `no_permohonan` **(PK)** | VARCHAR(20) | Kode unik pengajuan |
| `nik` **(FK)** | VARCHAR(16) | Menghubungkan ke `tabel_warga` |
| `id_jenis_surat` **(FK)** | INT | Menghubungkan ke `tabel_jenis_surat` |
| `tanggal_pengajuan` | DATE |  |
| `status_pengajuan` | ENUM('Pending', 'Proses', 'Selesai', 'Ditolak') | Untuk melacak status dokumen |
| `keterangan` | TEXT | Catatan jika ditolak atau catatan tambahan |

#### 4. Tabel `tabel_pengaduan`

| Nama Kolom | Tipe Data | Keterangan |
| --- | --- | --- |
| `id_pengaduan` **(PK)** | INT (Auto Increment) |  |
| `nik` **(FK)** | VARCHAR(16) | Menghubungkan ke `tabel_warga` (Pelapor) |
| `tanggal_pengaduan` | DATETIME |  |
| `isi_pengaduan` | TEXT | Detail keluhan warga |
| `kategori` | VARCHAR(50) | Pelayanan, Infrastruktur, dll. |
| `status_tindak_lanjut` | ENUM('Baru', 'Diproses', 'Selesai') |  |

---

## Bagaimana Model Ini Menjawab Tantangan Desa?

> * **Solusi Lambatnya Sistem & Pelacakan Status:** Melalui `tabel_permohonan_surat`, perangkat desa dapat mengubah `status_pengajuan` secara berkala (misal dari 'Proses' ke 'Selesai'), sehingga warga bisa melacak posisi dokumen mereka secara *real-time*.
> * **Solusi Kecepatan Pemrosesan Data (Bansos/SKTM):** Dengan adanya kolom `status_ekonomi` di `tabel_warga`, perangkat desa hanya perlu melakukan *query* sederhana untuk langsung mendapatkan daftar warga kurang mampu yang berhak menerima bantuan sosial.
> * **Solusi Transparansi via Pengaduan:** `tabel_pengaduan` memastikan setiap keluhan warga tercatat secara digital, tidak terlupakan, dan memiliki status tindak lanjut yang jelas.
> 
>
