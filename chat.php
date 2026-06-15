<?php
require_once '../includes/db.php';

$page_title = "Konsultasi HealthBot";

// Dapatkan ID User dan ambil riwayat percakapan sebelumnya jika ada
$user_id = getOrCreateUser($pdo);

try {
    $stmt = $pdo->prepare("SELECT * FROM chat_history WHERE user_id = ? ORDER BY created_at ASC");
    $stmt->execute([$user_id]);
    $chat_history = $stmt->fetchAll();
} catch (PDOException $e) {
    $chat_history = [];
}

require_once '../includes/header.php';
?>

<div class="container">
    <div class="chat-page-container fade-in-up">
        
        <!-- Header Chat -->
        <div class="chat-header">
            <div class="chat-bot-info">
                <div class="chat-avatar">
                    <i class="fa-solid fa-robot"></i>
                    <div class="chat-status-dot"></div>
                </div>
                <div class="chat-bot-details">
                    <h3>HealthBot</h3>
                    <div class="chat-bot-status">
                        <i class="fa-solid fa-circle-play"></i> Online - Asisten Medis
                    </div>
                </div>
            </div>
            
            <button class="btn-clear-chat" id="btnClearChat">
                <i class="fa-solid fa-trash-can"></i> Bersihkan Chat
            </button>
        </div>
        
        <!-- Body Chat (Pesan Log) -->
        <div class="chat-body" id="chatBody">
            
            <!-- Default Bot Welcome Message (jika riwayat kosong) -->
            <?php if (empty($chat_history)): ?>
                <div class="message-row bot">
                    <div class="message-bubble">
                        <div class="message-text">
                            Halo! Saya **HealthBot**, asisten virtual kesehatan Anda. 
                            Saya dapat membantu memberikan informasi tentang pola hidup sehat, nutrisi makanan, olahraga, tips tidur, dan penanganan mandiri penyakit ringan seperti flu, batuk, demam, maag, atau sakit kepala.
                            <br><br>
                            Ada yang ingin Anda tanyakan hari ini?
                        </div>
                        <span class="message-time"><?php echo date('H:i'); ?></span>
                    </div>
                </div>
            <?php else: ?>
                <!-- Render Riwayat dari Database -->
                <?php foreach ($chat_history as $chat): ?>
                    <!-- Pesan User -->
                    <div class="message-row user">
                        <div class="message-bubble">
                            <div class="message-text"><?php echo nl2br(htmlspecialchars($chat['user_message'])); ?></div>
                            <span class="message-time"><?php echo date('H:i', strtotime($chat['created_at'])); ?></span>
                        </div>
                    </div>
                    <!-- Respon Bot -->
                    <div class="message-row bot">
                        <div class="message-bubble">
                            <div class="message-text"><?php echo nl2br(htmlspecialchars($chat['bot_response'])); ?></div>
                            <span class="message-time"><?php echo date('H:i', strtotime($chat['created_at'])); ?></span>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php endif; ?>
            
        </div>
        
        <!-- Footer Chat & Suggestions -->
        <div class="chat-footer">
            
            <!-- Quick Suggestion Chips -->
            <div class="chat-suggestions" id="chatSuggestions">
                <div class="chat-suggestions-title">Rekomendasi Pertanyaan:</div>
                <div class="chips-container">
                    <div class="suggestion-chip" data-question="Bagaimana pola hidup sehat?">Pola Hidup Sehat</div>
                    <div class="suggestion-chip" data-question="Cara mengatasi flu dan bersin?">Pertolongan Flu</div>
                    <div class="suggestion-chip" data-question="Bagaimana menu makanan bergizi seimbang?">Gizi Seimbang</div>
                    <div class="suggestion-chip" data-question="Mengatasi nyeri lambung atau maag?">Sakit Maag</div>
                    <div class="suggestion-chip" data-question="Mengapa begadang berbahaya?">Bahaya Begadang</div>
                </div>
            </div>
            
            <!-- Input Form -->
            <form class="chat-input-form" id="chatForm" onsubmit="return false;">
                <div class="chat-input-wrapper">
                    <input type="text" class="chat-input" id="chatInput" placeholder="Ketik pertanyaan kesehatan Anda di sini..." autocomplete="off" required>
                </div>
                <button type="submit" class="btn-send-chat" id="btnSend" aria-label="Kirim Pesan">
                    <i class="fa-solid fa-paper-plane"></i>
                </button>
            </form>
            
        </div>
        
    </div>
</div>

<!-- Scripts -->
<script src="../assets/js/chat.js"></script>

<?php
require_once '../includes/footer.php';
?>
