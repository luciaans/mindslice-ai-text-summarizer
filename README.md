# 🧠 MindSlice - AI Text Summarizer

**Ubah teks panjang menjadi ringkasan singkat menggunakan Artificial Intelligence.**

MindSlice adalah aplikasi web berbasis Streamlit yang menggunakan Ollama untuk meringkas teks panjang menjadi ringkasan yang mudah dipahami. Mendukung berbagai format file dan dilengkapi dengan template prompt kustom untuk hasil ringkasan yang optimal.

## ✨ Fitur

- 🤖 **AI-Powered Summarization** - Menggunakan berbagai model AI lokal via Ollama
- 📁 **Multi-Format Support** - Mendukung PDF, DOCX, dan TXT
- 🌐 **Dual Language** - Ringkasan dalam Bahasa Indonesia dan English
- 📏 **Flexible Length** - Pilihan ringkasan singkat, sedang, atau panjang
- ✏️ **Custom Prompts** - Template prompt khusus untuk berbagai kebutuhan
- 📊 **Text Statistics** - Analisis kata, karakter, kalimat, dan estimasi waktu baca
- 💾 **Download Results** - Export ringkasan dalam format TXT
- 🎨 **Modern UI** - Interface yang responsive dan user-friendly
- ⚡ **Real-time Processing** - Status koneksi dan progress indicator

## 🚀 Quick Start

### Prasyarat

1. **Python 3.7+** - Pastikan Python sudah terinstall
2. **Ollama** - Install dan jalankan Ollama server
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Jalankan Ollama server
   ollama serve
   
   # Download model AI (pilih salah satu)
   ollama pull llama3.2:3b
   ollama pull mistral:7b
   ollama pull phi3:mini
   ```

### Instalasi

1. Clone repository ini:
   ```bash
   git clone https://github.com/username/mindslice.git
   cd mindslice
   ```

2. Buat virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

5. Akses aplikasi di `http://localhost:8501`

## 🛠️ Struktur Project

```
mindslice/
├── venv/                 # Python virtual environment
│   ├── etc/             # Environment config
│   ├── Include/         # Header files
│   ├── Lib/            # Python libraries
│   └── Scripts/        # Executable scripts
├── share/              # Shared resources
├── pyvenv.cfg          # Virtual env configuration
├── app.py              # Main Streamlit application
├── index.html          # Static HTML (if any)
├── index.js            # JavaScript files (if any)
└── requirements.txt    # Python dependencies
```

## 📋 Dependencies

File `requirements.txt` harus berisi:

```txt
streamlit>=1.28.0
requests>=2.31.0
PyPDF2>=3.0.1
python-docx>=0.8.11
ollama>=0.1.0
```

## 🎯 Template Prompt

### Template Tersedia:
- **Fokus Metodologi** - Ringkasan dengan fokus pada cara penelitian dilakukan
- **Fokus Hasil** - Emphasis pada temuan dan hasil utama
- **Fokus Kesimpulan** - Highlight kesimpulan dan rekomendasi
- **Poin-poin Penting** - Format bullet points yang mudah dibaca
- **Ringkasan Eksekutif** - Format untuk presentasi manajemen
- **Custom** - Tulis instruksi sendiri

## 🤖 Model AI yang Didukung

- **llama3.2:3b** - Model ringan, cepat
- **llama3.2:7b** - Model medium, balance antara speed dan quality
- **llama3.1:8b** - Model advanced dengan kualitas tinggi
- **phi3:mini** - Model Microsoft yang efisien
- **mistral:7b** - Model Mistral dengan performa baik
- **gemma:7b** - Model Google Gemma
- **qwen2:7b** - Model Qwen dengan kemampuan multilingual

## 📊 Fitur Statistik

### Input Statistics:
- **Jumlah Kata** - Total kata dalam teks
- **Jumlah Karakter** - Total karakter termasuk spasi
- **Jumlah Kalimat** - Estimasi berdasarkan tanda baca
- **Estimasi Waktu Baca** - Berdasarkan 200 kata/menit

### Summary Statistics:
- **Rasio Kompresi** - Persentase pengurangan teks
- **Waktu Proses** - Durasi pembuatan ringkasan
- **Model & Konfigurasi** - Detail pengaturan yang digunakan

## 🎨 Kustomisasi

### Mengubah Model Default
Edit di `app.py`:

```python
self.model_tersedia = [
    "model-baru:7b",  # Tambah model baru
    "llama3.2:3b",
    # ... model lainnya
]
```

### Menambah Template Prompt
Tambahkan di section template_prompt:

```python
template_prompt = {
    "Template Baru": "Instruksi prompt baru Anda...",
    # ... template lainnya
}
```

### Mengubah Tema UI
Modifikasi CSS di bagian `st.markdown()` untuk styling kustom.

## 📱 Penggunaan

1. **Pilih Input Method**:
   - Upload file (PDF/DOCX/TXT)
   - Paste teks langsung

2. **Konfigurasi di Sidebar**:
   - Pilih model AI
   - Atur panjang ringkasan
   - Pilih bahasa output
   - Optional: gunakan template prompt

3. **Generate Summary**:
   - Klik tombol "Buat Ringkasan"
   - Tunggu proses selesai
   - Review hasil dan statistik

4. **Download Results**:
   - Download ringkasan saja
   - Download format lengkap dengan metadata

## 🔧 Troubleshooting

### Ollama Connection Error
```bash
# Pastikan Ollama berjalan
ollama serve

# Test koneksi
curl http://localhost:11434/api/tags
```

### Model Not Found
```bash
# List model yang tersedia
ollama list

# Download model yang diperlukan
ollama pull llama3.2:3b
```

### Memory Issues
- Gunakan model yang lebih kecil (phi3:mini)
- Batasi panjang teks input
- Restart Ollama service

### File Upload Error
- Periksa format file (PDF/DOCX/TXT only)
- Maksimal ukuran file 10MB
- Pastikan file tidak corrupt

## 🚀 Performance Tips

1. **Model Selection**:
   - `phi3:mini` - Tercepat, kualitas cukup
   - `llama3.2:3b` - Balance speed/quality
   - `llama3.2:7b` - Kualitas terbaik

2. **Text Length**:
   - Optimal: 1000-5000 kata
   - Minimum: 100 kata
   - Maximum: 50,000 karakter

3. **Hardware Requirements**:
   - RAM: Minimum 8GB (16GB recommended)
   - CPU: Multi-core processor
   - Storage: 5GB+ untuk model

## 🤝 Kontribusi

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/fitur-baru`)
3. Commit perubahan (`git commit -am 'Tambah fitur baru'`)
4. Push ke branch (`git push origin feature/fitur-baru`)
5. Buat Pull Request

## 📄 Format Output

### Ringkasan Standard
```
Ringkasan teks dalam format paragraf yang mudah dipahami...
```

### Format Lengkap
```
RINGKASAN TEKS
==================================================

INFORMASI:
- Tanggal: 24/07/2025 10:30:00
- Model: llama3.2:3b
- Panjang: Sedang
- Bahasa: Indonesia

RINGKASAN (150 kata):
[Isi ringkasan...]

STATISTIK:
- Rasio Kompresi: 15.2%
- Waktu Proses: 3.4 detik
```

## 🔒 Privacy & Security

- ✅ Semua pemrosesan dilakukan secara lokal
- ✅ Tidak ada data yang dikirim ke server eksternal
- ✅ File upload bersifat sementara
- ✅ Riwayat tidak disimpan secara permanen

---

**Made by Lucians**
