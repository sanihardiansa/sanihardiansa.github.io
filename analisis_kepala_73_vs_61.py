#!/usr/bin/env python3
# Script untuk menganalisis mengapa ada 73 kepala keluarga di data mentah
# tetapi dashboard hanya menghitung 61

import json

def analisis_kepala_73_vs_61():
    # Baca file data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 120)
    print("ANALISIS: 73 KEPALA KELUARGA DI DATA MENTAH vs 61 DI DASHBOARD")
    print("=" * 120)
    
    # 1. Cari semua individu dengan kedudukan 'Kepala' di data mentah
    semua_kepala = []
    for warga in data:
        kedudukan = str(warga.get('kedudukan', '')).lower()
        if 'kepala' in kedudukan:
            semua_kepala.append(warga)
    
    print(f"Total individu dengan kedudukan 'Kepala' di data mentah: {len(semua_kepala)}")
    
    # 2. Terapkan filter dashboard
    kepala_setelah_filter = []
    for warga in semua_kepala:
        keterangan = str(warga.get('keterangan', '')).lower()
        status_alamat = str(warga.get('statusAlamat', '')).upper()
        
        # Filter dashboard: (!w.keterangan || !w.keterangan.toLowerCase().includes('meninggal')) &&
        # (w.statusAlamat || '').toUpperCase() !== 'PINDAH'
        if ('meninggal' not in keterangan) and (status_alamat != 'PINDAH'):
            kepala_setelah_filter.append(warga)
    
    print(f"Kepala keluarga setelah filter dashboard (non-meninggal, non-pindah): {len(kepala_setelah_filter)}")
    
    # 3. Analisis perbedaan
    print("\nANALISIS PERBEDAAN 73 vs 61:")
    print("-" * 60)
    
    # Cari kepala keluarga yang dihapus oleh filter
    kepala_yang_dihapus = []
    for warga in semua_kepala:
        keterangan = str(warga.get('keterangan', '')).lower()
        status_alamat = str(warga.get('statusAlamat', '')).upper()
        nama = warga.get('nama', 'N/A')
        
        dihapus_karena = []
        
        if 'meninggal' in keterangan:
            dihapus_karena.append("meninggal")
        
        if status_alamat == 'PINDAH':
            dihapus_karena.append("pindah")
        
        if dihapus_karena:
            kepala_yang_dihapus.append((nama, dihapus_karena, status_alamat, keterangan))
    
    print(f"Kepala keluarga yang dihapus oleh filter dashboard: {len(kepala_yang_dihapus)}")
    
    if kepala_yang_dihapus:
        print("\nDETAIL KEPALA KELUARGA YANG DIHAPUS:")
        print("-" * 60)
        for nama, alasan, status, ket in kepala_yang_dihapus:
            print(f"  - {nama}:")
            print(f"     Dihapus karena: {', '.join(alasan)}")
            print(f"     Status alamat: {status}")
            print(f"     Keterangan: {ket if ket else '(kosong)'}")
    
    # 4. Verifikasi matematika
    print("\nVERIFIKASI MATEMATIKA:")
    print("-" * 60)
    print(f"73 (total kepala di data mentah)")
    print(f"- {len(kepala_yang_dihapus)} (dihapus oleh filter)")
    print(f"= {73 - len(kepala_yang_dihapus)} (seharusnya di dashboard)")
    
    # 5. Cek apakah ada masalah dengan string matching
    print("\nANALISIS STRING MATCHING 'Kepala':")
    print("-" * 60)
    
    variasi_kedudukan = set()
    for warga in data:
        kedudukan = warga.get('kedudukan', '')
        if kedudukan:
            variasi_kedudukan.add(kedudukan)
    
    print("Variasi nilai 'kedudukan' di data:")
    for kedudukan in sorted(variasi_kedudukan):
        if 'kepala' in kedudukan.lower():
            print(f"  - '{kedudukan}' (TERDETEKSI)")
        else:
            print(f"  - '{kedudukan}'")
    
    # 6. Cek apakah dashboard menggunakan .includes('Kepala') dengan case sensitive
    print("\nANALISIS CASE SENSITIVE:")
    print("-" * 60)
    
    kepala_case_sensitive = []
    for warga in data:
        kedudukan = warga.get('kedudukan', '')
        if kedudukan and 'Kepala' in kedudukan:  # Case sensitive
            kepala_case_sensitive.append(warga)
    
    print(f"Kepala keluarga dengan 'Kepala' (case sensitive): {len(kepala_case_sensitive)}")
    
    # Filter case sensitive dengan filter dashboard
    kepala_case_sensitive_filtered = []
    for warga in kepala_case_sensitive:
        keterangan = str(warga.get('keterangan', '')).lower()
        status_alamat = str(warga.get('statusAlamat', '')).upper()
        
        if ('meninggal' not in keterangan) and (status_alamat != 'PINDAH'):
            kepala_case_sensitive_filtered.append(warga)
    
    print(f"Setelah filter dashboard: {len(kepala_case_sensitive_filtered)}")
    
    return {
        'total_kepala_mentah': len(semua_kepala),
        'kepala_setelah_filter': len(kepala_setelah_filter),
        'kepala_dihapus': len(kepala_yang_dihapus),
        'variasi_kedudukan': list(variasi_kedudukan),
        'kepala_case_sensitive': len(kepala_case_sensitive),
        'kepala_case_sensitive_filtered': len(kepala_case_sensitive_filtered)
    }

if __name__ == "__main__":
    hasil = analisis_kepala_73_vs_61()
    
    print("\n" + "=" * 120)
    print("KESIMPULAN AKHIR:")
    print("=" * 120)
    
    print(f"1. Data mentah memiliki {hasil['total_kepala_mentah']} individu dengan kedudukan mengandung 'kepala'")
    print(f"2. Setelah filter dashboard (non-meninggal, non-pindah): {hasil['kepala_setelah_filter']}")
    print(f"3. {hasil['kepala_dihapus']} kepala keluarga dihapus oleh filter")
    print(f"4. Dashboard menghitung {hasil['kepala_case_sensitive_filtered']} dengan 'Kepala' (case sensitive)")
    
    if hasil['kepala_setelah_filter'] == 61:
        print("\n✅ DASHBOARD BENAR: Menghitung 61 kepala keluarga setelah filter")
    else:
        print(f"\n❌ ADA MASALAH: Dashboard seharusnya menghitung {hasil['kepala_setelah_filter']}, bukan 61")
        
    print("\nCatatan: JavaScript .includes() adalah case-sensitive!")
    print("Jika data memiliki 'kepala keluarga' (huruf kecil), tidak akan terdeteksi oleh 'Kepala'")