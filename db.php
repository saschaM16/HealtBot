<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

$db_host = 'localhost';
$db_user = 'root';
$db_pass = ''; // Default XAMPP/Laragon password
$db_name = 'healthbot';

try {
    // Connect to MySQL server first without selecting a database
    $pdo = new PDO("mysql:host=$db_host;charset=utf8mb4", $db_user, $db_pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ]);
    
    // Create database if it does not exist
    $pdo->exec("CREATE DATABASE IF NOT EXISTS `$db_name` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $pdo->exec("USE `$db_name`");
    
    // Auto-initialize tables from healthbot.sql if they do not exist
    $tableCheck = $pdo->query("SHOW TABLES LIKE 'knowledge_base'");
    if ($tableCheck->rowCount() === 0) {
        $sqlPath = dirname(__DIR__) . '/database/healthbot.sql';
        if (file_exists($sqlPath)) {
            $sql = file_get_contents($sqlPath);
            // PDO exec can run multiple queries if the driver allows it. 
            // In case of multiple queries, we can run them directly.
            $pdo->exec($sql);
        }
    }
    
    // Pastikan admin 'kugle' terdaftar (menangani migrasi jika db sudah dibuat sebelumnya)
    try {
        $adminCheck = $pdo->prepare("SELECT COUNT(*) FROM admin WHERE username = ?");
        $adminCheck->execute(['kugle']);
        if ($adminCheck->fetchColumn() == 0) {
            // Bersihkan data admin lama agar tidak menumpuk
            $pdo->exec("DELETE FROM admin WHERE username = 'admin'");
            
            // Insert admin 'kugle' dengan password 'kugle32'
            $insertAdmin = $pdo->prepare("INSERT INTO admin (id, username, password, name) VALUES (?, ?, ?, ?)");
            $insertAdmin->execute([1, 'kugle', '$2y$10$FOtikTcDGZNc5zVorH4fTeGtqvEU.5LNG2yLiWu42F8HV0M/YqAnK', 'Dr. Budi Santoso']);
        }
    } catch (PDOException $e) {
        // Abaikan jika tabel admin belum terbuat
    }
} catch (PDOException $e) {
    die("Koneksi ke database gagal. Pastikan XAMPP/MySQL Anda sudah aktif. Error: " . $e->getMessage());
}

/**
 * Mendapatkan ID User berdasarkan session token.
 * Jika belum ada, maka akan dibuatkan user baru di database.
 */
function getOrCreateUser($pdo) {
    if (!isset($_SESSION['user_token'])) {
        $_SESSION['user_token'] = bin2hex(random_bytes(16));
    }
    
    $token = $_SESSION['user_token'];
    
    $stmt = $pdo->prepare("SELECT id FROM users WHERE session_token = ?");
    $stmt->execute([$token]);
    $user = $stmt->fetch();
    
    if (!$user) {
        $userAgent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';
        $ipAddress = $_SERVER['REMOTE_ADDR'] ?? 'Unknown';
        
        $insert = $pdo->prepare("INSERT INTO users (session_token, user_agent, ip_address) VALUES (?, ?, ?)");
        $insert->execute([$token, $userAgent, $ipAddress]);
        return $pdo->lastInsertId();
    }
    
    return $user['id'];
}
?>
