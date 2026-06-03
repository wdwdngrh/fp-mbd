-- 1. Membuat Tipe Data ENUM (Kustom) untuk Kolom Pilihan
CREATE TYPE jenis_kelamin_enum AS ENUM ('L', 'P');
CREATE TYPE status_pengajuan_enum AS ENUM ('Pending', 'Proses', 'Selesai', 'Ditolak');
CREATE TYPE status_pengaduan_enum AS ENUM ('Baru', 'Diproses', 'Selesai');

-- 2. Membuat Tabel Master Warga
CREATE TABLE tabel_warga (
    nik VARCHAR(16) PRIMARY KEY,
    no_kk VARCHAR(16) NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    tempat_lahir VARCHAR(50) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    jenis_kelamin jenis_kelamin_enum NOT NULL,
    alamat TEXT NOT NULL,
    pendidikan_terakhir VARCHAR(30),
    pekerjaan VARCHAR(50),
    status_ekonomi VARCHAR(20) DEFAULT 'Mampu'
);

-- 3. Membuat Tabel Master Jenis Surat
CREATE TABLE tabel_jenis_surat (
    id_jenis_surat SERIAL PRIMARY KEY,
    nama_surat VARCHAR(50) NOT NULL UNIQUE,
    syarat_dokumen TEXT
);

-- 4. Membuat Tabel Transaksi Permohonanan Surat
CREATE TABLE tabel_permohonan_surat (
    no_permohonan VARCHAR(20) PRIMARY KEY,
    nik VARCHAR(16) NOT NULL,
    id_jenis_surat INT NOT NULL,
    tanggal_pengajuan DATE DEFAULT CURRENT_DATE,
    status_pengajuan status_pengajuan_enum DEFAULT 'Pending',
    keterangan TEXT,
    
    -- Hubungan Foreign Key
    CONSTRAINT fk_permohonan_warga 
        FOREIGN KEY (nik) 
        REFERENCES tabel_warga(nik) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
        
    CONSTRAINT fk_permohonan_jenis 
        FOREIGN KEY (id_jenis_surat) 
        REFERENCES tabel_jenis_surat(id_jenis_surat) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 5. Membuat Tabel Transaksi Pengaduan Masyarakat
CREATE TABLE tabel_pengaduan (
    id_pengaduan SERIAL PRIMARY KEY,
    nik VARCHAR(16) NOT NULL,
    tanggal_pengaduan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    isi_pengaduan TEXT NOT NULL,
    kategori VARCHAR(50) NOT NULL,
    status_tindak_lanjut status_pengaduan_enum DEFAULT 'Baru',
    
    -- Hubungan Foreign Key
    CONSTRAINT fk_pengaduan_warga 
        FOREIGN KEY (nik) 
        REFERENCES tabel_warga(nik) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);
