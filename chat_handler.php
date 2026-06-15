<?php
header('Content-Type: application/json; charset=utf-8');
require_once '../includes/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'message' => 'Metode request tidak diizinkan.']);
    exit;
}

// Mendapatkan data input JSON
$input = json_decode(file_get_contents('php://input'), true);

// Aksi membersihkan chat
if (isset($input['action']) && $input['action'] === 'clear') {
    $user_id = getOrCreateUser($pdo);
    try {
        $stmt = $pdo->prepare("DELETE FROM chat_history WHERE user_id = ?");
        $stmt->execute([$user_id]);
        echo json_encode(['status' => 'success', 'message' => 'Riwayat percakapan telah dihapus.']);
    } catch (PDOException $e) {
        echo json_encode(['status' => 'error', 'message' => 'Gagal menghapus riwayat: ' . $e->getMessage()]);
    }
    exit;
}

$user_message = $input['message'] ?? $_POST['message'] ?? '';
$user_message = trim($user_message);

if ($user_message === '') {
    echo json_encode(['status' => 'error', 'message' => 'Pesan kosong tidak dapat diproses.']);
    exit;
}

// Dapatkan atau buat user ID session
$user_id = getOrCreateUser($pdo);

$bot_response = null;

try {
    // Ambil data knowledge base untuk dicocokkan
    $stmt = $pdo->query("SELECT * FROM knowledge_base");
    $knowledge = $stmt->fetchAll();
    
    // Normalisasi input pesan
    $normalized_msg = strtolower($user_message);
    
    // Mencari kecocokan kata kunci
    foreach ($knowledge as $row) {
        $keywords = explode(',', $row['keyword']);
        foreach ($keywords as $kw) {
            $kw = trim(strtolower($kw));
            if ($kw !== '' && strpos($normalized_msg, $kw) !== false) {
                $bot_response = $row['response'];
                break 2; // Berhenti mencari jika sudah menemukan kecocokan pertama
            }
        }
    }
    
    // Jika tidak ditemukan kecocokan
    if (!$bot_response) {
        $bot_response = "Maaf, HealthBot belum memahami pertanyaan Anda. Silakan tanyakan hal lain seputar kesehatan seperti 'flu', 'batuk', 'demam', 'pola hidup', 'olahraga', atau 'nutrisi makanan'. Harap diingat bahwa informasi ini bersifat dasar dan bukan pengganti pemeriksaan medis dokter.";
    }
    
    // Simpan ke riwayat database
    $insert = $pdo->prepare("INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)");
    $insert->execute([$user_id, $user_message, $bot_response]);
    
    // Kirim respon JSON
    echo json_encode([
        'status' => 'success',
        'response' => $bot_response,
        'timestamp' => date('H:i')
    ]);
    
} catch (PDOException $e) {
    echo json_encode([
        'status' => 'error',
        'message' => 'Terjadi kesalahan database: ' . $e->getMessage()
    ]);
}
?>
