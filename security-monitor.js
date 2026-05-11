// Security Monitor untuk RT04-App
// Memantau dan melaporkan issue keamanan

class SecurityMonitor {
    constructor() {
        this.issues = [];
        this.startTime = Date.now();
        this.init();
    }
    
    init() {
        console.log('🔍 Security Monitor diaktifkan...');
        this.checkSecurityIssues();
        this.setupEventListeners();
        this.logSecurityStatus();
    }
    
    checkSecurityIssues() {
        // 1. Cek localStorage untuk data sensitif
        this.checkLocalStorage();
        
        // 2. Cek penggunaan innerHTML yang berbahaya
        this.checkInnerHTMLUsage();
        
        // 3. Cek token GitHub
        this.checkGitHubToken();
        
        // 4. Cek password hash
        this.checkPasswordSecurity();
        
        // 5. Cek session security
        this.checkSessionSecurity();
    }
    
    checkLocalStorage() {
        try {
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                const value = localStorage.getItem(key);
                
                // Cek data sensitif
                if (key.includes('warga') || key.includes('data')) {
                    try {
                        const data = JSON.parse(value);
                        if (Array.isArray(data) && data.length > 0) {
                            const sample = data[0];
                            const sensitiveFields = ['nik', 'noKK', 'noHP', 'alamat'];
                            const hasSensitiveData = sensitiveFields.some(field => 
                                sample[field] && !sample[field].includes('ENCRYPTED:')
                            );
                            
                            if (hasSensitiveData) {
                                this.addIssue('HIGH', 
                                    `Data sensitif ditemukan di ${key} tanpa enkripsi`,
                                    'Gunakan data-encryption.js untuk mengenkripsi data'
                                );
                            }
                        }
                    } catch (e) {
                        // Bukan JSON, skip
                    }
                }
            }
        } catch (error) {
            console.error('Error checking localStorage:', error);
        }
    }
    
    checkInnerHTMLUsage() {
        // Monitor penggunaan innerHTML
        const originalQuerySelectorAll = document.querySelectorAll;
        
        // Deteksi penggunaan innerHTML yang berpotensi berbahaya
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                const elementsWithInnerHTML = originalQuerySelectorAll.call(document, '[innerhtml]');
                if (elementsWithInnerHTML.length > 0) {
                    this.addIssue('MEDIUM',
                        `${elementsWithInnerHTML.length} elemen menggunakan innerHTML`,
                        'Pertimbangkan menggunakan textContent atau sanitizeHTML()'
                    );
                }
            }, 1000);
        });
    }
    
    checkGitHubToken() {
        const token = localStorage.getItem('rt04_gist_token');
        const encryptedToken = localStorage.getItem('rt04_gist_token_encrypted');
        
        if (token && !encryptedToken) {
            this.addIssue('HIGH',
                'GitHub token disimpan sebagai plaintext',
                'Gunakan setupGitHubToken() untuk enkripsi token'
            );
        }
        
        if (!token && !encryptedToken) {
            this.addIssue('LOW',
                'GitHub token tidak ditemukan',
                'Fitur sync ke Gist akan dinonaktifkan'
            );
        }
    }
    
    checkPasswordSecurity() {
        // Cek apakah menggunakan default password hash
        const defaultAdminHash = '5b74fd3fb7f9e12b57d68c29878968216fa9c11ea427403b02d562b7d63e9914';
        const storedAdminHash = localStorage.getItem('rt04_admin_hash');
        
        if (!storedAdminHash || storedAdminHash === defaultAdminHash) {
            this.addIssue('HIGH',
                'Menggunakan default password hash',
                'Ubah password default di production'
            );
        }
    }
    
    checkSessionSecurity() {
        // Cek session timeout
        const session = JSON.parse(sessionStorage.getItem('rt04_session') || 'null');
        if (session) {
            const sessionAge = Date.now() - (session.exp - 7200000); // 2 jam dalam ms
            if (sessionAge > 3600000) { // Lebih dari 1 jam
                this.addIssue('LOW',
                    `Session aktif selama ${Math.round(sessionAge / 60000)} menit`,
                    'Pertimbangkan untuk logout setelah tidak aktif'
                );
            }
        }
    }
    
    addIssue(severity, description, recommendation) {
        const issue = {
            id: this.issues.length + 1,
            severity,
            description,
            recommendation,
            timestamp: new Date().toISOString()
        };
        
        this.issues.push(issue);
        
        // Log ke console berdasarkan severity
        const emoji = severity === 'HIGH' ? '🚨' : severity === 'MEDIUM' ? '⚠️' : 'ℹ️';
        console.log(`${emoji} [${severity}] ${description}`);
        
        return issue;
    }
    
    setupEventListeners() {
        // Monitor form submissions
        document.addEventListener('submit', (e) => {
            const form = e.target;
            const inputs = form.querySelectorAll('input[type="text"], input[type="password"], textarea');
            
            inputs.forEach(input => {
                if (input.value && input.value.length > 1000) {
                    this.addIssue('MEDIUM',
                        `Input panjang ditemukan di form ${form.id || 'unknown'}`,
                        'Tambahkan validasi panjang input'
                    );
                }
            });
        });
        
        // Monitor AJAX requests
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            const [url, options] = args;
            
            // Cek URL untuk API calls
            if (typeof url === 'string' && url.includes('api.github.com')) {
                console.log('🔐 GitHub API request:', url);
                
                // Cek jika token ter-expose di URL
                if (url.includes('token=')) {
                    SecurityMonitor.getInstance().addIssue('CRITICAL',
                        'GitHub token ter-expose di URL',
                        'Jangan pernah menyimpan token di URL'
                    );
                }
            }
            
            return originalFetch.apply(this, args);
        };
    }
    
    logSecurityStatus() {
        setTimeout(() => {
            const highIssues = this.issues.filter(i => i.severity === 'HIGH').length;
            const mediumIssues = this.issues.filter(i => i.severity === 'MEDIUM').length;
            const lowIssues = this.issues.filter(i => i.severity === 'LOW').length;
            
            console.log(`
📊 SECURITY STATUS REPORT
=========================
⏱️  Waktu pemantauan: ${Math.round((Date.now() - this.startTime) / 1000)} detik
📈 Total issues: ${this.issues.length}
🚨 HIGH: ${highIssues} issue${highIssues !== 1 ? 's' : ''}
⚠️  MEDIUM: ${mediumIssues} issue${mediumIssues !== 1 ? 's' : ''}
ℹ️  LOW: ${lowIssues} issue${lowIssues !== 1 ? 's' : ''}

${highIssues > 0 ? '❌ PERBAIKAN SEGERA DIPERLUKAN!' : '✅ Status keamanan cukup baik'}
            `);
            
            // Tampilkan issues HIGH
            if (highIssues > 0) {
                console.log('🚨 ISSUES KRITIS:');
                this.issues.filter(i => i.severity === 'HIGH').forEach(issue => {
                    console.log(`  ${issue.id}. ${issue.description}`);
                    console.log(`     💡 Rekomendasi: ${issue.recommendation}`);
                });
            }
            
        }, 3000);
    }
    
    getReport() {
        return {
            timestamp: new Date().toISOString(),
            issues: this.issues,
            summary: {
                total: this.issues.length,
                high: this.issues.filter(i => i.severity === 'HIGH').length,
                medium: this.issues.filter(i => i.severity === 'MEDIUM').length,
                low: this.issues.filter(i => i.severity === 'LOW').length
            }
        };
    }
    
    static getInstance() {
        if (!SecurityMonitor.instance) {
            SecurityMonitor.instance = new SecurityMonitor();
        }
        return SecurityMonitor.instance;
    }
}

// Fungsi untuk menampilkan security dashboard
function showSecurityDashboard() {
    const monitor = SecurityMonitor.getInstance();
    const report = monitor.getReport();
    
    const html = `
        <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3>🔒 Security Dashboard</h3>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 15px 0;">
                <div style="background: ${report.summary.high > 0 ? '#ff6b6b' : '#51cf66'}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold;">${report.summary.high}</div>
                    <div>HIGH</div>
                </div>
                <div style="background: ${report.summary.medium > 0 ? '#ffd93d' : '#51cf66'}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold;">${report.summary.medium}</div>
                    <div>MEDIUM</div>
                </div>
                <div style="background: #51cf66; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold;">${report.summary.low}</div>
                    <div>LOW</div>
                </div>
                <div style="background: #339af0; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold;">${report.summary.total}</div>
                    <div>TOTAL</div>
                </div>
            </div>
            
            ${report.issues.length > 0 ? `
                <h4>Issues Terdeteksi:</h4>
                <div style="max-height: 300px; overflow-y: auto;">
                    ${report.issues.map(issue => `
                        <div style="border-left: 4px solid ${issue.severity === 'HIGH' ? '#ff6b6b' : issue.severity === 'MEDIUM' ? '#ffd93d' : '#339af0'}; padding: 10px; margin: 5px 0; background: #f8f9fa;">
                            <strong>${issue.severity}:</strong> ${issue.description}
                            <div style="font-size: 0.9em; color: #666; margin-top: 5px;">
                                💡 ${issue.recommendation}
                            </div>
                        </div>
                    `).join('')}
                </div>
            ` : '<p style="color: #51cf66;">✅ Tidak ada issue keamanan yang terdeteksi</p>'}
            
            <div style="margin-top: 15px; display: flex; gap: 10px;">
                <button onclick="runSecurityScan()" style="background: #339af0; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                    🔍 Scan Ulang
                </button>
                <button onclick="exportSecurityReport()" style="background: #51cf66; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">
                    📥 Export Report
                </button>
            </div>
        </div>
    `;
    
    // Cari tempat untuk menampilkan dashboard
    const container = document.querySelector('.container');
    if (container) {
        const existingDashboard = document.getElementById('securityDashboard');
        if (existingDashboard) {
            existingDashboard.innerHTML = html;
        } else {
            const dashboardDiv = document.createElement('div');
            dashboardDiv.id = 'securityDashboard';
            dashboardDiv.innerHTML = html;
            container.insertBefore(dashboardDiv, container.firstChild);
        }
    }
}

// Fungsi untuk scan ulang
function runSecurityScan() {
    const monitor = SecurityMonitor.getInstance();
    monitor.issues = [];
    monitor.checkSecurityIssues();
    showSecurityDashboard();
    alert('Security scan selesai!');
}

// Fungsi untuk export report
function exportSecurityReport() {
    const monitor = SecurityMonitor.getInstance();
    const report = monitor.getReport();
    
    const dataStr = JSON.stringify(report, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `security-report-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
}

// Aktifkan security monitor
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        SecurityMonitor.getInstance();
        
        // Tambahkan menu security di navbar untuk admin
        setTimeout(() => {
            const userRole = window.currentUser?.role;
            if (userRole === 'admin') {
                const navLinks = document.querySelector('.nav-links');
                if (navLinks) {
                    const securityLink = document.createElement('a');
                    securityLink.href = '#';
                    securityLink.innerHTML = '🔒 Security';
                    securityLink.onclick = (e) => {
                        e.preventDefault();
                        showSecurityDashboard();
                    };
                    securityLink.style.cursor = 'pointer';
                    navLinks.appendChild(securityLink);
                }
            }
        }, 1000);
    });
} else {
    SecurityMonitor.getInstance();
}

// Export untuk penggunaan global
window.SecurityMonitor = SecurityMonitor;
window.showSecurityDashboard = showSecurityDashboard;
window.runSecurityScan = runSecurityScan;
window.exportSecurityReport = exportSecurityReport;