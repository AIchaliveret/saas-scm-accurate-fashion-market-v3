import streamlit as st
import pandas as pd

st.set_page_config(page_title="SAAS SCM V4 - Fashion Garment", page_icon="🧵", layout="wide")

# FIXED - no multiline in caption
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/892/892458.png", width=60)
st.sidebar.title("SAAS.SCM.V3")
st.sidebar.caption("Prototype Fashion Garment Market Control - Autonomous + Accurate")
st.sidebar.info("WiFi: super-infrared.local 192.168.4.1 - 192.168.4.22 HP")

menu = st.sidebar.radio("Navigasi", [
    "Dashboard Accurate",
    "Master Bahan Baku",
    "FIFO LIFO Average",
    "Vendor Notes",
    "PO SQR BAPO Surat Jalan",
    "Keuangan Buku Besar Kwitansi Invoice",
    "Gudang C12 GC Kepala Gudang",
    "Transport GPS Live",
    "Ruang Teduh Loker Ruach Ha Kadosh",
    "Marketing Digital Links",
    "Director Statistik Demand Planner",
    "Market Tradisional Faktur Nota"
])

if menu == "Dashboard Accurate":
    st.title("SAAS.SCM.SYSTEM V4 - Prototype Fashion Garment Market Control V3.5")
    st.write("ERP Garment Autonomous + Accurate + Vendor Notes + GPS + Ruang Teduh - saingi Accurate")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Persediaan Yards", "12,450 Yd", "+320")
    c2.metric("Nilai FIFO", "Rp 186,750,000", "-2.1%")
    c3.metric("PO Pending", "8 PO", "BAPO Waiting GC")
    c4.metric("Sales Hari Ini", "47 Kodi", "+12%")
    st.bar_chart(pd.DataFrame({"size":[180,200,240,270,300,340],"kodi":[12,18,22,15,9,6]}), x="size", y="kodi")

elif menu == "Master Bahan Baku":
    st.header("Persediaan Bahan Baku Batik Keseluruhan")
    st.caption("Kain katun yards bal-balan + pewarna reactive + kimia naptol AS-G AS-BS AS-BO + nitrit air keras soda api soda abu emping kuweh lilin parafin siongkah")
    data = [
        ["Mori Primis 90cm 6kg/25 kodi","Kain","Yd",450,"PT Sinar Kainindo"],
        ["Reactive Blue 300gr/25L","Pewarna","L",25,"Kimia Makmur"],
        ["Reactive Pink 150gr","Pewarna","L",18,"Kimia Makmur"],
        ["Naptol AS-G 75-300gr","Kimia","Kg",32,"Kimia Makmur"],
        ["Naptol AS-BS","Kimia","Kg",18,"Kimia Makmur"],
        ["Naptol AS-BO","Kimia","Kg",15,"Kimia Makmur"],
        ["NaNO2 Nitrit 3kg","Aux","Kg",24,"Kimia Makmur"],
        ["HCl Air Keras 8L","Aux","L",40,"Kimia Makmur"],
        ["NaOH Soda Api 6L","Aux","L",36,"Kimia Makmur"],
        ["Garam 10kg","Aux","Kg",100,"UD Garam"],
        ["Soda Ash Na2CO3","Aux","Kg",60,"UD Kimia"],
        ["Lilin Parafin 60% + Micro 20% + Siongkah 15% + Beeswax 5%","Lilin","Kg",85,"UD Siongkah Jaya"],
    ]
    st.dataframe(pd.DataFrame(data, columns=["Nama Bahan","Kategori","Satuan","Stok","Vendor"]))

elif menu == "FIFO LIFO Average":
    st.header("Buku Besar + FIFO LIFO Average - Saingi Accurate")
    method = st.selectbox("Metode", ["FIFO","LIFO","Average Weighted"])
    tx = pd.DataFrame([
        ["2026-10-20","Masuk","Mori Primis","100 Yd","10,000","1,000,000"],
        ["2026-10-25","Masuk","Mori Primis","50 Yd","12,000","600,000"],
        ["2026-10-28","Keluar","Potong 200cm","120 Yd","-","-"],
    ], columns=["Tanggal","Jenis","Item","Qty","Harga/Yd","Total"])
    st.table(tx)
    if method=="FIFO":
        st.success("FIFO: Jual 120 Yd = 100 Yd @10k + 20 Yd @12k = Rp 1,240,000 | Sisa 30 Yd @12k = Rp 360,000")
    elif method=="LIFO":
        st.warning("LIFO: Jual 120 Yd = 50 Yd @12k + 70 Yd @10k = Rp 1,300,000 | Sisa 30 Yd @10k = Rp 300,000")
    else:
        st.info("Average: Avg = 10,666.7 | HPP = 1,280,000 | Sisa 320,000")

elif menu == "Vendor Notes":
    st.header("Vendor Notes - Lembar Halaman Untuk Vendor")
    st.write("Sudah disediakan lembar halaman untuk vendor agar memudahkan business utama mencatat dan merekam para vendor")
    vendors = [
        {"nama":"PT Sinar Kainindo","kat":"Kain Mori Primis","email":"sales@sinarkain.co.id","phone":"0812-1234-5678","saldo":12500000,"notes":"Langganan sejak 2019, kualitas Mori Primis 90cm 6kg/25kodi bagus, tempo 14 hari, pernah telat 2 hari Jan 2026."},
        {"nama":"Toko Kimia Makmur Pekalongan","kat":"Kimia Naptol Reactive","email":"kimia.makmur.pkl@gmail.com","phone":"0823-9876-5432","saldo":8750000,"notes":"Supplier AS-G AS-BS AS-BO, Nitrit, Fast Red B Blue B. Harga stabil."},
        {"nama":"UD Siongkah Jaya","kat":"Lilin Gondorukem","email":"siongkah.jaya@yahoo.com","phone":"0857-1111-2222","saldo":3200000,"notes":"Parafin 60% 52-56C Micro 20% Siongkah 15% Beeswax 5%."},
    ]
    for v in vendors:
        with st.expander(f"{v['nama']} - {v['kat']} - Hutang Rp {v['saldo']:,}"):
            st.write(f"Email: {v['email']} | Phone: {v['phone']}")
            st.text_area(f"Notes {v['nama']}", value=v['notes'], key=v['nama'])

elif menu == "PO SQR BAPO Surat Jalan":
    st.header("SQR + PO + BAPO + Surat Jalan + GC Kepala Gudang")
    st.write("PO-2026-001 Mori Primis 25 Kodi 200cm - 15,000,000 - Approved - GC Mr Soesendi Lim & Mister Aliang")
    st.write("Sopir: Ahmad Subarjo Grand Max 5-8 Bal 800kg, Rian Hidayat L300 10-15 Bal 1.5 Ton, M Faisal Truk Engkel 25-40 Bal 2.5-4 Ton, Dedi Kurniawan Fuso 80-120 Bal 7-12 Ton - Phone aktif di kwitansi")

elif menu == "Keuangan Buku Besar Kwitansi Invoice":
    st.header("Keuangan Lengkap - Buku Besar + Kwitansi Kas Manual + Invoice ESC/POS")
    j = pd.DataFrame([
        ["2026-10-28","Persediaan - Mori Primis","Debet","15,000,000",""],
        ["2026-10-28","Kas / Hutang Usaha","Kredit","","15,000,000"],
        ["2026-10-29","Kas","Debet","5,000,000","Pelunasan KWT-001"],
    ], columns=["Tanggal","Akun","D/K","Debet","Kredit"])
    st.dataframe(j)
    st.write("Kwitansi KWT-2026-001 PT Sinar Kainindo Rp 5,000,000 Kas Manual Lunas - Email ke sales@sinarkain.co.id")
    st.write("Invoice Tanah Abang INV-TA-2026-012 25 Kodi @200cm Rp 7,500,000 ESC/POS 58mm")

elif menu == "Gudang C12 GC Kepala Gudang":
    st.header("Gudang C12 - GC Kepala Gudang Approval")
    st.map(pd.DataFrame({"lat":[-6.2088],"lon":[106.8456]}))
    st.write("Rak A1 Mori Primis 45 Kodi QR-001, Rak A2 Reactive Blue 25 L, Ketel Uap 500L 2 Ruang 2.5 bar 90kg/jam 88%")

elif menu == "Transport GPS Live":
    st.header("Transportasi Terhubung GPS atau Google Maps")
    st.map(pd.DataFrame({"lat":[-6.2088,-6.21,-6.19],"lon":[106.8456,106.86,106.84]}))
    st.write("Ahmad Subarjo Grand Max On the way 12km ETA 25min - Rian Hidayat Delivered - M Faisal Return - Dedi Kurniawan To Pekalongan ITC")
    st.write("Turbine Francis Faraday epsilon=-dPhi/dt Generator 1000W x4")

elif menu == "Ruang Teduh Loker Ruach Ha Kadosh":
    st.header("Ruang Teduh Loker + Ruach Ha Kadosh - Spiritual Kelestarian Lingkungan Kerja Lebih Baik")
    st.write("Zero Blast Radius: CV parsing isolated sandbox docker rm -f verifiable - security PC817 5kVrms")
    st.write("Future of Work: Jadwal wawancara Playwright browser automation sandbox + calendar + GPS -6.2088,106.8456")
    st.write("Ruach Ha Kadosh: wellbeing AI max 60km dari rumah - Building in public Elohim is")
    st.link_button("Buka ruang-teduh-ai", "https://github.com/AIchaliveret/ruang-teduh-ai")

elif menu == "Marketing Digital Links":
    st.header("Laman Link URL Marketing Digital Instagram dan Media Sosial Lain")
    st.link_button("Instagram @cinhonest", "https://instagram.com/cinhonest")
    st.link_button("GitHub Repo V3", "https://github.com/AIchaliveret/saas_scm_fashion_market_v3")
    st.link_button("Facebook Even Garden", "https://facebook.com/even.garden.637384")

elif menu == "Director Statistik Demand Planner":
    st.header("Direktur Business Owner - Statistik Penjualan Menyeluruh")
    st.write("Penjualan Aktual vs Permintaan - Hukum Permintaan Berbanding Survey Market Control ala Syst Meta.AI")
    df_sales = pd.DataFrame({
        "Market":["Tanah Abang","ITC Pekalongan","IG Online","Shopee","TikTok","Grosir Solo/Jogja"],
        "Actual":[120,75,68,45,20,14],
        "Permintaan":[145,90,85,60,30,20]
    })
    st.bar_chart(df_sales, x="Market", y=["Actual","Permintaan"])
    st.success("AI.Meta Generate: Motif Parang Kusumo Blue Reactive naik 23% - stok AS-G critical - rekomendasi produksi 25 kodi 200cm")

elif menu == "Market Tradisional Faktur Nota":
    st.header("Market Tradisional - Faktur Nota Kwitansi Penjualan - Demand Planner Tradisi")
    st.write("Faktur penjualan / nota penjualan / kwitansi penjualan Tanah Abang ITC sebagai berita acara permintaan pelanggan - systematis tradisi perdagangan")
    df = pd.DataFrame([
        ["FK-TA-2026-101","2026-10-25","Tanah Abang","Parang Kusumo","Blue Reactive","200","25","300,000","7,500,000","Toko Sari Jaya","0812-9999-0001","Lunas"],
        ["NT-ITC-2026-045","2026-10-26","ITC Pekalongan","Mega Mendung","Pink","200","18","320,000","5,760,000","Grosir Solo","0823-8888-0002","Belum Lunas"],
        ["KWT-PS-2026-012","2026-10-27","Grosir Solo/Jogja","Kawung","Coklat AS-BS","240","12","350,000","4,200,000","Buyer Amerika Afrika","0857-7777-0003","Lunas"],
    ], columns=["No Faktur","Tanggal","Pasar","Model","Warna","Ukuran","Kodi","Harga/Kodi","Total","Buyer","Phone","Status"])
    st.dataframe(df)

st.divider()
st.caption("SAAS.SCM.SYSTEM V3.5 - Vultr Agent Rush - Zero Blast Radius sandbox-code + browser Playwright + verifiable + security PC817 5kVrms + Future of Work SDM Recruitment Ruang Teduh + Ruach Ha Kadosh | Team 7 Aku Bald Lead Mr Soesendi Lim Mister Aliang | License SUPER SECURE SYST v3.0 | Even Garden x Cerebral Valley x Vultr | meta.aichaliveret | super-infrared.local")
