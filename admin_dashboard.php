<?php
require_once '../includes/db.php';

// Proteksi Halaman: Hanya admin yang boleh masuk
if (!isset($_SESSION['admin_logged_in']) || $_SESSION['admin_logged_in'] !== true) {
    header("Location: admin_login.php");
    exit;
}

$success_msg = '';
$error_msg = '';

// Proses CRUD Pengetahuan Chatbot via POST
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    $action = $_POST['action'];
    
    if ($action === 'add') {
        $category = trim($_POST['category'] ?? '');
        $keyword = trim($_POST['keyword'] ?? '');
        $response = trim($_POST['response'] ?? '');
        
        if ($category !== '' && $keyword !== '' && $response !== '') {
            try {
                $stmt = $pdo->prepare("INSERT INTO knowledge_base (category, keyword, response) VALUES (?, ?, ?)");
                $stmt->execute([$category, $keyword, $response]);
                $success_msg = "Data pengetahuan chatbot berhasil ditambahkan.";
            } catch (PDOException $e) {
                $error_msg = "Gagal menambahkan data: " . $e->getMessage();
            }
        } else {
            $error_msg = "Harap isi semua kolom form.";
        }
    }
    
    elseif ($action === 'edit') {
        $id = intval($_POST['id'] ?? 0);
        $category = trim($_POST['category'] ?? '');
        $keyword = trim($_POST['keyword'] ?? '');
        $response = trim($_POST['response'] ?? '');
        
        if ($id > 0 && $category !== '' && $keyword !== '' && $response !== '') {
            try {
                $stmt = $pdo->prepare("UPDATE knowledge_base SET category = ?, keyword = ?, response = ? WHERE id = ?");
                $stmt->execute([$category, $keyword, $response, $id]);
                $success_msg = "Data pengetahuan chatbot berhasil diperbarui.";
            } catch (PDOException $e) {
                $error_msg = "Gagal memperbarui data: " . $e->getMessage();
            }
        } else {
            $error_msg = "Data tidak valid atau kolom form kosong.";
        }
    }
}

// Proses Hapus Data via GET
if (isset($_GET['delete_kb']) && intval($_GET['delete_kb']) > 0) {
    $delete_id = intval($_GET['delete_kb']);
    try {
        $stmt = $pdo->prepare("DELETE FROM knowledge_base WHERE id = ?");
        $stmt->execute([$delete_id]);
        $success_msg = "Data pengetahuan chatbot berhasil dihapus.";
    } catch (PDOException $e) {
        $error_msg = "Gagal menghapus data: " . $e->getMessage();
    }
}

// Mengatur Tab Aktif
$tab = $_GET['tab'] ?? 'overview';

// Fetch statistik
$stats = ['chats' => 0, 'users' => 0, 'knowledge' => 0];
try {
    $stats['chats'] = $pdo->query("SELECT COUNT(*) FROM chat_history")->fetchColumn();
    $stats['users'] = $pdo->query("SELECT COUNT(*) FROM users")->fetchColumn();
    $stats['knowledge'] = $pdo->query("SELECT COUNT(*) FROM knowledge_base")->fetchColumn();
} catch (PDOException $e) {}

// Fetch daftar data knowledge base
$kb_list = [];
try {
    $kb_list = $pdo->query("SELECT * FROM knowledge_base ORDER BY category ASC, id DESC")->fetchAll();
} catch (PDOException $e) {}

// Fetch daftar log konsultasi terbaru
$logs_list = [];
try {
    $logs_list = $pdo->query("
        SELECT ch.*, u.session_token 
        FROM chat_history ch
        JOIN users u ON ch.user_id = u.id
        ORDER BY ch.created_at DESC
        LIMIT 100
    ")->fetchAll();
} catch (PDOException $e) {}

$page_title = "Dashboard Admin";
require_once '../includes/header.php';
?>

<div class="dashboard-layout">
    
    <!-- Sidebar Kiri -->
    <aside class="admin-sidebar">
        <ul class="sidebar-menu">
            <li>
                <a href="admin_dashboard.php?tab=overview" class="sidebar-link <?php echo $tab === 'overview' ? 'active' : ''; ?>">
                    <i class="fa-solid fa-chart-pie"></i> Ringkasan
                </a>
            </li>
            <li>
                <a href="admin_dashboard.php?tab=knowledge" class="sidebar-link <?php echo $tab === 'knowledge' ? 'active' : ''; ?>">
                    <i class="fa-solid fa-database"></i> Basis Pengetahuan
                </a>
            </li>
            <li>
                <a href="admin_dashboard.php?tab=logs" class="sidebar-link <?php echo $tab === 'logs' ? 'active' : ''; ?>">
                    <i class="fa-solid fa-clock-rotate-left"></i> Riwayat Konsultasi
                </a>
            </li>
        </ul>
        
        <div class="admin-profile">
            <div class="admin-avatar">
                <i class="fa-solid fa-user-md"></i>
            </div>
            <div class="admin-meta">
                <h4><?php echo htmlspecialchars($_SESSION['admin_name']); ?></h4>
                <span>Administrator</span>
            </div>
        </div>
    </aside>
    
    <!-- Konten Kanan -->
    <main class="admin-content">
        
        <!-- Notifikasi -->
        <?php if ($success_msg !== ''): ?>
            <div class="alert alert-success fade-in-up">
                <i class="fa-solid fa-circle-check"></i>
                <span><?php echo htmlspecialchars($success_msg); ?></span>
            </div>
        <?php endif; ?>
        
        <?php if ($error_msg !== ''): ?>
            <div class="alert alert-danger fade-in-up">
                <i class="fa-solid fa-circle-exclamation"></i>
                <span><?php echo htmlspecialchars($error_msg); ?></span>
            </div>
        <?php endif; ?>
        
        <!-- TAB OVERVIEW -->
        <?php if ($tab === 'overview'): ?>
            <div class="page-title-box">
                <h2>Ringkasan Statistik HealthBot</h2>
                <p>Selamat datang kembali, berikut ringkasan aktivitas konsultasi dan volume data hari ini.</p>
            </div>
            
            <div class="widgets-grid">
                <!-- Widget 1: Total Chat -->
                <div class="widget-card info">
                    <div class="widget-details">
                        <h4>Total Percakapan</h4>
                        <span><?php echo number_format($stats['chats']); ?></span>
                    </div>
                    <div class="widget-icon-container">
                        <i class="fa-solid fa-comments"></i>
                    </div>
                </div>
                
                <!-- Widget 2: Total Pengunjung -->
                <div class="widget-card primary">
                    <div class="widget-details">
                        <h4>Pengunjung Unik</h4>
                        <span><?php echo number_format($stats['users']); ?></span>
                    </div>
                    <div class="widget-icon-container">
                        <i class="fa-solid fa-users"></i>
                    </div>
                </div>
                
                <!-- Widget 3: Total Knowledge -->
                <div class="widget-card warning">
                    <div class="widget-details">
                        <h4>Data Kata Kunci</h4>
                        <span><?php echo number_format($stats['knowledge']); ?></span>
                    </div>
                    <div class="widget-icon-container">
                        <i class="fa-solid fa-brain"></i>
                    </div>
                </div>
            </div>
            
            <!-- Quick View Logs -->
            <div class="admin-panel">
                <div class="panel-header">
                    <h3>Konsultasi Terkini</h3>
                    <a href="admin_dashboard.php?tab=logs" style="font-size: 0.875rem; color: var(--primary); font-weight: 600;">Lihat Semua <i class="fa-solid fa-arrow-right"></i></a>
                </div>
                <div class="panel-body data-table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th style="width: 15%;">Waktu</th>
                                <th style="width: 20%;">Pengunjung</th>
                                <th style="width: 30%;">Pertanyaan</th>
                                <th style="width: 35%;">Jawaban Bot</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($logs_list)): ?>
                                <tr>
                                    <td colspan="4" style="text-align: center; color: var(--gray);">Belum ada riwayat percakapan masuk.</td>
                                </tr>
                            <?php else: ?>
                                <?php for($i = 0; $i < min(5, count($logs_list)); $i++): $log = $logs_list[$i]; ?>
                                    <tr>
                                        <td><strong><?php echo date('d M H:i', strtotime($log['created_at'])); ?></strong></td>
                                        <td><code><?php echo substr($log['session_token'], 0, 10); ?>...</code></td>
                                        <td><?php echo htmlspecialchars($log['user_message']); ?></td>
                                        <td><?php echo htmlspecialchars(substr($log['bot_response'], 0, 80)) . (strlen($log['bot_response']) > 80 ? '...' : ''); ?></td>
                                    </tr>
                                <?php endfor; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        
        <!-- TAB KNOWLEDGE BASE -->
        <?php elseif ($tab === 'knowledge'): ?>
            <div class="page-title-box" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h2>Basis Pengetahuan Chatbot</h2>
                    <p>Kelola daftar kata kunci pemicu dan respon jawaban chatbot HealthBot.</p>
                </div>
                <button class="btn-primary" onclick="openAddModal()" style="padding: 0.625rem 1.25rem; font-size: 0.9rem;">
                    <i class="fa-solid fa-plus"></i> Tambah Data Q&A
                </button>
            </div>
            
            <div class="admin-panel">
                <div class="panel-body data-table-container" style="padding: 0;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th style="width: 15%;">Kategori</th>
                                <th style="width: 25%;">Kata Kunci Pemicu</th>
                                <th style="width: 45%;">Respon Jawaban Bot</th>
                                <th style="width: 15%; text-align: center;">Aksi</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($kb_list)): ?>
                                <tr>
                                    <td colspan="4" style="text-align: center; color: var(--gray); padding: 2rem;">Data basis pengetahuan kosong.</td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($kb_list as $row): ?>
                                    <tr>
                                        <td><span class="bmi-category-badge badge-normal" style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; border: none; padding: 0.25rem 0.75rem;"><?php echo htmlspecialchars($row['category']); ?></span></td>
                                        <td><code><?php echo htmlspecialchars($row['keyword']); ?></code></td>
                                        <td style="font-size: 0.9rem; line-height: 1.4;"><?php echo nl2br(htmlspecialchars(substr($row['response'], 0, 150))) . (strlen($row['response']) > 150 ? '...' : ''); ?></td>
                                        <td style="text-align: center;">
                                            <div style="display: flex; justify-content: center; gap: 0.5rem;">
                                                <button class="btn-action edit" title="Edit Data" 
                                                        onclick="openEditModal(
                                                            <?php echo $row['id']; ?>, 
                                                            '<?php echo addslashes($row['category']); ?>', 
                                                            '<?php echo addslashes($row['keyword']); ?>', 
                                                            '<?php echo addslashes($row['response']); ?>'
                                                        )">
                                                    <i class="fa-solid fa-pen"></i>
                                                </button>
                                                <a href="admin_dashboard.php?tab=knowledge&delete_kb=<?php echo $row['id']; ?>" 
                                                   class="btn-action delete" title="Hapus Data"
                                                   onclick="return confirm('Apakah Anda yakin ingin menghapus kata kunci ini?');">
                                                    <i class="fa-solid fa-trash-can"></i>
                                                </a>
                                            </div>
                                        </td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
            
        <!-- TAB LOGS -->
        <?php elseif ($tab === 'logs'): ?>
            <div class="page-title-box">
                <h2>Riwayat Percakapan Pengguna</h2>
                <p>Log lengkap pesan konsultasi pengguna dan respon bot yang dicatat secara real-time.</p>
            </div>
            
            <div class="admin-panel">
                <div class="panel-body data-table-container" style="padding: 0;">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th style="width: 15%;">Waktu</th>
                                <th style="width: 20%;">Token Sesi Pengunjung</th>
                                <th style="width: 30%;">Pesan Pengguna</th>
                                <th style="width: 35%;">Respon Jawaban Bot</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php if (empty($logs_list)): ?>
                                <tr>
                                    <td colspan="4" style="text-align: center; color: var(--gray); padding: 2rem;">Belum ada log percakapan tercatat.</td>
                                </tr>
                            <?php else: ?>
                                <?php foreach ($logs_list as $log): ?>
                                    <tr>
                                        <td><strong><?php echo date('d M Y H:i:s', strtotime($log['created_at'])); ?></strong></td>
                                        <td><code><?php echo htmlspecialchars($log['session_token']); ?></code></td>
                                        <td style="font-size: 0.9rem;"><?php echo htmlspecialchars($log['user_message']); ?></td>
                                        <td style="font-size: 0.9rem; line-height: 1.4;"><?php echo nl2br(htmlspecialchars($log['bot_response'])); ?></td>
                                    </tr>
                                <?php endforeach; ?>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        <?php endif; ?>
        
    </main>
</div>

<!-- Modal Dialog CRUD (Basis Pengetahuan) -->
<div class="modal-overlay" id="kbModal">
    <div class="admin-modal">
        <div class="modal-header">
            <h3 id="modalTitle">Tambah Data Pengetahuan</h3>
            <button class="modal-close" onclick="closeModal()"><i class="fa-solid fa-xmark"></i></button>
        </div>
        
        <form action="admin_dashboard.php?tab=knowledge" method="POST">
            <input type="hidden" name="action" id="actionType" value="add">
            <input type="hidden" name="id" id="kbId" value="">
            
            <div class="modal-body">
                <div class="form-group">
                    <label for="kbCategory">Kategori</label>
                    <select name="category" id="kbCategory" class="form-control" required>
                        <option value="greeting">Greeting / Sambutan</option>
                        <option value="pola_hidup">Pola Hidup Sehat</option>
                        <option value="makanan">Makanan Bergizi</option>
                        <option value="olahraga">Olahraga Teratur</option>
                        <option value="tidur">Tidur Cukup</option>
                        <option value="tips_sehat">Tips Kesehatan Tubuh</option>
                        <option value="flu">Penyakit: Flu / Pilek</option>
                        <option value="batuk">Penyakit: Batuk</option>
                        <option value="demam">Penyakit: Demam</option>
                        <option value="sakit_kepala">Penyakit: Sakit Kepala</option>
                        <option value="maag">Penyakit: Maag</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="kbKeyword">Kata Kunci Pemicu (Gunakan koma sebagai pemisah)</label>
                    <input type="text" name="keyword" id="kbKeyword" class="form-control" placeholder="Contoh: batuk, tenggorokan gatal, berdahak" required autocomplete="off">
                </div>
                
                <div class="form-group">
                    <label for="kbResponse">Respon Jawaban Bot</label>
                    <textarea name="response" id="kbResponse" class="form-control" rows="5" placeholder="Tulis rincian jawaban atau pertolongan pertama kesehatan..." required></textarea>
                </div>
            </div>
            
            <div class="modal-footer">
                <button type="button" class="btn-secondary" style="padding: 0.625rem 1.25rem;" onclick="closeModal()">Batal</button>
                <button type="submit" class="btn-primary" style="padding: 0.625rem 1.25rem;">Simpan Perubahan</button>
            </div>
        </form>
    </div>
</div>

<!-- Scripts Modal -->
<script>
    const kbModal = document.getElementById('kbModal');
    
    function openAddModal() {
        document.getElementById('modalTitle').textContent = 'Tambah Data Pengetahuan';
        document.getElementById('actionType').value = 'add';
        document.getElementById('kbId').value = '';
        document.getElementById('kbCategory').value = 'greeting';
        document.getElementById('kbKeyword').value = '';
        document.getElementById('kbResponse').value = '';
        
        kbModal.classList.add('open');
    }
    
    function openEditModal(id, category, keyword, response) {
        document.getElementById('modalTitle').textContent = 'Edit Data Pengetahuan';
        document.getElementById('actionType').value = 'edit';
        document.getElementById('kbId').value = id;
        document.getElementById('kbCategory').value = category;
        document.getElementById('kbKeyword').value = keyword;
        document.getElementById('kbResponse').value = response;
        
        kbModal.classList.add('open');
    }
    
    function closeModal() {
        kbModal.classList.remove('open');
    }
    
    // Tutup modal jika mengklik background overlay
    window.addEventListener('click', function(e) {
        if (e.target === kbModal) {
            closeModal();
        }
    });
</script>

<?php
require_once '../includes/footer.php';
?>
