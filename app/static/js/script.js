// Tüm sayfalarda çalışacak genel JavaScript kodları
document.addEventListener('DOMContentLoaded', function() {
    // Tooltip'leri etkinleştir
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popover'ları etkinleştir
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Form doğrulama
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Otomatik kapanan alert'leri kapat
    var alertList = document.querySelectorAll('.alert-auto-close');
    alertList.forEach(function(alert) {
        setTimeout(function() {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Sayfa yüklendiğinde animasyon ekle
    document.body.classList.add('animate-fade-in');
});

// Dosya yükleme işlemleri
function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    
    const files = evt.target.files || evt.dataTransfer.files;
    handleFiles(files);
}

function handleFiles(files) {
    const file = files[0];
    const fileType = file.type;
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (!validTypes.includes(fileType)) {
        showAlert('Lütfen sadece PDF veya Word belgesi yükleyin.', 'danger');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) { // 5MB sınırı
        showAlert('Dosya boyutu 5MB\'dan büyük olamaz.', 'danger');
        return;
    }
    
    // Dosya önizlemesi göster
    showFilePreview(file);
}

function showFilePreview(file) {
    const previewContainer = document.getElementById('file-preview');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const uploadBtn = document.getElementById('upload-btn');
    
    // Dosya bilgilerini göster
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    // Önizleme container'ını göster
    previewContainer.classList.remove('d-none');
    
    // Yükleme butonunu aktif et
    uploadBtn.disabled = false;
    
    // Form verisini güncelle
    const fileInput = document.querySelector('input[type="file"]');
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.alerts-container') || document.querySelector('main');
    container.prepend(alertDiv);
    
    // 5 saniye sonra otomatik kapat
    setTimeout(() => {
        const alert = new bootstrap.Alert(alertDiv);
        alert.close();
    }, 5000);
}

// CV analiz sonuçları için grafik oluşturma
function createRadarChart(data) {
    const ctx = document.getElementById('radarChart');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Eğitim', 'Deneyim', 'Yetenekler', 'Dil', 'Sertifikalar'],
            datasets: [{
                label: 'CV Puanı',
                data: data,
                backgroundColor: 'rgba(78, 115, 223, 0.2)',
                borderColor: 'rgba(78, 115, 223, 1)',
                pointBackgroundColor: 'rgba(78, 115, 223, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(78, 115, 223, 1)'
            }]
        },
        options: {
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
}

// Sayfa yüklendiğinde grafiği oluştur
if (document.getElementById('radarChart')) {
    // Örnek veri, gerçek verilerle değiştirilecek
    const sampleData = [85, 75, 90, 60, 70];
    createRadarChart(sampleData);
}

// Dropzone işlevselliği
function setupDropzone() {
    const dropArea = document.getElementById('drop-area');
    if (!dropArea) return;
    
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ;['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ;['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.classList.add('highlight');
    }
    
    function unhighlight() {
        dropArea.classList.remove('highlight');
    }
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
}

// Sayfa yüklendiğinde dropzone'u ayarla
document.addEventListener('DOMContentLoaded', setupDropzone);
