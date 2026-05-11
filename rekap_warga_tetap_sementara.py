#!/usr/bin/env python3
# Script untuk rekap data warga dengan status alamat 'tetap' atau 'sementara'
# dan keterangan tidak sama dengan 'meninggal'

import json
import re
from collections import defaultdict

def rekap_warga_tetap_sementara():
    # Baca file data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter warga berdasarkan kriteria:
    # 1. Status alamat = 'TETAP' atau 'SEMENTARA' (case-insensitive)
    # 2. Keterangan tidak mengandung kata 'meninggal' (case-insensitive)
    # 3. Berperan sebagai kartu keluarga (memiliki No KK)
    
    warga_filtered = []
    
    for warga in data:
        status_alamat = str(warga.get('statusAlamat', '')).upper()
        keterangan = str(warga.get('keterangan', '')).lower()
        no_kk = warga.get('noKK')
        
        # Cek kriteria
        if (status_alamat in ['TETAP', 'SEMENTARA'] and 
            'meninggal' not in keterangan and
            no_kk and no_kk != '-' and no_kk != 'None'):
            warga_filtered.append(warga)
    
    print(f"Total data warga: {len(data)}")
    print(f"Warga yang memenuhi kriteria: {len(warga_filtered)}")
    print("=" * 120)
    
    # Kelompokkan berdasarkan No KK
    keluarga_dict = defaultdict(list)
    
    for warga in warga_filtered:
        no_kk = warga.get('noKK')
        if no_kk:
            keluarga_dict[no_kk].append(warga)
    
    print(f"Total Kartu Keluarga yang memenuhi kriteria: {len(keluarga_dict)}")
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
            # Hitung statistik untuk keluarga ini
            jumlah_laki = sum(1 for w in anggota if w.get('jenisKelamin') == 'L')
            jumlah_perempuan = sum(1 for w in anggota if w.get('jenisKelamin') == 'P')
            usia_list = [w.get('usia', 0) for w in anggota if w.get('usia')]
            rata_usia = sum(usia_list) / len(usia_list) if usia_list else 0
            
            rekap_keluarga.append({
                'no_kk': no_kk,
                'kepala_keluarga': kepala_keluarga.get('nama', 'Tidak diketahui'),
                'nik_kepala': kepala_keluarga.get('nik', ''),
                'alamat': kepala_keluarga.get('alamat', 'Tidak diketahui'),
                'status_alamat': kepala_keluarga.get('statusAlamat', 'Tidak diketahui'),
                'jumlah_anggota': len(anggota),
                'jumlah_laki': jumlah_laki,
                'jumlah_perempuan': jumlah_perempuan,
                'rata_usia': rata_usia,
                'anggota': anggota
            })
    
    # Tampilkan rekap
    total_anggota = 0
    total_laki = 0
    total_perempuan = 0
    
    for i, keluarga in enumerate(rekap_keluarga, 1):
        print(f"{i}. No KK: {keluarga['no_kk']}")
        print(f"   Kepala Keluarga: {keluarga['kepala_keluarga']}")
        print(f"   NIK Kepala: {keluarga['nik_kepala']}")
        print(f"   Alamat: {keluarga['alamat']}")
        print(f"   Status Alamat: {keluarga['status_alamat']}")
        print(f"   Jumlah Anggota: {keluarga['jumlah_anggota']} orang (L: {keluarga['jumlah_laki']}, P: {keluarga['jumlah_perempuan']})")
        print(f"   Rata-rata Usia: {keluarga['rata_usia']:.1f} tahun")
        
        # Tampilkan detail anggota
        print("   Anggota Keluarga:")
        for j, anggota in enumerate(keluarga['anggota'], 1):
            nama = anggota.get('nama', 'N/A')
            jk = anggota.get('jenisKelamin', 'N/A')
            usia = anggota.get('usia', 'N/A')
            kedudukan = anggota.get('kedudukan', 'Tidak diketahui')
            if not kedudukan:
                kedudukan = 'Tidak diketahui'
            
            pekerjaan = anggota.get('pekerjaan', 'Tidak diketahui')
            status_alamat = anggota.get('statusAlamat', 'Tidak diketahui')
            
            print(f"     {j}. {nama} ({jk}, {usia} th) - {kedudukan}")
            print(f"         Pekerjaan: {pekerjaan}, Status: {status_alamat}")
        
        total_anggota += keluarga['jumlah_anggota']
        total_laki += keluarga['jumlah_laki']
        total_perempuan += keluarga['jumlah_perempuan']
        print("-" * 80)
    
    # Statistik lengkap
    print("\n" + "=" * 120)
    print("STATISTIK LENGKAP WARGA TETAP & SEMENTARA (NON-MENINGGAL)")
    print("=" * 120)
    
    # Hitung berdasarkan status alamat
    status_count = defaultdict(int)
    for keluarga in rekap_keluarga:
        status = keluarga['status_alamat']
        status_count[status] += 1
    
    print(f"\nTotal Kartu Keluarga: {len(rekap_keluarga)}")
    print(f"Total Warga: {total_anggota} orang")
    print(f"  Laki-laki: {total_laki} orang ({total_laki/total_anggota*100:.1f}%)")
    print(f"  Perempuan: {total_perempuan} orang ({total_perempuan/total_anggota*100:.1f}%)")
    
    print("\nStatus Alamat Keluarga:")
    for status, count in sorted(status_count.items()):
        print(f"  {status}: {count} KK ({count/len(rekap_keluarga)*100:.1f}%)")
    
    # Distribusi jumlah anggota
    distribusi_anggota = defaultdict(int)
    for keluarga in rekap_keluarga:
        distribusi_anggota[keluarga['jumlah_anggota']] += 1
    
    print("\nDistribusi Jumlah Anggota Keluarga:")
    for jumlah, count in sorted(distribusi_anggota.items()):
        print(f"  {jumlah} orang: {count} KK ({count/len(rekap_keluarga)*100:.1f}%)")
    
    # Rata-rata usia per keluarga
    usia_keluarga = [k['rata_usia'] for k in rekap_keluarga if k['rata_usia'] > 0]
    if usia_keluarga:
        rata_usia_total = sum(usia_keluarga) / len(usia_keluarga)
        print(f"\nRata-rata usia per keluarga: {rata_usia_total:.1f} tahun")
    
    # Analisis pekerjaan kepala keluarga
    pekerjaan_count = defaultdict(int)
    for keluarga in rekap_keluarga:
        for anggota in keluarga['anggota']:
            if anggota.get('nama') == keluarga['kepala_keluarga']:
                pekerjaan = anggota.get('pekerjaan', 'Tidak diketahui')
                if not pekerjaan:
                    pekerjaan = 'Tidak diketahui'
                pekerjaan_count[pekerjaan] += 1
                break
    
    print("\nPekerjaan Kepala Keluarga (Top 10):")
    sorted_pekerjaan = sorted(pekerjaan_count.items(), key=lambda x: x[1], reverse=True)
    for pekerjaan, count in sorted_pekerjaan[:10]:
        print(f"  {pekerjaan}: {count} KK ({count/len(rekap_keluarga)*100:.1f}%)")
    
    # Analisis pendidikan kepala keluarga
    pendidikan_count = defaultdict(int)
    for keluarga in rekap_keluarga:
        for anggota in keluarga['anggota']:
            if anggota.get('nama') == keluarga['kepala_keluarga']:
                pendidikan = anggota.get('pendidikan', 'Tidak diketahui')
                if not pendidikan:
                    pendidikan = 'Tidak diketahui'
                pendidikan_count[pendidikan] += 1
                break
    
    print("\nPendidikan Kepala Keluarga:")
    for pendidikan, count in sorted(pendidikan_count.items()):
        print(f"  {pendidikan}: {count} KK ({count/len(rekap_keluarga)*100:.1f}%)")
    
    # Simpan ke file JSON
    output_file = 'rekap_warga_tetap_sementara.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rekap_keluarga, f, indent=2, ensure_ascii=False)
    
    print(f"\nData telah disimpan ke: {output_file}")
    
    # Buat file CSV
    csv_file = 'rekap_warga_tetap_sementara.csv'
    with open(csv_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("No,No KK,Nama Kepala Keluarga,NIK Kepala,Alamat,Status Alamat,Jumlah Anggota,Jumlah Laki,Jumlah Perempuan,Rata Usia,Anggota Detail\n")
        
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
            
            f.write(f"{i},{keluarga['no_kk']},{keluarga['kepala_keluarga']},{keluarga['nik_kepala']},{keluarga['alamat']},{keluarga['status_alamat']},{keluarga['jumlah_anggota']},{keluarga['jumlah_laki']},{keluarga['jumlah_perempuan']},{keluarga['rata_usia']:.1f},\"{anggota_str}\"\n")
    
    print(f"Data CSV telah disimpan ke: {csv_file}")
    
    # Buat file ringkasan
    ringkasan_file = 'ringkasan_warga_tetap_sementara.txt'
    with open(ringkasan_file, 'w', encoding='utf-8') as f:
        f.write("RINGKASAN DATA WARGA TETAP & SEMENTARA (NON-MENINGGAL)\n")
        f.write("RT 04/RW 11 Kel. Jatihandap Kec. Mandalajati\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total Kartu Keluarga: {len(rekap_keluarga)}\n")
        f.write(f"Total Warga: {total_anggota} orang\n")
        f.write(f"  Laki-laki: {total_laki} orang\n")
        f.write(f"  Perempuan: {total_perempuan} orang\n\n")
        
        f.write("STATISTIK:\n")
        f.write(f"Rata-rata anggota per keluarga: {total_anggota/len(rekap_keluarga):.1f} orang\n")
        
        if usia_keluarga:
            f.write(f"Rata-rata usia per keluarga: {rata_usia_total:.1f} tahun\n\n")
        
        f.write("Status Alamat:\n")
        for status, count in sorted(status_count.items()):
            f.write(f"  {status}: {count} KK\n")
        
        f.write("\nDistribusi Jumlah Anggota:\n")
        for jumlah, count in sorted(distribusi_anggota.items()):
            f.write(f"  {jumlah} orang: {count} KK\n")
        
        f.write("\nPekerjaan Kepala Keluarga (Top 5):\n")
        for pekerjaan, count in sorted_pekerjaan[:5]:
            f.write(f"  {pekerjaan}: {count} KK\n")
        
        f.write("\nPendidikan Kepala Keluarga:\n")
        for pendidikan, count in sorted(pendidikan_count.items()):
            f.write(f"  {pendidikan}: {count} KK\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("CATATAN:\n")
        f.write("- Data ini hanya mencakup warga dengan status alamat 'TETAP' atau 'SEMENTARA'\n")
        f.write("- Warga dengan keterangan 'meninggal' telah disaring\n")
        f.write("- Hanya warga yang memiliki No KK yang valid\n")
        f.write(f"Tanggal: 5 Mei 2026\n")
    
    print(f"Ringkasan telah disimpan ke: {ringkasan_file}")
    
    return rekap_keluarga

if __name__ == "__main__":
    rekap_warga_tetap_sementara()