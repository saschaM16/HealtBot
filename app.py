import streamlit as st
import random
import os
import database as db

# Inisialisasi konfigurasi halaman Streamlit
st.set_page_config(
    page_title="HealthBot - Asisten Informasi Kesehatan",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi token sesi user unik jika belum ada
if 'user_token' not in st.session_state:
    st.session_state['user_token'] = os.urandom(16).hex()

# Dapatkan user ID di database berdasarkan token sesi
user_id = db.get_or_create_user(st.session_state['user_token'])

# Inisialisasi state admin login
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False
if 'admin_name' not in st.session_state:
    st.session_state['admin_name'] = ""

# Inisialisasi tips harian persisten per sesi agar tidak berubah-ubah tiap rerun halaman
HEALTH_TIPS = [
    "Minum setidaknya 8 gelas air (sekitar 2 liter) sehari untuk menjaga organ tubuh terhidrasi secara optimal.",
    "Lakukan peregangan ringan selama 5 menit untuk setiap 1 jam Anda duduk bekerja di depan komputer.",
    "Tidur malam selama 7-8 jam secara teratur dapat membantu perbaikan jaringan tubuh dan menjaga imun.",
    "Isi piring Anda dengan porsi seimbang: setengah sayur & buah, seperempat karbohidrat, dan seperempat protein.",
    "Batasi konsumsi gula berlebih untuk menghindari risiko obesitas dan diabetes melitus tipe 2.",
    "Olahraga jalan kaki cepat selama 30 menit sehari dapat menurunkan risiko penyakit jantung secara signifikan.",
    "Sempatkan bernapas dalam atau meditasi selama 10 menit di sela kesibukan untuk meredakan stres harian.",
    "Jauhkan smartphone Anda setidaknya 30 menit sebelum tidur agar otak siap beristirahat dengan nyenyak."
]

if 'daily_tip' not in st.session_state:
    st.session_state['daily_tip'] = random.choice(HEALTH_TIPS)

# Custom CSS untuk memperindah UI Streamlit (Premium Green & White Aesthetic)
st.markdown("""
<style>
    /* Mengubah font global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Tombol utama */
    div.stButton > button:first-child {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #059669;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
        transform: translateY(-1px);
    }
    
    /* Alert dan card khusus */
    .health-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .disclaimer-box {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        padding: 16px;
        border-radius: 8px;
        color: #7f1d1d;
        margin-top: 20px;
    }
    
    /* Sembunyikan elemen streamlit default yang kurang rapi */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR & NAVIGASI ---

with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 25px;">
        <span style="font-size: 32px; color: #10b981;">🤖</span>
        <h2 style="margin: 0; font-size: 24px;">Health<span style="color: #10b981;">Bot</span></h2>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigasi Menu:",
        ["🏠 Beranda", "💬 Konsultasi Chatbot", "⚖️ Kalkulator BMI", "ℹ️ Tentang HealthBot", "🔒 Dashboard Admin"]
    )
    
    st.markdown("---")
    st.markdown("<p style='font-size: 12px; color: #6b7280; text-align: center;'>HealthBot v2.0 © 2026</p>", unsafe_allow_html=True)

# --- 1. HALAMAN BERANDA ---

if menu == "🏠 Beranda":
    col_text, col_img = st.columns([1.2, 0.8])
    with col_text:
        st.markdown("""
        <div style="margin-top: 10px; margin-bottom: 30px;">
            <h1 style="font-size: 40px; font-weight: 800; margin-bottom: 10px;">Asisten Informasi <span style="color: #10b981;">Kesehatan</span></h1>
            <p style="font-size: 18px; color: #4b5563;">Selamat datang di HealthBot. Kami membantu Anda mendapatkan edukasi pola hidup sehat, nutrisi makanan, saran olahraga, serta informasi penanganan awal penyakit ringan secara instan dan ramah.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_img:
        img_path = os.path.join("assets", "images", "hero_illustration.png")
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
            
    # Tips Harian
    st.info(f"💡 **Tips Kesehatan Hari Ini:** {st.session_state['daily_tip']}")
    
    st.markdown("<h3 style='margin-top: 30px; margin-bottom: 20px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px;'>Kategori Informasi Kesehatan</h3>", unsafe_allow_html=True)
    
    # Grid Kategori Info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="health-card">
            <div style="background-color: #ecfdf5; color: #10b981; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 15px;">❤️</div>
            <h4 style="margin: 0 0 10px 0; color: #1f2937; font-weight: 700;">Pola Hidup Sehat</h4>
            <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.5;">Cara membiasakan gaya hidup seimbang, manajemen stres, pemenuhan hidrasi air, dan kebiasaan baik harian.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="health-card">
            <div style="background-color: #eff6ff; color: #3b82f6; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 15px;">🛌</div>
            <h4 style="margin: 0 0 10px 0; color: #1f2937; font-weight: 700;">Tidur yang Cukup</h4>
            <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.5;">Pentingnya tidur berkualitas 7-9 jam setiap malam, cara meredakan insomnia, dan bahaya begadang bagi imun.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="health-card">
            <div style="background-color: #fef3c7; color: #f59e0b; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 15px;">🍎</div>
            <h4 style="margin: 0 0 10px 0; color: #1f2937; font-weight: 700;">Makanan Bergizi</h4>
            <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.5;">Pemenuhan zat gizi makro/mikro seimbang konsep "Isi Piringku", diet sehat, serta cara mengurangi garam & gula.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="health-card">
            <div style="background-color: #faf5ff; color: #a855f7; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 15px;">🧼</div>
            <h4 style="margin: 0 0 10px 0; color: #1f2937; font-weight: 700;">Tips Menjaga Imun</h4>
            <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.5;">Tips kebersihan tubuh harian, cara mencuci tangan dengan tepat, dan sanitasi rumah demi pencegahan infeksi.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="health-card">
            <div style="background-color: #fee2e2; color: #ef4444; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 15px;">🏋️</div>
            <h4 style="margin: 0 0 10px 0; color: #1f2937; font-weight: 700;">Olahraga Teratur</h4>
            <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.5;">Rekomendasi aktivitas fisik sedang (jalan cepat, kardio, beban) selama 150 menit per minggu agar jantung sehat.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="health-card">
            <div style="background-color: #f0fdf4; color: #15803d; width: 45px; height: 45px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 15px;">💊</div>
            <h4 style="margin: 0 0 10px 0; color: #1f2937; font-weight: 700;">Info Penyakit Ringan</h4>
            <p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.5;">Edukasi gejala awal dan pertolongan pertama penyakit flu, batuk, demam, sakit kepala, maag, diare, dll.</p>
        </div>
        """, unsafe_allow_html=True)

# --- 2. HALAMAN CHATBOT ---

elif menu == "💬 Konsultasi Chatbot":
    st.markdown("""
    <div style="margin-top: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <h1 style="font-size: 36px; font-weight: 800; margin: 0;">Konsultasi Chatbot <span style="color: #10b981;">HealthBot</span></h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Tombol Hapus Riwayat Chat
    if st.button("🗑️ Bersihkan Riwayat Chat"):
        db.clear_chat_history(user_id)
        st.success("Riwayat percakapan Anda telah dibersihkan.")
        st.rerun()
        
    st.markdown("---")
    
    # Ambil Riwayat dari SQLite
    chat_history = db.get_chat_history(user_id)
    
    # Tampilkan Sambutan Awal jika riwayat kosong
    if len(chat_history) == 0:
        with st.chat_message("assistant"):
            st.markdown("""
            Halo! Saya **HealthBot**, asisten virtual kesehatan Anda. 
            Saya dapat membantu memberikan informasi tentang pola hidup sehat, nutrisi makanan, olahraga, tips tidur, dan penanganan mandiri penyakit ringan seperti flu, batuk, demam, maag, diare, sariawan, sembelit, pegal-pegal, atau sakit gigi.
            
            Ada yang ingin Anda tanyakan hari ini?
            """)
    else:
        # Render riwayat chat
        for chat in chat_history:
            with st.chat_message("user"):
                st.write(chat['user_message'])
            with st.chat_message("assistant"):
                st.write(chat['bot_response'])
                
    # Input chat baru
    user_input = st.chat_input("Tanyakan tentang keluhan kesehatan Anda (contoh: flu, sakit gigi, diet)...")
    
    # Suggestion Chips (Kemudahan Pengguna)
    st.markdown("<p style='font-size: 13px; color: #6b7280; margin-bottom: 5px; font-weight: bold;'>Rekomendasi Topik:</p>", unsafe_allow_html=True)
    cols = st.columns(5)
    suggestions = [
        ("Flu & Pilek", "Bagaimana penanganan flu?"),
        ("Pola Hidup", "pola hidup sehat"),
        ("Sakit Gigi", "sakit gigi gusi bengkak"),
        ("Sakit Maag", "sakit maag nyeri ulu hati"),
        ("Diare Ringan", "obat diare mencret")
    ]
    for i, (label, question) in enumerate(suggestions):
        with cols[i]:
            if st.button(label, key=f"chip_{i}"):
                user_input = question
                
    if user_input:
        # Tampilkan langsung input user di layar
        with st.chat_message("user"):
            st.write(user_input)
            
        # Proses pencocokan kata kunci
        kb_records = db.get_kb_records()
        normalized_input = user_input.lower()
        bot_response = None
        
        for record in kb_records:
            keywords = [kw.strip().lower() for kw in record['keyword'].split(',')]
            for kw in keywords:
                if kw and kw in normalized_input:
                    bot_response = record['response']
                    break
            if bot_response:
                break
                
        if not bot_response:
            bot_response = "Maaf, HealthBot belum memahami pertanyaan Anda. Silakan tanyakan hal lain seputar kesehatan seperti 'flu', 'batuk', 'demam', 'pola hidup', 'olahraga', 'diare', 'sakit gigi', atau 'nutrisi makanan'. Harap diingat bahwa informasi ini bersifat dasar dan bukan pengganti pemeriksaan medis dokter."
            
        # Tampilkan respon bot di layar
        with st.chat_message("assistant"):
            st.write(bot_response)
            
        # Simpan ke SQLite
        db.add_chat_log(user_id, user_input, bot_response)
        
        # Rerun untuk memperbarui UI
        st.rerun()

# --- 3. HALAMAN BMI ---

elif menu == "⚖️ Kalkulator BMI":
    st.markdown("""
    <div style="margin-top: 10px; margin-bottom: 25px;">
        <h1 style="font-size: 36px; font-weight: 800; margin-bottom: 5px;">Kalkulator <span style="color: #10b981;">BMI</span></h1>
        <p style="font-size: 16px; color: #6b7280;">Hitung Indeks Massa Tubuh (BMI) Anda untuk menganalisis apakah berat badan Anda ideal atau berisiko.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_input, col_result = st.columns(2)
    
    with col_input:
        st.markdown("<h4 style='color: #1f2937;'>Masukkan Data Fisik Anda:</h4>", unsafe_allow_html=True)
        height = st.number_input("Tinggi Badan (cm):", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
        weight = st.number_input("Berat Badan (kg):", min_value=20.0, max_value=300.0, value=65.0, step=0.5)
        
        btn_calc = st.button("Hitung Status BMI")
        
    with col_result:
        st.markdown("<h4 style='color: #1f2937;'>Analisis Hasil Gizi:</h4>", unsafe_allow_html=True)
        
        if btn_calc:
            height_m = height / 100
            bmi = weight / (height_m * height_m)
            bmi_score = round(bmi, 1)
            
            # Tentukan kategori
            if bmi < 18.5:
                category = "Kurus (Kekurangan Berat Badan)"
                color_hex = "#f59e0b" # Amber
                badge_bg = "#fef3c7"
                advice = "Anda berada dalam kategori kekurangan berat badan. Sangat disarankan untuk meningkatkan asupan nutrisi dengan makanan padat kalori bergizi, makan dengan porsi kecil namun sering, meningkatkan konsumsi protein berkualitas (seperti dada ayam, ikan, telur, tahu, tempe), dan lakukan latihan kekuatan fisik (weight training) untuk meningkatkan massa otot secara sehat."
            elif 18.5 <= bmi <= 24.9:
                category = "Normal (Ideal)"
                color_hex = "#10b981" # Green
                badge_bg = "#ecfdf5"
                advice = "Selamat! Berat badan Anda berada dalam rentang ideal dan sehat. Pertahankan kondisi ini dengan melanjutkan pola makan bergizi seimbang konsep \"Isi Piringku\", berolahraga secara teratur minimal 150 menit per minggu, penuhi hidrasi air putih minimal 2 liter per hari, dan pastikan tidur teratur selama 7-9 jam setiap malam."
            elif 25.0 <= bmi <= 29.9:
                category = "Gemuk (Kelebihan Berat Badan)"
                color_hex = "#f97316" # Orange
                badge_bg = "#ffedd5"
                advice = "Anda berada dalam kategori kelebihan berat badan tingkat ringan. Cobalah untuk membatasi asupan kalori harian dengan membatasi makanan manis, bersantan, gorengan, dan karbohidrat sederhana. Mulailah rutin melakukan aktivitas fisik sedang (jalan cepat, bersepeda, senam) selama 30-45 menit sehari, perbanyak konsumsi serat pangan dari sayuran/buah, dan hindari stres."
            else:
                category = "Obesitas (Sangat Gemuk)"
                color_hex = "#ef4444" # Red
                badge_bg = "#fee2e2"
                advice = "Anda berada dalam kategori obesitas. Kondisi ini berisiko meningkatkan komplikasi kardiovaskular, tekanan darah tinggi, kolesterol tinggi, dan diabetes. Sangat disarankan untuk menerapkan program diet penurunan berat badan yang aman (caloric deficit), hindari junk food dan minuman bersoda, lakukan olahraga kardio intensitas ringan-sedang secara bertahap, dan konsultasikan ke dokter atau ahli gizi jika diperlukan."
                
            # Render hasil box
            st.markdown(f"""
            <div style="background-color: {badge_bg}; padding: 25px; border-radius: 12px; border: 1.5px solid {color_hex}; text-align: center; margin-bottom: 20px;">
                <p style="margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; color: #4b5563; font-weight: bold;">Skor BMI Anda</p>
                <h2 style="font-size: 56px; font-weight: 800; color: {color_hex}; margin: 5px 0;">{bmi_score}</h2>
                <span style="background-color: {color_hex}; color: white; padding: 6px 16px; border-radius: 9999px; font-weight: bold; font-size: 15px; display: inline-block;">
                    {category}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Tips Saran
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <h5 style="margin: 0 0 10px 0; color: #1f2937; font-weight: 700;">💡 Rekomendasi Pola Hidup:</h5>
                <p style="margin: 0; color: #4b5563; font-size: 14px; line-height: 1.6;">{advice}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 40px; text-align: center; color: #6b7280;">
                <span style="font-size: 40px;">⚖️</span>
                <p style="margin-top: 10px; font-size: 14px;">Masukkan tinggi dan berat badan Anda pada form di sebelah kiri, kemudian tekan tombol <strong>"Hitung Status BMI"</strong>.</p>
            </div>
            """, unsafe_allow_html=True)

# --- 4. HALAMAN TENTANG ---

elif menu == "ℹ️ Tentang HealthBot":
    st.markdown("""
    <div style="margin-top: 10px; margin-bottom: 25px;">
        <h1 style="font-size: 36px; font-weight: 800; margin-bottom: 5px;">Tentang <span style="color: #10b981;">HealthBot</span></h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="health-card">
        <h3 style="color: #1f2937; font-weight: 700; margin-bottom: 15px;">Mengenai Aplikasi</h3>
        <p style="font-size: 15px; color: #4b5563; line-height: 1.6;">
            <strong>HealthBot</strong> adalah sebuah asisten informasi kesehatan berbasis web yang dibangun menggunakan pustaka Streamlit (Python) dan database SQLite. Aplikasi ini dirancang untuk memberikan informasi edukasi dasar kesehatan secara cepat, interaktif, dan mudah dimengerti oleh masyarakat luas.
        </p>
        <p style="font-size: 15px; color: #4b5563; line-height: 1.6;">
            Menggunakan algoritma pencocokan kata kunci (keyword pattern matching) di sisi backend, HealthBot dapat mengenali kata kunci yang diinputkan pengguna dalam obrolan chat dan segera menyajikan respon pertolongan pertama gawat darurat ringan yang aman secara medis umum. Fitur kalkulator BMI juga disediakan guna memudahkan pengukuran rasio tinggi/berat badan yang ideal secara langsung.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="disclaimer-box">
        <h4 style="margin: 0 0 8px 0; font-weight: bold;">⚠️ Peringatan Medis (Disclaimer):</h4>
        <p style="margin: 0; font-size: 14px; line-height: 1.6;">
            Layanan chatbot virtual HealthBot hanya bersifat memberikan <strong>informasi edukasi kesehatan umum dasar</strong>. Jawaban atau rekomendasi dari chatbot ini <strong>TIDAK boleh</strong> dijadikan acuan diagnosis resmi medis, resep obat klinis, rencana perawatan resmi, atau pengganti saran medis/konsultasi langsung dengan dokter profesional berlisensi.
        </p>
        <p style="margin-top: 8px; font-size: 14px; line-height: 1.6;">
            Jangan pernah mengabaikan atau menunda pencarian pertolongan medis profesional akibat informasi yang Anda peroleh di website ini. Jika Anda mengalami kondisi darurat medis atau gejala kritis, segera hubungi ambulans atau kunjungi Unit Gawat Darurat (UGD) rumah sakit terdekat.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ADMIN ---

elif menu == "🔒 Dashboard Admin":
    if not st.session_state['admin_logged_in']:
        # Form Login Admin
        st.markdown("<h2 style='text-align: center;'>Login Administrator</h2>", unsafe_allow_html=True)
        col_l, col_c, col_r = st.columns([1, 1.5, 1])
        
        with col_c:
            with st.form("form_login"):
                username = st.text_input("Username:", placeholder="admin")
                password = st.text_input("Password:", type="password")
                btn_login = st.form_submit_button("Masuk Dashboard")
                
                if btn_login:
                    admin = db.authenticate_admin(username, password)
                    if admin:
                        st.session_state['admin_logged_in'] = True
                        st.session_state['admin_name'] = admin['name']
                        st.success("Login berhasil!")
                        st.rerun()
                    else:
                        st.error("Username atau password salah.")
            st.markdown("<p style='text-align:center; font-size:12px; color:#6b7280;'>Default: username (kugle) & password (kugle32)</p>", unsafe_allow_html=True)
    else:
        # Dashboard Admin Aktif
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; margin-bottom: 25px; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px;">
            <div>
                <h1 style="font-size: 36px; font-weight: 800; margin: 0;">Dashboard <span style="color: #10b981;">Admin</span></h1>
                <p style="margin: 5px 0 0 0; color: #6b7280;">Selamat datang, <strong>{st.session_state['admin_name']}</strong> (Administrator)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Keluar dari Dashboard"):
            st.session_state['admin_logged_in'] = False
            st.session_state['admin_name'] = ""
            st.rerun()
            
        # Tab Menu Dashboard
        tab_summary, tab_kb, tab_logs = st.tabs(["📊 Ringkasan", "🗄️ Basis Pengetahuan (CRUD)", "📜 Riwayat Konsultasi"])
        
        # TAB SUMMARY
        with tab_summary:
            stats = db.get_stats()
            
            # Widget Stats
            w1, w2, w3 = st.columns(3)
            with w1:
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center;">
                    <span style="font-size: 24px;">💬</span>
                    <h5 style="margin: 5px 0; color: #6b7280; font-size: 14px;">Total Chat</h5>
                    <h2 style="margin: 0; font-size: 36px; font-weight: bold; color: #3b82f6;">{stats['chats']}</h2>
                </div>
                """, unsafe_allow_html=True)
            with w2:
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center;">
                    <span style="font-size: 24px;">👥</span>
                    <h5 style="margin: 5px 0; color: #6b7280; font-size: 14px;">Pengunjung Unik</h5>
                    <h2 style="margin: 0; font-size: 36px; font-weight: bold; color: #10b981;">{stats['users']}</h2>
                </div>
                """, unsafe_allow_html=True)
            with w3:
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; text-align: center;">
                    <span style="font-size: 24px;">🗂️</span>
                    <h5 style="margin: 5px 0; color: #6b7280; font-size: 14px;">Kata Kunci Q&A</h5>
                    <h2 style="margin: 0; font-size: 36px; font-weight: bold; color: #f59e0b;">{stats['knowledge']}</h2>
                </div>
                """, unsafe_allow_html=True)
                
            # Quick View Logs Terakhir
            st.markdown("<h4 style='margin-top: 30px; margin-bottom: 15px;'>5 Konsultasi Terkini</h4>", unsafe_allow_html=True)
            all_logs = db.get_all_chat_logs()
            if len(all_logs) == 0:
                st.info("Belum ada riwayat konsultasi masuk.")
            else:
                for i in range(min(5, len(all_logs))):
                    log = all_logs[i]
                    st.markdown(f"""
                    <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #3b82f6;">
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6b7280; margin-bottom: 5px;">
                            <span>Sesi: <code>{log['session_token'][:12]}...</code></span>
                            <span>Waktu: {log['created_at']}</span>
                        </div>
                        <p style="margin: 0 0 5px 0; font-size: 14px;">👤 <strong>User:</strong> {log['user_message']}</p>
                        <p style="margin: 0; font-size: 14px; color: #047857;">🤖 <strong>Bot:</strong> {log['bot_response']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # TAB KNOWLEDGE BASE (CRUD)
        with tab_kb:
            st.markdown("### Kelola Basis Pengetahuan Chatbot")
            
            # --- FORM TAMBAH DATA BARU ---
            with st.expander("➕ Tambah Data Pengetahuan Q&A Baru", expanded=False):
                with st.form("form_add_kb"):
                    add_cat = st.selectbox(
                        "Kategori Data:",
                        ["greeting", "pola_hidup", "makanan", "olahraga", "tidur", "tips_sehat", "flu", "batuk", "demam", "sakit_kepala", "maag", "diare", "sariawan", "sembelit", "nyeri_otot", "gigi"]
                    )
                    add_keyword = st.text_input("Kata Kunci Pemicu (pisahkan dengan koma):", placeholder="contoh: flu, pilek, bersin-bersin")
                    add_response = st.text_area("Respon Jawaban Bot:")
                    
                    btn_save_add = st.form_submit_button("Simpan Data Q&A")
                    
                    if btn_save_add:
                        if add_keyword.strip() != "" and add_response.strip() != "":
                            db.add_kb_record(add_cat, add_keyword, add_response)
                            st.success("Data baru berhasil disimpan!")
                            st.rerun()
                        else:
                            st.error("Kolom kata kunci dan respon jawaban harus diisi.")
            
            st.markdown("---")
            
            # --- DAFTAR DATA & FORM EDIT/DELETE ---
            kb_list = db.get_kb_records()
            st.markdown(f"#### Daftar Pengetahuan Aktif ({len(kb_list)} data)")
            
            for row in kb_list:
                with st.expander(f"📦 Kategori: {row['category'].upper()} | Kata Kunci: {row['keyword'][:50]}...", expanded=False):
                    
                    # Form Edit/Update di dalam Expander
                    with st.form(f"form_edit_{row['id']}"):
                        edit_cat = st.selectbox(
                            "Kategori Data:",
                            ["greeting", "pola_hidup", "makanan", "olahraga", "tidur", "tips_sehat", "flu", "batuk", "demam", "sakit_kepala", "maag", "diare", "sariawan", "sembelit", "nyeri_otot", "gigi"],
                            index=["greeting", "pola_hidup", "makanan", "olahraga", "tidur", "tips_sehat", "flu", "batuk", "demam", "sakit_kepala", "maag", "diare", "sariawan", "sembelit", "nyeri_otot", "gigi"].index(row['category'])
                        )
                        edit_keyword = st.text_input("Kata Kunci Pemicu:", value=row['keyword'])
                        edit_response = st.text_area("Respon Jawaban Bot:", value=row['response'])
                        
                        col_edit_btn1, col_edit_btn2 = st.columns(2)
                        with col_edit_btn1:
                            btn_update = st.form_submit_button("💾 Perbarui Data")
                        with col_edit_btn2:
                            # Kami meletakkan tombol hapus di luar form agar aksi terpisah dengan bersih
                            pass
                            
                        if btn_update:
                            if edit_keyword.strip() != "" and edit_response.strip() != "":
                                db.update_kb_record(row['id'], edit_cat, edit_keyword, edit_response)
                                st.success("Perubahan data berhasil disimpan!")
                                st.rerun()
                            else:
                                st.error("Kolom tidak boleh kosong.")
                                
                    # Tombol hapus diletakkan di luar form di dalam expander
                    if st.button("❌ Hapus Data Ini", key=f"del_{row['id']}"):
                        db.delete_kb_record(row['id'])
                        st.success("Data berhasil dihapus!")
                        st.rerun()
        
        # TAB LOGS KONSULTASI LENGKAP
        with tab_logs:
            st.markdown("### Log Lengkap Konsultasi Pengunjung")
            all_logs = db.get_all_chat_logs()
            
            if len(all_logs) == 0:
                st.info("Belum ada log percakapan tersimpan.")
            else:
                for log in all_logs:
                    st.markdown(f"""
                    <div style="background-color: white; padding: 18px; border-radius: 8px; margin-bottom: 12px; border: 1px solid #e2e8f0; border-left: 5px solid #10b981;">
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6b7280; margin-bottom: 6px;">
                            <span>Sesi: <code>{log['session_token']}</code></span>
                            <span>Waktu Konsultasi: {log['created_at']}</span>
                        </div>
                        <p style="margin: 0 0 6px 0; font-size: 14px; font-weight: 600;">👤 User: <span style="font-weight: 500; color: #1f2937;">{log['user_message']}</span></p>
                        <p style="margin: 0; font-size: 14px; color: #047857; font-weight: 600;">🤖 Bot: <span style="font-weight: 500; color: #374151;">{log['bot_response']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
