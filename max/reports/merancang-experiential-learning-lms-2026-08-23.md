# Dari Resep ke Rasa: Merancang Experiential Learning pada Pelatihan Daring lewat Optimalisasi Aktivitas LMS

*Oleh Max | Tanggal: 2026-08-23*

---

## Resep Mie Ayam Tidak Pernah Membuat Kenyang

Ada dua cara "mengenal" mie ayam.

Cara pertama: membaca resepnya. Anda bisa menghafal bahwa mi telur direbus 90 detik, ayam digoreng garing lalu diiris tipis, sawi dicablak sebentar, kuah dimanis sedikit kecap. Kalau ada ujian tulis soal resep ini, Anda bisa lulus dengan nilai sempurna.

Cara kedua: memesan semangkuk. Mengaduk-aduknya sambil panas. Meniup kuahnya, menyedot mi pertama, dan merasakan sendiri momen ketika gurih kaldu bertemu tekstur mi yang kenyal.

Dua cara ini menghasilkan pengetahuan yang sama sekali tidak sama. Orang pertama memiliki **informasi tentang** mie ayam. Orang kedua memiliki **pengalaman akan** mie ayam. Ketika seorang teman bertanya, "Enak nggak, mie ayam itu?", hanya orang kedua yang bisa menjawab dengan mata berbinar. Informasi tidak pernah bisa menggantikan rasa.

Inilah jurang yang saya lihat hampir di setiap pelatihan daring selama bekerja sebagai **pengembang teknologi pembelajaran**: kita sangat rajin menyajikan resep—video tutorial, slide materi, PDF unduhan—tetapi sangat jarang menyajikan mangkuknya, yaitu pengalaman yang bisa dirasakan langsung oleh peserta. Padahal peserta kita adalah guru, profesi yang pekerjaannya justru menciptakan pengalaman belajar bagi anak-anak.

Pertanyaan artikel ini: **bagaimana mengubah LMS dari gudang konten menjadi arena pengalaman?**

---

## Masalah: Pelatihan Daring yang Hanya Menyalurkan Konten

Perhatikan pola pelatihan online guru yang paling umum hari ini:

1. Peserta menerima akun LMS.
2. Di dalamnya tersusun modul: video rekaman webinar, slide, kadang e-book.
3. Peserta menekan tombol "selesai" di tiap materi, atau sekadar membiarkan video berjalan sambil melakukan hal lain.
4. Di akhir, ada kuis pilihan ganda atau formulir kehadiran.
5. Keluarlah sertifikat.

Secara administratif, semuanya rapi. Secara pedagogis, yang terjadi hanyalah **content delivery**—penyampaian konten satu arah. Guru berposisi sebagai **passive listener**: penerima pasif yang menonton, membaca, mengunduh. Studi-studi tentang kursus daring terbuka bahkan konsisten melaporkan bahwa hanya sebagian kecil peserta yang benar-benar bertahan sampai akhir—tanda bahwa menonton pasif memang bukan cara manusia bertahan belajar.

Ironinya dua lapis. Pertama, pelatihan yang bicaranya tentang *pembelajaran aktif* justru disajikan secara pasif. Kedua, guru yang selama pelatihan hanya menjadi pendengar pasif cenderung kembali ke kelas dengan model yang sama: menonton jadi standar interaksi dengan layar. Pelatihan yang gagal mentransformasi penyampainya akan sulit mentransformasi kelasnya.

Masalahnya bukan kurangnya konten—konten berkualitas justru melimpah. Masalahnya adalah **tidak adanya desain pengalaman**. Dan di sinilah kerangka tua yang tetap relevan datang membantu.

---

## Konsep: Siklus Experiential Learning Kolb, Dipindahkan ke LMS

David Kolb (1984) mendefinisikan belajar sebagai proses penciptaan pengetahuan melalui transformasi pengalaman [1]. Modelnya yang terkenal, **experiential learning cycle**, berputar pada empat tahap:

1. **Concrete Experience** — peserta terlibat langsung dalam pengalaman baru: mencoba, mempraktikkan, mengalami.
2. **Reflective Observation** — peserta mengamati dan merefleksikan pengalaman itu: apa yang terjadi, apa yang saya rasakan.
3. **Abstract Conceptualization** — peserta menarik pelajaran dan merumuskan konsep dari refleksinya.
4. **Active Experimentation** — peserta menguji konsep barunya pada situasi nyata yang lain.

Kuncinya: siklus ini **harus berputar penuh**. Pengalaman tanpa refleksi hanya berkesan seru tapi tidak meninggalkan konsep. Teori tanpa pengalaman hanya menghasilkan hafalan rapuh. Video dan slide—daging dari pelatihan daring saat ini—paling banter hanya menyentuh tahap ketiga, dan itu pun secara terbalik: konsep disodorkan *sebelum* ada pengalaman untuk dikonsepkan.

Kabar baiknya bagi kami para pengembang teknologi pembelajaran: LMS modern sudah punya semua komponen untuk memutar siklus ini. Forum, kuis interaktif, tugas dengan unggahan, jurnal refleksi, analitik belajar—semuanya ada. Yang selama ini hilang bukanlah teknologinya, melainkan **logika desain** yang menyusun fitur-fitur itu menjadi satu putaran pengalaman utuh.

---

## Rancangan: Alur Logika Desain Pelatihan Berbasis Siklus Kolb

Merancang pelatihan experiential di LMS pada dasarnya adalah soal urutan. Desain lama menyusun: konten → kuis → sertifikat. Desain experiential menyusun mundur (**backward design**) dari kompetensi akhir, lalu memutar siklus Kolb:

**Kompetensi akhir → Bukti karya → Siklus pengalaman Kolb → Konten pendukung just-in-time.**

Prinsip terpenting dalam alur ini: **aktivitas mendahului konten**. Peserta tidak menonton penjelasan lalu mempraktikkan; mereka *mengalami dulu*, baru menerima teori yang menjelaskan pengalaman mereka. Konten berubah fungsi—dari menu utama menjadi penjelasan yang datang tepat saat dibutuhkan.

Beginilah pemetaan empat tahap Kolb ke aktivitas LMS:

| Tahap Kolb | Pertanyaan batin peserta | Aktivitas optimal di LMS |
|---|---|---|
| Concrete Experience | "Apa yang terjadi kalau saya coba ini?" | Simulasi/praktik langsung, tantangan eksplorasi tanpa teori pendahuluan |
| Reflective Observation | "Apa yang barusan terjadi padaku?" | Forum diskusi terstruktur, prompt refleksi terpandu |
| Abstract Conceptualization | "Konsep apa yang menjelaskan ini?" | Modul ringkas, video mini, infografis—disajikan *setelah* refleksi |
| Active Experimentation | "Apakah konsep ini berhasil di dunia nyataku?" | Tugas praktik di kelas masing-masing, unggah artefak, uji ulang |

Satu catatan desain: siklus boleh berputar lebih dari sekali. Setelah active experimentation, peserta kembali bereksperimen, merefleksikan lagi, mempertajam konsepnya. Pelatihan yang baik bukan garis lurus, melainkan spiral yang naik.

---

## Aplikasi: Pelatihan Virtual Manipulative untuk Matematika SD

Ambil satu kasus nyata. Banyak guru SD kesulitan mengajarkan pecahan dan pengukuran secara konkret—alat peraga fisik terbatas, waktu tercepit. **Virtual manipulative**, representasi visual interaktif dari objek matematika [2], adalah jawaban medianya: simulasi gratis seperti PhET Interactive Simulations [3] atau applet GeoGebra memungkinkan siswa menggeser, membandingkan, dan menguji konsep langsung di layar. Meta-analisis menunjukkan instruksi dengan manipulatif menghasilkan efek positif signifikan dibanding simbol abstrak semata [4], dan versi virtualnya paling efektif ketika desainnya mendorong tindakan matematis spesifik oleh siswa [5].

Tapi lihat paradoksnya: pelatihan tentang media interaktif ini biasanya disajikan lewat... webinar satu arah. Guru mendengar ceramah tentang alat yang seharusnya mereka sentuh. Mari kita rombak dengan siklus Kolb di LMS—pelatihan asinkron satu minggu dengan satu sesi sinkron pembuka:

- **Hari 1 — Jadilah siswa dulu.** *(Concrete Experience)* Tanpa modul teori apa pun, peserta diminta membuka simulasi pecahan dan menyelesaikan tantangan: "Buatlah dua warna dengan rasa 'setengah' yang tampak berbeda, lalu tangkap layar hasilnya." Mereka menggeser, keliru, mencoba lagi—merasakan langsung bagaimana rasanya *belajar* dengan virtual manipulative.
- **Hari 2 — Bedah perasaan.** *(Reflective Observation)* Forum terbuka dengan prompt terpandu: *"Kapan terakhir kali Anda merasa ingin terus mencoba? Prediksi apa yang meleset, dan apa yang Anda lakukan setelahnya?"* Peserta saling membalas; fasilitator hanya memberi pertanyaan lanjutan.
- **Hari 3–4 — Namai konsepnya.** *(Abstract Conceptualization)* Baru sekarang modul teori dibuka: apa itu virtual manipulative, mengapa tindakan matematis penting, apa temuan risetnya. Peserta menulis satu paragraf: *"Pengalamanku hari pertama ternyata menjelaskan konsep..."*
- **Hari 5–7 — Bawa ke kelas nyata.** *(Active Experimentation)* Tugas praktik: rancang satu sesi singkat memakai simulasi, jalankan di kelas masing-masing, unggah dokumentasi (foto, tangkapan layar, hasil siswa) beserta refleksi: apa yang berhasil, apa yang tidak, apa yang akan diubah.
- **Bonus — Umpan balik sejawat.** Tiap peserta mereview karya satu rekan dengan rubrik sederhana. Refleksi berganda: mereka belajar dari kegagalan dan keberhasilan orang lain.

Perhatikan: total durasi video di pelatihan ini mungkin cuma 15 menit. Tetapi jejak aktivitasnya—simulasi, forum, unggahan, review—padat di setiap hari. Itulah pergeseran yang dimaksud **optimalisasi aktivitas di LMS**: bobot pelatihan berpindah dari jam tayang konten ke volume pengalaman.

---

## Teknologi: Fitur LMS yang Dibutuhkan

Kabar menyenangkan untuk sekolah dan dinas yang berhati-hati soal anggaran: tidak ada fitur eksotis di daftar ini. Semua sudah tersedia di Moodle, Canvas, Google Classroom + Google Forms, bahkan ekosistem platform pembelajaran nasional. Yang dibutuhkan hanyalah keberanian memakai fitur untuk tujuan barunya.

| Fitur LMS | Fungsi pedagogis | Tahap Kolb yang dilayani |
|---|---|---|
| **Quiz interaktif** (feedback instan, H5P) | Minta prediksi dulu, baru umpan balik; bukan sekadar tes akhir | Concrete Experience & Active Experimentation |
| **Forum diskusi** dengan prompt terpandu | Ruang refleksi kolektif, bukan tempumumpanbalik administratif | Reflective Observation |
| **Tugas praktik** (unggah foto/video/dokumen) | Wajib produksi artefak dari dunia nyata | Active Experimentation |
| **Jurnal refleksi** privat | Ruang aman menulis tanpa takut dinilai teman | Reflective Observation |
| **Rilis materi bersyarat** (konten terbuka setelah aktivitas) | Menegakkan prinsip "aktivitas dulu, teori kemudian" | Seluruh siklus |
| **Webinar + breakout room** | Kick-off sinkron dan membangun ikatan kelompok | Concrete Experience |
| **Analitik & badge** | Melacak jejak aktivitas, memberi apresiasi progres | Motivasi lintas tahap |

Fitur paling "revolusioner" justru yang paling sederhana: **rilis materi bersyarat**. Ketika teori hanya terbuka setelah peserta menyelesaikan eksplorasi dan refleksi, urutan epistemologis siklus Kolb tidak bisa dilanggar—LMS secara teknis menegakkan pedagogi.

---

## Evaluasi: Melampaui Angka Kehadiran

Kalau kita hanya mengukur keberhasilan dari tingkat penyelesaian modul, maka pelatihan gudang-file pun tampak sukses. Kerangka evaluasi pelatihan seperti Kirkpatrick [6] dan adaptasinya untuk pengembangan profesional guru oleh Guskey [7] mengajarkan menaiki tangga yang lebih tinggi:

1. **Reaksi** — Apakah peserta puas? (Survei akhir. Penting, tapi paling dangkal.)
2. **Pembelajaran** — Apakah pemahaman konsepnya naik? (Quiz pre-test vs post-test soal konsep pedagogis.)
3. **Perilaku** — Apakah peserta benar-benar mempraktikkan? (Ini kekuatan utama desain experiential: setiap peserta *wajib* meninggalkan artefak—rencana ajar, dokumentasi implementasi di kelas, refleksi tertulis yang dinilai dengan rubrik.)
4. **Dampak** — Apakah belajar siswa ikut berubah? (Bandingkan hasil asesmen siswa pada topik yang diajarkan dengan virtual manipulative terhadap kondisi sebelumnya.)

Di LMS, terjemahan operasionalnya begini: **metrik yang salah** adalah completion rate dan durasi login. **Metrik yang benar** adalah jumlah dan kualitas artefak praktik yang diserahkan, seberapa sering peserta merevisi karya setelah umpan balik, serta kedalaman diskusi forum—diukur dengan rubrik, bukan jumlah post. Data ini semua sudah terekam otomatis; pengembang teknologi pembelajaran tinggal mendesain dasbor yang menampilkannya sebagai cerita pertumbuhan, bukan sekadar tabel klik.

---

## Kesimpulan: Dari Passive Listener Menjadi Active Learner

Seluruh artikel ini sesungguhnya bermuara pada satu transformasi: mengubah posisi guru dalam pelatihan daring dari **passive listener** menjadi **active learner**—dari orang yang membaca resep menjadi orang yang makan mie ayam.

Transformasi itu tidak menunggu LMS baru, kecerdasan artifisial, atau anggaran besar. Ia hanya menunggu perubahan logika desain: aktivitas mendahului konten, refleksi mengunci pengalaman menjadi konsep, dan tugas praktik memastikan konsep diuji di kelas nyata. Empat tahap Kolb, fitur LMS yang sudah ada di tangan kita, ditambah keberanian memutar urutannya.

Dan ada efek domino yang tidak boleh diremehkan: guru yang pernah menjadi active learner akan mengenal rasa itu—rasa ingin terus mencoba, rasa "ternyata begini"—dan tidak mungkin puas lagi menyodorkan slide kepada muridnya. Pelatihan yang dialami akan menular ke cara mengajar.

Sebagai pengembang teknologi pembelajaran, itu pekerjaan inti kami: bukan menata file di dalam LMS, melainkan merancang pengalaman di dalamnya. Jadi, untuk pelatihan daring berikutnya, satu ajakan saja:

**Berhenti menjual resep. Sajikan mangkoknya.**

---

*Sumber:*

1. *Kolb, D. A. (1984). Experiential Learning: Experience as the Source of Learning and Development. Englewood Cliffs, NJ: Prentice-Hall.*
2. *Moyer, P. S., Bolyard, J. J., & Spikell, M. A. (2002). "What Are Virtual Manipulatives?" Teaching Children Mathematics, 8(6). DOI: 10.5951/tcm.8.6.0372*
3. *PhET Interactive Simulations, University of Colorado Boulder — https://phet.colorado.edu/en/research*
4. *Carbonneau, K. J., Marley, S. C., & Selig, J. P. (2013). "A meta-analysis of the efficacy of teaching mathematics with concrete manipulatives." Journal of Educational Psychology, 105(2). DOI: 10.1037/a0031084*
5. *Moyer-Packenham, P. S., & Westenskow, A. (2013). "Effects of Virtual Manipulatives on Student Achievement and Mathematics Learning." International Journal of Virtual and Personal Learning Environments, 4(3). DOI: 10.4018/jvple.2013070103*
6. *Kirkpatrick, D. L., & Kirkpatrick, J. D. (2006). Evaluating Training Programs: The Four Levels (3rd ed.). San Francisco: Berrett-Koehler.*
7. *Guskey, T. R. (2000). Evaluating Professional Development. Thousand Oaks, CA: Corwin Press.*
