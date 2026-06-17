Optimasi Query 1

Mencari kunjungan atas nama tertentu (misal: 'Siti Rahayu')

Sebelum Indexing
```
explain analyze SELECT *
FROM kunjungan
WHERE id_pasien = (select id_pasien from pasien where nama_pasien = 'Siti Rahayu');
```
<img width="792" height="538" alt="image" src="https://github.com/user-attachments/assets/0b9714c0-6e08-4252-90d3-34ada04473a0" />

Indexing id_pasien dengan cara
```
CREATE INDEX idx_kunjungan_pasien
ON kunjungan(id_pasien);
```

Setelah Indexing
```
explain analyze SELECT *
FROM kunjungan
WHERE id_pasien = (select id_pasien from pasien where nama_pasien = 'Siti Rahayu');
```
<img width="847" height="551" alt="image" src="https://github.com/user-attachments/assets/661deb2c-6b2f-4226-ac29-4c0e86f4c808" />
