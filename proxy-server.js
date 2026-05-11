// Proxy Server Simulasi untuk RT04-App
// File ini mensimulasikan server-side proxy untuk menghindari hardcoded token di client

class GitHubProxy {
    constructor() {
        this.baseURL = 'https://api.github.com';
        this.token = localStorage.getItem('rt04_gist_token');
        this.useProxy = false;
    }
    
    // Cek apakah bisa menggunakan proxy
    async checkProxyAvailable() {
        try {
            // Coba akses endpoint proxy sederhana
            const response = await fetch('/api/health', { method: 'HEAD' });
            this.useProxy = response.ok;
            console.log('Proxy available:', this.useProxy);
            return this.useProxy;
        } catch (error) {
            console.log('Proxy not available, using direct API');
            this.useProxy = false;
            return false;
        }
    }
    
    // Request ke GitHub API melalui proxy atau langsung
    async request(endpoint, options = {}) {
        if (!this.token) {
            throw new Error('GitHub token tidak ditemukan');
        }
        
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Authorization': `token ${this.token}`,
            'Accept': 'application/vnd.github.v3+json',
            ...options.headers
        };
        
        try {
            if (this.useProxy) {
                // Gunakan proxy server
                const proxyResponse = await fetch('/api/github-proxy', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        url: endpoint,
                        method: options.method || 'GET',
                        headers: headers,
                        body: options.body
                    })
                });
                
                if (!proxyResponse.ok) {
                    throw new Error(`Proxy error: ${proxyResponse.status}`);
                }
                
                return await proxyResponse.json();
            } else {
                // Gunakan API langsung (fallback)
                const response = await fetch(url, {
                    ...options,
                    headers: headers
                });
                
                if (!response.ok) {
                    throw new Error(`GitHub API error: ${response.status}`);
                }
                
                return await response.json();
            }
        } catch (error) {
            console.error('GitHub request error:', error);
            throw error;
        }
    }
    
    // Get Gist
    async getGist(gistId) {
        return this.request(`/gists/${gistId}`);
    }
    
    // Update Gist
    async updateGist(gistId, files) {
        return this.request(`/gists/${gistId}`, {
            method: 'PATCH',
            body: JSON.stringify({ files })
        });
    }
    
    // Create Gist
    async createGist(files, description = 'RT04 App Data') {
        return this.request('/gists', {
            method: 'POST',
            body: JSON.stringify({
                description,
                files,
                public: false
            })
        });
    }
}

// Update gist-sync.js untuk menggunakan proxy
function updateGistSyncForProxy() {
    console.log('🔄 Memperbarui Gist sync untuk menggunakan proxy...');
    
    // Simpan fungsi asli
    const originalUpdateGistFile = window.updateGistFile;
    
    // Override dengan proxy
    window.updateGistFile = async function(filename, data) {
        try {
            const proxy = new GitHubProxy();
            await proxy.checkProxyAvailable();
            
            // Get current Gist
            const gist = await proxy.getGist(window.GIST_ID);
            const files = gist.files || {};
            
            // Update file
            files[filename] = {
                content: JSON.stringify(data, null, 2)
            };
            
            // Update Gist
            await proxy.updateGist(window.GIST_ID, files);
            console.log(`✅ Updated ${filename} via ${proxy.useProxy ? 'proxy' : 'direct API'}`);
            return true;
        } catch (error) {
            console.error('Error updating Gist via proxy:', error);
            
            // Fallback ke metode asli
            if (originalUpdateGistFile) {
                console.log('Fallback ke metode original...');
                return originalUpdateGistFile(filename, data);
            }
            
            return false;
        }
    };
    
    console.log('✅ Gist sync telah diupdate untuk proxy support');
}

// Aktifkan saat halaman dimuat
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateGistSyncForProxy);
} else {
    updateGistSyncForProxy();
}

// Fungsi untuk setup token dengan aman
function setupGitHubToken() {
    const token = prompt(`Masukkan GitHub Personal Access Token:

🔐 Token akan disimpan di localStorage browser ini SAJA.
📋 Token harus memiliki permission "gist".
⚙️ Cara membuat token:
1. Login ke GitHub
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Klik "Generate new token (classic)"
4. Beri nama "RT04-App"
5. Centang "gist"
6. Klik "Generate token"
7. Copy token dan paste di sini

⚠️ PERINGATAN: Jangan share token ini dengan siapapun!`);

    if (!token || token.trim().length < 20) {
        alert('Token tidak valid atau dibatalkan');
        return false;
    }
    
    // Simpan token
    localStorage.setItem('rt04_gist_token', token.trim());
    
    // Enkripsi token (sederhana)
    const encryptedToken = btoa(token.trim().split('').reverse().join(''));
    localStorage.setItem('rt04_gist_token_encrypted', encryptedToken);
    
    // Hapus token plaintext setelah beberapa detik
    setTimeout(() => {
        localStorage.removeItem('rt04_gist_token');
        console.log('Token plaintext telah dihapus dari memory');
    }, 5000);
    
    alert('✅ Token berhasil disimpan! Token plaintext akan dihapus otomatis dalam 5 detik.');
    return true;
}

// Fungsi untuk mendapatkan token (dengan dekripsi)
function getGitHubToken() {
    // Coba ambil dari encrypted storage
    const encryptedToken = localStorage.getItem('rt04_gist_token_encrypted');
    if (encryptedToken) {
        try {
            return atob(encryptedToken).split('').reverse().join('');
        } catch (error) {
            console.error('Error decrypting token:', error);
        }
    }
    
    // Fallback ke plaintext (jika masih ada)
    return localStorage.getItem('rt04_gist_token');
}

// Export untuk penggunaan di file lain
window.GitHubProxy = GitHubProxy;
window.setupGitHubToken = setupGitHubToken;
window.getGitHubToken = getGitHubToken;