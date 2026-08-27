# Bab 10: Atrofi Moral

*Esai Non-Fiksi | Agustus 2026*

---

## Siapa yang Bertanggung Jawab?

Di pengadilan, jika keputusan dijatuhkan oleh sistem AI, siapa yang bisa dimintai pertanggungjawaban? Di rumah sakit, jika diagnosis salah dibuat oleh algoritma, apakah dokter yang salah, atau programmer yang salah, atau data yang salah?

AI menawarkan efisiensi pengambilan keputusan. Tapi efisiensi ini memindahkan beban moral dari manusia ke mesin. Dan ketika mesin犯错, manusia berhak untuk "tidak tahu."

Ini adalah atrofi moral dalam arti literal: kelelahan kemampuan moral karena tidak digunakan.

Setiap kali kita menyerahkan keputusan etis kepada AI—siapa yang layak mendapatkan pinjaman, siapa yang pantas dapat pekerjaan, siapa yang harus ditahan—kita tidak hanya mengotomatisasi proses. Kita mengotomatisasi akuntabilitas.

Perusahaan teknologi menjual AI sebagai netral. Tapi tidak ada yang netral dalam desain, pelatihan, atau deployemen. Yang ada hanyalah bias yang disembunyikan di balik antarmuka yang bersih.

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img" aria-labelledby="moral-title">
  <title id="moral-title">Atrofi Moral: Pengalihan Tanggung Jawab kepada Algoritma</title>
  
  <rect width="800" height="450" fill="#f8fafc"/>
  
  <!-- Title -->
  <text x="400" y="40" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#1e293b" font-weight="bold">Atrofi Moral</text>
  
  <!-- Decision chain -->
  <g transform="translate(50, 100)">
    <text x="150" y="30" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#475569" font-weight="bold">Rantai Pertanggungjawaban yang Terputus</text>
    
    <!-- Decision points -->
    <rect x="20" y="60" width="100" height="60" rx="8" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
    <text x="70" y="85" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#1e40af">Programmer</text>
    <text x="70" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#64748b">Membuat kode</text>
    
    <rect x="160" y="60" width="100" height="60" rx="8" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
    <text x="210" y="85" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#1e40af">Data Scientist</text>
    <text x="210" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#64748b">Melatih model</text>
    
    <rect x="300" y="60" width="100" height="60" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
    <text x="350" y="85" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#78350f">Manajer</text>
    <text x="350" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#92400e">Deploy sistem</text>
    
    <rect x="440" y="60" width="100" height="60" rx="8" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
    <text x="490" y="85" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#14532d">AI System</text>
    <text x="490" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#166534">Mengambil keputusan</text>
    
    <!-- Broken arrow -->
    <path d="M 540 90 L 600 90" stroke="#ef4444" stroke-width="3" stroke-dasharray="5,5"/>
    <text x="570" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#dc2626">TERPUTUS</text>
    
    <!-- Human victim -->
    <rect x="620" y="60" width="120" height="60" rx="8" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
    <text x="680" y="85" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#dc2626" font-weight="bold">Manusia</text>
    <text x="680" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#991b1b">Korban keputusan</text>
  </g>
  
  <!-- Accountability gap -->
  <g transform="translate(100, 250)">
    <rect x="0" y="0" width="600" height="180" rx="12" fill="#fff7ed" stroke="#fde68a" stroke-width="2"/>
    <text x="300" y="40" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="#78350f" font-weight="bold">Celana Akuntabilitas (Accountability Gap)</text>
    
    <text x="50" y="80" font-family="sans-serif" font-size="14" fill="#475569">• Programmer: "Saya hanya menulis kode."</text>
    <text x="50" y="110" font-family="sans-serif" font-size="14" fill="#475569">• Data Scientist: "Data yang saya gunakan bersih."</text>
    <text x="50" y="140" font-family="sans-serif" font-size="14" fill="#475569">• Manajer: "Saya hanya mengikuti prosedur."</text>
    <text x="50" y="170" font-family="sans-serif" font-size="14" fill="#dc2626" font-weight="bold">→ Tidak ada yang bisa dimintai pertanggungjawaban.</text>
  </g>
</svg>
```

## The Algorithmic Black Box

One of the most troubling aspects of AI decision-making is the "black box" problem. Even the developers of AI systems often cannot explain why a particular decision was made. The neural networks that power modern AI are so complex that their internal decision processes are opaque—even to their creators.

This creates a fundamental accountability gap. When a human judge makes a decision, they can explain their reasoning. When an AI system makes a decision, no one can fully explain why.

This is not merely a technical problem—it is a democratic problem. In a society based on rule of law, decisions that affect people's lives must be explainable dan contestable. When AI systems make irrevocable decisions without transparency, they undermine the very foundations of legal dan moral accountability.

## The Banality of Algorithmic Evil

Hannah Arendt wrote about the "banality of evil"—the idea that great evils are often committed not by monsters, but by ordinary people following rules dan procedures. AI introduces a new form of this banality: the banality of algorithmic evil.

When harmful decisions are made by algorithms, it is easy for humans to deflect responsibility. "The algorithm decided," they say. "I was just following the system." This diffuses accountability across a chain of actors—programmers, managers, executives, users—until no one is left to answer for the harm caused.

The result is a moral vacuum at the center of technological decision-making. A vacuum that is filled not by responsibility, but by abstraction.

## Moral Atrophy as Structural Phenomenon

The atrophy of moral capacity is not just an individual problem—it is a structural one. Societies that delegate moral decisions to algorithms develop institutions that are increasingly incapable of moral reasoning.

Consider the development of autonomous weapons systems. Military planners may argue that AI-driven weapons are more "humane" because they can supposedly distinguish between combatants and civilians better than humans. But this argument assumes that moral judgment can be reduced to pattern recognition—and history suggests that moral judgment is far more complex dan contextual than any algorithm can capture.

The danger is that as we delegate more moral decisions to machines, we lose the practice of making them ourselves. And like any muscle, moral capacity atrophies when not used.

## Reclaiming Moral Agency

The solution is not to reject AI outright, but to insist on human oversight in morally significant decisions. This requires:

- Transparency in AI systems that affect people's lives
- Accountability mechanisms that trace decisions back to human agents
- Legal frameworks that prevent algorithmic decision-making in critical domains
- Public education about the moral implications of AI

Without these safeguards, we risk creating a world where efficiency is prized over ethics, dan where human moral agency is gradually surrendered to machines that cannot share our moral burdens.

The question is not whether AI can make decisions. The question is whether we should let it—and at what cost to our moral capacities.

---

*Kutipan kunci: "Atrofi moral bukan karena manusia menjadi lebih jahat, tapi karena mereka berhenti menggunakan otot moral mereka."*
