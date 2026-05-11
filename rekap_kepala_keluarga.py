#!/usr/bin/env python3
# Script untuk membuat rekap data warga berdasarkan kepala keluarga

import json
import re
from collections import defaultdict

def rekap_kepala_keluarga():
    # Baca file data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Kelompokkan data berdasarkan No KK
    keluarga_dict = defaultdict(list)
    
    for warga in data:
        no_kk = warga.get('noKK')
        if no_kk:
            keluarga_dict[no_kk].append(warga)
    
    print(f"Total Kartu Keluarga: {len(keluarga_dict)}")
    print(f"Total Warga: {len(data)}")
    print("=" * 120)
    
    # Urutkan berdasarkan No KK
    sorted_keluarga = sorted(keluarga_dict.items(), key=lambda x: x[0])
    
    # Cari kepala keluarga untuk setiap KK
    rekap_keluarga = []
    
    for no_kk, anggota in sorted_keluarga:
        # Cari kepala keluarga (kedudukan = "Kepala Keluarga")
        kepala_keluarga = None
        for warga in anggota:
            if warga.get('kedudukan') == 'Kepala Keluarga':
                kepala_keluarga = warga
                break
        
        # Jika tidak ditemukan kepala keluarga, ambil yang pertama
        if not kepala_keluarga and anggota:
            kepala_keluarga = anggota[0]
        
        if kepala_keluarga:
            rekap_keluarga.append({
                'no_kk': no_kk,
                'kepala_keluarga': kepala_keluarga.get('nama', 'Tidak diketahui'),
                'nik_kepala': kepala_keluarga.get('nik', ''),
                'alamat': kepala_keluarga.get('alamat', 'Tidak diketahui'),
                'status_alamat': kepala_keluarga.get('statusAlamat', 'Tidak diketahui'),
                'jumlah_anggota': len(anggota),
                'anggota': anggota
            })
    
    # Tampilkan rekap
    total_anggota = 0
    
    for i, keluarga in enumerate(rekap_keluarga, 1):
        print(f"{i}. No KK: {keluarga['no_kk']}")
        print(f"   Kepala Keluarga: {keluarga['kepala_keluarga']}")
        print(f"   NIK Kepala: {keluarga['nik_kepala']}")
        print(f"   Alamat: {keluarga['alamat']}")
        print(f"   Status Alamat: {keluarga['status_alamat']}")
        print(f"   Jumlah Anggota: {keluarga['jumlah_anggota']} orang")
        
        # Tampilkan detail anggota
        print("   Anggota Keluarga:")
        for j, anggota in enumerate(keluarga['anggota'], 1):
            kedudukan = anggota.get('kedudukan', 'Tidak diketahui')
            if not kedudukan:
                kedudukan = 'Tidak diketahui'
                
            print(f"     {j}. {anggota.get('nama', 'N/A')} ({anggota.get('jenisKelamin', 'N/A')}, {anggota.get('usia', 'N/A')} th) - {kedudukan}")
        
        total_anggota += keluarga['jumlah_anggota']
        print("-" * 80)
    
    # Statistik
    print("\n" + "=" * 120)
    print("STATISTIK KEPALA KELUARGA")
    print("=" * 120)
    
    # Hitung berdasarkan jenis kelamin kepala keluarga
    jenis_kelamin_count = {'L': 0, 'P': 0, 'Tidak diketahui': 0}
    for keluarga in rekap_keluarga:
        for anggota in keluarga['anggota']:
            if anggota.get('nama') == keluarga['kepala_keluarga']:
                jk = anggota.get('jenisKelamin')
                if jk in ['L', 'P']:
                    jenis_kelamin_count[jk] += 1
                else:
                    jenis_kelamin_count['Tidak diketahui'] += 1
                break
    
    print(f"\nJenis Kelamin Kepala Keluarga:")
    print(f"  Laki-laki: {jenis_kelamin_count['L']} KK ({jenis_kelamin_count['L']/len(rekap_keluarga)*100:.1f}%)")
    print(f"  Perempuan: {jenis_kelamin_count['P']} KK ({jenis_kelamin_count['P']/len(rekap_keluarga)*100:.1f}%)")
    if jenis_kelamin_count['Tidak diketahui'] > 0:
        print(f"  Tidak diketahui: {jenis_kelamin_count['Tidak diketahui']} KK")
    
    # Hitung rata-rata anggota per keluarga
    rata_anggota = total_anggota / len(rekap_keluarga) if rekap_keluarga else 0
    print(f"\nRata-rata anggota per keluarga: {rata_anggota:.1f} orang")
    
    # Distribusi jumlah anggota
    distribusi_anggota = defaultdict(int)
    for keluarga in rekap_keluarga:
        distribusi_anggota[keluarga['jumlah_anggota']] += 1
    
    print("\nDistribusi Jumlah Anggota Keluarga:")
    for jumlah, count in sorted(distribusi_anggota.items()):
        print(f"  {jumlah} orang: {count} KK ({count/len(rekap_keluarga)*100:.1f}%)")
    
    # Status alamat
    status_count = defaultdict(int)
    for keluarga in rekap_keluarga:
        status = keluarga['status_alamat']
        status_count[status] += 1
    
    print("\nStatus Alamat Keluarga:")
    for status, count in sorted(status_count.items()):
        print(f"  {status}: {count} KK ({count/len(rekap_keluarga)*100:.1f}%)")
    
    # Simpan ke file JSON
    output_file = 'rekap_kepala_keluarga.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rekap_keluarga, f, indent=2, ensure_ascii=False)
    
    print(f"\nData telah disimpan ke: {output_file}")
    
    # Buat file CSV
    csv_file = 'rekap_kepala_keluarga.csv'
    with open(csv_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("No,No KK,Nama Kepala Keluarga,NIK Kepala,Alamat,Status Alamat,Jumlah Anggota,Anggota Detail\n")
        
        # Data
        for i, keluarga in enumerate(rekap_keluarga, 1):
            anggota_detail = []
            for anggota in keluarga['anggota']:
                nama = anggota.get('nama', '')
                jk = anggota.get('jenisKelamin', '')
                usia = anggota.get('usia', '')
                kedudukan = anggota.get('kedudukan', '')
                if not kedudukan:
                    kedudukan = 'Tidak diketahui'
                
                anggota_detail.append(f"{nama} ({jk}, {usia} th) - {kedudukan}")
            
            anggota_str = " | ".join(anggota_detail)
            
            f.write(f"{i},{keluarga['no_kk']},{keluarga['kepala_keluarga']},{keluarga['nik_kepala']},{keluarga['alamat']},{keluarga['status_alamat']},{keluarga['jumlah_anggota']},\"{anggota_str}\"\n")
    
    print(f"Data CSV telah disimpan ke: {csv_file}")
    
    # Buat file ringkasan
    ringkasan_file = 'ringkasan_kepala_keluarga.txt'
    with open(ringkasan_file, 'w', encoding='utf-8') as f:
        f.write("RINGKASAN DATA KEPALA KELUARGA RT 04/RW 11\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total Kartu Keluarga: {len(rekap_keluarga)}\n")
        f.write(f"Total Warga: {total_anggota}\n")
        f.write(f"Rata-rata anggota per keluarga: {rata_anggota:.1f} orang\n\n")
        
        f.write("STATISTIK:\n")
        f.write(f"Kepala Keluarga Laki-laki: {jenis_kelamin_count['L']} KK\n")
        f.write(f"Kepala Keluarga Perempuan: {jenis_kelamin_count['P']} KK\n\n")
        
        f.write("Distribusi Jumlah Anggota:\n")
        for jumlah, count in sorted(distribusi_anggota.items()):
            f.write(f"  {jumlah} orang: {count} KK\n")
        
        f.write("\nStatus Alamat:\n")
        for status, count in sorted(status_count.items()):
            f.write(f"  {status}: {count} KK\n")
    
    print(f"Ringkasan telah disimpan ke: {ringkasan_file}")
    
    return rekap_keluarga

if __name__ == "__main__":
    rekap_kepala_keluarga()