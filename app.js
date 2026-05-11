let wargaData = [];
let filteredData = [];

loadData();

async function loadData() {
    try {
        const response = await fetch('data.json');
        wargaData = await response.json();
        filteredData = wargaData;
        console.log('Loaded:', wargaData.length, 'warga');
        updateDashboard();
        renderTable();
    } catch (error) {
        console.error('Error:', error);
    }
}

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
    document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
    event.target.classList.add('active');
}

function updateDashboard() {
    const total = wargaData.length;
    const kk = wargaData.filter(w => w.kedudukan && w.kedudukan.includes('Kepala')).length;
    const male = wargaData.filter(w => w.jenisKelamin === 'L').length;
    const female = wargaData.filter(w => w.jenisKelamin === 'P').length;

    document.getElementById('totalWarga').textContent = total;
    document.getElementById('totalKK').textContent = kk;
    document.getElementById('lakilaki').textContent = male;
    document.getElementById('perempuan').textContent = female;

    // Age groups
    const ageGroups = {'0-17': 0, '18-30': 0, '31-45': 0, '46-60': 0, '60+': 0};
    wargaData.forEach(w => {
        if (w.usia) {
            if (w.usia <= 17) ageGroups['0-17']++;
            else if (w.usia <= 30) ageGroups['18-30']++;
            else if (w.usia <= 45) ageGroups['31-45']++;
            else if (w.usia <= 60) ageGroups['46-60']++;
            else ageGroups['60+']++;
        }
    });
    renderChart('ageChart', Object.entries(ageGroups).map(([k, v]) => ({label: k + ' tahun', value: v})));

    // Jobs
    const jobs = {};
    wargaData.forEach(w => {
        const job = w.pekerjaan || 'Tidak Diketahui';
        jobs[job] = (jobs[job] || 0) + 1;
    });
    const topJobs = Object.entries(jobs).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k, v]) => ({label: k, value: v}));
    renderChart('jobChart', topJobs);

    // Agama
    const agama = {};
    wargaData.forEach(w => {
        const ag = w.agama || 'Tidak Diketahui';
        agama[ag] = (agama[ag] || 0) + 1;
    });
    renderChart('agamaChart', Object.entries(agama).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({label: k, value: v})));

    // Pendidikan
    const pendidikan = {};
    wargaData.forEach(w => {
        const pend = w.pendidikan || 'Tidak Diketahui';
        pendidikan[pend] = (pendidikan[pend] || 0) + 1;
    });
    renderChart('pendidikanChart', Object.entries(pendidikan).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([k, v]) => ({label: k, value: v})));

    // Status Alamat
    const statusAlamat = {};
    wargaData.forEach(w => {
        const status = w.statusAlamat || 'Tidak Diketahui';
        statusAlamat[status] = (statusAlamat[status] || 0) + 1;
    });
    renderChart('statusAlamatChart', Object.entries(statusAlamat).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({label: k, value: v})));

    // Keterangan
    const keterangan = {};
    wargaData.forEach(w => {
        const ket = w.keterangan || '';
        if (ket && ket !== 'nan') {
            keterangan[ket] = (keterangan[ket] || 0) + 1;
        }
    });
    if (Object.keys(keterangan).length > 0) {
        renderChart('keteranganChart', Object.entries(keterangan).sort((a, b) => b[1] - a[1]).map(([k, v]) => ({label: k, value: v})));
    } else {
        document.getElementById('keteranganChart').innerHTML = '<p style="color:#999;">Tidak ada keterangan</p>';
    }
}

function renderChart(elementId, data) {
    const max = Math.max(...data.map(d => d.value), 1);
    const html = data.map(d => `
        <div class="chart-bar">
            <div class="chart-label">${d.label}</div>
            <div class="chart-bar-bg">
                <div class="chart-bar-fill" style="width: ${(d.value/max*100)}%">${d.value}</div>
            </div>
        </div>
    `).join('');
    document.getElementById(elementId).innerHTML = html;
}

function renderTable() {
    const tbody = document.querySelector('#wargaTable tbody');
    tbody.innerHTML = filteredData.map((w, i) => `
        <tr>
            <td>${i + 1}</td>
            <td>${w.nama}</td>
            <td>${w.jenisKelamin || '-'}</td>
            <td>${w.usia || '-'}</td>
            <td>${w.nik}</td>
            <td>${w.noKK}</td>
            <td>${w.alamat}</td>
            <td>${w.kedudukan}</td>
            <td>${w.pekerjaan}</td>
            <td>${w.noHP || '-'}</td>
        </tr>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('search').addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        if (query === '') {
            filteredData = wargaData;
        } else {
            filteredData = wargaData.filter(w =>
                w.nama.toLowerCase().includes(query) ||
                w.nik.includes(query) ||
                w.alamat.toLowerCase().includes(query) ||
                w.noKK.includes(query)
            );
        }
        renderTable();
    });
});
