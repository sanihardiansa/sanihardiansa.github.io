// Jalankan fungsi ini SEKALI untuk membuat Google Form otomatis
function buatFormPermohonanSurat() {
  const form = FormApp.create('Permohonan Surat RT 04/RW 11 - Kel. Jatihandap');
  form.setDescription(
    'Silakan isi form ini untuk mengajukan permohonan surat keterangan dari RT 04/RW 11.\n' +
    'Surat akan diproses dalam 1x24 jam kerja.\n' +
    'Hubungi pengurus RT jika ada pertanyaan.'
  );
  form.setConfirmationMessage(
    'Terima kasih! Permohonan surat Anda telah diterima.\n' +
    'Pengurus RT akan menghubungi Anda dalam 1x24 jam.'
  );
  form.setAllowResponseEdits(false);
  form.setLimitOneResponsePerUser(false);

  // Pertanyaan 1 - Nama
  form.addTextItem()
    .setTitle('Nama Lengkap')
    .setRequired(true);

  // Pertanyaan 2 - NIK
  const nikItem = form.addTextItem()
    .setTitle('NIK (Nomor Induk Kependudukan)')
    .setHelpText('Masukkan 16 digit NIK sesuai KTP')
    .setRequired(true);
  nikItem.setValidation(
    FormApp.createTextValidation()
      .requireNumberBetween(1000000000000000, 9999999999999999)
      .build()
  );

  // Pertanyaan 3 - No HP
  form.addTextItem()
    .setTitle('Nomor WhatsApp Aktif')
    .setHelpText('Contoh: 08123456789')
    .setRequired(true);

  // Pertanyaan 4 - Jenis Surat
  const jenisSurat = form.addListItem()
    .setTitle('Jenis Surat yang Dimohon')
    .setRequired(true);
  jenisSurat.setChoiceValues([
    'Surat Keterangan Domisili',
    'Surat Keterangan Tidak Mampu',
    'Surat Pengantar KTP',
    'Surat Pengantar KK',
    'Surat Keterangan Usaha',
    'Surat Keterangan Kelahiran',
    'Surat Keterangan Kematian',
    'Surat Keterangan Lainnya',
  ]);

  // Pertanyaan 5 - Tujuan
  form.addTextItem()
    .setTitle('Tujuan Pembuatan Surat')
    .setHelpText('Contoh: Keperluan bank, melamar kerja, dll')
    .setRequired(true);

  // Pertanyaan 6 - Keterangan
  form.addParagraphTextItem()
    .setTitle('Keterangan Tambahan')
    .setHelpText('Isi jika ada informasi tambahan yang perlu disampaikan')
    .setRequired(false);

  // Hubungkan ke Spreadsheet
  const ss = SpreadsheetApp.create('Data Permohonan Surat RT04');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  // Tampilkan link form dan spreadsheet
  const formUrl = form.getPublishedUrl();
  const ssUrl = ss.getUrl();

  Logger.log('✅ Form berhasil dibuat!');
  Logger.log('🔗 Link Form: ' + formUrl);
  Logger.log('📊 Link Spreadsheet: ' + ssUrl);

  // Tampilkan popup
  const ui = SpreadsheetApp.getUi ? SpreadsheetApp.getUi() : null;
  if (ui) {
    ui.alert(
      '✅ Form Berhasil Dibuat!\n\n' +
      'Link Form:\n' + formUrl + '\n\n' +
      'Spreadsheet:\n' + ssUrl
    );
  }

  return { formUrl, ssUrl };
}
