import streamlit as st
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="LPG NPSO Primkopal Lanal", page_icon="🔥")

# --- DATABASE SEDERHANA (File Teks) ---
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
                return 10, 5
    return 10, 5  # Stok awal jika file belum ada

# Ambil data stok terbaru
stok_12kg_skrg, stok_5kg_skrg = baca_data()

# --- TAMPILAN UTAMA ---
st.title(" ✨Layanan Order LPG NPSO Primkopal")
st.subheader("Bright Gas 5,5 Kg & Bright Gas 12 Kg  ")
st.write("---")

# --- MENU TAB ---
tab1, tab2 = st.tabs(["🛒 Order LPG (Pembeli)", "⚙️ Update Stok (Admin)"])

# --- HALAMAN PEMBELI ---
with tab1:
    st.info("Silakan cek stok ketersediaan di bawah ini.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("LPG 12kg (NPSO)", f"{stok_12kg_skrg} Tabung")
    with col2:
        st.metric("Bright Gas 5.5kg", f"{stok_5kg_skrg} Tabung")

    st.write("### Formulir Pemesanan")
    nama = st.text_input("Nama Pangkalan")
    alamat = st.text_area("Alamat Pengiriman")
    jenis = st.selectbox("Pilih Jenis LPG", ["LPG 12kg", "Bright Gas 5.5kg"])
    jumlah = st.number_input("Jumlah Tabung", min_value=1, step=1)

    # Konfigurasi WhatsApp
    nomor_wa = "6285876146502" # <--- GANTI DENGAN NOMOR WA KAMU
    pesan_wa = f"Halo Admin Primkopal, saya *{nama}* mau order *{jenis}* sebanyak *{jumlah}* tabung. Kirim ke alamat: *{alamat}*."
    link_wa = f"https://wa.me/{nomor_wa}?text={pesan_wa.replace(' ', '%20')}"

    if st.button("Pesan Sekarang via WhatsApp"):
        if not nama or not alamat:
            st.error("⚠️ Mohon isi Nama dan Alamat pengiriman!")
        else:
            # Logika Cek Stok & Kurangi Otomatis
            if jenis == "LPG 12kg":
                if stok_12kg_skrg >= jumlah:
                    stok_baru = stok_12kg_skrg - jumlah
                    simpan_data(stok_baru, stok_5kg_skrg)
                    st.success(f"Berhasil! Pesanan {jumlah} tabung 12kg diproses.")
                    st.markdown(f'**[KLIK DI SINI UNTUK KIRIM PESAN KE WHATSAPP]({link_wa})**')
                    st.balloons()
                else:
                    st.error("Maaf, stok LPG 12kg tidak mencukupi.")
            
            elif jenis == "Bright Gas 5.5kg":
                if stok_5kg_skrg >= jumlah:
                    stok_baru = stok_5kg_skrg - jumlah
                    simpan_data(stok_12kg_skrg, stok_baru)
                    st.success(f"Berhasil! Pesanan {jumlah} tabung 5.5kg diproses.")
                    st.markdown(f'**[KLIK DI SINI UNTUK KIRIM PESAN KE WHATSAPP]({link_wa})**')
                    st.balloons()
                else:
                    st.error("Maaf, stok Bright Gas 5.5kg tidak mencukupi.")

# --- HALAMAN ADMIN ---
with tab2:
    st.write("### Panel Update Stok Gudang")
    pwd = st.text_input("Masukkan Password Admin", type="password")
    
    if pwd == "lanal123": # <--- GANTI PASSWORD SESUKAMU
        st.write("Input jumlah stok fisik yang ada di gudang saat ini:")
        up_12 = st.number_input("Stok 12kg Baru", value=stok_12kg_skrg)
        up_5 = st.number_input("Stok 5.5kg Baru", value=stok_5kg_skrg)
        
        if st.button("Simpan & Perbarui Web"):
            simpan_data(up_12, up_5)
            st.success("Data stok di website berhasil diperbarui!")
            st.rerun()
    elif pwd:
        st.warning("Password salah!")
