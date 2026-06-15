<?php
require_once '../includes/db.php';

$page_title = "Tentang Kami";

require_once '../includes/header.php';
?>

<div class="container">
    <section class="about-section">
        <div class="about-card fade-in-up">
            <h2><i class="fa-solid fa-circle-info"></i> Tentang HealthBot</h2>
            <div class="about-text">
                <p>
                    <strong>HealthBot</strong> adalah sebuah platform web asisten informasi kesehatan sederhana yang dirancang untuk membantu masyarakat luas memperoleh akses instan terhadap panduan kesehatan umum dan pertolongan pertama penyakit ringan.
                </p>
                <p>
                    Aplikasi ini menggunakan teknologi pencocokan kata kunci berbasis database (Keyword-based Matching) untuk mengidentifikasi topik pertanyaan pengguna dan segera menyajikan saran perawatan awal yang divalidasi secara umum. Dilengkapi pula dengan fitur Kalkulator Indeks Massa Tubuh (BMI) untuk memantau status berat badan ideal secara mudah.
                </p>
                <p>
                    Kami berkomitmen untuk terus menyebarkan edukasi tentang pola hidup sehat, nutrisi bergizi seimbang, pentingnya olahraga, dan istirahat yang cukup demi tercapainya kualitas hidup masyarakat yang lebih baik.
                </p>
            </div>
            
            <div class="about-disclaimer">
                <h4><i class="fa-solid fa-triangle-exclamation"></i> Peringatan Medis (Disclaimer)</h4>
                <p>
                    Layanan dan respon yang diberikan oleh HealthBot bersifat **edukatif dasar** dan **bukan** merupakan saran medis, rencana terapi, diagnosis formal, ataupun pengganti pendapat medis profesional dari dokter, apoteker, atau penyedia layanan kesehatan berlisensi.
                </p>
                <p style="margin-top: 0.75rem;">
                    Selalu konsultasikan masalah kesehatan Anda langsung kepada dokter ahli. Jangan pernah mengabaikan saran medis profesional atau menunda untuk mencarinya karena sesuatu yang telah Anda baca di website ini. Jika Anda mengalami kondisi darurat medis, segera hubungi ambulans atau instalasi gawat darurat terdekat.
                </p>
            </div>
        </div>
    </section>
</div>

<?php
require_once '../includes/footer.php';
?>
