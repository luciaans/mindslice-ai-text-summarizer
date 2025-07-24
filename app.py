import streamlit as st
import requests
import json
import PyPDF2
import docx
import io
import time
from typing import Optional

# Konfigurasi halaman
st.set_page_config(
    page_title="MindSlice",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS kustom yang diperbaiki
st.markdown("""
<style>
    /* Reset dan base styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        font-family: 'Arial', sans-serif;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.5;
    }
    
    /* Card sections */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
    }
    
    .upload-card {
        background: linear-gradient(135deg, #fef7f7 0%, #fef2f2 100%);
        border: 1px solid #fecaca;
    }
    
    .result-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
    }
    
    .summary-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-left: 4px solid #0284c7;
        margin: 1rem 0;
    }
    
    /* Stats container */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px -2px rgba(0, 0, 0, 0.15);
    }
    
    .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #059669;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Alert boxes */
    .alert-success {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .alert-error {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fcd34d;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    .sidebar-section {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px -2px rgba(220, 38, 38, 0.3);
    }
    
    /* Download buttons */
    .download-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .download-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .main-header {
            font-size: 2rem;
        }
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #6b7280;
        font-size: 0.9rem;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-radius: 8px;
        margin-top: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Responsive improvements */
    @media (max-width: 640px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .card {
            padding: 1rem;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Loading spinner custom */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        flex-direction: column;
    }
    
    .loading-text {
        margin-top: 1rem;
        color: #6b7280;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

class PeringkasTeks:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_tersedia = [
            "llama3.2:3b",
            "llama3.2:7b", 
            "llama3.1:8b",
            "phi3:mini",
            "mistral:7b",
            "gemma:7b",
            "qwen2:7b"
        ]
    
    def periksa_koneksi_ollama(self):
        """Periksa apakah Ollama sedang berjalan"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def ambil_model_terinstall(self):
        """Ambil daftar model yang telah terinstall"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json()
                return [model['name'] for model in models['models']]
            return []
        except:
            return []
    
    def ringkas_teks(self, teks: str, model: str, panjang_ringkasan: str, bahasa: str = "Indonesia", prompt_kustom: str = "") -> Optional[str]:
        """Meringkas teks menggunakan Ollama"""
        
        # Jika prompt kustom tersedia, gunakan itu
        if prompt_kustom.strip():
            if bahasa == "Indonesia":
                prompt = f"{prompt_kustom}\n\nTeks yang akan diringkas:\n{teks}\n\nRingkasan:"
            else:
                prompt = f"{prompt_kustom}\n\nText to summarize:\n{teks}\n\nSummary:"
        else:
            # Gunakan prompt default berdasarkan panjang dan bahasa
            if bahasa == "Indonesia":
                prompt_panjang = {
                    "Singkat": "Buatlah ringkasan singkat dari teks ini dalam 2-3 kalimat, fokus pada poin utama:",
                    "Sedang": "Buatlah ringkasan komprehensif dari teks ini dalam 1-2 paragraf dengan bahasa Indonesia yang baik dan benar:",
                    "Panjang": "Buatlah ringkasan detail dari teks ini, termasuk poin-poin penting, detail yang relevan, dan kesimpulan utama dalam bahasa Indonesia yang mudah dipahami:"
                }
            else:
                prompt_panjang = {
                    "Singkat": "Summarize this text in 2-3 sentences, focusing on the main points:",
                    "Sedang": "Provide a comprehensive summary of this text in 1-2 paragraphs:",
                    "Panjang": "Create a detailed summary of this text, including key points, important details, and main conclusions:"
                }
            
            prompt = f"{prompt_panjang[panjang_ringkasan]}\n\n{teks}\n\nRingkasan:"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9,
                "max_tokens": 1500 if panjang_ringkasan == "Panjang" else 800,
                "num_predict": 1500 if panjang_ringkasan == "Panjang" else 800
            }
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            if response.status_code == 200:
                hasil = response.json()['response'].strip()
                return hasil.replace("Ringkasan:", "").replace("Summary:", "").strip()
            else:
                return None
        except Exception as e:
            st.error(f"❌ Kesalahan koneksi ke Ollama: {str(e)}")
            return None

def ekstrak_teks_dari_pdf(file):
    """Ekstrak teks dari file PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        teks = ""
        for halaman in pdf_reader.pages:
            teks += halaman.extract_text() + "\n"
        return teks.strip()
    except Exception as e:
        st.error(f"❌ Kesalahan membaca PDF: {str(e)}")
        return None

def ekstrak_teks_dari_docx(file):
    """Ekstrak teks dari file DOCX"""
    try:
        doc = docx.Document(file)
        teks = ""
        for paragraf in doc.paragraphs:
            teks += paragraf.text + "\n"
        return teks.strip()
    except Exception as e:
        st.error(f"❌ Kesalahan membaca DOCX: {str(e)}")
        return None

def ekstrak_teks_dari_txt(file):
    """Ekstrak teks dari file TXT"""
    try:
        return file.read().decode('utf-8')
    except UnicodeDecodeError:
        try:
            file.seek(0)
            return file.read().decode('latin-1')
        except Exception as e:
            st.error(f"❌ Kesalahan membaca TXT: {str(e)}")
            return None
    except Exception as e:
        st.error(f"❌ Kesalahan membaca file: {str(e)}")
        return None

def hitung_kata(teks):
    """Hitung jumlah kata dalam teks"""
    return len(teks.split())

def estimasi_waktu_baca(teks):
    """Estimasi waktu baca (rata-rata 200 kata per menit)"""
    jumlah_kata = hitung_kata(teks)
    return round(jumlah_kata / 200, 1)

def hitung_kalimat(teks):
    """Hitung jumlah kalimat dalam teks"""
    import re
    kalimat = re.split(r'[.!?]+', teks)
    return len([k for k in kalimat if k.strip()])

def tampilkan_statistik(teks):
    """Tampilkan statistik teks dalam grid responsif"""
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{}</div>
            <div class="stat-label">Kata</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{}</div>
            <div class="stat-label">Karakter</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{}</div>
            <div class="stat-label">Kalimat</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{} min</div>
            <div class="stat-label">Estimasi Baca</div>
        </div>
    </div>
    """.format(
        hitung_kata(teks),
        len(teks),
        hitung_kalimat(teks),
        estimasi_waktu_baca(teks)
    ), unsafe_allow_html=True)

def main():
    # Inisialisasi peringkas
    peringkas = PeringkasTeks()
    
    # Header
    st.markdown('<div class="main-header">🧠 MindSlice</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Ubah teks panjang menjadi ringkasan singkat menggunakan Artificial Intelligence</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Pengaturan")
        
        # Periksa koneksi Ollama
        if not peringkas.periksa_koneksi_ollama():
            st.markdown("""
            <div class="alert-error">
                <strong>🚨 Ollama tidak berjalan!</strong><br>
                Silakan jalankan Ollama terlebih dahulu.<br>
                <code>ollama serve</code>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Ambil model yang terinstall
        model_terinstall = peringkas.ambil_model_terinstall()
        if not model_terinstall:
            st.markdown("""
            <div class="alert-error">
                <strong>🚨 Tidak ada model yang ditemukan!</strong><br>
                Silakan install model terlebih dahulu.<br>
                <code>ollama pull llama3.2:3b</code>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Pemilihan model
        with st.container():
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            model_terpilih = st.selectbox(
                "🤖 Pilih Model AI",
                model_terinstall,
                help="Pilih model AI untuk meringkas teks"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Panjang ringkasan
        with st.container():
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            panjang_ringkasan = st.select_slider(
                "📏 Panjang Ringkasan",
                options=["Singkat", "Sedang", "Panjang"],
                value="Sedang",
                help="Pilih seberapa detail ringkasan yang diinginkan"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Pemilihan bahasa
        with st.container():
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            bahasa = st.selectbox(
                "🌐 Pilih Bahasa",
                ["Indonesia", "English"],
                index=0,
                help="Pilih bahasa untuk ringkasan"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Opsi prompt kustom
        st.markdown("---")
        with st.container():
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            gunakan_prompt_kustom = st.checkbox(
                "✏️ Gunakan Prompt Kustom",
                help="Aktifkan untuk menulis instruksi ringkasan sendiri"
            )
            
            prompt_kustom = ""
            if gunakan_prompt_kustom:
                # Template prompt cepat
                st.markdown("**🎯 Template Cepat:**")
                template_prompt = {
                    "Kustom": "",
                    "Fokus Metodologi": "Tolong ringkas teks ini dengan fokus pada metodologi dan cara penelitian dilakukan",
                    "Fokus Hasil": "Tolong ringkas teks ini dengan fokus pada hasil dan temuan utama",
                    "Fokus Kesimpulan": "Tolong ringkas teks ini dengan fokus pada kesimpulan dan rekomendasi",
                    "Poin-poin Penting": "Tolong buat ringkasan dalam bentuk poin-poin utama yang mudah dibaca",
                    "Ringkasan Eksekutif": "Tolong buat ringkasan eksekutif yang cocok untuk presentasi kepada manajemen"
                }
                
                template_terpilih = st.selectbox(
                    "📋 Template:",
                    list(template_prompt.keys()),
                    help="Pilih template atau 'Kustom' untuk menulis sendiri"
                )
                
                if template_terpilih != "Kustom":
                    prompt_kustom = template_prompt[template_terpilih]
                    st.text_area(
                        "📝 Pratinjau Prompt:",
                        value=prompt_kustom,
                        height=100,
                        disabled=True
                    )
                else:
                    prompt_kustom = st.text_area(
                        "📝 Instruksi Kustom",
                        placeholder="Contoh: Tolong ringkas file ini fokus pada bagian metodologi dan hasil penelitian saja...",
                        height=120,
                        help="Tulis instruksi khusus untuk ringkasan yang Anda inginkan"
                    )
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Konten utama
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="card upload-card">', unsafe_allow_html=True)
        st.subheader("📁 Input Teks")
        
        # Pemilihan metode input
        metode_input = st.radio(
            "Pilih metode input:",
            ["Upload File", "Tempel Teks"],
            horizontal=True
        )
        
        teks_terekstrak = ""
        
        if metode_input == "Upload File":
            file_terupload = st.file_uploader(
                "📤 Upload dokumen Anda",
                type=['pdf', 'docx', 'txt'],
                help="Format yang didukung: PDF, DOCX, TXT (maksimal 10MB)"
            )
            
            if file_terupload:
                # Periksa ukuran file
                ukuran_file = len(file_terupload.getvalue())
                if ukuran_file > 10 * 1024 * 1024:  # 10MB
                    st.markdown("""
                    <div class="alert-error">
                        ❌ Ukuran file terlalu besar! Maksimal 10MB.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    tipe_file = file_terupload.name.split('.')[-1].lower()
                    
                    # Loading sederhana
                    with st.spinner("🔄 Mengekstrak teks..."):
                        if tipe_file == 'pdf':
                            teks_terekstrak = ekstrak_teks_dari_pdf(file_terupload)
                        elif tipe_file == 'docx':
                            teks_terekstrak = ekstrak_teks_dari_docx(file_terupload)
                        elif tipe_file == 'txt':
                            teks_terekstrak = ekstrak_teks_dari_txt(file_terupload)
                    
                    if teks_terekstrak:
                        st.markdown(f"""
                        <div class="alert-success">
                            ✅ Teks berhasil diekstrak dari {file_terupload.name}!
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Pratinjau teks
                        with st.expander("📖 Pratinjau teks yang diekstrak"):
                            st.text_area(
                                "Konten yang diekstrak:",
                                teks_terekstrak[:1500] + "..." if len(teks_terekstrak) > 1500 else teks_terekstrak,
                                height=200,
                                disabled=True
                            )
        
        else:  # Tempel Teks
            teks_terekstrak = st.text_area(
                "📝 Tempel teks Anda di sini:",
                height=300,
                placeholder="Masukkan teks yang ingin Anda ringkas...\n\nContoh: Artikel berita, makalah penelitian, laporan, atau teks panjang lainnya."
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistik teks
        if teks_terekstrak:
            tampilkan_statistik(teks_terekstrak)
    
    with col2:
        st.markdown('<div class="card result-card">', unsafe_allow_html=True)
        st.subheader("✨ Hasil Ringkasan")
        
        if teks_terekstrak:
            if st.button("🚀 Buat Ringkasan", type="primary"):
                if len(teks_terekstrak.strip()) < 100:
                    st.markdown("""
                    <div class="alert-warning">
                        ⚠️ Teks terlalu pendek untuk diringkas! Minimal 100 kata.
                    </div>
                    """, unsafe_allow_html=True)
                elif len(teks_terekstrak.strip()) > 50000:
                    st.markdown("""
                    <div class="alert-warning">
                        ⚠️ Teks terlalu panjang! Maksimal 50.000 karakter.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Loading sederhana tanpa progress bar rumit
                    with st.spinner("🤖 Sedang membuat ringkasan... Mohon tunggu."):
                        start_time = time.time()
                        
                        ringkasan = peringkas.ringkas_teks(teks_terekstrak, model_terpilih, panjang_ringkasan, bahasa, prompt_kustom)
                        
                        end_time = time.time()
                        waktu_proses = round(end_time - start_time, 2)
                        
                        if ringkasan:
                            st.markdown(f"""
                            <div class="summary-card">
                                <h4>📝 Ringkasan</h4>
                                <p>{ringkasan}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Statistik ringkasan
                            col_ring1, col_ring2, col_ring3 = st.columns(3)
                            with col_ring1:
                                st.metric("📊 Kata", hitung_kata(ringkasan))
                            with col_ring2:
                                rasio_kompresi = round((hitung_kata(ringkasan) / hitung_kata(teks_terekstrak)) * 100, 1)
                                st.metric("📉 Kompresi", f"{rasio_kompresi}%")
                            with col_ring3:
                                st.metric("⏱️ Waktu", f"{waktu_proses}s")
                            
                            # Tombol download
                            st.markdown('<div class="download-grid">', unsafe_allow_html=True)
                            col_down1, col_down2 = st.columns(2)
                            with col_down1:
                                st.download_button(
                                    label="💾 Download Ringkasan",
                                    data=ringkasan,
                                    file_name=f"ringkasan_{int(time.time())}.txt",
                                    mime="text/plain",
                                    use_container_width=True
                                )
                            
                            with col_down2:
                                # Format lengkap untuk download
                                format_lengkap = f"""RINGKASAN TEKS
{'='*50}

INFORMASI:
- Tanggal: {time.strftime('%d/%m/%Y %H:%M:%S')}
- Model: {model_terpilih}
- Panjang: {panjang_ringkasan}
- Bahasa: {bahasa}

RINGKASAN ({hitung_kata(ringkasan)} kata):
{ringkasan}

STATISTIK:
- Rasio Kompresi: {rasio_kompresi}%
- Waktu Proses: {waktu_proses} detik
"""
                                st.download_button(
                                    label="📄 Download Lengkap",
                                    data=format_lengkap,
                                    file_name=f"ringkasan_lengkap_{int(time.time())}.txt",
                                    mime="text/plain",
                                    use_container_width=True
                                )
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Rating sederhana
                            st.markdown("---")
                            st.markdown("**📊 Berikan penilaian:**")
                            rating = st.select_slider(
                                "Kualitas ringkasan:",
                                options=["Buruk", "Kurang", "Cukup", "Baik", "Sangat Baik"],
                                value="Baik"
                            )
                        
                        else:
                            st.markdown("""
                            <div class="alert-error">
                                ❌ Gagal membuat ringkasan. Silakan coba lagi atau pilih model yang berbeda.
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-info">
                <h4>👆 Silakan upload file atau tempel teks untuk memulai!</h4>
                <p><strong>🔥 Fitur Unggulan:</strong></p>
                <ul>
                    <li>✅ Ringkasan dalam Bahasa Indonesia</li>
                    <li>✅ Berbagai pilihan panjang ringkasan</li>
                    <li>✅ Template prompt khusus</li>
                    <li>✅ Statistik lengkap</li>
                    <li>✅ Download hasil ringkasan</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        © 2025 <strong>lucians</strong>. All rights reserved.<br>
        🕒 Last updated: {time.strftime('%d/%m/%Y %H:%M:%S WIB')}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()