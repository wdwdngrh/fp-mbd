"""
Dataset Domain Klinik Pribadi
Menggabungkan semua domain menjadi satu set data yang kohesif
dengan variasi kasus sebanyak mungkin.

PERUBAHAN:
- NIK konsisten dengan tanggal_lahir & jenis_kelamin
  Format: PPKKCC-DDMMYY-XXXX  (DD +40 untuk perempuan)
  Kode wilayah: pool kode kecamatan Jawa Timur (Surabaya, Sidoarjo, Gresik, Malang, Jember)
- no_telepon menggunakan prefix operator seluler Indonesia yang valid
- Nama pasien dijamin konsisten dengan jenis_kelamin (tanpa overflow lintas gender)
"""

import random
import itertools
from datetime import datetime, timedelta, date

# ─────────────────────────────────────────────
# 1. DATA MASTER: PASIEN
# ─────────────────────────────────────────────

nama_pool = {
    "L": [
        "Budi Santoso", "Ahmad Fauzi", "Rizky Pratama", "Denny Kurniawan", "Iwabe Anka",
        "Hendra Wijaya", "Fajar Nugroho", "Eko Susanto", "Wahyu Hidayat", "Setya Novan",
        "Agus Setiawan", "Doni Firmansyah", "Irfan Maulana", "Rudi Hartono", "Ari Amar",
        "Sandi Putra", "Taufik Rahman", "Yusuf Hakim", "Agus Setya", "Joko Wijaya", "Andi Wijaya",
        "Aditya Pratama", "Bayu Segara", "Cahyo Wicaksono", "Dwi Saputra", "Galih Permana",
        "Haris Fadilah", "Ivan Kurniawan", "Jaka Samudra", "Kurnia Adi", "Lukman Hakim",
        "Maulana Yusuf", "Nanda Wijaya", "Okky Pradana", "Putra Mandala", "Qodri Hidayat",
        "Rifki Ramadhan", "Seno Aji", "Teguh Santoso", "Umar Said", "Vino Pratama",
        "Wawan Setiawan", "Xavier Putra", "Yoga Prasetyo", "Zulfikar Ali", "Arif Budiman",
        "Dimas Prayoga", "Gilang Ramadhan", "Heri Susanto", "Joko Widodo", "Kiki Firmansyah"
    ],
    "P": [
        "Siti Rahayu", "Dewi Lestari", "Nur Indah", "Fitri Anggraeni", "Laras Tari",
        "Rina Wulandari", "Yuni Astuti", "Mega Permata", "Laila Sari", "Ika Nadi",
        "Ayu Pratiwi", "Hana Kusuma", "Vina Marlina", "Sri Wahyuni", "Layla Amro",
        "Putri Amalia", "Novia Rahmawati", "Dian Safitri", "Melissa Subando", "Citra Dewi",
        "Elisa Putri", "Fani Anggraini", "Gita Lestari", "Hilda Fitriani", "Indah Permata Sari",
        "Julia Rahmawati", "Kartika Sari", "Lina Marlina", "Maya Anggraini", "Nisa Amelia",
        "Olivia Putri", "Putri Indah Sari", "Qiana Dewi", "Risa Amelia", "Susi Susanti",
        "Tia Fitriani", "Umi Kalsum", "Via Oktaviana", "Wulan Sari", "Xena Putri",
        "Yolanda Putri", "Zahra Amelia", "Anisa Putri", "Bunga Lestari", "Cinta Dewi",
        "Dina Rahayu", "Eka Sari", "Fira Andriani", "Gita Amelia", "Hani Wulandari"
    ]
}

alamat_pool = [
    "Jl. Mawar, Surabaya",
    "Jl. Melati, Sidoarjo",
    "Jl. Kenanga, Gresik",
    "Perum Griya Indah, Surabaya",
    "Jl. Pahlawan, Malang",
    "Jl. Diponegoro, Surabaya",
    "Jl. Raya Darmo, Surabaya",
    "Jl. Kalimantan, Jember",
    "Komplek Perumahan Bumi Asri, Sidoarjo",
    "Jl. Veteran, Malang",
]

# ── Kode wilayah NIK Jawa Timur (per kecamatan) ──────────────────────────────
# Format: PPKK CC  (provinsi=35, kabupaten/kota, kecamatan)
# Sumber: Permendagri No. 58/2021 — subset representatif
kode_wilayah_pool = [
    "357801",  # Surabaya – Genteng
    "357802",  # Surabaya – Bubutan
    "357803",  # Surabaya – Tambaksari
    "357804",  # Surabaya – Sawahan
    "357805",  # Surabaya – Wonokromo
    "351501",  # Sidoarjo – Sidoarjo
    "351502",  # Sidoarjo – Candi
    "352501",  # Gresik – Gresik
    "356101",  # Malang – Klojen
    "356102",  # Malang – Blimbing
    "350901",  # Jember – Kaliwates
]

# Prefix no. telepon operator seluler Indonesia yang valid
# (Telkomsel, Indosat, XL, Axis, Tri, Smartfren)
prefix_telepon_pool = [
    "0811", "0812", "0813", "0821", "0822", "0823",  # Telkomsel
    "0814", "0815", "0816", "0855", "0856", "0857", "0858",  # Indosat
    "0817", "0818", "0819", "0859", "0877", "0878",  # XL
    "0831", "0832", "0833", "0838",                  # Axis
    "0895", "0896", "0897", "0898", "0899",          # Tri
    "0881", "0882", "0883", "0884",                  # Smartfren
]


def _nik_encode_tanggal(tgl_lahir: date, jenis_kelamin: str) -> str:
    """
    Encode tanggal lahir ke 6 digit segmen NIK (DDMMYY).
    Untuk perempuan, nilai DD ditambah 40 (standar NIK Indonesia).
    """
    dd = tgl_lahir.day
    if jenis_kelamin == "P":
        dd += 40
    mm = tgl_lahir.month
    yy = tgl_lahir.year % 100          # 2 digit terakhir tahun
    return f"{dd:02d}{mm:02d}{yy:02d}"


def _generate_nik(tgl_lahir: date, jenis_kelamin: str,
                  used_nik: set, rng: random.Random) -> str:
    """
    Buat NIK 16 digit yang unik dan konsisten dengan data pasien:
      [kode_wilayah 6 digit] [tgl_lahir 6 digit] [nomor_urut 4 digit]
    """
    kode_wil   = rng.choice(kode_wilayah_pool)
    tgl_enc    = _nik_encode_tanggal(tgl_lahir, jenis_kelamin)
    for _ in range(10_000):             # hindari infinite loop
        nomor_urut = f"{rng.randint(1, 9999):04d}"
        nik = kode_wil + tgl_enc + nomor_urut
        if nik not in used_nik:
            used_nik.add(nik)
            return nik
    raise RuntimeError("Tidak bisa generate NIK unik — coba perlebar pool nomor urut.")


def _generate_telepon(rng: random.Random) -> str:
    """
    Buat nomor telepon dengan prefix operator valid (10–13 digit total).
    """
    prefix  = rng.choice(prefix_telepon_pool)
    # Sisa digit: 6–9 angka agar total 10–13 digit
    n_sisa  = rng.randint(6, 9)
    sisa    = "".join([str(rng.randint(0, 9)) for _ in range(n_sisa)])
    return prefix + sisa


def generate_pasien(n: int = 30, seed: int | None = None) -> list[dict]:
    rng = random.Random(seed)
    pasien_list: list[dict] = []
    used_nik: set[str]      = set()
    used_rm:  set[str]      = set()

    # Siapkan pool nama yang bisa di-shuffle per gender agar tidak berulang terlalu cepat
    nama_shuffled = {
        jk: list(pool) * (n // len(pool) + 2)   # cukup panjang untuk n pasien
        for jk, pool in nama_pool.items()
    }
    idx_nama = {"L": 0, "P": 0}

    for i in range(n):
        jk = rng.choice(["L", "P"])

        # Ambil nama sesuai jenis kelamin, tanpa pernah melintas ke gender lain
        nama = nama_shuffled[jk][idx_nama[jk] % len(nama_shuffled[jk])]
        idx_nama[jk] += 1

        tgl_lahir = date(
            rng.randint(1955, 2005),
            rng.randint(1, 12),
            rng.randint(1, 28),
        )

        nik = _generate_nik(tgl_lahir, jk, used_nik, rng)

        # Nomor RM unik RM-XXXXXX
        while True:
            rm = f"RM-{rng.randint(100000, 999999)}"
            if rm not in used_rm:
                used_rm.add(rm)
                break

        tgl_daftar = datetime(
            2024,
            rng.randint(1, 12),
            rng.randint(1, 28),
            rng.randint(7, 16),
            rng.randint(0, 59),
        )

        pasien_list.append({
            "id_pasien":      i + 1,
            "nomor_rm":       rm,
            "nama_pasien":    nama,
            "nik":            nik,
            "jenis_kelamin":  jk,
            "tanggal_lahir":  tgl_lahir.isoformat(),
            "alamat":         rng.choice(alamat_pool),
            "no_telepon":     _generate_telepon(rng),
            "tanggal_daftar": tgl_daftar.isoformat(sep=" "),
        })
    return pasien_list


# ─────────────────────────────────────────────
# 2. DATA MASTER: DOKTER
# ─────────────────────────────────────────────

dokter_pool = [
    {"nama": "dr. Andi Wibowo",         "spesialisasi": "Umum"},
    {"nama": "dr. Siska Maharani",      "spesialisasi": "Umum"},
    {"nama": "dr. Brama Kusuma, Sp.PD", "spesialisasi": "Penyakit Dalam"},
    {"nama": "dr. Lena Puspita, Sp.A",  "spesialisasi": "Anak"},
    {"nama": "dr. Faris Hakim",         "spesialisasi": "Umum"},
]


def generate_dokter() -> list[dict]:
    dokter_list = []
    for i, d in enumerate(dokter_pool):
        dokter_list.append({
            "id_dokter":    i + 1,
            "kode_dokter":  f"DOK-{str(i+1).zfill(3)}",
            "nama_dokter":  d["nama"],
            "spesialisasi": d["spesialisasi"],
            "no_sip":       f"SIP/{random.randint(100,999)}/{random.randint(2018,2023)}/IDI",
            "no_telepon":   _generate_telepon(random.Random()),
            "aktif":        True,
        })
    return dokter_list


# ─────────────────────────────────────────────
# 3. DATA MASTER: OBAT
# ─────────────────────────────────────────────

nama_obat_pool = [
    {"nama": "Paracetamol 500mg",   "satuan": "Tablet", "harga": 5000,  "stok": 500},
    {"nama": "Antasida Doen",       "satuan": "Tablet", "harga": 4000,  "stok": 300},
    {"nama": "Amoxicillin 500mg",   "satuan": "Kapsul", "harga": 12000, "stok": 200},
    {"nama": "OBH Combi Sirup",     "satuan": "Botol",  "harga": 25000, "stok": 150},
    {"nama": "Cetirizine 10mg",     "satuan": "Tablet", "harga": 8000,  "stok": 250},
    {"nama": "Ibuprofen 400mg",     "satuan": "Tablet", "harga": 7000,  "stok": 400},
    {"nama": "Ranitidine 150mg",    "satuan": "Tablet", "harga": 6000,  "stok": 350},
    {"nama": "Ambroxol Sirup",      "satuan": "Botol",  "harga": 18000, "stok": 120},
    {"nama": "Metformin 500mg",     "satuan": "Tablet", "harga": 9000,  "stok": 180},
    {"nama": "Amlodipine 5mg",      "satuan": "Tablet", "harga": 11000, "stok": 160},
    {"nama": "Salbutamol 2mg",      "satuan": "Tablet", "harga": 6500,  "stok": 200},
    {"nama": "Dexamethasone 0.5mg", "satuan": "Tablet", "harga": 4500,  "stok": 300},
]


def generate_obat() -> list[dict]:
    obat_list = []
    for i, o in enumerate(nama_obat_pool):
        obat_list.append({
            "id_obat":    i + 1,
            "kode_obat":  f"OBT-{str(i+1).zfill(4)}",
            "nama_obat":  o["nama"],
            "satuan":     o["satuan"],
            "harga_jual": o["harga"],
            "stok_obat":  o["stok"],
        })
    return obat_list


# ─────────────────────────────────────────────
# 4. KLINIS: KELUHAN ↔ DIAGNOSA ↔ OBAT (terkoneksi logis)
# ─────────────────────────────────────────────

skenario_klinis = [
    {
        "keluhan":        "Demam tinggi dan sakit kepala.",
        "diagnosa":       "Febris / Demam virus",
        "tindakan":       "Pemberian antipiretik dan edukasi istirahat",
        "obat_ids":       [1],
        "aturan":         "3 x 1 tablet setelah makan",
        "tarif_layanan":  50000,
    },
    {
        "keluhan":        "Batuk berdahak dan flu berat.",
        "diagnosa":       "Acute Nasopharyngitis",
        "tindakan":       "Edukasi hidrasi dan pemberian ekspektoran",
        "obat_ids":       [4, 8],
        "aturan":         "3 x 1 sendok takar sesudah makan",
        "tarif_layanan":  50000,
    },
    {
        "keluhan":        "Nyeri lambung dan mual-mual.",
        "diagnosa":       "Dispepsia / Maag Akut",
        "tindakan":       "Pemberian antasida dan edukasi pola makan",
        "obat_ids":       [2, 7],
        "aturan":         "3 x 1 tablet kunyah sebelum makan",
        "tarif_layanan":  50000,
    },
    {
        "keluhan":        "Gatal-gatal di seluruh tubuh.",
        "diagnosa":       "Urtikaria Akut / Alergi",
        "tindakan":       "Pemberian antihistamin",
        "obat_ids":       [5],
        "aturan":         "1 x 1 tablet malam hari",
        "tarif_layanan":  50000,
    },
    {
        "keluhan":        "Pemeriksaan rutin tekanan darah.",
        "diagnosa":       "Hipertensi Esensial",
        "tindakan":       "Edukasi diet rendah garam dan pemantauan tensi",
        "obat_ids":       [10],
        "aturan":         "1 x 1 tablet pagi hari",
        "tarif_layanan":  75000,
    },
    {
        "keluhan":        "Sesak napas ringan setelah beraktivitas.",
        "diagnosa":       "Asma Bronkial Ringan",
        "tindakan":       "Edukasi pembatasan pemicu alergi",
        "obat_ids":       [11],
        "aturan":         "3 x 1 tablet setelah makan",
        "tarif_layanan":  75000,
    },
    {
        "keluhan":        "Nyeri sendi pada lutut kanan.",
        "diagnosa":       "Osteoarthritis",
        "tindakan":       "Pemberian analgetik topikal/oral",
        "obat_ids":       [6, 12],
        "aturan":         "3 x 1 tablet setelah makan",
        "tarif_layanan":  75000,
    },
    {
        "keluhan":        "Sakit gigi berdenyut sejak 2 hari.",
        "diagnosa":       "Pulpitis / Radang Gigi",
        "tindakan":       "Rujukan ke dokter gigi setelah nyeri reda",
        "obat_ids":       [1, 3],
        "aturan":         "3 x 1 tablet setelah makan",
        "tarif_layanan":  50000,
    },
    {
        "keluhan":        "Rasa haus berlebihan, sering buang air kecil.",
        "diagnosa":       "Diabetes Mellitus Tipe 2",
        "tindakan":       "Edukasi pola makan dan olahraga rutin",
        "obat_ids":       [9],
        "aturan":         "2 x 1 tablet sesudah makan",
        "tarif_layanan":  100000,
    },
    {
        "keluhan":        "Batuk kering terus-menerus lebih dari seminggu.",
        "diagnosa":       "Faringitis Kronis",
        "tindakan":       "Pemberian antibiotik dan edukasi minum air putih",
        "obat_ids":       [3, 8],
        "aturan":         "3 x 1 tablet setelah makan",
        "tarif_layanan":  50000,
    },
    {
        "keluhan":        "Mual dan muntah sejak pagi, tidak bisa makan.",
        "diagnosa":       "Gastroenteritis Akut",
        "tindakan":       "Rehidrasi oral dan istirahat",
        "obat_ids":       [2],
        "aturan":         "3 x 1 tablet kunyah sebelum makan",
        "tarif_layanan":  50000,
    },
    {
        "keluhan":        "Pilek dan bersin-bersin setiap pagi.",
        "diagnosa":       "Rhinitis Alergi",
        "tindakan":       "Edukasi hindari alergen dan pemberian antihistamin",
        "obat_ids":       [5, 12],
        "aturan":         "1 x 1 tablet malam hari",
        "tarif_layanan":  50000,
    },
]


# ─────────────────────────────────────────────
# 5. VITAL SIGN: VARIASI PER DIAGNOSA
# ─────────────────────────────────────────────

vital_sign_pool = {
    "Febris / Demam virus":     {"tensi": "110/70", "bb_range": (50, 85),  "suhu_range": (38.5, 40.0)},
    "Acute Nasopharyngitis":    {"tensi": "120/80", "bb_range": (45, 90),  "suhu_range": (37.5, 38.5)},
    "Dispepsia / Maag Akut":    {"tensi": "115/75", "bb_range": (50, 80),  "suhu_range": (36.5, 37.2)},
    "Urtikaria Akut / Alergi":  {"tensi": "120/80", "bb_range": (50, 85),  "suhu_range": (36.5, 37.5)},
    "Hipertensi Esensial":      {"tensi": "150/95", "bb_range": (60, 100), "suhu_range": (36.5, 37.0)},
    "Asma Bronkial Ringan":     {"tensi": "125/80", "bb_range": (45, 80),  "suhu_range": (36.5, 37.5)},
    "Osteoarthritis":           {"tensi": "130/85", "bb_range": (55, 95),  "suhu_range": (36.5, 37.0)},
    "Pulpitis / Radang Gigi":   {"tensi": "120/80", "bb_range": (50, 85),  "suhu_range": (36.8, 38.0)},
    "Diabetes Mellitus Tipe 2": {"tensi": "135/85", "bb_range": (60, 100), "suhu_range": (36.5, 37.0)},
    "Faringitis Kronis":        {"tensi": "115/75", "bb_range": (45, 80),  "suhu_range": (37.2, 38.0)},
    "Gastroenteritis Akut":     {"tensi": "100/65", "bb_range": (45, 80),  "suhu_range": (37.5, 38.5)},
    "Rhinitis Alergi":          {"tensi": "120/80", "bb_range": (50, 85),  "suhu_range": (36.5, 37.2)},
}

status_kunjungan_pool  = ["Menunggu", "Diperiksa", "Selesai"]
status_pembayaran_pool = ["Belum Lunas", "Lunas"]


# ─────────────────────────────────────────────
# 6. GENERATOR UTAMA: KUNJUNGAN + TRANSAKSI
# ─────────────────────────────────────────────

def generate_kunjungan(
    pasien_list: list[dict],
    dokter_list: list[dict],
    obat_list:   list[dict],
    n_kunjungan: int = 50,
) -> dict:
    kunjungan_list    = []
    pemeriksaan_list  = []
    resep_list        = []
    detail_resep_list = []
    pembayaran_list   = []

    obat_by_id = {o["id_obat"]: o for o in obat_list}
    id_kunjungan    = 1
    id_pemeriksaan  = 1
    id_resep        = 1
    id_detail_resep = 1
    id_pembayaran   = 1

    base_date = datetime(2025, 1, 1, 8, 0)

    for _ in range(n_kunjungan):
        pasien   = random.choice(pasien_list)
        dokter   = random.choice(dokter_list)
        skenario = random.choice(skenario_klinis)
        diagnosa = skenario["diagnosa"]
        vital    = vital_sign_pool.get(diagnosa, {
            "tensi": "120/80", "bb_range": (50, 80), "suhu_range": (36.5, 37.5)
        })

        offset_hari  = random.randint(0, 364)
        offset_menit = random.randint(0, 480)
        tgl_kunjungan = base_date + timedelta(days=offset_hari, minutes=offset_menit)

        status_kunjungan = random.choices(
            status_kunjungan_pool,
            weights=[10, 15, 75],
            k=1,
        )[0]

        kunjungan_list.append({
            "id_kunjungan":      id_kunjungan,
            "id_pasien":         pasien["id_pasien"],
            "id_dokter":         dokter["id_dokter"],
            "tanggal_kunjungan": tgl_kunjungan.isoformat(sep=" "),
            "keluhan_utama":     skenario["keluhan"],
            "status_kunjungan":  status_kunjungan,
        })

        if status_kunjungan in ("Diperiksa", "Selesai"):
            bb    = round(random.uniform(*vital["bb_range"]), 1)
            suhu  = round(random.uniform(*vital["suhu_range"]), 1)
            tensi = vital["tensi"]

            tgl_periksa = tgl_kunjungan + timedelta(minutes=random.randint(10, 60))

            pemeriksaan_list.append({
                "id_pemeriksaan":  id_pemeriksaan,
                "id_kunjungan":    id_kunjungan,
                "tanggal_periksa": tgl_periksa.isoformat(sep=" "),
                "tensi_darah":     tensi,
                "berat_badan":     bb,
                "suhu_tubuh":      suhu,
                "diagnosa":        diagnosa,
                "tindakan_medis":  skenario["tindakan"],
            })

            total_biaya_obat = 0
            if status_kunjungan == "Selesai":
                tgl_resep = tgl_periksa + timedelta(minutes=random.randint(5, 20))
                resep_list.append({
                    "id_resep":       id_resep,
                    "id_pemeriksaan": id_pemeriksaan,
                    "tanggal_resep":  tgl_resep.isoformat(sep=" "),
                })

                for obat_id in skenario["obat_ids"]:
                    obat = obat_by_id.get(obat_id)
                    if not obat:
                        continue
                    jumlah     = random.choice([5, 10, 15, 20, 30])
                    biaya_item = obat["harga_jual"] * jumlah
                    total_biaya_obat += biaya_item

                    detail_resep_list.append({
                        "id_detail_resep": id_detail_resep,
                        "id_resep":        id_resep,
                        "id_obat":         obat_id,
                        "jumlah":          jumlah,
                        "aturan_pakai":    skenario["aturan"],
                    })
                    id_detail_resep += 1

                id_resep += 1

            if status_kunjungan == "Selesai":
                tarif         = skenario["tarif_layanan"]
                tarif_variasi = random.choice([tarif, tarif - 10000, tarif + 25000])
                tarif_variasi = max(tarif_variasi, 0)

                status_bayar = random.choices(
                    status_pembayaran_pool,
                    weights=[20, 80],
                    k=1,
                )[0]

                waktu_bayar = None
                if status_bayar == "Lunas":
                    waktu_bayar = (
                        tgl_periksa + timedelta(minutes=random.randint(5, 30))
                    ).isoformat(sep=" ")

                pembayaran_list.append({
                    "id_pembayaran":       id_pembayaran,
                    "id_kunjungan":        id_kunjungan,
                    "total_biaya_layanan": tarif_variasi,
                    "total_biaya_obat":    round(total_biaya_obat, 2),
                    "total_keseluruhan":   round(tarif_variasi + total_biaya_obat, 2),
                    "status_pembayaran":   status_bayar,
                    "waktu_pembayaran":    waktu_bayar,
                })
                id_pembayaran += 1

            id_pemeriksaan += 1

        id_kunjungan += 1

    return {
        "kunjungan":    kunjungan_list,
        "pemeriksaan":  pemeriksaan_list,
        "resep":        resep_list,
        "detail_resep": detail_resep_list,
        "pembayaran":   pembayaran_list,
    }


# ─────────────────────────────────────────────
# 7. SATU SET LENGKAP
# ─────────────────────────────────────────────

def generate_dataset(
    n_pasien:    int = 100,
    n_kunjungan: int = 200_000,
    seed:        int = 42,
) -> dict:
    random.seed(seed)

    pasien_list = generate_pasien(n_pasien, seed=seed)
    dokter_list = generate_dokter()
    obat_list   = generate_obat()
    transaksi   = generate_kunjungan(pasien_list, dokter_list, obat_list, n_kunjungan)

    return {
        "pasien":       pasien_list,
        "dokter":       dokter_list,
        "obat":         obat_list,
        "kunjungan":    transaksi["kunjungan"],
        "pemeriksaan":  transaksi["pemeriksaan"],
        "resep":        transaksi["resep"],
        "detail_resep": transaksi["detail_resep"],
        "pembayaran":   transaksi["pembayaran"],
    }


# ─────────────────────────────────────────────
# 8. SQL EXPORT (streaming, tidak load semua ke RAM)
# ─────────────────────────────────────────────

BATCH_SIZE = 5_000
OUT_FILE   = "klinik_seed.sql"


def esc(s: object) -> str:
    """Escape single-quote untuk string PostgreSQL."""
    return str(s).replace("'", "''")


def write_insert(f, table: str, cols: str, rows: list[str]) -> None:
    if not rows:
        return
    f.write(f"INSERT INTO {table} ({cols}) VALUES\n")
    for i, row in enumerate(rows):
        sep = ";" if i == len(rows) - 1 else ","
        f.write(f"  {row}{sep}\n")
    f.write("\n")


def export_to_sql(dataset: dict, out_file: str = OUT_FILE) -> dict:
    from collections import Counter
    stats: Counter = Counter()

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("-- =====================================================\n")
        f.write("-- KLINIK SEED DATA — dihasilkan oleh klinik_dataset.py\n")
        f.write(f"-- Kunjungan : {len(dataset['kunjungan']):,}\n")
        f.write(f"-- Pasien    : {len(dataset['pasien']):,}\n")
        f.write("-- =====================================================\n\n")
        f.write("BEGIN;\n")
        f.write("SET session_replication_role = replica; -- bypass FK saat bulk insert\n\n")

        # ── Master: Pasien ──
        f.write("-- ─────────────── PASIEN ───────────────────────────\n")
        cols = ("id_pasien,nomor_rm,nama_pasien,nik,jenis_kelamin,"
                "tanggal_lahir,alamat,no_telepon,tanggal_daftar")
        batch: list[str] = []
        for p in dataset["pasien"]:
            batch.append(
                f"({p['id_pasien']},'{esc(p['nomor_rm'])}','{esc(p['nama_pasien'])}',"
                f"'{p['nik']}','{p['jenis_kelamin']}','{p['tanggal_lahir']}',"
                f"'{esc(p['alamat'])}','{p['no_telepon']}','{p['tanggal_daftar']}')"
            )
            if len(batch) >= BATCH_SIZE:
                write_insert(f, "pasien", cols, batch)
                batch.clear()
        write_insert(f, "pasien", cols, batch)

        # ── Master: Dokter ──
        f.write("-- ─────────────── DOKTER ───────────────────────────\n")
        cols = "id_dokter,kode_dokter,nama_dokter,spesialisasi,no_sip,no_telepon,aktif"
        rows: list[str] = []
        for d in dataset["dokter"]:
            aktif = "TRUE" if d["aktif"] else "FALSE"
            rows.append(
                f"({d['id_dokter']},'{d['kode_dokter']}','{esc(d['nama_dokter'])}',"
                f"'{esc(d['spesialisasi'])}','{d['no_sip']}','{d['no_telepon']}',{aktif})"
            )
        write_insert(f, "dokter", cols, rows)

        # ── Master: Obat ──
        f.write("-- ─────────────── OBAT ─────────────────────────────\n")
        cols = "id_obat,kode_obat,nama_obat,satuan,harga_jual,stok_obat"
        rows = []
        for o in dataset["obat"]:
            rows.append(
                f"({o['id_obat']},'{o['kode_obat']}','{esc(o['nama_obat'])}',"
                f"'{o['satuan']}',{o['harga_jual']},{o['stok_obat']})"
            )
        write_insert(f, "obat", cols, rows)

        # ── Transaksi ──
        tables = [
            (
                "kunjungan",
                "id_kunjungan,id_pasien,id_dokter,tanggal_kunjungan,keluhan_utama,status_kunjungan",
                lambda r: (
                    f"({r['id_kunjungan']},{r['id_pasien']},{r['id_dokter']},"
                    f"'{r['tanggal_kunjungan']}','{esc(r['keluhan_utama'])}',"
                    f"'{r['status_kunjungan']}')"
                ),
            ),
            (
                "pemeriksaan",
                "id_pemeriksaan,id_kunjungan,tanggal_periksa,tensi_darah,berat_badan,suhu_tubuh,diagnosa,tindakan_medis",
                lambda r: (
                    f"({r['id_pemeriksaan']},{r['id_kunjungan']},'{r['tanggal_periksa']}',"
                    f"'{r['tensi_darah']}',{r['berat_badan']},{r['suhu_tubuh']},"
                    f"'{esc(r['diagnosa'])}','{esc(r['tindakan_medis'])}')"
                ),
            ),
            (
                "resep",
                "id_resep,id_pemeriksaan,tanggal_resep",
                lambda r: f"({r['id_resep']},{r['id_pemeriksaan']},'{r['tanggal_resep']}')",
            ),
            (
                "detail_resep",
                "id_detail_resep,id_resep,id_obat,jumlah,aturan_pakai",
                lambda r: (
                    f"({r['id_detail_resep']},{r['id_resep']},{r['id_obat']},"
                    f"{r['jumlah']},'{esc(r['aturan_pakai'])}')"
                ),
            ),
            (
                "pembayaran",
                "id_pembayaran,id_kunjungan,total_biaya_layanan,total_biaya_obat,status_pembayaran,waktu_pembayaran",
                lambda r: (
                    f"({r['id_pembayaran']},{r['id_kunjungan']},"
                    f"{r['total_biaya_layanan']},{r['total_biaya_obat']},"
                    f"'{r['status_pembayaran']}',"
                    f"{'NULL' if r['waktu_pembayaran'] is None else chr(39)+r['waktu_pembayaran']+chr(39)})"
                ),
            ),
        ]

        for tbl_name, cols, row_fn in tables:
            f.write(f"-- ─────────────── {tbl_name.upper()} {'─'*(40-len(tbl_name))}\n")
            batch = []
            for row in dataset[tbl_name]:
                batch.append(row_fn(row))
                stats[tbl_name] += 1
                if len(batch) >= BATCH_SIZE:
                    write_insert(f, tbl_name, cols, batch)
                    batch.clear()
            write_insert(f, tbl_name, cols, batch)

        # ── Reset sequences ──
        f.write("-- ─────────────── SEQUENCES ────────────────────────\n")
        seq_map = [
            ("pasien_id_pasien_seq",            len(dataset["pasien"])),
            ("dokter_id_dokter_seq",            len(dataset["dokter"])),
            ("obat_id_obat_seq",                len(dataset["obat"])),
            ("kunjungan_id_kunjungan_seq",      stats["kunjungan"]),
            ("pemeriksaan_id_pemeriksaan_seq",  stats["pemeriksaan"]),
            ("resep_id_resep_seq",              stats["resep"]),
            ("detail_resep_id_detail_resep_seq",stats["detail_resep"]),
            ("pembayaran_id_pembayaran_seq",    stats["pembayaran"]),
        ]
        for seq, val in seq_map:
            f.write(f"SELECT setval('{seq}', {val});\n")

        f.write("\nSET session_replication_role = DEFAULT;\n")
        f.write("COMMIT;\n")

    return stats


# ─────────────────────────────────────────────
# 9. VALIDASI KONSISTENSI NIK (opsional, jalankan sendiri)
# ─────────────────────────────────────────────

def _validasi_nik(pasien_list: list[dict]) -> None:
    """
    Periksa apakah setiap NIK konsisten dengan tanggal_lahir & jenis_kelamin.
    Cetak baris yang tidak valid (seharusnya kosong).
    """
    errors = 0
    for p in pasien_list:
        nik        = p["nik"]
        tgl_lahir  = date.fromisoformat(p["tanggal_lahir"])
        jk         = p["jenis_kelamin"]
        expected   = _nik_encode_tanggal(tgl_lahir, jk)
        actual_tgl = nik[6:12]   # karakter ke-7 s.d. ke-12

        # Juga periksa prefix wilayah ada di pool
        prefix = nik[:6]
        if actual_tgl != expected or prefix not in kode_wilayah_pool:
            print(f"[INVALID] id={p['id_pasien']} nik={nik} expected_tgl={expected}")
            errors += 1

    if errors == 0:
        print(f"Validasi NIK OK — {len(pasien_list):,} pasien, tidak ada error.")
    else:
        print(f"Ditemukan {errors} NIK tidak valid.")


# ─────────────────────────────────────────────
# 10. JALANKAN & RINGKASAN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    from collections import Counter
    import os

    print("Generating dataset (5.000 pasien, 200.000 kunjungan)...", flush=True)
    dataset = generate_dataset(n_pasien=100, n_kunjungan=200_000)

    print("Validasi konsistensi NIK...", flush=True)
    _validasi_nik(dataset["pasien"])

    print(f"Exporting ke {OUT_FILE} ...", flush=True)
    stats = export_to_sql(dataset, OUT_FILE)

    size_mb = os.path.getsize(OUT_FILE) / 1024 / 1024

    print()
    print("=" * 55)
    print("  DATASET KLINIK — RINGKASAN")
    print("=" * 55)
    label_map = {
        "pasien":       ("Pasien",       len(dataset["pasien"])),
        "dokter":       ("Dokter",       len(dataset["dokter"])),
        "obat":         ("Obat",         len(dataset["obat"])),
        "kunjungan":    ("Kunjungan",    stats["kunjungan"]),
        "pemeriksaan":  ("Pemeriksaan",  stats["pemeriksaan"]),
        "resep":        ("Resep",        stats["resep"]),
        "detail_resep": ("Detail Resep", stats["detail_resep"]),
        "pembayaran":   ("Pembayaran",   stats["pembayaran"]),
    }
    for label, count in label_map.values():
        print(f"  {label:<20} : {count:>9,} rows")

    print()
    print("  STATUS KUNJUNGAN")
    print("-" * 55)
    status_cnt = Counter(k["status_kunjungan"] for k in dataset["kunjungan"])
    for status, cnt in status_cnt.items():
        print(f"  {status:<20}: {cnt:>9,}")

    print()
    print(f"  Output : {OUT_FILE}")
    print(f"  Size   : {size_mb:.1f} MB")
    print("=" * 55)
