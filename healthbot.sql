-- Create Database if not exists
CREATE DATABASE IF NOT EXISTS healthbot;
USE healthbot;

-- Table admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table users (to track unique guest sessions)
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `session_token` VARCHAR(255) NOT NULL UNIQUE,
  `user_agent` VARCHAR(255) DEFAULT NULL,
  `ip_address` VARCHAR(45) DEFAULT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table knowledge_base (chatbot Q&A)
CREATE TABLE IF NOT EXISTS `knowledge_base` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `category` VARCHAR(50) NOT NULL,
  `keyword` TEXT NOT NULL, -- Comma-separated keywords
  `response` TEXT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table chat_history (consultation logs)
CREATE TABLE IF NOT EXISTS `chat_history` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `user_message` TEXT NOT NULL,
  `bot_response` TEXT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed default admin account
-- Username: kugle, Password: kugle32 (hashed using PASSWORD_DEFAULT)
INSERT INTO `admin` (`id`, `username`, `password`, `name`) VALUES
(1, 'kugle', '$2y$10$FOtikTcDGZNc5zVorH4fTeGtqvEU.5LNG2yLiWu42F8HV0M/YqAnK', 'Dr. Budi Santoso')
ON DUPLICATE KEY UPDATE `username`=VALUES(`username`), `password`=VALUES(`password`);


-- Seed Knowledge Base
INSERT INTO `knowledge_base` (`category`, `keyword`, `response`) VALUES
('greeting', 'halo, hai, hei, hello, pagi, siang, sore, malam, hi', 
 'Halo! Saya HealthBot, asisten informasi kesehatan Anda. Ada yang bisa saya bantu hari ini? Anda bisa menanyakan tentang pola hidup, olahraga, nutrisi, atau penyakit ringan seperti flu, batuk, dan maag.'),

('pola_hidup', 'pola hidup, gaya hidup, sehat, kebiasaan baik, hidup sehat', 
 'Pola hidup sehat melibatkan tiga pilar utama: makan makanan bergizi seimbang, berolahraga secara teratur (minimal 150 menit per minggu), dan tidur yang cukup (7-9 jam per malam). Selain itu, hindari stres berlebih dan konsumsi air putih minimal 2 liter per hari.'),

('makanan', 'makanan, gizi, nutrisi, sayur, buah, diet, karbohidrat, protein', 
 'Makanan bergizi seimbang harus memenuhi konsep \"Isi Piringku\": 50% porsi piring diisi oleh sayur dan buah, 25% makanan pokok (sumber karbohidrat seperti nasi merah, gandum, atau kentang), dan 25% lauk-pauk (sumber protein seperti ikan, dada ayam, tahu, atau tempe). Kurangi konsumsi gula, garam, dan minyak berlebih.'),

('olahraga', 'olahraga, senam, lari, cardio, fisik, fitness, workout', 
 'Untuk menjaga kesehatan tubuh, lakukan aktivitas fisik sedang seperti jalan cepat, bersepeda, atau berenang selama 30 menit per hari, 5 kali seminggu. Olahraga secara rutin dapat melancarkan peredaran darah, meningkatkan kekebalan tubuh, menjaga berat badan ideal, dan mengurangi risiko penyakit jantung.'),

('tidur', 'tidur, istirahat, tidur cukup, insomnia, begadang, kurang tidur', 
 'Tidur yang cukup sangat penting bagi pemulihan sel tubuh dan fungsi otak. Orang dewasa disarankan tidur 7 hingga 9 jam setiap malam. Kebiasaan begadang dapat melemahkan sistem imun, meningkatkan stres, dan memicu obesitas. Usahakan untuk tidur dan bangun pada jam yang konsisten setiap hari.'),

('flu', 'flu, pilek, selesma, hidung tersumbat, bersin', 
 'Flu atau pilek umumnya disebabkan oleh infeksi virus dan dapat sembuh sendiri (self-limiting disease). Penanganan terbaik adalah dengan istirahat total, minum air hangat yang cukup untuk menjaga hidrasi, dan mengonsumsi makanan hangat berkuah. Jika hidung tersumbat, Anda bisa menghirup uap air hangat. Bila gejala sangat mengganggu, obat seperti parasetamol atau dekongestan bebas dapat meredakannya. Jika gejala berlanjut lebih dari 7 hari, segera hubungi dokter.'),

('batuk', 'batuk, tenggorokan gatal, dahak', 
 'Untuk meredakan batuk ringan, Anda bisa meminum air hangat yang dicampur dengan perasan lemon dan madu alami (madu hanya untuk usia di atas 1 tahun). Hindari makanan berminyak, pedas, dan minuman dingin. Mandi air hangat dapat membantu mengencerkan dahak di saluran napas. Jika batuk disertai sesak napas, demam tinggi, atau berlangsung lebih dari 2 minggu, segeralah berkonsultasi ke fasilitas kesehatan.'),

('demam', 'demam, panas, menggigil, suhu tinggi', 
 'Demam adalah respon alami tubuh saat melawan infeksi. Suhu tubuh dikatakan demam jika di atas 37.5°C. Penanganan pertama meliputi istirahat yang cukup, mengenakan pakaian tipis dan nyaman, kompres air hangat di area dahi atau lipat ketiak, serta minum banyak air putih. Anda dapat meminum Parasetamol untuk menurunkan suhu tubuh. Jika demam tidak turun setelah 3 hari atau mencapai >39°C, hubungi dokter.'),

('sakit_kepala', 'sakit kepala, pusing, migrain, kepala cekot-cekot', 
 'Sakit kepala ringan dapat diredakan dengan beristirahat di ruangan yang tenang dan gelap, minum air putih yang cukup (karena dehidrasi sering menjadi pemicu pusing), serta melakukan pijatan ringan di area pelipis. Hindari paparan layar gadget berlebih. Jika nyeri mengganggu, parasetamol atau ibuprofen dapat diminum sesuai dosis. Segera cari pertolongan medis jika sakit kepala terasa sangat hebat secara tiba-tiba atau disertai leher kaku.'),

('maag', 'maag, lambung, asam lambung, nyeri ulu hati, mual, perih', 
 'Sakit maag atau nyeri ulu hati biasanya dipicu oleh telat makan, konsumsi makanan terlalu pedas, asam, berlemak, kopi, atau stres. Untuk mengatasinya, makanlah dengan porsi kecil namun sering (small frequent meals), hindari langsung berbaring setelah makan (tunggu minimal 2 jam), dan kelola stres. Antasida dapat diminum sebelum makan untuk menetralisir asam lambung. Bila nyeri terus berulang, segera periksakan ke dokter.'),

('tips_sehat', 'tips menjaga kesehatan, imun, daya tahan tubuh, cuci tangan, sanitasi', 
 'Untuk menjaga kesehatan tubuh dan meningkatkan imun secara umum, lakukan kebiasaan bersih berikut: 1) Cuci tangan dengan sabun dan air mengalir selama minimal 20 detik (sebelum makan, setelah toilet, atau setelah batuk/bersin), 2) Konsumsi vitamin C dan D alami dari buah jeruk atau dari paparan sinar matahari pagi (10-15 menit), 3) Jaga kebersihan lingkungan rumah untuk mencegah bersarangnya kuman.'),

('diare', 'diare, mencret, buang air besar terus, mulas lambung', 
 'Diare ringan umumnya sembuh dalam beberapa hari. Penanganan utama adalah mencegah dehidrasi. Minumlah cairan oralit atau air putih hangat setiap habis buang air besar. Konsumsi makanan lunak seperti bubur atau pisang, dan hindari produk susu, santan, makanan pedas, atau asam untuk sementara. Hubungi dokter jika diare berlangsung lebih dari 2 hari atau disertai demam tinggi.'),

('sariawan', 'sariawan, bibir perih, sariawan di lidah, bibir pecah-pecah', 
 'Sariawan dapat dipicu kekurangan vitamin C, tergigit, atau stres. Cara meredakannya: 1) Jaga kebersihan mulut dengan menyikat gigi secara perlahan, 2) Kumur air garam hangat (1/2 sendok teh garam dalam segelas air hangat) 2-3 kali sehari, 3) Hindari makanan pedas, panas, atau asam, 4) Perbanyak buah kaya vitamin C seperti kiwi atau jeruk.'),

('sembelit', 'sembelit, susah bab, konstipasi, sulit buang air besar', 
 'Susah buang air besar (sembelit) terjadi akibat kekurangan serat dan cairan. Penanganannya: 1) Perbanyak konsumsi makanan tinggi serat seperti pepaya, pisang, sayuran hijau, dan oatmeal, 2) Minum air putih minimal 2 liter per hari, 3) Lakukan aktivitas fisik ringan untuk merangsang gerakan usus, 4) Hindari menahan keinginan buang air besar.'),

('nyeri_otot', 'nyeri otot, pegal-pegal, badan pegal, linu, otot kaku', 
 'Pegal-pegal atau nyeri otot ringan dapat diredakan dengan: 1) Istirahatkan bagian otot yang sakit, 2) Kompres hangat jika otot terasa kaku, atau kompres dingin jika ada pembengkakan baru, 3) Lakukan peregangan otot ringan secara berkala, 4) Minum pereda nyeri bebas seperti parasetamol jika diperlukan.'),

('gigi', 'sakit gigi, gusi bengkak, gigi ngilu, linu gigi', 
 'Sakit gigi umumnya dipicu gusi meradang atau gigi berlubang. Penanganan awal di rumah: 1) Kumur air garam hangat untuk membersihkan kuman di area mulut, 2) Gunakan benang gigi (dental floss) jika ada sisa makanan tersangkut, 3) Tempel kompres es pada pipi luar jika bengkak, 4) Minum parasetamol untuk mengurangi rasa nyeri sementara. Segera periksakan diri ke dokter gigi.');

