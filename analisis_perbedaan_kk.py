#!/usr/bin/env python3
# Script untuk menganalisis perbedaan jumlah kepala keluarga antara dashboard dan rekap Python

import json
from collections import defaultdict

def analisis_perbedaan():
    # Baca file data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 120)
    print("ANALISIS PERBEDAAN JUMLAH KEPALA KELUARGA")
    print("=" * 120)
    
    # 1. ANALISIS DASHBOARD APLIKASI
    print("\n1. LOGIKA DASHBOARD APLIKASI (index.html):")
    print("-" * 60)
    
    # Filter seperti di dashboard: hapus meninggal dan pindah
    warga_filtered_dashboard = []
    for warga in data:
        keterangan = str(warga.get('keterangan', '')).lower()
        status_alamat = str(warga.get('statusAlamat', '')).upper()
        
        # Filter dashboard: (!w.keterangan || !w.keterangan.toLowerCase().includes('meninggal')) &&
        # (w.statusAlamat || '').toUpperCase() !== 'PINDAH'
        if ('meninggal' not in keterangan) and (status_alamat != 'PINDAH'):
            warga_filtered_dashboard.append(warga)
    
    # Hitung kepala keluarga seperti dashboard: w.kedudukan && w.kedudukan.includes('Kepala')
    kepala_dashboard = []
    for warga in warga_filtered_dashboard:
        kedudukan = str(warga.get('kedudukan', '')).lower()
        if 'kepala' in kedudukan:
            kepala_dashboard.append(warga)
    
    print(f"Total data warga: {len(data)}")
    print(f"Warga setelah filter dashboard (non-meninggal, non-pindah): {len(warga_filtered_dashboard)}")
    print(f"Kepala Keluarga (individu dengan kedudukan 'Kepala'): {len(kepala_dashboard)}")
    
    # 2. ANALISIS SCRIPT PYTHON REKAP
    print("\n2. LOGIKA SCRIPT PYTHON REKAP:")
    print("-" * 60)
    
    warga_filtered_python = []
    for warga in data:
        status_alamat = str(warga.get('statusAlamat', '')).upper()
        keterangan = str(warga.get('keterangan', '')).lower()
        no_kk = warga.get('noKK')
        
        # Filter Python: status alamat 'TETAP' atau 'SEMENTARA', 
        # keterangan tidak 'meninggal', No KK valid
        if (status_alamat in ['TETAP', 'SEMENTARA'] and 
            'meninggal' not in keterangan and
            no_kk and no_kk != '-' and no_kk != 'None'):
            warga_filtered_python.append(warga)
    
    # Kelompokkan berdasarkan No KK
    keluarga_dict = defaultdict(list)
    for warga in warga_filtered_python:
        no_kk = warga.get('noKK')
        if no_kk:
            keluarga_dict[no_kk].append(warga)
    
    print(f"Warga setelah filter Python (tetap/sementara, non-meninggal, No KK valid): {len(warga_filtered_python)}")
    print(f"Kartu Keluarga (No KK unik): {len(keluarga_dict)}")
    
    # 3. ANALISIS DETAIL PERBEDAAN
    print("\n3. ANALISIS DETAIL PERBEDAAN:")
    print("-" * 60)
    
    # Cari kepala keluarga di data yang difilter Python
    kepala_python = []
    for warga in warga_filtered_python:
        kedudukan = str(warga.get('kedudukan', '')).lower()
        if 'kepala' in kedudukan:
            kepala_python.append(warga)
    
    print(f"Kepala Keluarga (individu) di data Python: {len(kepala_python)}")
    
    # Analisis perbedaan status alamat
    print("\n4. DISTRIBUSI STATUS ALAMAT:")
    print("-" * 60)
    
    status_count = defaultdict(int)
    for warga in data:
        status = str(warga.get('statusAlamat', 'TIDAK DIKETAHUI')).upper()
        status_count[status] += 1
    
    for status, count in sorted(status_count.items()):
        print(f"  {status}: {count} warga")
    
    # Analisis data dengan No KK tidak valid
    print("\n5. ANALISIS No KK:")
    print("-" * 60)
    
    no_kk_invalid = []
    no_kk_valid = []
    
    for warga in data:
        no_kk = warga.get('noKK')
        if not no_kk or no_kk == '-' or no_kk == 'None':
            no_kk_invalid.append(warga)
        else:
            no_kk_valid.append(warga)
    
    print(f"Warga dengan No KK valid: {len(no_kk_valid)}")
    print(f"Warga dengan No KK tidak valid (kosong, '-', 'None'): {len(no_kk_invalid)}")
    
    # Analisis warga dengan status alamat selain TETAP/SEMENTARA
    print("\n6. WARGA DENGAN STATUS ALAMAT LAIN:")
    print("-" * 60)
    
    status_lain = []
    for warga in data:
        status = str(warga.get('statusAlamat', '')).upper()
        if status not in ['TETAP', 'SEMENTARA', '']:
            status_lain.append(warga)
    
    print(f"Warga dengan status alamat selain TETAP/SEMENTARA: {len(status_lain)}")
    for warga in status_lain[:10]:  # Tampilkan 10 contoh
        nama = warga.get('nama', 'N/A')
        status = warga.get('statusAlamat', 'N/A')
        no_kk = warga.get('noKK', 'N/A')
        print(f"  - {nama}: Status={status}, No KK={no_kk}")
    
    if len(status_lain) > 10:
        print(f"  ... dan {len(status_lain) - 10} lainnya")
    
    # 7. REKOMENDASI
    print("\n7. REKOMENDASI:")
    print("-" * 60)
    print("Untuk konsistensi data, disarankan:")
    print("1. Dashboard aplikasi sebaiknya menghitung Kartu Keluarga (No KK unik)")
    print("2. Gunakan filter yang sama: status alamat 'TETAP' atau 'SEMENTARA'")
    print("3. Validasi No KK sebelum menghitung")
    print("4. Jika ingin menghitung individu, pastikan setiap KK memiliki tepat 1 kepala keluarga")
    
    return {
        'total_data': len(data),
        'dashboard_filtered': len(warga_filtered_dashboard),
        'dashboard_kepala': len(kepala_dashboard),
        'python_filtered': len(warga_filtered_python),
        'python_keluarga': len(keluarga_dict),
        'python_kepala': len(kepala_python)
    }

if __name__ == "__main__":
    hasil = analisis_perbedaan()
    
    print("\n" + "=" * 120)
    print("RINGKASAN PERBEDAAN:")
    print("=" * 120)
    print(f"Total data: {hasil['total_data']}")
    print(f"Dashboard - Warga setelah filter: {hasil['dashboard_filtered']}")
    print(f"Dashboard - Kepala Keluarga (individu): {hasil['dashboard_kepala']}")
    print(f"Python - Warga setelah filter: {hasil['python_filtered']}")
    print(f"Python - Kartu Keluarga (No KK unik): {hasil['python_keluarga']}")
    print(f"Python - Kepala Keluarga (individu): {hasil['python_kepala']}")
    print("\nPERBEDAAN UTAMA:")
    print(f"- Dashboard menghitung {hasil['dashboard_kepala']} INDIVIDU dengan kedudukan 'Kepala'")
    print(f"- Python menghitung {hasil['python_keluarga']} KARTU KELUARGA (No KK unik)")
    print(f"- Selisih: {abs(hasil['dashboard_kepala'] - hasil['python_keluarga'])}")