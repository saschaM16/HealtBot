<?php
require_once '../includes/db.php';

$page_title = "Asisten Informasi Kesehatan";

// Array Tips Kesehatan Harian Acak
$health_tips = [
    "Minum setidaknya 8 gelas air (sekitar 2 liter) sehari untuk menjaga organ tubuh terhidrasi secara optimal.",
    "Lakukan peregangan ringan selama 5 menit untuk setiap 1 jam Anda duduk bekerja di depan komputer.",
    "Tidur malam selama 7-8 jam secara teratur dapat membantu perbaikan jaringan tubuh dan menjaga imun.",
    "Isi piring Anda dengan porsi seimbang: setengah sayur & buah, seperempat karbohidrat, dan seperempat protein.",
    "Batasi konsumsi gula berlebih untuk menghindari risiko obesitas dan diabetes melitus tipe 2.",
    "Olahraga jalan kaki cepat selama 30 menit sehari dapat menurunkan risiko penyakit jantung secara signifikan.",
    "Sempatkan bernapas dalam atau meditasi selama 10 menit di sela kesibukan untuk meredakan stres harian.",
    "Jauhkan smartphone Anda setidaknya 30 menit sebelum tidur agar otak siap beristirahat dengan nyenyak."
];

// Memilih tips secara acak
$random_tip = $health_tips[array_rand($health_tips)];

require_once '../includes/header.php';
?>

<!-- Hero Section -->
<section class="hero">
    <div class="container">
        <div class="hero-grid">
            <div class="hero-content fade-in-up">
                <div class="hero-badge">
                    <i class="fa-solid fa-circle-check"></i> Asisten Kesehatan Berbasis Artificial Intelligence
                </div>
                <h1 class="hero-title">Health<span>Bot</span>: Asisten Informasi Kesehatan</h1>
                <p class="hero-desc">
                    Mulai hidup lebih sehat dari sekarang. HealthBot membantu Anda menemukan informasi pola hidup, tips gizi harian, menghitung berat badan ideal, dan memberikan saran pertolongan pertama penyakit ringan secara interaktif.
                </p>
                <div class="hero-actions">
                    <a href="chat.php" class="btn-primary">
                        <i class="fa-solid fa-comments"></i> Mulai Konsultasi
                    </a>
                    <a href="bmi.php" class="btn-secondary">
                        <i class="fa-solid fa-calculator"></i> Hitung BMI
                    </a>
                </div>
            </div>
            <div class="hero-image">
                <div class="hero-circle-bg"></div>
                <!-- Image will be generated or fell back to SVG if not loaded -->
                <img src="../assets/images/hero_illustration.png" alt="HealthBot Assistant" onerror="this.onerror=null; this.src='https://illustrations.pixeden.com/images/free-medical-icon-set-pixeden-preview.jpg'; this.style.borderRadius='var(--radius-xl)';">
            </div>
        </div>
    </div>
</section>

<!-- Random Tips Section -->
<section class="tips-section">
    <div class="container">
        <div class="tips-box fade-in-up">
            <div class="tips-icon">
                <i class="fa-solid fa-lightbulb"></i>
            </div>
            <div class="tips-content">
                <h3>Tips Kesehatan Hari Ini</h3>
                <p>"<?php echo htmlspecialchars($random_tip); ?>"</p>
            </div>
        </div>
    </div>
</section>

<!-- Medical Categories Section -->
<section class="categories-section">
    <div class="container">
        <div class="section-header">
            <span class="section-subtitle">Kategori Informasi</span>
            <h2 class="section-title">Telusuri Panduan Kesehatan Dasar</h2>
        </div>
        
        <div class="category-grid">
            <!-- Pola Hidup Sehat -->
            <div class="category-card">
                <div class="cat-icon-container">
                    <i class="fa-solid fa-heart"></i>
                </div>
                <h3>Pola Hidup Sehat</h3>
                <p>Panduan membiasakan gaya hidup seimbang, manajemen stres, pemenuhan kebutuhan cairan harian, serta pencegahan penyakit kronis sejak dini.</p>
            </div>
            
            <!-- Makanan Bergizi -->
            <div class="category-card">
                <div class="cat-icon-container">
                    <i class="fa-solid fa-apple-whole"></i>
                </div>
                <h3>Makanan Bergizi</h3>
                <p>Informasi zat gizi makro dan mikro, porsi piring makan seimbang, rekomendasi diet sehat, serta cara membatasi garam, gula, dan lemak.</p>
            </div>
            
            <!-- Olahraga Teratur -->
            <div class="category-card">
                <div class="cat-icon-container">
                    <i class="fa-solid fa-dumbbell"></i>
                </div>
                <h3>Olahraga & Aktivitas Fisik</h3>
                <p>Tips memilih jenis olahraga cardio atau beban yang aman, intensitas latihan yang dianjurkan mingguan, dan cara tetap aktif bergerak.</p>
            </div>
            
            <!-- Tidur Cukup -->
            <div class="category-card">
                <div class="cat-icon-container">
                    <i class="fa-solid fa-bed"></i>
                </div>
                <h3>Tidur yang Cukup</h3>
                <p>Pentingnya istirahat berkualitas 7-9 jam, cara mengatasi insomnia, memahami ritme sirkadian tubuh, serta bahaya kebiasaan sering begadang.</p>
            </div>
            
            <!-- Tips Menjaga Kesehatan Tubuh -->
            <div class="category-card">
                <div class="cat-icon-container">
                    <i class="fa-solid fa-hand-holding-medical"></i>
                </div>
                <h3>Tips Kesehatan Tubuh</h3>
                <p>Rangkaian tips praktis sehari-hari menjaga imun tubuh seperti cara mencuci tangan yang benar dan menjaga sanitasi lingkungan.</p>
            </div>
            
            <!-- Penyakit Ringan -->
            <div class="category-card">
                <div class="cat-icon-container">
                    <i class="fa-solid fa-capsules"></i>
                </div>
                <h3>Informasi Penyakit Ringan</h3>
                <p>Penjelasan gejala, pertolongan pertama, obat bebas yang diizinkan, serta batasan konsultasi mandiri untuk demam, flu, batuk, pusing, dan maag.</p>
            </div>
        </div>
    </div>
</section>

<?php
require_once '../includes/footer.php';
?>
