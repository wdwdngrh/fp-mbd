QUERY1
```
SELECT 
    p.nama_pasien,
    p.nomor_rm,
    k.tanggal_kunjungan,
    k.keluhan_utama,
    pm.diagnosa,
    pm.tindakan_medis,
    pm.tensi_darah,
    pm.berat_badan
FROM pasien p
JOIN kunjungan k ON p.id_pasien = k.id_pasien
JOIN pemeriksaan pm ON k.id_kunjungan = pm.id_kunjungan
WHERE p.nomor_rm = 'RM-00123'
ORDER BY k.tanggal_kunjungan DESC;
```

```
CREATE INDEX idx_pemeriksaan_id_kunjungan 
ON pemeriksaan(id_kunjungan);
```

QUERY2

```
SELECT 
    o.nama_obat,
    o.kode_obat,
    SUM(dr.jumlah) AS total_penggunaan,
    SUM(dr.jumlah * o.harga_jual) AS total_pendapatan
FROM detail_resep dr
JOIN obat o ON dr.id_obat = o.id_obat
GROUP BY o.id_obat, o.nama_obat, o.kode_obat
ORDER BY total_pendapatan DESC;
```

```
CREATE INDEX idx_detail_resep_id_obat 
ON detail_resep(id_obat);
```

```
CREATE INDEX idx_resep_id_pemeriksaan 
ON resep(id_pemeriksaan);
```

```
SELECT 
    o.nama_obat,
    SUM(dr.jumlah) AS total_qty
FROM detail_resep dr
JOIN resep r ON dr.id_resep = r.id_resep
JOIN obat o ON dr.id_obat = o.id_obat
WHERE r.id_pemeriksaan = 45
GROUP BY o.nama_obat;
```

QUERY3
```
SELECT 
    DATE_TRUNC('day', waktu_pembayaran) AS tanggal,
    SUM(total_keseluruhan) AS total_pendapatan,
    COUNT(*) AS jumlah_transaksi
FROM pembayaran
WHERE status_pembayaran = 'Lunas'
  AND waktu_pembayaran BETWEEN '2026-06-01' AND '2026-06-30'
GROUP BY DATE_TRUNC('day', waktu_pembayaran)
ORDER BY tanggal;
```

```
CREATE INDEX idx_pembayaran_waktu 
ON pembayaran(waktu_pembayaran);
```

```
CREATE INDEX idx_pembayaran_status_waktu 
ON pembayaran(status_pembayaran, waktu_pembayaran);
```
