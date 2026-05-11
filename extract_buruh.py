#!/usr/bin/env python3
# Script untuk mengekstrak data warga yang bekerja sebagai buruh

import json
import re

def extract_buruh_workers():
    # Baca file data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter warga dengan pekerjaan mengandung kata "buruh" (case-insensitive)
    buruh_workers = []
    
    for warga in data:
        pekerjaan = warga.get('pekerjaan')
        if pekerjaan:
            pekerjaan_lower = str(pekerjaan).lower()
        else:
            pekerjaan_lower = ''
        
        # Cek jika pekerjaan mengandung kata "buruh"
        if 'buruh' in pekerjaan_lower:
            buruh_workers.append(warga)
    
    # Urutkan berdasarkan nomor
    buruh_workers.sort(key=lambda x: x.get('no', 0))
    
    # Tampilkan hasil
    print(f"Total warga yang bekerja sebagai buruh: {len(buruh_workers)}")
    print("=" * 100)
    
    for i, warga in enumerate(buruh_workers, 1):
        print(f"{i}. No: {warga.get('no', 'N/A')}")
        print(f"   Nama: {warga.get('nama', 'N/A')}")
        print(f"   Jenis Kelamin: {warga.get('jenisKelamin', 'N/A')}")
        print(f"   Usia: {warga.get('usia', 'N/A')}")
        print(f"   Pekerjaan: {warga.get('pekerjaan', 'N/A')}")
        print(f"   Alamat: {warga.get('alamat', 'N/A')}")
        print(f"   NIK: {warga.get('nik', 'N/A')}")
        print(f"   No KK: {warga.get('noKK', 'N/A')}")
        print(f"   Pendidikan: {warga.get('pendidikan', 'N/A')}")
        print(f"   Status Alamat: {warga.get('statusAlamat', 'N/A')}")
        print("-" * 50)
    
    # Buat ringkasan statistik
    print("\n" + "=" * 100)
    print("RINGKASAN STATISTIK:")
    print("=" * 100)
    
    # Hitung berdasarkan jenis kelamin
    laki_laki = sum(1 for w in buruh_workers if w.get('jenisKelamin') == 'L')
    perempuan = sum(1 for w in buruh_workers if w.get('jenisKelamin') == 'P')
    print(f"Laki-laki: {laki_laki} orang")
    print(f"Perempuan: {perempuan} orang")
    
    # Hitung berdasarkan jenis buruh
    jenis_buruh = {}
    for w in buruh_workers:
        pekerjaan = w.get('pekerjaan', '')
        if pekerjaan:
            pekerjaan_lower = str(pekerjaan).lower()
        else:
            pekerjaan_lower = ''
            
        if 'harian lepas' in pekerjaan_lower:
            jenis = 'Buruh Harian Lepas'
        elif 'harian' in pekerjaan_lower:
            jenis = 'Buruh Harian'
        else:
            jenis = 'Buruh'
        
        jenis_buruh[jenis] = jenis_buruh.get(jenis, 0) + 1
    
    print("\nJenis Pekerjaan Buruh:")
    for jenis, jumlah in jenis_buruh.items():
        print(f"  {jenis}: {jumlah} orang")
    
    # Hitung rata-rata usia
    usia_list = [w.get('usia', 0) for w in buruh_workers if w.get('usia')]
    if usia_list:
        rata_rata_usia = sum(usia_list) / len(usia_list)
        print(f"\nRata-rata usia: {rata_rata_usia:.1f} tahun")
        print(f"Usia termuda: {min(usia_list)} tahun")
        print(f"Usia tertua: {max(usia_list)} tahun")
    
    # Hitung berdasarkan pendidikan
    pendidikan_count = {}
    for w in buruh_workers:
        pendidikan = w.get('pendidikan', 'Tidak diketahui')
        pendidikan_count[pendidikan] = pendidikan_count.get(pendidikan, 0) + 1
    
    print("\nTingkat Pendidikan:")
    for pendidikan, jumlah in sorted(pendidikan_count.items()):
        print(f"  {pendidikan}: {jumlah} orang")
    
    # Hitung berdasarkan status alamat
    status_count = {}
    for w in buruh_workers:
        status = w.get('statusAlamat', 'Tidak diketahui')
        status_count[status] = status_count.get(status, 0) + 1
    
    print("\nStatus Alamat:")
    for status, jumlah in sorted(status_count.items()):
        print(f"  {status}: {jumlah} orang")
    
    # Simpan ke file JSON
    output_file = 'warga_buruh.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(buruh_workers, f, indent=2, ensure_ascii=False)
    
    print(f"\nData telah disimpan ke: {output_file}")
    
    # Buat file CSV juga
    csv_file = 'warga_buruh.csv'
    with open(csv_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("No,Nama,Jenis Kelamin,Usia,Pekerjaan,Alamat,NIK,No KK,Pendidikan,Status Alamat\n")
        
        # Data
        for w in buruh_workers:
            no = str(w.get('no', ''))
            nama = w.get('nama', '').replace(',', ' ')
            jenis_kelamin = w.get('jenisKelamin', '')
            usia = str(w.get('usia', ''))
            pekerjaan = w.get('pekerjaan', '').replace(',', ' ')
            alamat = str(w.get('alamat', '')).replace(',', ' ')
            nik = w.get('nik', '')
            no_kk = w.get('noKK', '')
            pendidikan = w.get('pendidikan', '').replace(',', ' ')
            status_alamat = w.get('statusAlamat', '')
            
            f.write(f"{no},{nama},{jenis_kelamin},{usia},{pekerjaan},{alamat},{nik},{no_kk},{pendidikan},{status_alamat}\n")
    
    print(f"Data CSV telah disimpan ke: {csv_file}")

if __name__ == "__main__":
    extract_buruh_workers()