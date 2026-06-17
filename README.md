Optimasi Query 1: Mencari riwayat kunjungan atas nama tertentu (misal: 'Siti Rahayu')

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

Optimasi Query 3: Mencari data kunjungan ke dokter tertentu (misal: 'dr. Faris Hakim')

Sebelum Indexing
```
explain analyze select * from kunjungan 
where id_dokter = (select id_dokter from dokter where nama_dokter = 'dr. Faris Hakim')
```
<img width="779" height="507" alt="image" src="https://github.com/user-attachments/assets/eb9c4921-e7da-4c81-b5c6-b4c27c1696b7" />

Indexing id_dokter dengan cara
```
CREATE INDEX idx_kunjungan_dokter
ON kunjungan(id_dokter);
```

Setelah Indexing
```
explain analyze select * from kunjungan 
where id_dokter = (select id_dokter from dokter where nama_dokter = 'dr. Faris Hakim')
```
<img width="878" height="597" alt="image" src="https://github.com/user-attachments/assets/8f551974-a782-48f2-8140-6b521a7dfac8" />

