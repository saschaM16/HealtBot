<?php
require_once '../includes/db.php';

$page_title = "Kalkulator BMI";

require_once '../includes/header.php';
?>

<div class="container">
    <div class="bmi-container fade-in-up">
        
        <!-- Header Panel -->
        <div class="bmi-header">
            <h2><i class="fa-solid fa-weight-scale"></i> Kalkulator Indeks Massa Tubuh (BMI)</h2>
            <p>Ketahui status gizi tubuh Anda dengan mudah berdasarkan perbandingan berat dan tinggi badan.</p>
        </div>
        
        <!-- Body Panel -->
        <div class="bmi-content">
            
            <!-- Left Side: Inputs Form -->
            <div class="bmi-form-section">
                <form id="bmiForm" onsubmit="return false;">
                    
                    <div class="bmi-form-group">
                        <label for="height">Tinggi Badan</label>
                        <div class="bmi-input-wrapper">
                            <input type="number" id="height" placeholder="Contoh: 170" min="50" max="250" required>
                            <span class="unit">cm</span>
                        </div>
                    </div>
                    
                    <div class="bmi-form-group">
                        <label for="weight">Berat Badan</label>
                        <div class="bmi-input-wrapper">
                            <input type="number" id="weight" placeholder="Contoh: 65" min="20" max="300" required>
                            <span class="unit">kg</span>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn-calculate" id="btnCalculate">
                        <i class="fa-solid fa-calculator"></i> Hitung Sekarang
                    </button>
                    
                </form>
            </div>
            
            <!-- Right Side: Results Display -->
            <div class="bmi-results" id="bmiResultsBox">
                <!-- Placeholder awal sebelum user menghitung -->
                <div class="bmi-result-placeholder" id="bmiPlaceholder">
                    <i class="fa-solid fa-circle-question"></i>
                    <h3>Belum Ada Hasil</h3>
                    <p>Masukkan tinggi badan dan berat badan Anda, lalu klik tombol "Hitung Sekarang" untuk melihat hasil analisis gizi.</p>
                </div>
                
                <!-- Container Hasil (Akan ditampilkan secara dinamis oleh JavaScript) -->
                <div id="bmiResultContent" style="display: none;">
                    <div class="bmi-score-box">
                        <div class="bmi-score-label">Skor BMI Anda</div>
                        <div class="bmi-score-val" id="bmiScoreVal">0.0</div>
                        <div class="bmi-category-badge" id="bmiCategoryBadge">Normal</div>
                    </div>
                    
                    <div class="bmi-tips-box">
                        <h4><i class="fa-solid fa-circle-info"></i> Rekomendasi Kesehatan</h4>
                        <p id="bmiAdviceText">Isi data kesehatan Anda untuk melihat tips pola hidup sehat yang sesuai dengan kategori BMI tubuh Anda.</p>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</div>

<!-- Scripts -->
<script src="../assets/js/bmi.js"></script>

<?php
require_once '../includes/footer.php';
?>
