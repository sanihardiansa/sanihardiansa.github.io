# Panduan Setup Google Forms + WA Notifikasi RT04

## Alur Sistem
```
Warga isi Google Form
       ↓
Data masuk Google Spreadsheet
       ↓
Apps Script trigger otomatis
       ↓
Email + WA link ke pengurus RT
       ↓
Pengurus klik → WA terbuka dengan pesan terisi
       ↓
Pengurus buka aplikasi RT04 → input NIK → generate surat
```

---

## LANGKAH 1 — Buat Google Form

1. Buka https://forms.google.com → klik **+ Blank**
2. Judul form: `Permohonan Surat RT 04/RW 11 - Kel. Jatihandap`
3. Tambahkan pertanyaan berikut (urutan HARUS sama):

| No | Pertanyaan | Tipe | Wajib |
|----|-----------|------|-------|
| 1 | Nama Lengkap | Short answer | ✅ |
| 2 | NIK (16 digit) | Short answer | ✅ |
| 3 | Nomor WhatsApp | Short answer | ✅ |
| 4 | Jenis Surat | Dropdown | ✅ |
| 5 | Tujuan Pembuatan Surat | Short answer | ✅ |
| 6 | Keterangan Tambahan | Paragraph | ❌ |

4. Untuk **Jenis Surat** (dropdown), isi pilihan:
   - Surat Keterangan Domisili
   - Surat Keterangan Tidak Mampu
   - Surat Pengantar KTP
   - Surat Pengantar KK
   - Surat Keterangan Usaha
   - Surat Keterangan Kelahiran
   - Surat Keterangan Kematian
   - Lainnya

5. Klik ikon **Settings** (⚙️) → aktifkan:
   - "Collect email addresses" → OFF (agar warga tidak perlu login)
   - "Limit to 1 response" → OFF

---

## LANGKAH 2 — Hubungkan Form ke Spreadsheet

1. Di Google Form, klik tab **Responses**
2. Klik ikon **Google Sheets** (hijau)
3. Pilih **Create a new spreadsheet**
4. Nama: `Data Permohonan Surat RT04`
5. Klik **Create**

---

## LANGKAH 3 — Setup Apps Script

1. Di Google Spreadsheet yang baru dibuat, klik menu **Extensions → Apps Script**
2. Hapus semua kode yang ada
3. Copy-paste seluruh isi file `notifikasi-wa.gs`
4. **Edit konfigurasi** di bagian `CONFIG`:
   ```javascript
   NOMOR_WA_RT: '6281234567890',  // Ganti dengan nomor WA pengurus RT
   ```
5. Klik **Save** (Ctrl+S), beri nama project: `RT04 WA Notifikasi`

---

## LANGKAH 4 — Set Trigger

1. Di Apps Script, klik ikon **Triggers** (jam alarm) di sidebar kiri
2. Klik **+ Add Trigger** (pojok kanan bawah)
3. Isi pengaturan:
   - Function: `onFormSubmit`
   - Event source: `From spreadsheet`
   - Event type: `On form submit`
4. Klik **Save**
5. Akan muncul popup izin → klik **Allow**

---

## LANGKAH 5 — Test

1. Di Apps Script, pilih function `testNotifikasi`
2. Klik **Run** (▶️)
3. Cek email pengurus RT — harus ada email dengan tombol "Buka di WhatsApp"
4. Klik tombol → WA terbuka dengan pesan terisi otomatis

---

## LANGKAH 6 — Bagikan Form ke Warga

1. Di Google Form, klik tombol **Send**
2. Salin link form
3. Bagikan via WA group RT:
   ```
   📋 *Form Permohonan Surat RT 04/RW 11*
   
   Untuk mengajukan permohonan surat, silakan isi form berikut:
   [LINK FORM]
   
   Surat akan diproses dalam 1x24 jam.
   ```
4. Bisa juga buat QR code dari link form di https://qr-code-generator.com

---

## Cara Kerja Setelah Setup

1. **Warga** isi Google Form dari HP
2. **Pengurus RT** terima email otomatis berisi data pemohon + tombol WA
3. **Pengurus** klik tombol → WA terbuka, pesan sudah terisi → tinggal Send
4. **Pengurus** buka aplikasi RT04 → input NIK → generate & cetak surat
5. Di spreadsheet ada kolom **"Kirim Konfirmasi"** → klik untuk balas WA ke pemohon

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Email tidak masuk | Cek folder Spam, pastikan trigger sudah aktif |
| Error "Authorization required" | Jalankan `testNotifikasi` manual dulu untuk grant permission |
| Nomor kolom tidak sesuai | Sesuaikan `COL_*` di CONFIG dengan urutan pertanyaan form |
