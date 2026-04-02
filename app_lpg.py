import streamlit as st
import os
from datetime import date

# --- 1. KONFIGURASI ---
st.set_page_config(page_title="LPG NPSO Primkopal", page_icon="🔥")

# --- 2. FUNGSI DATABASE ---
FILE_STOK = "data_stok.txt"

def simpan_data(s12, s5):
    with open(FILE_STOK, "w") as f:
        f.write(f"{s12},{s5}")

def baca_data():
    if os.path.exists(FILE_STOK):
        with open(FILE_STOK, "r") as f:
            try:
                d = f.read().split(",")
                return int(d[0]), int(d[1])
            except: return 20, 20
    return 20, 20

st12, st5 = baca_data()

# --- 3. STYLE (MENGHILANGKAN KOTAK PUTIH) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?q=80&w=1920");
        background-size: cover;
    }
    [data-testid="stMetricValue"] { color: #FF4B4B !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. ISI WEB ---
st.title("📦 Layanan LPG NPSO Primkopal")
st.subheader("Lanal Cilacap")

t1, t2 = st.tabs(["🛒 Pesan LPG", "⚙️ Admin"])

with t1:
    col1, col2 = st.columns(2)
    col1.metric("Bright Gas 12 Kg", f"{st12} Tabung")
    col2.metric("Bright Gas 5.5 Kg", f"{st5} Tabung")

    st.write("---")
    nama = st.text_input("Nama Pangkalan")
    
    hari_ini = date.today()
    akhir_thn = date(hari_ini.year, 12, 31)
    tgl = st.date_input("Tanggal Penerimaan", value=hari_ini, min_value=hari_ini, max_value=akhir_thn)
    
    jn = st.selectbox("Pilih Jenis", ["Bright Gas 12kg", "Bright Gas 5.5kg"])
    jml = st.number_input("Jumlah (Tabung)", min_value=1, step=1)

    if st.button("Proses Pesanan Sekarang"):
        if not nama:
            st.error("Isi Nama Pangkalan!")
        else:
            ok = False
            if "12kg" in jn and st12 >= jml:
                simpan_data(st12 - jml, st5)
                ok = True
            elif "5.5kg" in jn and st5 >= jml:
                simpan_data(st12, st5 - jml)
                ok = True
            else:
                st.error("Stok Habis!")

            if ok:
                st.success(f"Pesanan terekam untuk {tgl.strftime('%d-%m-%Y')}!")
                # FORMAT LINK WA YANG LEBIH AMAN (MENGHINDARI TEKS MENTAH)
                wa_no = "6285876146502"
                txt = f"Halo Admin Primkopal, saya *{nama}* pesan *{jn}* sebanyak *{jml}* tabung. Kirim tgl: {tgl.strftime('%d-%m-%Y')}"
                link = f"https://wa.me/{wa_no}?text={txt.replace(' ', '%20')}"
                
                # TOMBOL VERSI BERSIH
                st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;font-size:20px;">📲 KIRIM KE WHATSAPP</div></a>', unsafe_allow_html=True)
                st.balloons()

with t2:
    pw = st.text_input("Password", type="password")
    if pw == "lanal123":
        n12 = st.number_input("Stok 12kg", value=st12)
        n5 = st.number_input("Stok 5.5kg", value=st5)
        if st.button("Update"):
            simpan_data(n12, n5)
            st.success("Berhasil!")
            st.rerun()
