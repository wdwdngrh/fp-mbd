-- PostgreSQL DDL Script untuk Sistem Basis Data Klinik Pribadi

-- =========================================================================
-- 1. TABEL DATA MASTER
-- =========================================================================

-- Tabel Pasien
CREATE TABLE pasien (
    id_pasien SERIAL PRIMARY KEY,
    nomor_rm VARCHAR(15) UNIQUE NOT NULL, -- Nomor Rekam Medis (unik)
    nama_pasien VARCHAR(100) NOT NULL,
    nik CHAR(16) UNIQUE,
    jenis_kelamin CHAR(1) CHECK (jenis_kelamin IN ('L', 'P')) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    alamat TEXT,
    no_telepon VARCHAR(15),
    tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Obat
CREATE TABLE obat (
    id_obat SERIAL PRIMARY KEY,
    kode_obat VARCHAR(10) UNIQUE NOT NULL,
    nama_obat VARCHAR(100) NOT NULL,
    satuan VARCHAR(20) NOT NULL, -- contoh: Tablet, Botol, Kapsul
    harga_jual NUMERIC(12, 2) NOT NULL CHECK (harga_jual >= 0),
    stok_obat INT NOT NULL DEFAULT 0 CHECK (stok_obat >= 0)
);

-- =========================================================================
-- TAMBAHAN: TABEL DOKTER (Data Master)
-- =========================================================================

CREATE TABLE dokter (
    id_dokter     SERIAL PRIMARY KEY,
    kode_dokter   VARCHAR(10)  UNIQUE NOT NULL,
    nama_dokter   VARCHAR(100) NOT NULL,
    spesialisasi  VARCHAR(100) NOT NULL DEFAULT 'Umum',
    no_sip        VARCHAR(30)  UNIQUE NOT NULL, -- Nomor Surat Izin Praktik
    no_telepon    VARCHAR(15),
    aktif         BOOLEAN      NOT NULL DEFAULT TRUE
);

-- =========================================================================
-- RELASI: Tambah kolom id_dokter ke tabel kunjungan
-- =========================================================================

ALTER TABLE kunjungan
    ADD COLUMN id_dokter INT REFERENCES dokter(id_dokter) ON DELETE RESTRICT;

-- =========================================================================
-- 2. TABEL PELAYANAN & REKAM MEDIS
-- =========================================================================

-- Tabel Kunjungan (Menampung antrean/pendaftaran pasien saat datang)
CREATE TABLE kunjungan (
    id_kunjungan SERIAL PRIMARY KEY,
    id_pasien INT REFERENCES pasien(id_pasien) ON DELETE RESTRICT,
    tanggal_kunjungan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    keluhan_utama TEXT NOT NULL,
    status_kunjungan VARCHAR(20) DEFAULT 'Menunggu' -- Menunggu, Diperiksa, Selesai
);

-- Tabel Pemeriksaan / Rekam Medis
CREATE TABLE pemeriksaan (
    id_pemeriksaan SERIAL PRIMARY KEY,
    id_kunjungan INT UNIQUE REFERENCES kunjungan(id_kunjungan) ON DELETE RESTRICT,
    tanggal_periksa TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tensi_darah VARCHAR(10), -- contoh: 120/80
    berat_badan NUMERIC(5,2),
    suhu_tubuh NUMERIC(4,1),
    diagnosa TEXT NOT NULL,
    tindakan_medis TEXT
);

-- =========================================================================
-- 3. TABEL RESEP & OBAT
-- =========================================================================

-- Tabel Resep (Header)
CREATE TABLE resep (
    id_resep SERIAL PRIMARY KEY,
    id_pemeriksaan INT UNIQUE REFERENCES pemeriksaan(id_pemeriksaan) ON DELETE RESTRICT,
    tanggal_resep TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Detail Resep (Menampung banyak obat dalam satu resep)
CREATE TABLE detail_resep (
    id_detail_resep SERIAL PRIMARY KEY,
    id_resep INT REFERENCES resep(id_resep) ON DELETE CASCADE,
    id_obat INT REFERENCES obat(id_obat) ON DELETE RESTRICT,
    jumlah INT NOT NULL CHECK (jumlah > 0),
    aturan_pakai VARCHAR(100) NOT NULL -- contoh: 3x1 sehari setelah makan
);

-- =========================================================================
-- 4. TABEL TRANSAKSI & PEMBAYARAN
-- =========================================================================

-- Tabel Pembayaran
CREATE TABLE pembayaran (
    id_pembayaran SERIAL PRIMARY KEY,
    id_kunjungan INT UNIQUE REFERENCES kunjungan(id_kunjungan) ON DELETE RESTRICT,
    total_biaya_layanan NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (total_biaya_layanan >= 0),
    total_biaya_obat NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (total_biaya_obat >= 0),
    total_keseluruhan NUMERIC(12, 2) GENERATED ALWAYS AS (total_biaya_layanan + total_biaya_obat) STORED,
    status_pembayaran VARCHAR(20) DEFAULT 'Belum Lunas' CHECK (status_pembayaran IN ('Belum Lunas', 'Lunas')),
    waktu_pembayaran TIMESTAMP
);

