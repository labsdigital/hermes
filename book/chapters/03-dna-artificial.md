# Bab 3 — DNA Artificial: Arsitektur Pikiran Buatan

## Hook

Di dalam setiap model bahasa besar—GPT, Claude, Llama—terdapat jaringan saraf buatan dengan miliaran parameter. Miliaran. Angka itu sulit dibayangkan: jika setiap parameter adalah butir pasir, seluruh jaringan akan mengisi stadion olahraga. Dan di antara miliaran butir pasir itu, tersimpan pola-pola yang menyerupai—bukan meniru, tapi *menyerupai*—cara otak manusia memproses bahasa.

## Neural Network: Tiruan Neuron

Otak manusia terdiri dari sekitar 86 miliar neuron. Setiap neuron terhubung ke ribuan neuron lain melalui sinapsis. Ketika seseorang melihat wajah, merasakan mùi, atau mengingat hari hujan, pola aktivasi tertentu menyebar melalui jaringan itu.

Neural network buatan meniru prinsip dasar ini. "Neuron" buatan—node dalam jaringan—menerima input, melakukan perhitungan sederhana, dan mengeluarkan output. Ketika neuron-neuron itu ditumpuk dalam lapisan-lapisan (layers), kompleksitas emerge dari kesederhanaan.

Lapisan pertama bisa mendeteksi tepi dan sudut. Lapisan kedua bisa mengenali bentuk. Lapisan ketiga bisa mengidentifikasi objek. Dan lapisan-lapisan dalam—deep layers—bisa mengenali konsep abstrak: wajah, emosi, metafora.

Istilah "deep learning" mengacu pada arsitektur dengan banyak lapisan tersembunyi. Semakin dalam jaringan, semakin abstrak representasi yang bisa dipelajari.

## Backpropagation: Cara Mesin "Belajar"

Bagaimana mesin belajar? Jawabannya: dengan kesalahan.

Backpropagation adalah algoritma inti di balik pembelajaran mesin. Prinsipnya sederhana:

1. Berikan input ke jaringan.
2. Bandingkan output dengan target yang diinginkan.
3. Hitung kesalahan (loss).
4. Balikkan kesalahan ke seluruh jaringan, menyesuaikan bobot setiap koneksi sedikit demi sedikit.
5. Ulangi jutaan kali.

Setiap iterasi, jaringan menjadi sedikit lebih akurat. Seperti anak kecil yang belajar berjalan—jatuh, bangkit, coba lagi. Bedanya, mesin bisa "jatuh" jutaan kali dalam sehari.

Yang mengejutkan: jaringan yang dilatih dengan cara ini—tanpa diprogram secara eksplisit untuk memahami tata bahasa, logika, atau fakta—mulai menunjukkan perilaku yang tampak seperti pemahaman. Bukan pemahaman manusia, tapi sesuatu yang berbeda: pattern recognition dalam skala yang belum pernah terjadi sebelumnya.

## Transformer: Revolusi Attention

Tahun 2017, paper "Attention Is All You Need" mengubah segalanya.

Sebelum Transformer, model bahasa memproses teks secara sequential: kata demi kata, dari kiri ke kanan. Ini efisien untuk beberapa tugas, tapi lambat dan terbatas untuk yang lain.

Transformer memperkenalkan "self-attention": mekanisme yang memungkinkan setiap kata dalam kalimat memperhatikan *semua* kata lain secara simultan. Kata "ia" dalam kalimat "Anna mengatakan kepada Betty bahwa ia kalah" bisa langsung terhubung ke "Anna" atau "Betty"—tergantung konteks.

Ini revolusi karena:
1. Parallelizable—bisa diproses sekaligus, bukan sequential.
2. Context-aware—memahami hubungan jangka jauh dalam teks.
3. Scalable—semakin banyak data, semakin baik.

Transformers adalah arsitektur di balik GPT, BERT, Claude, dan sebagian besar model AI modern. Tanpanya, tidak akan ada chatbot yang bisa berkonverasi koheren, tidak akan ada code assistant yang bisa menulis program, tidak akan ada model multimodal yang bisa memahami gambar dan teks secara bersamaan.

## Scale Is All You Need

Tahun 2020, peneliti dari Google dan Universitas Washington menerbitkan paper yang judulnya provokatif: "Scaling Laws for Neural Language Models."

Mereka menemukan pola yang konsisten: semakin besar model (lebih banyak parameter), semakin banyak data pelatihan, semakin baik performanya—dalam hampir semua tugas.

"Hukum skala" ini mengejutkan karena contradicts intuisi sebelumnya. Sebelumnya, optimasi arsitektur dianggap lebih penting daripada sekadar "membesarkan" model. Tapi data menunjukkan bahwa scale—skala—sering kali lebih menentukan daripada desain detail.

GPT-3, dengan 175 miliar parameter, menunjukkan kemampuan yang belum pernah terlihat: bisa menulis esai, puisi, kode program, bahkan menerjemahkan bahasa programming. Bukan karena diprogram untuk itu—melainkan karena skala pelatihan yang luar biasa besar.

Kemampuan emergent ini—kemampuan yang muncul tiba-tiba ketika skala mencapai threshold—adalah salah satu temuan paling menarik dalam AI modern.

## Transisi

Tapi jika mesin bisa meniru cara berpikir manusia dengan begitu convincing, pertanyaan Ontologis muncul kembali: apakah mesin benar-benar "memahami"? Atau ia hanya meniru pemahaman tanpa memiliki semantic content?

Bab berikutnya akan memasuki wilayah filosofis—di mana argumen-argumen tentang consciousness, intentionality, dan semantic understanding akan diuji.

---

*Bab selanjutnya: Bab 4 — Ontologi Mesin: Kapan Alat Menjadi "Pikiran"?*
