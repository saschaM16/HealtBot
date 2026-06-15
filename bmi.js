document.addEventListener('DOMContentLoaded', function() {
    const bmiForm = document.getElementById('bmiForm');
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiPlaceholder = document.getElementById('bmiPlaceholder');
    const bmiResultContent = document.getElementById('bmiResultContent');
    const bmiScoreVal = document.getElementById('bmiScoreVal');
    const bmiCategoryBadge = document.getElementById('bmiCategoryBadge');
    const bmiAdviceText = document.getElementById('bmiAdviceText');

    if (bmiForm) {
        bmiForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const heightCm = parseFloat(heightInput.value);
            const weightKg = parseFloat(weightInput.value);
            
            if (isNaN(heightCm) || isNaN(weightKg) || heightCm <= 0 || weightKg <= 0) {
                alert('Silakan masukkan nilai tinggi badan dan berat badan yang valid.');
                return;
            }
            
            // Konversi tinggi badan ke meter
            const heightM = heightCm / 100;
            
            // Hitung BMI: Berat (kg) / (Tinggi (m) ^ 2)
            const bmi = weightKg / (heightM * heightM);
            const bmiScore = bmi.toFixed(1);
            
            // Tentukan kategori dan rekomendasi
            let categoryText = '';
            let badgeClass = '';
            let adviceText = '';
            
            if (bmi < 18.5) {
                categoryText = 'Kurus (Kekurangan Berat Badan)';
                badgeClass = 'badge-kurus';
                adviceText = 'Anda berada dalam kategori kekurangan berat badan. Sangat disarankan untuk meningkatkan asupan nutrisi dengan makanan padat kalori bergizi, makan dengan porsi kecil namun sering, meningkatkan konsumsi protein berkualitas (seperti dada ayam, ikan, telur, tahu, tempe), dan lakukan latihan kekuatan fisik (weight training) untuk merangsang pertumbuhan otot secara sehat.';
            } else if (bmi >= 18.5 && bmi <= 24.9) {
                categoryText = 'Normal (Ideal)';
                badgeClass = 'badge-normal';
                adviceText = 'Selamat! Berat badan Anda berada dalam rentang ideal dan sehat. Pertahankan kondisi ini dengan melanjutkan pola makan bergizi seimbang konsep \"Isi Piringku\", berolahraga secara teratur minimal 150 menit per minggu, penuhi hidrasi air putih minimal 2 liter per hari, dan pastikan tidur teratur selama 7-9 jam setiap malam.';
            } else if (bmi >= 25.0 && bmi <= 29.9) {
                categoryText = 'Gemuk (Kelebihan Berat Badan)';
                badgeClass = 'badge-gemuk';
                adviceText = 'Anda berada dalam kategori kelebihan berat badan tingkat ringan. Cobalah untuk membatasi asupan kalori harian dengan membatasi makanan manis, bersantan, gorengan, dan karbohidrat sederhana. Mulailah rutin melakukan aktivitas fisik sedang (jalan cepat, bersepeda, senam) selama 30-45 menit sehari, perbanyak konsumsi serat pangan dari sayuran/buah, dan hindari stres.';
            } else {
                categoryText = 'Obesitas (Sangat Gemuk)';
                badgeClass = 'badge-obesitas';
                adviceText = 'Anda berada dalam kategori obesitas. Kondisi ini berisiko meningkatkan komplikasi kardiovaskular, tekanan darah tinggi, kolesterol tinggi, dan diabetes. Sangat disarankan untuk menerapkan program diet penurunan berat badan yang aman (caloric deficit), hindari junk food dan minuman bersoda, lakukan olahraga kardio intensitas ringan-sedang secara bertahap, dan konsultasikan ke dokter atau ahli gizi jika diperlukan.';
            }
            
            // Perbarui UI secara dinamis
            bmiScoreVal.textContent = bmiScore;
            bmiCategoryBadge.textContent = categoryText;
            
            // Bersihkan semua class badge sebelumnya
            bmiCategoryBadge.className = 'bmi-category-badge';
            // Tambahkan class badge yang baru
            bmiCategoryBadge.classList.add(badgeClass);
            
            // Perbarui teks rekomendasi
            bmiAdviceText.textContent = adviceText;
            
            // Tampilkan konten hasil dan sembunyikan placeholder
            bmiPlaceholder.style.display = 'none';
            bmiResultContent.style.display = 'block';
            
            // Animasi transisi kecil pada kotak hasil
            const resultsBox = document.getElementById('bmiResultsBox');
            resultsBox.style.animation = 'none';
            // Trigger reflow
            void resultsBox.offsetWidth;
            resultsBox.style.animation = 'fadeInUp 0.4s ease forwards';
        });
    }
});
