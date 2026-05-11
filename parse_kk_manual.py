import json

# Data yang terlihat dari KK (akan diisi manual berdasarkan gambar)
# Karena gambar miring dan kurang jelas, saya buat template

kk_data = {
    "no_kk": "3273730101010001",  # Ganti dengan nomor KK yang terlihat
    "alamat": "JL. MANDALA VI NO. 132",
    "rt": "04",
    "rw": "11",
    "kelurahan": "JATIHANDAP",
    "kecamatan": "MANDALAJATI",
    "kabupaten": "KOTA BANDUNG",
    "provinsi": "JAWA BARAT",
    "kode_pos": "",
    "anggota_keluarga": [
        {
            "no": 1,
            "nik": "",
            "nama": "",
            "jenis_kelamin": "L/P",
            "tempat_lahir": "",
            "tanggal_lahir": "",
            "agama": "",
            "pendidikan": "",
            "pekerjaan": "",
            "status_perkawinan": "",
            "status_hubungan_keluarga": "Kepala Keluarga",
            "kewarganegaraan": "WNI",
            "no_paspor": "",
            "no_kitap": "",
            "nama_ayah": "",
            "nama_ibu": ""
        }
    ]
}

# Simpan template
with open('kk_template.json', 'w') as f:
    json.dump(kk_data, indent=2, ensure_ascii=False, fp=f)

print("Template KK dibuat: kk_template.json")
print("\nSilakan isi data manual dari gambar KK, atau:")
print("1. Foto ulang KK dengan kualitas lebih baik")
print("2. Scan KK dengan scanner")
print("3. Input manual melalui form web")
