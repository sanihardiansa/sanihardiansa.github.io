// Supabase Client
let supabaseClient = null;
let SUPABASE_URL = '';
let SUPABASE_ANON_KEY = '';

function initSupabase(url, anonKey) {
    SUPABASE_URL = url;
    SUPABASE_ANON_KEY = anonKey;
    
    // Load Supabase client library
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
    script.onload = () => {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        console.log('Supabase client initialized');
        loadAllData();
    };
    document.head.appendChild(script);
}

// Load all data from Supabase
async function loadAllData() {
    try {
        // Load warga data
        const { data: wargaData, error: wargaError } = await supabaseClient
            .from('warga')
            .select('*');
        
        if (!wargaError && wargaData) {
            window.allWargaData = wargaData;
            window.wargaData = wargaData.filter(w => 
                (!w.keterangan || !w.keterangan.toLowerCase().includes('meninggal')) &&
                (w.status_alamat || '').toUpperCase() !== 'PINDAH'
            );
            window.filteredData = window.wargaData;
            localStorage.setItem('rt04_wargaData', JSON.stringify(wargaData));
            console.log('Loaded warga from Supabase:', wargaData.length);
        }
        
        // Load surat pengantar
        const { data: suratData, error: suratError } = await supabaseClient
            .from('surat_pengantar')
            .select('*')
            .order('created_at', { ascending: false });
        
        if (!suratError && suratData) {
            window.suratPengantarData = suratData.map(s => ({
                id: s.id,
                tanggalSurat: s.tanggal_surat,
                noSurat: s.no_surat,
                noKTP: s.no_ktp,
                nama: s.nama,
                jenisKelamin: s.jenis_kelamin,
                ttl: s.ttl,
                pekerjaan: s.pekerjaan,
                alamat: s.alamat,
                noKK: s.no_kk,
                statusPerkawinan: s.status_perkawinan,
                maksudTujuan: s.maksud_tujuan,
                catatan: s.catatan,
                status: s.status,
                approvedRT: s.approved_rt,
                approvedRTDate: s.approved_rt_date,
                approvedRW: s.approved_rw,
                approvedRWDate: s.approved_rw_date,
                alasanTolak: s.alasan_tolak,
                ditolakOleh: s.ditolak_oleh,
                ditolakDate: s.ditolak_date
            }));
            console.log('Loaded surat pengantar from Supabase:', suratData.length);
        }
        
        // Load kartu keluarga
        const { data: kkData, error: kkError } = await supabaseClient
            .from('kartu_keluarga')
            .select('*');
        
        if (!kkError && kkData) {
            window.kartuKeluargaData = kkData.map(kk => ({
                id: kk.id,
                noKK: kk.no_kk,
                tanggalKK: kk.tanggal_kk,
                alamat: kk.alamat,
                rt: kk.rt,
                rw: kk.rw,
                kelurahan: kk.kelurahan,
                kecamatan: kk.kecamatan,
                kabupaten: kk.kabupaten,
                provinsi: kk.provinsi,
                statusAlamat: kk.status_alamat,
                anggota: kk.anggota
            }));
            console.log('Loaded KK from Supabase:', kkData.length);
        }
        
        // Update UI
        if (window.updateDashboard) window.updateDashboard();
        if (window.renderTable) window.renderTable();
        if (window.renderSuratPengantarTable) window.renderSuratPengantarTable();
        if (window.renderKKTable) window.renderKKTable();
        
    } catch (error) {
        console.error('Error loading data from Supabase:', error);
        // Fallback to localStorage
        fallbackToLocalStorage();
    }
}

// Save surat pengantar to Supabase
async function saveSuratPengantarToSupabase(surat) {
    if (!supabaseClient) return null;
    
    try {
        const { data, error } = await supabaseClient
            .from('surat_pengantar')
            .insert([{
                tanggal_surat: surat.tanggalSurat,
                no_surat: surat.noSurat,
                no_ktp: surat.noKTP,
                nama: surat.nama,
                jenis_kelamin: surat.jenisKelamin,
                ttl: surat.ttl,
                pekerjaan: surat.pekerjaan,
                alamat: surat.alamat,
                no_kk: surat.noKK,
                status_perkawinan: surat.statusPerkawinan,
                maksud_tujuan: surat.maksudTujuan,
                catatan: surat.catatan,
                status: surat.status || 'pending'
            }])
            .select();
        
        if (error) throw error;
        console.log('Saved surat to Supabase:', data);
        return data[0].id;
    } catch (error) {
        console.error('Error saving to Supabase:', error);
        return null;
    }
}

// Update surat pengantar status (approve/reject)
async function updateSuratPengantarStatus(id, updates) {
    if (!supabaseClient) return false;
    
    try {
        const { error } = await supabaseClient
            .from('surat_pengantar')
            .update(updates)
            .eq('id', id);
        
        if (error) throw error;
        console.log('Updated surat status in Supabase');
        return true;
    } catch (error) {
        console.error('Error updating Supabase:', error);
        return false;
    }
}

// Fallback to localStorage if Supabase fails
function fallbackToLocalStorage() {
    console.log('Falling back to localStorage');
    // Data already loaded from localStorage in main script
}