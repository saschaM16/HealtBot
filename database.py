import sqlite3
import hashlib
import os

DB_FILE = "healthbot.db"

def get_connection():
    """Membuka koneksi ke database SQLite dan mengembalikan objek koneksi."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Mengembalikan hasil query berupa dictionary-like object
    return conn

def hash_password(password):
    """Mengamankan password menggunakan SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def init_db():
    """Membuat tabel-tabel database jika belum ada dan melakukan seeding data awal."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Tabel admin
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 2. Tabel users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_token TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 3. Tabel knowledge_base
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_base (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        keyword TEXT NOT NULL,
        response TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 4. Tabel chat_history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    
    # --- SEEDING DATA ---
    
    # Seed Admin 'kugle' / 'kugle32'
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        hashed_pwd = hash_password("kugle32")
        cursor.execute(
            "INSERT INTO admin (username, password, name) VALUES (?, ?, ?)",
            ("kugle", hashed_pwd, "Dr. Budi Santoso")
        )
        conn.commit()
        
    # Seed Knowledge Base
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    if cursor.fetchone()[0] == 0:
        initial_kb = [
            ('greeting', 'halo, hai, hei, hello, pagi, siang, sore, malam, hi', 
             'Halo! Saya HealthBot, asisten informasi kesehatan Anda. Ada yang bisa saya bantu hari ini? Anda bisa menanyakan tentang pola hidup, olahraga, nutrisi, atau penyakit ringan seperti flu, batuk, dan maag.'),
             
            ('pola_hidup', 'pola hidup, gaya hidup, sehat, kebiasaan baik, hidup sehat', 
             'Pola hidup sehat melibatkan tiga pilar utama: makan makanan bergizi seimbang, berolahraga secara teratur (minimal 150 menit per minggu), dan tidur yang cukup (7-9 jam per malam). Selain itu, hindari stres berlebih dan konsumsi air putih minimal 2 liter per hari.'),
             
            ('makanan', 'makanan, gizi, nutrisi, sayur, buah, diet, karbohidrat, protein', 
             'Makanan bergizi seimbang harus memenuhi konsep "Isi Piringku": 50% porsi piring diisi oleh sayur dan buah, 25% makanan pokok (sumber karbohidrat seperti nasi merah, gandum, atau kentang), dan 25% lauk-pauk (sumber protein seperti ikan, dada ayam, tahu, atau tempe). Kurangi konsumsi gula, garam, dan minyak berlebih.'),
             
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
             'Sakit gigi umumnya dipicu gusi meradang atau gigi berlubang. Penanganan awal di rumah: 1) Kumur air garam hangat untuk membersihkan kuman di area mulut, 2) Gunakan benang gigi (dental floss) jika ada sisa makanan tersangkut, 3) Tempel kompres es pada pipi luar jika bengkak, 4) Minum parasetamol untuk mengurangi rasa nyeri sementara. Segera periksakan diri ke dokter gigi.')
        ]
        
        cursor.executemany(
            "INSERT INTO knowledge_base (category, keyword, response) VALUES (?, ?, ?)",
            initial_kb
        )
        conn.commit()
        
    conn.close()

# --- FUNGSI DATA USER & CHAT ---

def get_or_create_user(session_token):
    """Mendapatkan ID user berdasarkan token sesi. Membuat user baru jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE session_token = ?", (session_token,))
    row = cursor.fetchone()
    
    if row:
        user_id = row['id']
    else:
        cursor.execute("INSERT INTO users (session_token) VALUES (?)", (session_token,))
        conn.commit()
        user_id = cursor.lastrowid
        
    conn.close()
    return user_id

def add_chat_log(user_id, user_message, bot_response):
    """Menyimpan log chat ke database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)",
        (user_id, user_message, bot_response)
    )
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    """Mengambil riwayat percakapan untuk user tertentu."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_message, bot_response, created_at FROM chat_history WHERE user_id = ? ORDER BY created_at ASC",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_chat_history(user_id):
    """Menghapus semua riwayat chat milik user tertentu."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# --- FUNGSI ADMIN & BASIS PENGETAHUAN (CRUD) ---

def authenticate_admin(username, password):
    """Memverifikasi username dan password administrator."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pwd = hash_password(password)
    
    cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, hashed_pwd))
    row = cursor.fetchone()
    conn.close()
    return row

def get_kb_records():
    """Mengambil semua data basis pengetahuan chatbot."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knowledge_base ORDER BY category ASC, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_kb_record(category, keyword, response):
    """Menambahkan data pengetahuan baru ke chatbot."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO knowledge_base (category, keyword, response) VALUES (?, ?, ?)",
        (category, keyword.strip(), response.strip())
    )
    conn.commit()
    conn.close()

def update_kb_record(kb_id, category, keyword, response):
    """Memperbarui data pengetahuan chatbot."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE knowledge_base SET category = ?, keyword = ?, response = ? WHERE id = ?",
        (category, keyword.strip(), response.strip(), kb_id)
    )
    conn.commit()
    conn.close()

def delete_kb_record(kb_id):
    """Menghapus data pengetahuan chatbot."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM knowledge_base WHERE id = ?", (kb_id,))
    conn.commit()
    conn.close()

def get_stats():
    """Mengambil statistik ringkasan untuk dashboard admin."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM chat_history")
    chats = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM knowledge_base")
    kb = cursor.fetchone()[0]
    
    conn.close()
    return {
        'chats': chats,
        'users': users,
        'knowledge': kb
    }

def get_all_chat_logs():
    """Mengambil riwayat percakapan semua user untuk dashboard admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ch.user_message, ch.bot_response, ch.created_at, u.session_token
        FROM chat_history ch
        JOIN users u ON ch.user_id = u.id
        ORDER BY ch.created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Inisialisasi DB saat modul diimpor pertama kali
init_db()
