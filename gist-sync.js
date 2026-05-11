// GitHub Gist Sync
let GIST_TOKEN = '';
let GIST_ID = 'cbd1df57e903f1f23e462829fe46539a'; // Shared Gist ID

// Data structure for Gist
const GIST_FILES = {
    'warga.json': 'Data warga',
    'surat-pengantar.json': 'Surat pengantar',
    'kartu-keluarga.json': 'Kartu keluarga'
};

// Initialize with GitHub token
function initGistSync(token) {
    GIST_TOKEN = token;
    loadGistId();
}

// Load Gist ID (use hardcoded shared ID)
function loadGistId() {
    // Always use shared Gist ID
    console.log('Using shared Gist:', GIST_ID);
    loadAllDataFromGist();
}

// Create new Gist (not needed - using shared Gist)
async function createNewGist() {
    console.log('Using shared Gist, no need to create new one');
    loadAllDataFromGist();
}

// Load all data from Gist
async function loadAllDataFromGist() {
    try {
        const response = await fetch(`https://api.github.com/gists/${GIST_ID}`, {
            headers: {
                'Authorization': `token ${GIST_TOKEN}`
            }
        });
        
        if (!response.ok) throw new Error('Failed to load Gist');
        
        const gist = await response.json();
        const files = gist.files;
        
        // Load warga data
        if (files['warga.json']) {
            const wargaData = JSON.parse(files['warga.json'].content);
            window.allWargaData = wargaData;
            window.wargaData = wargaData.filter(w => 
                (!w.keterangan || !w.keterangan.toLowerCase().includes('meninggal')) &&
                (w.statusAlamat || '').toUpperCase() !== 'PINDAH'
            );
            window.filteredData = window.wargaData;
            localStorage.setItem('rt04_wargaData', JSON.stringify(wargaData));
            console.log('Loaded warga from Gist:', wargaData.length);
        }
        
        // Load surat pengantar
        if (files['surat-pengantar.json']) {
            window.suratPengantarData = JSON.parse(files['surat-pengantar.json'].content);
            console.log('Loaded surat pengantar from Gist:', window.suratPengantarData.length);
        }
        
        // Load kartu keluarga
        if (files['kartu-keluarga.json']) {
            window.kartuKeluargaData = JSON.parse(files['kartu-keluarga.json'].content);
            console.log('Loaded KK from Gist:', window.kartuKeluargaData.length);
        }
        
        // Update UI
        if (window.updateDashboard) window.updateDashboard();
        if (window.renderTable) window.renderTable();
        if (window.renderSuratPengantarTable) window.renderSuratPengantarTable();
        if (window.renderKKTable) window.renderKKTable();
        
    } catch (error) {
        console.error('Error loading from Gist:', error);
        // Fallback to localStorage
        fallbackToLocalStorage();
    }
}

// Save surat pengantar to Gist
async function saveSuratPengantarToGist(surat) {
    try {
        // Add to local array
        window.suratPengantarData.push(surat);
        
        // Update Gist
        await updateGistFile('surat-pengantar.json', window.suratPengantarData);
        
        console.log('Saved surat to Gist');
        return true;
    } catch (error) {
        console.error('Error saving to Gist:', error);
        // Fallback to localStorage
        localStorage.setItem('suratPengantarData', JSON.stringify(window.suratPengantarData));
        return false;
    }
}

// Update surat pengantar status in Gist
async function updateSuratPengantarStatusInGist(id, updates) {
    try {
        const index = window.suratPengantarData.findIndex(s => s.id === id);
        if (index !== -1) {
            window.suratPengantarData[index] = { ...window.suratPengantarData[index], ...updates };
            await updateGistFile('surat-pengantar.json', window.suratPengantarData);
            console.log('Updated surat in Gist');
            return true;
        }
        return false;
    } catch (error) {
        console.error('Error updating Gist:', error);
        localStorage.setItem('suratPengantarData', JSON.stringify(window.suratPengantarData));
        return false;
    }
}

// Update a single file in Gist
async function updateGistFile(filename, data) {
    const response = await fetch(`https://api.github.com/gists/${GIST_ID}`, {
        method: 'PATCH',
        headers: {
            'Authorization': `token ${GIST_TOKEN}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            files: {
                [filename]: { content: JSON.stringify(data, null, 2) }
            }
        })
    });
    
    if (!response.ok) throw new Error('Failed to update Gist');
    return await response.json();
}

// Fallback to localStorage
function fallbackToLocalStorage() {
    console.log('Falling back to localStorage');
    // Data already loaded from localStorage in main script
}

// Export current data to Gist (manual sync)
async function exportToGist() {
    try {
        const data = {
            warga: window.allWargaData || [],
            surat_pengantar: window.suratPengantarData || [],
            kartu_keluarga: window.kartuKeluargaData || []
        };
        
        await updateGistFile('warga.json', data.warga);
        await updateGistFile('surat-pengantar.json', data.surat_pengantar);
        await updateGistFile('kartu-keluarga.json', data.kartu_keluarga);
        
        // Catat ke audit log jika fungsi logActivity tersedia
        if (typeof logActivity === 'function') {
            logActivity('sync', 'Menyinkronkan data ke GitHub Gist', {
                wargaCount: data.warga.length,
                suratPengantarCount: data.surat_pengantar.length,
                kartuKeluargaCount: data.kartu_keluarga.length,
                timestamp: new Date().toISOString()
            });
        }
        
        alert('Data berhasil di-sync ke GitHub Gist!');
        return true;
    } catch (error) {
        console.error('Error exporting to Gist:', error);
        
        // Catat error ke audit log jika fungsi logActivity tersedia
        if (typeof logActivity === 'function') {
            logActivity('error', 'Gagal menyinkronkan data ke GitHub Gist', {
                error: error.message,
                timestamp: new Date().toISOString()
            });
        }
        
        alert('Gagal sync ke Gist: ' + error.message);
        return false;
    }
}