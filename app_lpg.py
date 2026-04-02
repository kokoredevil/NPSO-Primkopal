import streamlit as st
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LPG NPSO Primkopal Lanal", page_icon="🔥", layout="centered")

# --- 2. DATABASE STOK (FILE TEKS) ---
FILE_STOK = "data_stok.txt"

def simpan_data(stok12, stok5):
    with open(FILE_STOK, "w") as f:
        f.write(f"{stok12},{stok5}")

def baca_data():
    if os.path.exists(FILE_STOK):
        with open(FILE_STOK, "r") as f:
            try:
                data = f.read().split(",")
                return int(data[0]), int(data[1])
            except:
                return 20, 20
    return 20, 20  # Stok default jika file baru dibuat

stok_12kg_skrg, stok_5kg_skrg = baca_data()

# --- 3. TAMPILAN VISUAL (CSS & BACKGROUND) ---
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    .main-box {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    h1, h2, h3 {
        color: #1E3A8A !important;
    }
    .stMetric {
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 4. ISI WEBSITE ---
st.title("📦 Layanan LPG NPSO Primkopal")
st.subheader("Lanal Cilacap - Fast Response & Reliable")
st.write("---")

tab1, tab2 = st.tabs(["🛒 Pesan LPG (Pelanggan)", "⚙️ Update Stok (Admin)"])

# --- TAB PEMBELI ---
with tab1:
    st.info("💡 Pilih jenis tabung dan isi data untuk memesan via WhatsApp.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("LPG 12kg (NPSO)", f"{stok_12kg_skrg} Tabung")
    with col2:
        st.metric("Bright Gas 5.5kg", f"{stok_5kg_skrg} Tabung")

    st.write("### 📝 Formulir Pemesanan")
    with st.container():
        nama = st.text_input("Nama Lengkap")
        alamat = st.text_area("Alamat Lengkap Pengiriman")
        jenis = st.selectbox("Pilih Jenis Tabung", ["LPG 12kg", "Bright Gas 5.5kg"])
        jumlah = st.number_input("Jumlah Pesanan (Tabung)", min_value=1, step=1)

        # Konfigurasi WhatsApp (GANTI NOMOR DISINI)
        nomor_wa = "628123456789" 
        pesan_wa = f"Halo Admin Primkopal, saya *{nama}* ingin memesan *{jenis}* sebanyak *{jumlah}* tabung.\n\nAlamat Kirim: *{alamat}*."
        link_wa = f"https://wa.me/{nomor_wa}?text={pesan_wa.replace(' ', '%20').replace('\\n', '%0A')}"

        if st.button("Proses Pesanan Sekarang"):
            if not nama or not alamat:
                st.error("⚠️ Mohon lengkapi Nama dan Alamat!")
            else:
                # Validasi Stok
                pesanan_valid = False
                if jenis == "LPG 12kg" and stok_12kg_skrg >= jumlah:
                    simpan_data(stok_12kg_skrg - jumlah, stok_5kg_skrg)
                    pesanan_valid = True
                elif jenis == "Bright Gas 5.5kg" and stok_5kg_skrg >= jumlah:
                    simpan_data(stok_12kg_skrg, stok_5kg_skrg - jumlah)
                    pesanan_valid = True
                else:
                    st.error(f"❌ Stok {jenis} tidak mencukupi!")

                if pesanan_valid:
                    st.success("✅ Stok berhasil dipesan! Klik tombol di bawah untuk kirim detail ke WhatsApp Admin.")
                    st.balloons()
                    
                    # TOMBOL WHATSAPP SAKTI (HTML)
                    st.markdown(f"""
                        <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                            <div style="
                                background-color: #25D366;
                                color: white;
                                padding: 18px;
                                text-align: center;
                                border-radius: 12px;
                                font-weight: bold;
                                font-size: 20px;
                                margin-top: 15px;
                                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                            ">
                                📲 KLIK DI SINI: KIRIM KE WHATSAPP
                            </div>
                        </a>
                    """, unsafe_allow_html=True)

# --- TAB ADMIN ---
with tab2:
    st.write("### 🔒 Panel Kendali Stok")
    pwd = st.text_input("Password Admin", type="password")
    
    if pwd == "lanal123":
        st.success("Akses Diterima.")
        new_12 = st.number_input("Update Stok Fisik 12kg", value=stok_12kg_skrg)
        new_5 = st.number_input("Update Stok Fisik 5.5kg", value=stok_5kg_skrg)
        
        if st.button("Simpan Perubahan Stok"):
            simpan_data(new_12, new_5)
            st.success("Data stok berhasil diperbarui!")
            st.rerun()
    elif pwd:
        st.error("Password salah!")
