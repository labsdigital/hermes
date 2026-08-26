# Bab 3 — DNA Artificial: Arsitektur Pikiran Buatan

## Hook

Di dalam setiap model bahasa besar—GPT-4, Claude 3, Llama 3—terdapat jaringan saraf buatan dengan ratusan miliar parameter. Bayangkan setiap parameter adalah butir pasir. Seluruh jaringan akan mengisi beberapa stadion olahraga. Dan di antara miliaran butir pasir itu, tersimpan pola-pola yang menyerupai—bukan meniru, tapi *menyerupai*—cara otak manusia memproses bahasa,reasoning, dan creativity.

Tapi apa sebenarnya "jaringan saraf" itu? Dan mengapa struktur yang terinspirasi dari biologi bisa menghasilkan perilaku yang tampaknya "pintar"?

## Neural Network: Tiruan Neuron

Otak manusia terdiri dari sekitar 86 miliar neuron. Setiap neuron terhubung ke ribuan neuron lain melalui sinapsis. Ketika seseorang melihat wajah, merasakan mùi, atau mengingat hari hujan, pola aktivasi tertentu menyebar melalui jaringan itu.

Neural network buatan meniru prinsip dasar ini, tapi dengan simplifikasi radical. "Neuron" buatan—disebut juga node atau unit—menerima beberapa input, melakukan perhitungan sederhana (weighted sum + activation function), dan mengeluarkan satu output.

Sederhana? Ya. Tapi ketika jutaan neuron buatan ditumpuk dalam lapisan-lapisan (layers), kompleksitas emerge dari kesederhanaan. Ini adalah prinsip fundamental dalam deep learning: composed simplicity dapat menghasilkan emergent complexity.

Lapisan pertama dalam image recognition network bisa mendeteksi tepi dan sudut. Lapisan kedua bisa mengenali bentuk sederhana seperti lingkaran atau segitiga. Lapisan ketiga bisa mengidentifikasi objek seperti mata, hidung, atau roda. Dan lapisan-lapisan dalam—deep layers—bisa mengenali konsep abstrak: wajah, emosi, metafora.

Istilah "deep learning" mengacu pada arsitektur dengan banyak lapisan tersembunyi. Semakin dalam jaringan, semakin abstrak representasi yang bisa dipelajari. Tapi "deep" juga berarti lebih sulit dilatih—memerlukan lebih banyak data, lebih banyak compute, dan algoritma yang lebih sophisticated.

## Backpropagation: Cara Mesin "Belajar"

Bagaimana mesin belajar? Jawabannya: dengan kesalahan.

Backpropagation adalah algoritma inti di balik pembelajaran mesin modern. Ditemukan secara independent oleh several researchers di tahun 1980-an, algoritma ini elegan dalam kesederhanaannya:

1. Berikan input ke jaringan.
2. Bandingkan output dengan target yang diinginkan.
3. Hitung kesalahan (loss)—berapa jauh prediksi dari reality.
4. Balikkan kesalahan ke seluruh jaringan, menyesuaikan bobot setiap koneksi sedikit demi sedikit.
5. Ulangi jutaan kali.

Setiap iterasi, jaringan menjadi sedikit lebih akurat. Seperti anak kecil yang belajar berjalan—jatuh, bangkit, coba lagi. Bedanya, mesin bisa "jatuh" jutaan kali dalam sehari. Dan karena komputer bisa mengulang dengan kecepatan luar biasa, pembelajaran yang membutuhkan tahun bagi manusia bisa selesai dalam jam bagi mesin.

Yang mengejutkan: jaringan yang dilatih dengan cara ini—tanpa diprogram secara eksplisit untuk memahami tata bahasa, logika, atau fakta—mulai menunjukkan perilaku yang tampak seperti pemahaman. Bukan pemahaman manusia, tapi sesuatu yang berbeda: pattern recognition dalam skala yang belum pernah terjadi sebelumnya.

## Transformer: Revolusi Attention

Tahun 2017, paper "Attention Is All You Need" dari peneliti Google mengubah segalanya.

Sebelum Transformer, model bahasa memproses teks secara sequential: kata demi kata, dari kiri ke kanan. Ini efisien untuk beberapa tugas, tapi lambat dan terbatas untuk yang lain. Memori jangka panjang terbatas—kata-kata di awal kalimat bisa "lupa" saat memproses kata-kata di akhir.

Transformer memperkenalkan "self-attention": mekanisme yang memungkinkan setiap kata dalam kalimat memperhatikan *semua* kata lain secara simultan. Kata "ia" dalam kalimat "Anna mengatakan kepada Betty bahwa ia kalah" bisa langsung terhubung ke "Anna" atau "Betty"—tergantung konteks.

Ini revolusi karena:
1. **Parallelizable**—bisa diproses sekaligus, bukan sequential. Mempercepat training secara signifikan.
2. **Context-aware**—memahami hubungan jangka jauh dalam teks.
3. **Scalable**—semakin banyak data, semakin baik. Tidak ada bottleneck teoritis.

Transformers adalah arsitektur di balik GPT, BERT, Claude, dan sebagian besar model AI modern. Tanpanya, tidak akan ada chatbot yang bisa berkonverasi koheren, tidak akan ada code assistant yang bisa menulis program, tidak akan ada model multimodal yang bisa memahami gambar dan teks secara bersamaan.

## Scale Is All You Need

Tahun 2020, peneliti dari Google dan Universitas Washington menerbitkan paper yang judulnya provokatif: "Scaling Laws for Neural Language Models."

Mereka menemukan pola yang konsisten: semakin besar model (lebih banyak parameter), semakin banyak data pelatihan, semakin baik performanya—dalam hampir semua tugas. Hubungan ini mengikuti power law yang predictible.

"Hukum skala" ini mengejutkan karena contradicts intuisi sebelumnya. Sebelumnya, optimasi arsitektur dianggap lebih penting daripada sekadar "membesarkan" model. Tapi data menunjukkan bahwa scale—skala—sering kali lebih menentukan daripada desain detail.

GPT-3, dengan 175 miliar parameter, menunjukkan kemampuan yang belum pernah terlihat: bisa menulis esai, puisi, kode program, bahkan menerjemahkan bahasa programming. Bukan karena diprogram untuk itu—melainkan karena skala pelatihan yang luar biasa besar.

Kemampuan emergent ini—kemampuan yang muncul tiba-tiba ketika skala mencapai threshold—adalah salah satu temuan paling menarik dalam AI modern. Misalnya, model kecil tidak bisa melakukan few-shot learning (belajar dari sedikit contoh). Tapi model besar bisa. Ini bukan karena fitur ditambahkan secara eksplisit—ia emerg dari scale.

## Multimodal AI

Perkembangan terbaru membawa AI dari text-only ke multimodal. Model seperti GPT-4V, CLIP, dan DALL-E bisa memahami dan generate across multiple modalities: text, image, audio, bahkan video.

Ini bukan sekadar menambahkan capability baru. Ini mengubah nature dari intelligence itu sendiri. Human cognition inherently multimodal—we see, hear, touch, dan process secara simultaneous. AI yang multimodal lebih mendekati cara manusia memahami dunia.

Tapi multimodal juga membawa新的挑战. Bagaimana memastikan consistency across modalities? Bagaimana menghindari hallucination di mana model generate informasi yang plausible tapi salah? Ini adalah area penelitian aktif.

## Limits of Current AI

Meski kemajuan pesat, AI modern memiliki batas fundamental:

1. **No true understanding**—Model memproses patterns, bukan meanings. Mereka tidak "tahu" apa itu appfel—mereka tahu appfel berkorelasi dengan kata-kata tertentu dalam konteks tertentu.

2. **No embodiment**—AI tidak memiliki tubuh, tidak memiliki sensory-motor experience. Ini membatasi pemahaman mereka tentang dunia fisik.

3. **No persistent memory**—Setiap interaction adalah stateless. AI tidak "ingat" conversations sebelumnya kecuali di dalam context window.

4. **No intrinsic motivation**—AI tidak memiliki goals sendiri. Mereka mengoptimalkan objective function yang diberikan, bukan desires yang emerge dari embodiment.

Batasan-batasan ini penting untuk diingat. Mereka mencegah anthropomorphization yang naif—kecenderungan untuk menganggap AI sebagai entitas yang "pikir" atau "merasakan" seperti manusia.

## Transisi

Tapi jika mesin bisa meniru cara berpikir manusia dengan begitu convincing, pertanyaan Ontologis muncul kembali: apakah mesin benar-benar "memahami"? Atau ia hanya meniru pemahaman tanpa memiliki semantic content?

Bab berikutnya akan memasuki wilayah filosofis—di mana argumen-argumen tentang consciousness, intentionality, dan semantic understanding akan diuji.

---

*Bab selanjutnya: Bab 4 — Ontologi Mesin: Kapan Alat Menjadi "Pikiran"?*
