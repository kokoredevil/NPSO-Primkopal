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
    return 20, 20

stok_12kg_skrg, stok_5kg_skrg = baca_data()

# --- 3. TAMPILAN VISUAL ---
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    .stTabs, .stMetric, .stMarkdown, .stTextInput, .stNumberInput, .stSelectbox, .stTextArea {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 4. ISI WEBSITE ---
st.title("📦 Layanan LPG NPSO Primkopal")
st.subheader("Lanal Cilacap")
st.write("---")

tab1, tab2 = st.tabs(["🛒 Pesan LPG", "⚙️ Update Stok (Admin)"])

# --- TAB PEMBELI ---
with tab1:
    st.info("💡 Pilih jenis tabung dan isi data untuk memesan.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("LPG 12kg (NPSO)", f"{stok_12kg_skrg} Tabung")
    with col2:
        st.metric("Bright Gas 5.5kg", f"{stok_5kg_skrg} Tabung")

    st.write("### 📝 Formulir Pemesanan")
    nama = st.text_input("Nama Lengkap")
    alamat = st.text_area("Alamat Lengkap Pengiriman")
    jenis = st.selectbox("Pilih Jenis Tabung", ["LPG 12kg", "Bright Gas 5.5kg"])
    jumlah = st.number_input("Jumlah Pesanan (Tabung)", min_value=1, step=1)

    # Konfigurasi WhatsApp (GANTI NOMOR DISINI)
    nomor_wa = "628123456789" 
    pesan_wa = f"Halo Admin Primkopal, saya *{nama}* ingin memesan *{jenis}* sebanyak *{jumlah}* tabung. Alamat Kirim: *{alamat}*."
    link_wa = f"https://wa.me/{nomor_wa}?text={pesan_wa.replace(' ', '%20')}"

    if st.button("Proses Pesanan Sekarang"):
        if not nama or not alamat:
            st.error("⚠️ Mohon lengkapi Nama dan Alamat!")
        else:
            valid = False
            if jenis == "LPG 12kg" and stok_12kg_skrg >= jumlah:
                simpan_data(stok_12kg_skrg - jumlah, stok_5kg_skrg)
                valid = True
            elif jenis == "Bright Gas 5.5kg" and stok_5kg_skrg >= jumlah:
                simpan_data(stok_12kg_skrg, stok_5kg_skrg - jumlah)
                valid = True
            else:
                st.error("❌ Stok tidak mencukupi!")

            if valid:
                st.success("✅ Stok berhasil dipesan! Klik tombol hijau di bawah.")
                # TOMBOL WHATSAPP TANPA TEKS MENTAH
                tombol_html = f'''
                    <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                        <div style="
                            background-color: #25D366;
                            color: white;
                            padding: 15px;
                            text-align: center;
                            border-radius: 10px;
                            font-weight: bold;
                            font-size: 20px;
                            margin-top: 10px;
                        ">
                            📲 KIRIM KE WHATSAPP
                        </div>
                    </a>
                '''
                st.markdown(tombol_html, unsafe_allow_html=True)
                st.balloons()

# --- TAB ADMIN ---
with tab2:
    st.write("### 🔒 Panel Admin")
    pwd = st.text_input("Password", type="password")
    if pwd == "lanal123":
        new_12 = st.number_input("Stok 12kg", value=stok_12kg_skrg)
        new_5 = st.number_input("Stok 5.5kg", value=stok_5kg_skrg)
        if st.button("Update Stok"):
            simpan_data(new_12, new_5)
            st.success("Stok diperbarui!")
            st.rerun()
