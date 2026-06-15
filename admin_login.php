<?php
require_once '../includes/db.php';

// Jika admin sudah login, langsung arahkan ke dashboard
if (isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true) {
    header("Location: admin_dashboard.php");
    exit;
}

$error_msg = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = trim($_POST['password'] ?? '');
    
    if ($username !== '' && $password !== '') {
        try {
            $stmt = $pdo->prepare("SELECT * FROM admin WHERE username = ?");
            $stmt->execute([$username]);
            $admin = $stmt->fetch();
            
            if ($admin && password_verify($password, $admin['password'])) {
                // Login berhasil, set sesi admin
                $_SESSION['admin_logged_in'] = true;
                $_SESSION['admin_id'] = $admin['id'];
                $_SESSION['admin_username'] = $admin['username'];
                $_SESSION['admin_name'] = $admin['name'];
                
                header("Location: admin_dashboard.php");
                exit;
            } else {
                $error_msg = "Username atau password salah.";
            }
        } catch (PDOException $e) {
            $error_msg = "Terjadi kesalahan database: " . $e->getMessage();
        }
    } else {
        $error_msg = "Harap isi semua kolom form login.";
    }
}

$page_title = "Admin Login";
require_once '../includes/header.php';
?>

<div class="container">
    <div class="login-container fade-in-up">
        <div class="login-card">
            <div class="login-icon">
                <i class="fa-solid fa-user-shield"></i>
            </div>
            <h2>Login Administrator</h2>
            <p>Masukkan kredensial admin Anda untuk mengelola chatbot HealthBot.</p>
            
            <!-- Alert Error -->
            <?php if ($error_msg !== ''): ?>
                <div class="alert alert-danger">
                    <i class="fa-solid fa-circle-exclamation"></i>
                    <span><?php echo htmlspecialchars($error_msg); ?></span>
                </div>
            <?php endif; ?>
            
            <!-- Login Form -->
            <form action="admin_login.php" method="POST">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" name="username" id="username" class="form-control" placeholder="Contoh: kugle" required autofocus autocomplete="off">
                </div>
                
                <div class="form-group" style="margin-bottom: 2rem;">
                    <label for="password">Password</label>
                    <input type="password" name="password" id="password" class="form-control" placeholder="Masukkan password Anda" required>
                </div>
                
                <button type="submit" class="btn-calculate btn-block">
                    <i class="fa-solid fa-right-to-bracket"></i> Masuk Dashboard
                </button>
            </form>
            
            <p style="margin-top: 1.5rem; font-size: 0.85rem; color: var(--gray);">
                Default: username (kugle) & password (kugle32)
            </p>
        </div>
    </div>
</div>

<?php
require_once '../includes/footer.php';
?>
