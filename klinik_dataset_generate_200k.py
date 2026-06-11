"""
Dataset Domain Klinik Pribadi
Menggabungkan semua domain menjadi satu set data yang kohesif
dengan variasi kasus sebanyak mungkin.
"""

import random
import itertools
from datetime import datetime, timedelta, date

# ─────────────────────────────────────────────
# 1. DATA MASTER: PASIEN
# ─────────────────────────────────────────────

nama_pool = {
    "L": [
        "Budi Santoso", "Ahmad Fauzi", "Rizky Pratama", "Denny Kurniawan",
        "Hendra Wijaya", "Fajar Nugroho", "Eko Susanto", "Wahyu Hidayat",
        "Agus Setiawan", "Doni Firmansyah", "Irfan Maulana", "Rudi Hartono",
        "Sandi Putra", "Taufik Rahman", "Yusuf Hakim",
    ],
    "P": [
        "Siti Rahayu", "Dewi Lestari", "Nur Indah", "Fitri Anggraeni",
        "Rina Wulandari", "Yuni Astuti", "Mega Permata", "Laila Sari",
        "Ayu Pratiwi", "Hana Kusuma", "Vina Marlina", "Sri Wahyuni",
        "Putri Amalia", "Novia Rahmawati", "Dian Safitri",
    ],
}

alamat_pool = [
    "Jl. Mawar No. 12, Surabaya",
    "Jl. Melati No. 5, Sidoarjo",
    "Jl. Kenanga No. 7, Gresik",
    "Perum Griya Indah Blok A-3, Surabaya",
    "Jl. Pahlawan No. 88, Malang",
    "Jl. Diponegoro No. 21, Surabaya",
    "Jl. Raya Darmo No. 44, Surabaya",
    "Jl. Kalimantan No. 3, Jember",
    "Komplek Perumahan Bumi Asri No. 15, Sidoarjo",
    "Jl. Veteran No. 9, Malang",
]

def generate_pasien(n=30):
    pasien_list = []
    counter = {"L": 0, "P": 0}
    used_nik = set()
    used_rm  = set()

    for i in range(n):
        jk = random.choice(["L", "P"])
        counter[jk] += 1
        nama_idx = (counter[jk] - 1) % len(nama_pool[jk])
        nama = nama_pool[jk][nama_idx]

        tgl_lahir = date(
            random.randint(1955, 2005),
            random.randint(1, 12),
            random.randint(1, 28),
        )

        # NIK unik 16 digit
        while True:
            nik = "".join([str(random.randint(0, 9)) for _ in range(16)])
            if nik not in used_nik:
                used_nik.add(nik)
                break

        # Nomor RM unik RM-XXXXXX
        while True:
            rm = f"RM-{random.randint(100000, 999999)}"
            if rm not in used_rm:
                used_rm.add(rm)
                break

        tgl_daftar = datetime(2024, random.randint(1, 12), random.randint(1, 28),
                              random.randint(7, 16), random.randint(0, 59))

        pasien_list.append({
            "id_pasien":      i + 1,
            "nomor_rm":       rm,
            "nama_pasien":    nama,
            "nik":            nik,
            "jenis_kelamin":  jk,
            "tanggal_lahir":  tgl_lahir.isoformat(),
            "alamat":         random.choice(alamat_pool),
            "no_telepon":     f"08{random.randint(100000000, 999999999)}",
            "tanggal_daftar": tgl_daftar.isoformat(sep=" "),
        })
    return pasien_list


# ─────────────────────────────────────────────
# 2. DATA MASTER: DOKTER
# ─────────────────────────────────────────────

dokter_pool = [
    {"nama": "dr. Andi Wibowo",        "spesialisasi": "Umum"},
    {"nama": "dr. Siska Maharani",     "spesialisasi": "Umum"},
    {"nama": "dr. Brama Kusuma, Sp.PD","spesialisasi": "Penyakit Dalam"},
    {"nama": "dr. Lena Puspita, Sp.A", "spesialisasi": "Anak"},
    {"nama": "dr. Faris Hakim",        "spesialisasi": "Umum"},
]

def generate_dokter():
    dokter_list = []
    for i, d in enumerate(dokter_pool):
        dokter_list.append({
            "id_dokter":   i + 1,
            "kode_dokter": f"DOK-{str(i+1).zfill(3)}",
            "nama_dokter": d["nama"],
            "spesialisasi":d["spesialisasi"],
            "no_sip":      f"SIP/{random.randint(100,999)}/{random.randint(2018,2023)}/IDI",
            "no_telepon":  f"08{random.randint(100000000, 999999999)}",
            "aktif":       True,
        })
    return dokter_list


# ─────────────────────────────────────────────
# 3. DATA MASTER: OBAT
# ─────────────────────────────────────────────

nama_obat_pool = [
    {"nama": "Paracetamol 500mg",  "satuan": "Tablet", "harga": 5000,  "stok": 500},
    {"nama": "Antasida Doen",      "satuan": "Tablet", "harga": 4000,  "stok": 300},
    {"nama": "Amoxicillin 500mg",  "satuan": "Kapsul", "harga": 12000, "stok": 200},
    {"nama": "OBH Combi Sirup",    "satuan": "Botol",  "harga": 25000, "stok": 150},
    {"nama": "Cetirizine 10mg",    "satuan": "Tablet", "harga": 8000,  "stok": 250},
    {"nama": "Ibuprofen 400mg",    "satuan": "Tablet", "harga": 7000,  "stok": 400},
    {"nama": "Ranitidine 150mg",   "satuan": "Tablet", "harga": 6000,  "stok": 350},
    {"nama": "Ambroxol Sirup",     "satuan": "Botol",  "harga": 18000, "stok": 120},
    {"nama": "Metformin 500mg",    "satuan": "Tablet", "harga": 9000,  "stok": 180},
    {"nama": "Amlodipine 5mg",     "satuan": "Tablet", "harga": 11000, "stok": 160},
    {"nama": "Salbutamol 2mg",     "satuan": "Tablet", "harga": 6500,  "stok": 200},
    {"nama": "Dexamethasone 0.5mg","satuan": "Tablet", "harga": 4500,  "stok": 300},
]

def generate_obat():
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

# Setiap skenario: keluhan → diagnosa → tindakan → obat yang relevan
skenario_klinis = [
    {
        "keluhan":   "Demam tinggi dan sakit kepala.",
        "diagnosa":  "Febris / Demam virus",
        "tindakan":  "Pemberian antipiretik dan edukasi istirahat",
        "obat_ids":  [1],           # Paracetamol
        "aturan":    "3 x 1 tablet setelah makan",
        "tarif_layanan": 50000,
    },
    {
        "keluhan":   "Batuk berdahak dan flu berat.",
        "diagnosa":  "Acute Nasopharyngitis",
        "tindakan":  "Edukasi hidrasi dan pemberian ekspektoran",
        "obat_ids":  [4, 8],        # OBH Combi, Ambroxol
        "aturan":    "3 x 1 sendok takar sesudah makan",
        "tarif_layanan": 50000,
    },
    {
        "keluhan":   "Nyeri lambung dan mual-mual.",
        "diagnosa":  "Dispepsia / Maag Akut",
        "tindakan":  "Pemberian antasida dan edukasi pola makan",
        "obat_ids":  [2, 7],        # Antasida, Ranitidine
        "aturan":    "3 x 1 tablet kunyah sebelum makan",
        "tarif_layanan": 50000,
    },
    {
        "keluhan":   "Gatal-gatal di seluruh tubuh.",
        "diagnosa":  "Urtikaria Akut / Alergi",
        "tindakan":  "Pemberian antihistamin",
        "obat_ids":  [5],           # Cetirizine
        "aturan":    "1 x 1 tablet malam hari",
        "tarif_layanan": 50000,
    },
    {
        "keluhan":   "Pemeriksaan rutin tekanan darah.",
        "diagnosa":  "Hipertensi Esensial",
        "tindakan":  "Edukasi diet rendah garam dan pemantauan tensi",
        "obat_ids":  [10],          # Amlodipine
        "aturan":    "1 x 1 tablet pagi hari",
        "tarif_layanan": 75000,
    },
    {
        "keluhan":   "Sesak napas ringan setelah beraktivitas.",
        "diagnosa":  "Asma Bronkial Ringan",
        "tindakan":  "Edukasi pembatasan pemicu alergi",
        "obat_ids":  [11],          # Salbutamol
        "aturan":    "3 x 1 tablet setelah makan",
        "tarif_layanan": 75000,
    },
    {
        "keluhan":   "Nyeri sendi pada lutut kanan.",
        "diagnosa":  "Osteoarthritis",
        "tindakan":  "Pemberian analgetik topikal/oral",
        "obat_ids":  [6, 12],       # Ibuprofen, Dexamethasone
        "aturan":    "3 x 1 tablet setelah makan",
        "tarif_layanan": 75000,
    },
    {
        "keluhan":   "Sakit gigi berdenyut sejak 2 hari.",
        "diagnosa":  "Pulpitis / Radang Gigi",
        "tindakan":  "Rujukan ke dokter gigi setelah nyeri reda",
        "obat_ids":  [1, 3],        # Paracetamol, Amoxicillin
        "aturan":    "3 x 1 tablet setelah makan",
        "tarif_layanan": 50000,
    },
    {
        "keluhan":   "Rasa haus berlebihan, sering buang air kecil.",
        "diagnosa":  "Diabetes Mellitus Tipe 2",
        "tindakan":  "Edukasi pola makan dan olahraga rutin",
        "obat_ids":  [9],           # Metformin
        "aturan":    "2 x 1 tablet sesudah makan",
        "tarif_layanan": 100000,
    },
    {
        "keluhan":   "Batuk kering terus-menerus lebih dari seminggu.",
        "diagnosa":  "Faringitis Kronis",
        "tindakan":  "Pemberian antibiotik dan edukasi minum air putih",
        "obat_ids":  [3, 8],        # Amoxicillin, Ambroxol
        "aturan":    "3 x 1 tablet setelah makan",
        "tarif_layanan": 50000,
    },
    {
        "keluhan":   "Mual dan muntah sejak pagi, tidak bisa makan.",
        "diagnosa":  "Gastroenteritis Akut",
        "tindakan":  "Rehidrasi oral dan istirahat",
        "obat_ids":  [2],           # Antasida
        "aturan":    "3 x 1 tablet kunyah sebelum makan",
        "tarif_layanan": 50000,
    },
    {
        "keluhan":   "Pilek dan bersin-bersin setiap pagi.",
        "diagnosa":  "Rhinitis Alergi",
        "tindakan":  "Edukasi hindari alergen dan pemberian antihistamin",
        "obat_ids":  [5, 12],       # Cetirizine, Dexamethasone
        "aturan":    "1 x 1 tablet malam hari",
        "tarif_layanan": 50000,
    },
]


# ─────────────────────────────────────────────
# 5. VITAL SIGN: VARIASI PER DIAGNOSA
# ─────────────────────────────────────────────

vital_sign_pool = {
    "Febris / Demam virus":       {"tensi": "110/70", "bb_range": (50, 85), "suhu_range": (38.5, 40.0)},
    "Acute Nasopharyngitis":      {"tensi": "120/80", "bb_range": (45, 90), "suhu_range": (37.5, 38.5)},
    "Dispepsia / Maag Akut":      {"tensi": "115/75", "bb_range": (50, 80), "suhu_range": (36.5, 37.2)},
    "Urtikaria Akut / Alergi":    {"tensi": "120/80", "bb_range": (50, 85), "suhu_range": (36.5, 37.5)},
    "Hipertensi Esensial":        {"tensi": "150/95", "bb_range": (60, 100),"suhu_range": (36.5, 37.0)},
    "Asma Bronkial Ringan":       {"tensi": "125/80", "bb_range": (45, 80), "suhu_range": (36.5, 37.5)},
    "Osteoarthritis":             {"tensi": "130/85", "bb_range": (55, 95), "suhu_range": (36.5, 37.0)},
    "Pulpitis / Radang Gigi":     {"tensi": "120/80", "bb_range": (50, 85), "suhu_range": (36.8, 38.0)},
    "Diabetes Mellitus Tipe 2":   {"tensi": "135/85", "bb_range": (60, 100),"suhu_range": (36.5, 37.0)},
    "Faringitis Kronis":          {"tensi": "115/75", "bb_range": (45, 80), "suhu_range": (37.2, 38.0)},
    "Gastroenteritis Akut":       {"tensi": "100/65", "bb_range": (45, 80), "suhu_range": (37.5, 38.5)},
    "Rhinitis Alergi":            {"tensi": "120/80", "bb_range": (50, 85), "suhu_range": (36.5, 37.2)},
}

status_kunjungan_pool   = ["Menunggu", "Diperiksa", "Selesai"]
status_pembayaran_pool  = ["Belum Lunas", "Lunas"]


# ─────────────────────────────────────────────
# 6. GENERATOR UTAMA: KUNJUNGAN + TRANSAKSI
# ─────────────────────────────────────────────

def generate_kunjungan(pasien_list, dokter_list, obat_list, n_kunjungan=50):
    """
    Menghasilkan kunjungan lengkap beserta pemeriksaan, resep,
    detail resep, dan pembayaran — semuanya terkoneksi secara relasional.
    """
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

    for k in range(n_kunjungan):
        pasien   = random.choice(pasien_list)
        dokter   = random.choice(dokter_list)
        skenario = random.choice(skenario_klinis)
        diagnosa = skenario["diagnosa"]
        vital    = vital_sign_pool.get(diagnosa, {
            "tensi": "120/80", "bb_range": (50, 80), "suhu_range": (36.5, 37.5)
        })

        # Distribusi waktu: tersebar acak sepanjang tahun 2025
        offset_hari  = random.randint(0, 364)
        offset_menit = random.randint(0, 480)
        tgl_kunjungan = base_date + timedelta(days=offset_hari, minutes=offset_menit)

        # Variasi status kunjungan
        # Kunjungan terlama lebih mungkin "Selesai"
        status_kunjungan = random.choices(
            status_kunjungan_pool,
            weights=[10, 15, 75],
            k=1
        )[0]

        kunjungan_list.append({
            "id_kunjungan":       id_kunjungan,
            "id_pasien":          pasien["id_pasien"],
            "id_dokter":          dokter["id_dokter"],
            "tanggal_kunjungan":  tgl_kunjungan.isoformat(sep=" "),
            "keluhan_utama":      skenario["keluhan"],
            "status_kunjungan":   status_kunjungan,
        })

        # Pemeriksaan hanya ada jika kunjungan sudah "Diperiksa" atau "Selesai"
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

            # Resep hanya ada jika kunjungan "Selesai"
            total_biaya_obat = 0
            if status_kunjungan == "Selesai":
                tgl_resep = tgl_periksa + timedelta(minutes=random.randint(5, 20))
                resep_list.append({
                    "id_resep":        id_resep,
                    "id_pemeriksaan":  id_pemeriksaan,
                    "tanggal_resep":   tgl_resep.isoformat(sep=" "),
                })

                # Variasi jumlah obat per resep (kadang hanya 1, kadang 2)
                obat_ids = skenario["obat_ids"]
                for obat_id in obat_ids:
                    obat      = obat_by_id.get(obat_id)
                    if not obat:
                        continue
                    jumlah    = random.choice([5, 10, 15, 20, 30])
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

            # Pembayaran hanya untuk kunjungan "Selesai"
            if status_kunjungan == "Selesai":
                tarif = skenario["tarif_layanan"]
                # Variasi diskon / pembulatan
                tarif_variasi = random.choice([tarif, tarif - 10000, tarif + 25000])
                tarif_variasi = max(tarif_variasi, 0)

                status_bayar = random.choices(
                    status_pembayaran_pool,
                    weights=[20, 80],
                    k=1
                )[0]

                waktu_bayar = None
                if status_bayar == "Lunas":
                    waktu_bayar = (tgl_periksa + timedelta(
                        minutes=random.randint(5, 30)
                    )).isoformat(sep=" ")

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

def generate_dataset(n_pasien=5_000, n_kunjungan=200_000, seed=42):
    random.seed(seed)

    pasien_list  = generate_pasien(n_pasien)
    dokter_list  = generate_dokter()
    obat_list    = generate_obat()
    transaksi    = generate_kunjungan(pasien_list, dokter_list, obat_list, n_kunjungan)

    return {
        # Master data
        "pasien":       pasien_list,
        "dokter":       dokter_list,
        "obat":         obat_list,
        # Transaksi
        "kunjungan":    transaksi["kunjungan"],
        "pemeriksaan":  transaksi["pemeriksaan"],
        "resep":        transaksi["resep"],
        "detail_resep": transaksi["detail_resep"],
        "pembayaran":   transaksi["pembayaran"],
    }


# ─────────────────────────────────────────────
# 8. SQL EXPORT (streaming, tidak load semua ke RAM)
# ─────────────────────────────────────────────

BATCH_SIZE = 5_000   # rows per INSERT statement
OUT_FILE   = "klinik_seed.sql"


def esc(s):
    """Escape single-quote untuk string PostgreSQL."""
    return str(s).replace("'", "''")


def write_insert(f, table, cols, rows):
    """Tulis satu blok INSERT ... VALUES ke file."""
    if not rows:
        return
    f.write(f"INSERT INTO {table} ({cols}) VALUES\n")
    for i, row in enumerate(rows):
        sep = ";" if i == len(rows) - 1 else ","
        f.write(f"  {row}{sep}\n")
    f.write("\n")


def export_to_sql(dataset, out_file=OUT_FILE):
    from collections import Counter
    stats = Counter()

    with open(out_file, "w", encoding="utf-8") as f:
        # ── Header ──
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
        batch = []
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
        rows = []
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

        # ── Transaksi: streaming per batch ──
        tables = [
            ("kunjungan",
             "id_kunjungan,id_pasien,id_dokter,tanggal_kunjungan,keluhan_utama,status_kunjungan",
             lambda r: (f"({r['id_kunjungan']},{r['id_pasien']},{r['id_dokter']},"
                        f"'{r['tanggal_kunjungan']}','{esc(r['keluhan_utama'])}',"
                        f"'{r['status_kunjungan']}')")),
            ("pemeriksaan",
             "id_pemeriksaan,id_kunjungan,tanggal_periksa,tensi_darah,berat_badan,suhu_tubuh,diagnosa,tindakan_medis",
             lambda r: (f"({r['id_pemeriksaan']},{r['id_kunjungan']},'{r['tanggal_periksa']}',"
                        f"'{r['tensi_darah']}',{r['berat_badan']},{r['suhu_tubuh']},"
                        f"'{esc(r['diagnosa'])}','{esc(r['tindakan_medis'])}')")),
            ("resep",
             "id_resep,id_pemeriksaan,tanggal_resep",
             lambda r: f"({r['id_resep']},{r['id_pemeriksaan']},'{r['tanggal_resep']}')"),
            ("detail_resep",
             "id_detail_resep,id_resep,id_obat,jumlah,aturan_pakai",
             lambda r: (f"({r['id_detail_resep']},{r['id_resep']},{r['id_obat']},"
                        f"{r['jumlah']},'{esc(r['aturan_pakai'])}')")),
            ("pembayaran",
             "id_pembayaran,id_kunjungan,total_biaya_layanan,total_biaya_obat,status_pembayaran,waktu_pembayaran",
             lambda r: (f"({r['id_pembayaran']},{r['id_kunjungan']},"
                        f"{r['total_biaya_layanan']},{r['total_biaya_obat']},"
                        f"'{r['status_pembayaran']}',"
                        f"{'NULL' if r['waktu_pembayaran'] is None else chr(39)+r['waktu_pembayaran']+chr(39)})")),
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
            ("pasien_id_pasien_seq",                  len(dataset["pasien"])),
            ("dokter_id_dokter_seq",                  len(dataset["dokter"])),
            ("obat_id_obat_seq",                      len(dataset["obat"])),
            ("kunjungan_id_kunjungan_seq",             stats["kunjungan"]),
            ("pemeriksaan_id_pemeriksaan_seq",         stats["pemeriksaan"]),
            ("resep_id_resep_seq",                     stats["resep"]),
            ("detail_resep_id_detail_resep_seq",       stats["detail_resep"]),
            ("pembayaran_id_pembayaran_seq",           stats["pembayaran"]),
        ]
        for seq, val in seq_map:
            f.write(f"SELECT setval('{seq}', {val});\n")

        f.write("\nSET session_replication_role = DEFAULT;\n")
        f.write("COMMIT;\n")

    return stats


# ─────────────────────────────────────────────
# 9. JALANKAN & RINGKASAN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    from collections import Counter
    import os

    print("Generating dataset (5.000 pasien, 200.000 kunjungan)...", flush=True)
    dataset = generate_dataset(n_pasien=5_000, n_kunjungan=200_000)

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
