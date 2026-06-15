document.addEventListener('DOMContentLoaded', function() {
    const chatBody = document.getElementById('chatBody');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const btnSend = document.getElementById('btnSend');
    const btnClearChat = document.getElementById('btnClearChat');
    const suggestionChips = document.querySelectorAll('.suggestion-chip');

    // Scroll otomatis ke dasar kolom chat saat halaman dimuat
    scrollToBottom();

    // Event listener kirim form
    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            sendMessage(chatInput.value);
        });
    }

    // Event listener klik pada Suggestion Chips
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', function() {
            const question = this.getAttribute('data-question');
            sendMessage(question);
        });
    });

    // Event listener hapus riwayat chat
    if (btnClearChat) {
        btnClearChat.addEventListener('click', function() {
            if (confirm('Apakah Anda yakin ingin menghapus seluruh riwayat percakapan Anda?')) {
                clearChatHistory();
            }
        });
    }

    /**
     * Mengirim pesan user ke backend via AJAX
     */
    function sendMessage(messageText) {
        messageText = messageText.trim();
        if (messageText === '') return;

        // Reset input dan disable element selama proses kirim
        chatInput.value = '';
        toggleInputState(true);

        // Render bubble pesan user di UI
        appendUserMessage(messageText);
        scrollToBottom();

        // Tampilkan indikator mengetik (typing indicator)
        const typingIndicator = appendTypingIndicator();
        scrollToBottom();

        // Delay buatan 800ms agar percakapan terasa natural
        setTimeout(() => {
            fetch('chat_handler.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Respons jaringan bermasalah.');
                }
                return response.json();
            })
            .then(data => {
                // Hapus indikator mengetik
                removeTypingIndicator(typingIndicator);

                if (data.status === 'success') {
                    appendBotMessage(data.response, data.timestamp);
                } else {
                    appendBotMessage('Maaf, sistem mengalami kesalahan saat memproses jawaban: ' + data.message, getCurrentTime());
                }
                scrollToBottom();
                toggleInputState(false);
                chatInput.focus();
            })
            .catch(error => {
                removeTypingIndicator(typingIndicator);
                appendBotMessage('Koneksi terputus. Silakan periksa jaringan internet Anda atau aktifkan server database lokal Anda.', getCurrentTime());
                scrollToBottom();
                toggleInputState(false);
                chatInput.focus();
            });
        }, 800);
    }

    /**
     * Membersihkan riwayat chat di database dan UI
     */
    function clearChatHistory() {
        fetch('chat_handler.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: 'clear' })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Bersihkan UI chat body dan masukkan sambutan awal default
                chatBody.innerHTML = `
                    <div class="message-row bot">
                        <div class="message-bubble">
                            <div class="message-text">
                                Riwayat chat berhasil dihapus. Ada lagi yang bisa saya bantu hari ini seputar kesehatan Anda?
                            </div>
                            <span class="message-time">${getCurrentTime()}</span>
                        </div>
                    </div>
                `;
            } else {
                alert('Gagal membersihkan riwayat chat: ' + data.message);
            }
        })
        .catch(err => {
            alert('Kesalahan jaringan saat membersihkan chat.');
        });
    }

    /* Helper Utilities */

    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function toggleInputState(disabled) {
        chatInput.disabled = disabled;
        btnSend.disabled = disabled;
    }

    function getCurrentTime() {
        const now = new Date();
        const hrs = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');
        return `${hrs}:${mins}`;
    }

    // Memformat teks chat (Escaping HTML + format **bold** + newline)
    function formatMessageText(text) {
        // Escape HTML
        let escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        // Format **teks** menjadi <strong>teks</strong>
        let boldFormatted = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Ganti baris baru (\n) menjadi <br>
        return boldFormatted.replace(/\n/g, '<br>');
    }

    function appendUserMessage(text) {
        const row = document.createElement('div');
        row.className = 'message-row user';
        
        row.innerHTML = `
            <div class="message-bubble">
                <div class="message-text">${formatMessageText(text)}</div>
                <span class="message-time">${getCurrentTime()}</span>
            </div>
        `;
        chatBody.appendChild(row);
    }

    function appendBotMessage(text, time) {
        const row = document.createElement('div');
        row.className = 'message-row bot';
        
        row.innerHTML = `
            <div class="message-bubble">
                <div class="message-text">${formatMessageText(text)}</div>
                <span class="message-time">${time}</span>
            </div>
        `;
        chatBody.appendChild(row);
    }

    function appendTypingIndicator() {
        const row = document.createElement('div');
        row.className = 'message-row bot temp-typing';
        
        row.innerHTML = `
            <div class="message-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        chatBody.appendChild(row);
        return row;
    }

    function removeTypingIndicator(element) {
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }
});
