<?php
// Get current page name for active link highlight
$current_page = basename($_SERVER['SCRIPT_NAME']);
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo isset($page_title) ? $page_title . " - HealthBot" : "HealthBot - Asisten Informasi Kesehatan"; ?></title>
    
    <!-- SEO Meta Tags -->
    <meta name="description" content="HealthBot membantu Anda mendapatkan informasi kesehatan dasar, pola hidup sehat, nutrisi, dan kalkulator BMI secara cepat dan mudah.">
    <meta name="keywords" content="HealthBot, asisten kesehatan, chatbot kesehatan, kalkulator BMI, pola hidup sehat, konsultasi kesehatan">
    <meta name="author" content="HealthBot Team">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- FontAwesome Icons (CDN) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Main Style CSS -->
    <link rel="stylesheet" href="../assets/css/style.css">
    
    <!-- Page Specific CSS -->
    <?php if ($current_page == 'chat.php'): ?>
        <link rel="stylesheet" href="../assets/css/chat.css">
    <?php elseif ($current_page == 'admin_dashboard.php' || $current_page == 'admin_login.php'): ?>
        <link rel="stylesheet" href="../assets/css/admin.css">
    <?php endif; ?>
</head>
<body>
    <div class="main-wrapper">
        <!-- Navbar -->
        <header class="navbar-header">
            <div class="container">
                <nav class="navbar">
                    <a href="home.php" class="logo">
                        <i class="fa-solid fa-heart-pulse"></i>
                        <span>Health<span>Bot</span></span>
                    </a>
                    
                    <ul class="nav-menu" id="navMenu">
                        <li><a href="home.php" class="nav-link <?php echo $current_page == 'home.php' ? 'active' : ''; ?>">Beranda</a></li>
                        <li><a href="bmi.php" class="nav-link <?php echo $current_page == 'bmi.php' ? 'active' : ''; ?>">Kalkulator BMI</a></li>
                        <li><a href="about.php" class="nav-link <?php echo $current_page == 'about.php' ? 'active' : ''; ?>">Tentang</a></li>
                        
                        <?php if (isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true): ?>
                            <li><a href="admin_dashboard.php" class="nav-link <?php echo $current_page == 'admin_dashboard.php' ? 'active' : ''; ?>">Dashboard Admin</a></li>
                            <li><a href="admin_logout.php" class="btn-consult" style="background-color: var(--danger);"><i class="fa-solid fa-right-from-bracket"></i> Keluar</a></li>
                        <?php else: ?>
                            <li><a href="admin_login.php" class="nav-link <?php echo $current_page == 'admin_login.php' ? 'active' : ''; ?>"><i class="fa-solid fa-lock"></i> Admin</a></li>
                            <li><a href="chat.php" class="btn-consult">Mulai Konsultasi</a></li>
                        <?php endif; ?>
                    </ul>
                    
                    <div class="nav-toggle" id="navToggle">
                        <i class="fa-solid fa-bars"></i>
                    </div>
                </nav>
            </div>
        </header>
        
        <script>
            // Mobile navigation toggle
            document.addEventListener('DOMContentLoaded', function() {
                const navToggle = document.getElementById('navToggle');
                const navMenu = document.getElementById('navMenu');
                
                if (navToggle && navMenu) {
                    navToggle.addEventListener('click', function() {
                        navMenu.classList.toggle('open');
                        const icon = navToggle.querySelector('i');
                        if (navMenu.classList.contains('open')) {
                            icon.className = 'fa-solid fa-xmark';
                        } else {
                            icon.className = 'fa-solid fa-bars';
                        }
                    });
                }
            });
        </script>
