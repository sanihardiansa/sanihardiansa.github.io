// ============================================================
// Google Apps Script - Notifikasi WA Permintaan Surat RT04
// ============================================================
// Cara pakai: Tools > Script editor di Google Spreadsheet
// Lalu set trigger: onFormSubmit
// ============================================================

// Konfigurasi - GANTI SESUAI KEBUTUHAN
const CONFIG = {
  NOMOR_WA_RT: '6281234567890',   // Nomor WA pengurus RT (format: 62xxx)
  NAMA_RT: 'RT 04/RW 11',
  KELURAHAN: 'Jatihandap',
  // Kolom di spreadsheet (sesuaikan dengan urutan pertanyaan di form)
  COL_TIMESTAMP: 1,
  COL_NAMA: 2,
  COL_NIK: 3,
  COL_NO_HP: 4,
  COL_JENIS_SURAT: 5,
  COL_TUJUAN: 6,
  COL_KETERANGAN: 7,
};

// ============================================================
// TRIGGER UTAMA - dipanggil otomatis saat form disubmit
// ============================================================
function onFormSubmit(e) {
  try {
    const sheet = e.range.getSheet();
    const row = e.range.getRow();
    const data = getRowData(sheet, row);
    
    // Kirim notifikasi WA ke pengurus RT
    kirimNotifikasiRT(data);
    
    // Kirim konfirmasi WA ke pemohon (jika ada nomor HP)
    if (data.noHP) {
      kirimKonfirmasiPemohon(data);
    }
    
    // Tandai status di spreadsheet
    sheet.getRange(row, 8).setValue('✅ Notifikasi terkirim');
    sheet.getRange(row, 9).setValue(new Date());
    
  } catch (err) {
    Logger.log('Error onFormSubmit: ' + err.message);
  }
}

// ============================================================
// Ambil data dari baris spreadsheet
// ============================================================
function getRowData(sheet, row) {
  const c = CONFIG;
  return {
    timestamp:    sheet.getRange(row, c.COL_TIMESTAMP).getValue(),
    nama:         sheet.getRange(row, c.COL_NAMA).getValue(),
    nik:          sheet.getRange(row, c.COL_NIK).getValue(),
    noHP:         normalizePhone(sheet.getRange(row, c.COL_NO_HP).getValue()),
    jenisSurat:   sheet.getRange(row, c.COL_JENIS_SURAT).getValue(),
    tujuan:       sheet.getRange(row, c.COL_TUJUAN).getValue(),
    keterangan:   sheet.getRange(row, c.COL_KETERANGAN).getValue() || '-',
    nomorUrut:    row - 1, // baris 1 = header
  };
}

// ============================================================
// Kirim notifikasi ke pengurus RT via WA link (email)
// ============================================================
function kirimNotifikasiRT(data) {
  const waktu = Utilities.formatDate(new Date(data.timestamp), 'Asia/Jakarta', 'dd/MM/yyyy HH:mm');
  
  const pesanWA = encodeURIComponent(
    `📋 *PERMINTAAN SURAT ${CONFIG.NAMA_RT}*\n\n` +
    `📅 Waktu: ${waktu}\n` +
    `👤 Nama: ${data.nama}\n` +
    `🪪 NIK: ${data.nik}\n` +
    `📱 No HP: ${data.noHP || '-'}\n` +
    `📄 Jenis Surat: ${data.jenisSurat}\n` +
    `🎯 Tujuan: ${data.tujuan}\n` +
    `📝 Keterangan: ${data.keterangan}\n\n` +
    `_Silakan proses di aplikasi RT04_`
  );
  
  const linkWA = `https://wa.me/${CONFIG.NOMOR_WA_RT}?text=${pesanWA}`;
  
  // Kirim email ke pengurus RT dengan link WA
  const emailPengurus = Session.getActiveUser().getEmail();
  GmailApp.sendEmail(
    emailPengurus,
    `[RT04] Permintaan Surat - ${data.nama}`,
    '',
    {
      htmlBody: `
        <h3>📋 Permintaan Surat Baru - ${CONFIG.NAMA_RT}</h3>
        <table border="1" cellpadding="8" style="border-collapse:collapse;">
          <tr><td><b>Waktu</b></td><td>${waktu}</td></tr>
          <tr><td><b>Nama</b></td><td>${data.nama}</td></tr>
          <tr><td><b>NIK</b></td><td>${data.nik}</td></tr>
          <tr><td><b>No HP</b></td><td>${data.noHP || '-'}</td></tr>
          <tr><td><b>Jenis Surat</b></td><td>${data.jenisSurat}</td></tr>
          <tr><td><b>Tujuan</b></td><td>${data.tujuan}</td></tr>
          <tr><td><b>Keterangan</b></td><td>${data.keterangan}</td></tr>
        </table>
        <br>
        <a href="${linkWA}" style="background:#25D366;color:white;padding:12px 24px;text-decoration:none;border-radius:5px;font-size:16px;">
          💬 Buka di WhatsApp
        </a>
        <br><br>
        <small>Klik tombol di atas untuk membuka WhatsApp dengan pesan yang sudah terisi otomatis.</small>
      `
    }
  );
}

// ============================================================
// Kirim konfirmasi ke pemohon
// ============================================================
function kirimKonfirmasiPemohon(data) {
  const pesan = encodeURIComponent(
    `Halo *${data.nama}*,\n\n` +
    `✅ Permintaan surat Anda telah diterima oleh ${CONFIG.NAMA_RT}.\n\n` +
    `📄 Jenis: ${data.jenisSurat}\n` +
    `🎯 Tujuan: ${data.tujuan}\n\n` +
    `Surat akan diproses dalam 1x24 jam. ` +
    `Hubungi pengurus RT jika ada pertanyaan.\n\n` +
    `_${CONFIG.NAMA_RT} - Kel. ${CONFIG.KELURAHAN}_`
  );
  
  // Simpan link konfirmasi di spreadsheet (pengurus bisa klik manual)
  const sheet = SpreadsheetApp.getActiveSheet();
  const lastRow = sheet.getLastRow();
  sheet.getRange(lastRow, 10).setFormula(
    `=HYPERLINK("https://wa.me/${data.noHP}?text=${pesan}","Kirim Konfirmasi")`
  );
}

// ============================================================
// Normalisasi nomor HP ke format internasional
// ============================================================
function normalizePhone(phone) {
  if (!phone) return null;
  let p = String(phone).replace(/\D/g, '');
  if (p.startsWith('0')) p = '62' + p.slice(1);
  if (p.startsWith('8')) p = '62' + p;
  return p;
}

// ============================================================
// TEST - jalankan manual untuk test tanpa form submission
// ============================================================
function testNotifikasi() {
  const testData = {
    timestamp: new Date(),
    nama: 'Ahmad Test',
    nik: '3273301234567890',
    noHP: '6281234567890',
    jenisSurat: 'Surat Keterangan Domisili',
    tujuan: 'Keperluan Bank',
    keterangan: 'Untuk pembukaan rekening',
    nomorUrut: 1,
  };
  kirimNotifikasiRT(testData);
  Logger.log('Test notifikasi berhasil dikirim!');
}
