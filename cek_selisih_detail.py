#!/usr/bin/env python3
# Script untuk mengecek detail selisih 2 antara dashboard dan Python rekap

import json
from collections import defaultdict

def cek_selisih_detail():
    # Baca file data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 120)
    print("CEK DETAIL SELISIH 2 ANTARA DASHBOARD DAN PYTHON REKAP")
    print("=" * 120)
    
    # 1. Cari semua No KK unik dengan filter Python
    keluarga_dict = defaultdict(list)
    for warga in data:
        status_alamat = str(warga.get('statusAlamat', '')).upper()
        keterangan = str(warga.get('keterangan', '')).lower()
        no_kk = warga.get('noKK')
        
        if (status_alamat in ['TETAP', 'SEMENTARA'] and 
            'meninggal' not in keterangan and
            no_kk and no_kk != '-' and no_kk != 'None'):
            keluarga_dict[no_kk].append(warga)
    
    # 2. Untuk setiap KK, cek apakah ada kepala keluarga
    print("\nANALISIS KEPALA KELUARGA PER NO KK:")
    print("-" * 60)
    
    kk_tanpa_kepala = []
    kk_dengan_kepala = []
    
    for no_kk, anggota in keluarga_dict.items():
        kepala_ditemukan = False
        for warga in anggota:
            kedudukan = str(warga.get('kedudukan', '')).lower()
            if 'kepala' in kedudukan:
                kepala_ditemukan = True
                break
        
        if kepala_ditemukan:
            kk_dengan_kepala.append(no_kk)
        else:
            kk_tanpa_kepala.append(no_kk)
    
    print(f"Total Kartu Keluarga (No KK unik): {len(keluarga_dict)}")
    print(f"KK dengan kepala keluarga teridentifikasi: {len(kk_dengan_kepala)}")
    print(f"KK TANPA kepala keluarga teridentifikasi: {len(kk_tanpa_kepala)}")
    
    if kk_tanpa_kepala:
        print("\nDETAIL KK TANPA KEPALA KELUARGA:")
        print("-" * 60)
        for no_kk in kk_tanpa_kepala:
            anggota = keluarga_dict[no_kk]
            print(f"\nNo KK: {no_kk}")
            print(f"Jumlah anggota: {len(anggota)}")
            for i, warga in enumerate(anggota, 1):
                nama = warga.get('nama', 'N/A')
                kedudukan = warga.get('kedudukan', 'Tidak diketahui')
                print(f"  {i}. {nama} - Kedudukan: {kedudukan}")
    
    # 3. Cari individu dengan kedudukan 'Kepala' tetapi No KK tidak valid
    print("\n\nANALISIS INDIVIDU DENGAN KEDUDUKAN 'KEPALA':")
    print("-" * 60)
    
    kepala_individu = []
    for warga in data:
        kedudukan = str(warga.get('kedudukan', '')).lower()
        if 'kepala' in kedudukan:
            kepala_individu.append(warga)
    
    print(f"Total individu dengan kedudukan 'Kepala': {len(kepala_individu)}")
    
    kepala_no_kk_tidak_valid = []
    kepala_no_kk_valid = []
    
    for warga in kepala_individu:
        no_kk = warga.get('noKK')
        nama = warga.get('nama', 'N/A')
        
        if not no_kk or no_kk == '-' or no_kk == 'None':
            kepala_no_kk_tidak_valid.append((nama, no_kk))
        else:
            kepala_no_kk_valid.append((nama, no_kk))
    
    print(f"Kepala keluarga dengan No KK valid: {len(kepala_no_kk_valid)}")
    print(f"Kepala keluarga dengan No KK TIDAK valid: {len(kepala_no_kk_tidak_valid)}")
    
    if kepala_no_kk_tidak_valid:
        print("\nDETAIL KEPALA KELUARGA DENGAN No KK TIDAK VALID:")
        print("-" * 60)
        for nama, no_kk in kepala_no_kk_tidak_valid:
            print(f"  - {nama}: No KK = '{no_kk}'")
    
    # 4. Kesimpulan
    print("\n" + "=" * 120)
    print("KESIMPULAN SELISIH 2:")
    print("=" * 120)
    
    total_kk = len(keluarga_dict)  # 63
    total_kepala_teridentifikasi = len(kk_dengan_kepala)  # Seharusnya <= 61
    
    print(f"Total Kartu Keluarga (No KK unik): {total_kk}")
    print(f"Kartu Keluarga dengan kepala teridentifikasi: {total_kepala_teridentifikasi}")
    print(f"Selisih: {total_kk - total_kepala_teridentifikasi}")
    
    if total_kk - total_kepala_teridentifikasi == 2:
        print("\n✅ TERBUKTI: Selisih 2 berasal dari:")
        print("   - Ada 2 Kartu Keluarga yang tidak memiliki anggota dengan kedudukan 'Kepala Keluarga'")
        print("   - Atau ada kepala keluarga dengan No KK tidak valid")
    
    return {
        'total_kk': total_kk,
        'kk_dengan_kepala': len(kk_dengan_kepala),
        'kk_tanpa_kepala': len(kk_tanpa_kepala),
        'kepala_no_kk_valid': len(kepala_no_kk_valid),
        'kepala_no_kk_tidak_valid': len(kepala_no_kk_tidak_valid)
    }

if __name__ == "__main__":
    cek_selisih_detail()