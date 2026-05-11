import pandas as pd
import json
import re
from datetime import datetime

df = pd.read_excel('/Users/cinot/mywork/rt04/Data Warga RT04.xlsx', header=5)
df = df.dropna(how='all')
df = df[df['NO'].notna()]
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 4'], errors='ignore')

# Rename kolom ke format yang diharapkan aplikasi
df.columns = df.columns.str.strip()
column_mapping = {
    'NO': 'no',
    'NAMA': 'nama',
    'L/P': 'jenisKelamin',
    'TEMPAT & TANGGAL LAHIR': 'tempatTanggalLahir',
    'NIK': 'nik',
    'NO KK': 'noKK',
    'ALAMAT LENGKAP': 'alamat',
    'KEDUDUKAN DALAM KELUARGA': 'kedudukan',
    'STATUS PERNIKAHAN': 'statusPernikahan',
    'AGAMA': 'agama',
    'PENDIDIKAN': 'pendidikan',
    'PEKERJAAN': 'pekerjaan',
    'NO TLP': 'noHP',
    'STATUS ALAMAT': 'statusAlamat',
    'KETERANGAN': 'keterangan'
}
df = df.rename(columns=column_mapping)

# Hitung usia dari tempatTanggalLahir
def calculate_age(ttl):
    if pd.isna(ttl) or ttl == '':
        return None
    match = re.search(r'(\d{4})', str(ttl))
    if match:
        year = int(match.group(1))
        return 2025 - year
    return None

df['usia'] = df['tempatTanggalLahir'].apply(calculate_age)
df = df.fillna('')

data = df.to_dict('records')

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Berhasil mengkonversi {len(data)} data warga")
