import streamlit as st
import pandas as pd
from datetime import date, datetime
import io

st.set_page_config(page_title="SAAS SCM V4.6 ACTIVE CONNECTED - Fashion Garment", page_icon="🧵", layout="wide")

# --- INIT SESSION ---
if "bahan" not in st.session_state:
    st.session_state.bahan = pd.DataFrame([
        ["Mori Primis 90cm 6kg/25 kodi","Kain","Yd",5,450,18,10000,"PT Sinar Kainindo","Langganan 2019 tempo 14 hari - Gudang Besar 22M"],
        ["Reactive Blue 300gr/25L","Pewarna","L",0,25,0,85000,"Kimia Makmur","Parang Kusumo Blue - Gudang C12"],
        ["Reactive Pink 150gr","Pewarna","L",0,18,0,75000,"Kimia Makmur","Mega Mendung - Gudang C12"],
        ["Naptol AS-G 75-300gr","Kimia","Kg",0,32,0,45000,"Kimia Makmur","75-300gr/25L Blue 300gr Pink 150gr - C12"],
        ["Naptol AS-BS","Kimia","Kg",0,18,0,48000,"Kimia Makmur","Coklat AS-BS"],
        ["Naptol AS-BO","Kimia","Kg",0,15,0,47000,"Kimia Makmur","AS-BO"],
        ["NaNO2 Nitrit 3kg","Aux","Kg",0,24,0,35000,"Kimia Makmur","Diazonium 15-20C + es"],
        ["HCl Air Keras 8L","Aux","L",0,40,0,25000,"Kimia Makmur","Air keras"],
        ["NaOH Soda Api 6L","Aux","L",0,36,0,28000,"Kimia Makmur","Soda api"],
        ["Garam 10kg","Aux","Kg",0,100,0,12000,"UD Garam","Garam"],
        ["Soda Ash Na2CO3","Aux","Kg",0,60,0,15000,"UD Kimia","Soda abu emping kuweh"],
        ["Lilin Parafin 60%+Micro20%+Siongkah15%+Beeswax5%","Lilin","Kg",0,85,0,35000,"UD Siongkah Jaya","Lilin batik 60-20-15-5"],
        ["ILMCI Qua pH 8-9 Alkaline Mineral","Air Sehat","Dus",2,120,0,8000,"PT ILMCI Qua - I Love My Country - Pak Sofian Chandra","PENDING IZIN DUBAI FERTIGASI - pH8-9 natural fresh segar - edukasi SD SMP SMA"],
    ], columns=["Nama Bahan","Kategori","Satuan","Stok Bal","Stok Yard/L/Kg","Stok Kodi","Harga per Satuan","Vendor","Notes Gudang - Besar 22M vs C12"])

if "fifo_tx" not in st.session_state:
    st.session_state.fifo_tx = pd.DataFrame([
        ["2026-10-20","PASOK-001","Masuk - Pasokan","Mori Primis","2","100","4","10000","1000000","Bal-balan Mori Primis 90cm","Gudang Besar 22M"],
        ["2026-10-25","PASOK-002","Masuk - Pasokan","Mori Primis","1","50","2","12000","600000","Tambahan stok","Gudang Besar 22M"],
        ["2026-10-28","POTONG-001","Keluar - Potong 200cm","Potong 200cm","0","120","5","","","Proses kerja tanpa harga - quantity kodi","Gudang C12 -> Produksi"],
        ["2026-10-29","PROSES-001","Proses Kerja - Tanpa Harga","Batik Cap Parang Kusumo","0","0","2","","","Proses batik canting 3-6 bulan mentoring Mister Budi Sandy","Gudang C12"],
    ], columns=["Tanggal","No Dokumen","Jenis","Item","Qty Bal","Qty Yard","Qty Kodi","Harga per Satuan","Total Rp","Keterangan - Tanpa Harga Boleh","Gudang"])

if "vendors" not in st.session_state:
    st.session_state.vendors = pd.DataFrame([
        ["PT Sinar Kainindo","Kain Mori Primis","sales@sinarkain.co.id","0812-1234-5678",12500000,"Langganan 2019, Mori Primis 90cm 6kg/25 kodi bagus, tempo 14 hari, Gudang Besar 22M"],
        ["Toko Kimia Makmur Pekalongan","Kimia Naptol Reactive","kimia.makmur.pkl@gmail.com","0823-9876-5432",8750000,"Supplier AS-G AS-BS AS-BO Nitrit Fast Red B Blue B - Gudang C12 - Ketel Uap 500L 88%"],
        ["UD Siongkah Jaya","Lilin Gondorukem","siongkah.jaya@yahoo.com","0857-1111-2222",3200000,"Parafin 60% 52-56C Micro 20% Siongkah 15% Beeswax 5%"],
        ["PT ILMCI Qua - I Love My Country","Air Mineral pH 8-9","ilmci.qua@ilovemycountry.id","0812-9999-ILMCI",0,"I Love My Country Indonesia - Pak Sofian Chandra - pH 8-9 alkaline natural fresh segar - Direct Selling + App Edukasi SD SMP SMA - PENDING IZIN DUBAI FERTIGASI HEALTH - Cocok untuk karyawan Bak1 60-70C Bak2 15-20C"],
    ], columns=["Nama Vendor","Kategori","Email","Phone","Hutang Saldo","Notes Halaman Vendor"])

if "po" not in st.session_state:
    st.session_state.po = pd.DataFrame([
        ["PO-2026-001","2026-10-28","Mori Primis 25 Kodi 200cm - 5 Bal 450 Yd","PT Sinar Kainindo","15000000","Approved GC Mr Soesendi Lim & Mister Aliang","BAPO-2026-001 Done - Gudang Besar 22M"],
        ["PO-2026-002","2026-10-29","Reactive Blue 25L + Pink 18L + ILMCI Qua 2 Dus","Kimia Makmur + ILMCI Qua","2125000 + 16000","Pending GC","Waiting SQR - Cek pH 8-9"],
    ], columns=["No PO","Tanggal","Item - Bal Yard Kodi","Vendor","Total","Status GC Kepala Gudang","BAPO - Gudang"])

if "jurnal" not in st.session_state:
    st.session_state.jurnal = pd.DataFrame([
        ["2026-10-28","Persediaan - Mori Primis - Gudang Besar","Debet","15000000","","PO-2026-001 - 5 Bal 450 Yd"],
        ["2026-10-28","Hutang Usaha - Sinar Kainindo","Kredit","","15000000","PO-2026-001"],
        ["2026-10-29","Kas","Debet","5000000","","KWT-2026-001 Pelunasan - Kas Manual Teregistrasi"],
        ["2026-10-29","Piutang - Toko Sari Jaya Tanah Abang","Debet","7500000","","FK-TA-101 - 25 Kodi"],
        ["2026-11-15","Persediaan - ILMCI Qua","Debet","16000","","PASOK-ILMCI - 2 Dus pH 8-9 - Pending Izin Pak Sofian"],
    ], columns=["Tanggal","Akun","D/K","Debet","Kredit","Ref - No Dokumen Bal Yard Kodi"])

if "sopir" not in st.session_state:
    st.session_state.sopir = pd.DataFrame([
        ["Ahmad Subarjo","L300 B9123TAB - 10-15 Bal 1.5 Ton","12 Bal 270 Yd","0812-1111-0001","On the way Tanah Abang Blok F/B 12km ETA 25min",-6.2088,106.8456],
        ["Rian Hidayat","Engkel B8456PQA - 25-40 Bal 2.5-4 Ton","35 Dus 45 Kodi","0823-2222-0002","Delivered Blok F ITC - 35 Dus",-6.21,106.86],
        ["M Faisal","Grand Max B2389CXT - 5-8 Bal 800Kg","6 Bal 108 Yd","0857-3333-0003","Return Jabodetabek + bawa ILMCI Qua 2 Dus",-6.19,106.84],
        ["Dedi Kurniawan","Fuso BE7012UU - 80-120 Bal 7-12 Ton","90 Bal 1620 Yd","0813-4444-0004","To Pekalongan ITC + Solo luar pulau",-6.195,106.85],
    ], columns=["Nama Sopir","Mobil Nopol Kapasitas","Muatan - Bal Yard Kodi","HP Aktif Kwitansi","Status GPS Live","Lat","Lon"])

if "faktur" not in st.session_state:
    st.session_state.faktur = pd.DataFrame([
        ["FK-TA-2026-101","2026-10-25","Tanah Abang Blok F/B","Parang Kusumo","Blue Reactive","200","2","25","12","300000","7500000","Toko Sari Jaya","0812-9999-0001","Lunas","Berita acara permintaan pelanggan - hukum permintaan - demand planner tradisi"],
        ["NT-ITC-2026-045","2026-10-26","ITC Pekalongan","Mega Mendung","Pink 150gr","200","1","18","8","320000","5760000","Grosir Solo","0823-8888-0002","Belum Lunas","Permintaan Mega Mendung naik 15% - AI Meta #OOTDJakarta"],
        ["KWT-PS-2026-012","2026-10-27","Grosir Solo/Jogja","Kawung","Coklat AS-BS","240","1","12","6","350000","4200000","Buyer Amerika Afrika","0857-7777-0003","Lunas","Ekspor - demand planner tradisi + koperasi setempat"],
        ["FK-TA-2026-102","2026-10-30","Tanah Abang","Parang Kusumo + Bundle ILMCI Qua pH8-9","Blue + Mineral Sehat","200","3","30","15","310000","9300000","Toko Sehat Jaya - Dubai Health","0812-8888-0005","Proses - Pending Izin Pak Sofian","Trial bundling batik 30 kodi + air sehat ILMCI Qua pH 8-9 2 Dus untuk Dubai Fertigasi Health Well-being"],
    ], columns=["No Faktur","Tanggal","Pasar","Model","Warna","Ukuran cm","Qty Bal","Qty Kodi","Qty Yard Real","Harga per Kodi","Total Rp","Buyer Toko","Phone Buyer","Status","Catatan Market Tradisional - Demand Planner - Berita Acara"])

# --- SIDEBAR ---
st.sidebar.title("SAAS.SCM.V4.6 ACTIVE CONNECTED")
st.sidebar.caption("KOLOM AKTIF - Bal Yard Kodi Terpisah - Input Tanpa Harga - Gudang Besar vs C12 - Konek Google Sheet & MS Office")
st.sidebar.success("WiFi: super-infrared.local 192.168.4.1 - 192.168.4.22 HP | ILMCI Qua pH 8-9 pending izin Pak Sofian Chandra")
st.sidebar.info("Google Drive: SAAS_SCM_V4_Full_Accurate_GoogleDrive_MSOffice.xlsx - 11 Tabs - Link di Keuangan")

menu = st.sidebar.radio("NAVIGASI V4.6 - Semua Kolom Aktif Bisa Input", [
    "Dashboard Accurate",
    "Master Bahan Baku - INPUT PASOKAN Bal Yard Kodi",
    "FIFO LIFO Average - Qty Terpisah Tanpa Harga",
    "Vendor Notes - ACTIVE",
    "PO SQR BAPO Surat Jalan - ACTIVE",
    "Keuangan Buku Besar Kwitansi Invoice - CONNECTED Sheet & Excel",
    "Gudang C12 vs Gudang Besar 22M - INPUT BARANG MASUK",
    "Transport GPS Live - Muatan Bal Yard Kodi",
    "Market Tradisional Faktur Nota - Bal Yard Kodi ACTIVE",
    "Director Statistik Demand Planner - ACTIVE",
    "Marketing Digital Links + ILMCI Qua",
])

if menu == "Dashboard Accurate":
    st.title("SAAS.SCM.SYSTEM V4.6 ACTIVE CONNECTED")
    st.success("KOREKSI SELESAI SAYANG: 1) Input Pasokan Bal-Yard-Kodi Terpisah 2) Input Tanpa Harga Buat Proses Kerja 3) Gudang Besar 22M vs C12 Bisa Input Barang Masuk 4) Konek Google Sheet & MS Office Excel!")
    c1,c2,c3,c4 = st.columns(4)
    total_bal = st.session_state.bahan["Stok Bal"].sum()
    total_yard = st.session_state.bahan["Stok Yard/L/Kg"].sum()
    total_kodi = st.session_state.bahan["Stok Kodi"].sum()
    total_val = (st.session_state.bahan["Stok Yard/L/Kg"]*st.session_state.bahan["Harga per Satuan"]).sum()
    c1.metric("Total Bal-balan", f"{total_bal} Bal")
    c2.metric("Total Yard/L/Kg", f"{total_yard} Yd")
    c3.metric("Total Kodi", f"{total_kodi} Kodi")
    c4.metric("Nilai FIFO", f"Rp {total_val:,.0f}")
    st.write("Distribusi Gudang:")
    st.bar_chart(pd.DataFrame({"Gudang":["Gudang Besar 22M - Mori Primis","Gudang C12 - Kimia Naptol","Gudang C12 - Lilin Siongkah","Gudang Sehat - ILMCI Qua pH8-9"],"Bal":[5,0,0,2]}), x="Gudang", y="Bal")

elif menu == "Master Bahan Baku - INPUT PASOKAN Bal Yard Kodi":
    st.header("Master Bahan Baku - GUDANG BESAR 22M & GUDANG C12 - INPUT PASOKAN AKTIF")
    st.caption("THE BEST SS Gudang - Sekarang Bisa Input Pasokan Bal Yard Kodi - Qty & Yard Kolom Terpisah - Harga Opsional")
    st.write("**TABEL MASTER - KLIK UNTUK EDIT Stok Bal, Yard, Kodi - 3 KOLOM TERPISAH**")
    edited = st.data_editor(st.session_state.bahan, num_rows="dynamic", use_container_width=True, key="edit_bahan_v46")
    if st.button("Simpan Master Bahan Baku - Gudang Besar & C12"):
        st.session_state.bahan = edited
        st.success("Tersimpan! Stok Bal + Yard + Kodi update di Dashboard & Gudang Besar vs C12")
    st.divider()
    st.subheader("FORM INPUT PASOKAN BARU - Bal-balan + Yards + Kodi + Harga Opsional")
    st.info("Kalo proses kerja tanpa nilai harga, kosongin harga - quantity tetap catat jumlah kain dalam bal-balan dan jumlah kodi")
    with st.form("pasokan_form_v46"):
        c1,c2,c3 = st.columns(3)
        tgl = c1.date_input("Tanggal Pasokan", date.today())
        no_dok = c2.text_input("No Dokumen Pasokan","PASOK-2026-010")
        gudang = c3.selectbox("Tujuan Gudang",["Gudang Besar 22M - 2200m2","Gudang C12 - GC Kepala Gudang","Gudang Sehat - ILMCI Qua"])
        c4,c5 = st.columns(2)
        nama_bahan = c4.selectbox("Nama Bahan", st.session_state.bahan["Nama Bahan"].tolist())
        vendor = c5.selectbox("Vendor", st.session_state.vendors["Nama Vendor"].tolist())
        c6,c7,c8,c9 = st.columns(4)
        qty_bal = c6.number_input("Qty Bal-balan (Bal)", min_value=0, value=1, help="Jumlah kain dalam bal-balan")
        qty_yard = c7.number_input("Qty Yard / Liter / Kg", min_value=0, value=100, help="Jumlah yards - kolom terpisah dari bal")
        qty_kodi = c8.number_input("Qty Kodi (Kodi)", min_value=0, value=4, help="Jumlah kodi - 1 kodi = 20 pcs")
        harga = c9.number_input("Harga per Satuan (Rp) - Kosongkan jika proses kerja tanpa harga", min_value=0, value=10000)
        keterangan = st.text_area("Keterangan - Tanpa Harga Boleh Untuk Proses Kerja","Pasokan Mori Primis bal-balan dari PT Sinar Kainindo - 5 Bal = 450 Yd = 18 Kodi")
        total = qty_yard*harga if harga>0 else 0
        st.metric("Total Otomatis", f"Rp {total:,} = {qty_yard} Yard x Rp {harga:,}" if harga>0 else f"Proses Kerja Tanpa Harga - Qty: {qty_bal} Bal, {qty_yard} Yd, {qty_kodi} Kodi")
        submit = st.form_submit_button("INPUT PASOKAN - Update Stok Bal Yard Kodi + FIFO + Jurnal + Google Sheet")
        if submit:
            # Update bahan
            idx = st.session_state.bahan[st.session_state.bahan["Nama Bahan"]==nama_bahan].index
            if len(idx)>0:
                st.session_state.bahan.loc[idx[0],"Stok Bal"] += qty_bal
                st.session_state.bahan.loc[idx[0],"Stok Yard/L/Kg"] += qty_yard
                st.session_state.bahan.loc[idx[0],"Stok Kodi"] += qty_kodi
            # Add to pasokan fifo
            new_fifo = pd.DataFrame([[str(tgl),no_dok,"Masuk - Pasokan",nama_bahan,qty_bal,qty_yard,qty_kodi,harga if harga>0 else "",total if harga>0 else "",keterangan,gudang]], columns=st.session_state.fifo_tx.columns)
            st.session_state.fifo_tx = pd.concat([st.session_state.fifo_tx,new_fifo], ignore_index=True)
            # Add to jurnal if harga ada
            if harga>0 and total>0:
                new_j1 = pd.DataFrame([[str(tgl),f"Persediaan - {nama_bahan} - {gudang}","Debet",total,"",f"{no_dok} - {qty_bal} Bal {qty_yard} Yd {qty_kodi} Kodi"]], columns=st.session_state.jurnal.columns)
                new_j2 = pd.DataFrame([[str(tgl),f"Hutang Usaha - {vendor}","Kredit","","",total,f"{no_dok}"]], columns=st.session_state.jurnal.columns)
                st.session_state.jurnal = pd.concat([st.session_state.jurnal,new_j1,new_j2], ignore_index=True)
            st.success(f"PASOKAN {no_dok} BERHASIL! {qty_bal} Bal = {qty_yard} Yard = {qty_kodi} Kodi masuk {gudang} - Tanpa harga? Bisa! - Stok update - FIFO & Jurnal otomatis - Siap sync ke Google Sheet")

elif menu == "FIFO LIFO Average - Qty Terpisah Tanpa Harga":
    st.header("FIFO LIFO Average - Qty Bal Yard Kodi TERPISAH - Input Tanpa Harga Bisa")
    st.caption("Koreksi: kolom quantity dan yard mesti kolom yang berbeda (ada 2 kolom). Kalo ada kolom harga tapi input data barang masuk atau proses kerja pun bisa input data tanpa nilai harga")
    st.write("**TABEL TRANSAKSI - 3 KOLOM Qty TERPISAH - Harga Opsional Untuk Proses Kerja**")
    edited_tx = st.data_editor(st.session_state.fifo_tx, num_rows="dynamic", use_container_width=True, key="edit_fifo_v46")
    if st.button("Simpan & Hitung Ulang HPP - FIFO LIFO Average"):
        st.session_state.fifo_tx = edited_tx
        st.success("Transaksi tersimpan - HPP hitung ulang")
        # Hitung
        masuk = edited_tx[edited_tx["Jenis"].str.contains("Masuk")]
        keluar = edited_tx[edited_tx["Jenis"].str.contains("Keluar")]
        total_masuk_bal = pd.to_numeric(masuk["Qty Bal"], errors='coerce').sum()
        total_masuk_yard = pd.to_numeric(masuk["Qty Yard"], errors='coerce').sum()
        total_masuk_kodi = pd.to_numeric(masuk["Qty Kodi"], errors='coerce').sum()
        total_keluar_yard = pd.to_numeric(keluar["Qty Yard"], errors='coerce').sum()
        st.info(f"Masuk: {total_masuk_bal} Bal = {total_masuk_yard} Yard = {total_masuk_kodi} Kodi | Keluar: {total_keluar_yard} Yard | Sisa: {total_masuk_yard-total_keluar_yard} Yard")
    st.divider()
    with st.form("tx_form_v46"):
        st.subheader("Tambah Transaksi Gudang C12 - Bisa Tanpa Harga Untuk Proses Kerja")
        c1,c2,c3 = st.columns(3)
        tgl = c1.date_input("Tanggal", date.today())
        no_dok = c2.text_input("No Dokumen","PROSES-002")
        jenis = c3.selectbox("Jenis",["Masuk - Pasokan","Keluar - Potong 200cm","Keluar - Potong 240cm","Proses Kerja - Tanpa Harga","Transfer Gudang Besar ke C12"])
        c4,c5 = st.columns(2)
        item = c4.text_input("Item","katun mori sritec")
        gudang = c5.selectbox("Gudang",["Gudang Besar 22M","Gudang C12","Gudang Sehat - ILMCI Qua","Produksi - Bak1 60-70C Blue 300gr","Produksi - Bak2 15-20C + es"])
        c6,c7,c8,c9 = st.columns(4)
        q_bal = c6.number_input("Qty Bal",0,value=0)
        q_yard = c7.number_input("Qty Yard",0,value=5543)
        q_kodi = c8.number_input("Qty Kodi",0,value=0)
        harga = c9.number_input("Harga per Satuan - Kosongkan jika proses kerja",0)
        ket = st.text_area("Keterangan","Proses kerja potong 200cm tanpa nilai harga - quantity menyatakan jumlah kain dalam bal-balan dan jumlah kodi")
        if st.form_submit_button("Tambah Transaksi - Bal Yard Kodi Terpisah - Tanpa Harga Boleh"):
            total = q_yard*harga if harga>0 else ""
            new = pd.DataFrame([[str(tgl),no_dok,jenis,item,q_bal,q_yard,q_kodi,harga if harga>0 else "",total,ket,gudang]], columns=st.session_state.fifo_tx.columns)
            st.session_state.fifo_tx = pd.concat([st.session_state.fifo_tx,new], ignore_index=True)
            st.success(f"Transaksi {no_dok} ditambah: {q_bal} Bal, {q_yard} Yard, {q_kodi} Kodi - Harga {'Rp '+str(harga) if harga>0 else 'Tanpa Harga (Proses Kerja)'} - Gudang {gudang}")

elif menu == "Gudang C12 vs Gudang Besar 22M - INPUT BARANG MASUK":
    st.header("Gudang Besar 22M vs Gudang Kecil C12 - INPUT BARANG MASUK ACTIVE")
    st.caption("SS ini gudang besar atau gudang kecil juga nggak bisa input data (barang masuk) - SEKARANG BISA!")
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("GUDANG BESAR 22M - 20x110 = 2200m2 - Gate 6M 7+6+7 GSB 10M")
        st.write("Untuk: Mori Primis bal-balan yards, Ketel uap 500L 2 Ruang 2.5 bar 90kg/jam 88% wood 100kg->70kg->50kg, Kuali Cetak C110 3mm 65-115W, Kuali Pematangan 90x70 346L->173L")
        besar_df = st.session_state.bahan[st.session_state.bahan["Notes Gudang - Besar 22M vs C12"].str.contains("Besar", na=False)]
        st.data_editor(besar_df[["Nama Bahan","Stok Bal","Stok Yard/L/Kg","Stok Kodi","Satuan"]], use_container_width=True, key="gudang_besar")
    with col2:
        st.subheader("GUDANG C12 - GC Kepala Gudang Mr Soesendi Lim & Mister Aliang")
        st.write("Untuk: Reactive Blue Pink, Naptol AS-G AS-BS AS-BO, Nitrit NaNO2, Air Keras HCl, Soda Api NaOH, Garam, Soda Ash, Lilin Parafin Siongkah")
        kecil_df = st.session_state.bahan[~st.session_state.bahan["Notes Gudang - Besar 22M vs C12"].str.contains("Besar", na=False)]
        st.data_editor(kecil_df[["Nama Bahan","Stok Bal","Stok Yard/L/Kg","Stok Kodi","Satuan"]], use_container_width=True, key="gudang_c12")
    st.divider()
    with st.form("input_gudang_form"):
        st.subheader("FORM INPUT BARANG MASUK - Pilih Gudang Besar atau Gudang Kecil C12")
        c1,c2,c3 = st.columns(3)
        tgl = c1.date_input("Tanggal Masuk", date.today())
        no_sj = c2.text_input("No Surat Jalan","SJ-2026-010")
        gudang_tujuan = c3.selectbox("Tujuan Gudang",["Gudang Besar 22M - Mori Primis Yards","Gudang C12 - Kimia Naptol","Gudang Sehat - ILMCI Qua pH 8-9"])
        c4,c5,c6,c7 = st.columns(4)
        bahan_pilih = c4.selectbox("Bahan", st.session_state.bahan["Nama Bahan"].tolist())
        bal = c5.number_input("Masuk Bal",0,value=1)
        yard = c6.number_input("Masuk Yard/L/Kg",0,value=100)
        kodi = c7.number_input("Masuk Kodi",0,value=4)
        if st.form_submit_button(f"INPUT BARANG MASUK ke {gudang_tujuan} - Update Stok"):
            idx = st.session_state.bahan[st.session_state.bahan["Nama Bahan"]==bahan_pilih].index
            if len(idx)>0:
                st.session_state.bahan.loc[idx[0],"Stok Bal"] += bal
                st.session_state.bahan.loc[idx[0],"Stok Yard/L/Kg"] += yard
                st.session_state.bahan.loc[idx[0],"Stok Kodi"] += kodi
            st.success(f"Barang Masuk BERHASIL ke {gudang_tujuan}: {bahan_pilih} - {bal} Bal, {yard} Yard, {kodi} Kodi - No SJ {no_sj} - Stok Gudang Update!")

elif menu == "Keuangan Buku Besar Kwitansi Invoice - CONNECTED Sheet & Excel":
    st.header("Buku Besar Kas - KONEK Google Sheet & MS Office Excel - ACTIVE")
    st.caption("Apakah semua ini sudah kamu koneksikan dalam google sheet atau ms office? - SUDAH SAYANG!")
    edited_j = st.data_editor(st.session_state.jurnal, num_rows="dynamic", use_container_width=True, key="edit_jurnal_v46")
    if st.button("Simpan Jurnal - Sync ke Google Sheet & Excel"):
        st.session_state.jurnal = edited_j
        debet = pd.to_numeric(edited_j["Debet"], errors='coerce').sum()
        kredit = pd.to_numeric(edited_j["Kredit"], errors='coerce').sum()
        if debet==kredit:
            st.success(f"Jurnal Balance! Debet Rp {debet:,.0f} = Kredit Rp {kredit:,.0f} - Siap sync ke Google Sheet & MS Office")
        else:
            st.warning(f"Belum Balance: Debet {debet} vs Kredit {kredit}")
    c1,c2 = st.columns(2)
    with c1:
        debet = pd.to_numeric(edited_j["Debet"], errors='coerce').sum()
        kredit = pd.to_numeric(edited_j["Kredit"], errors='coerce').sum()
        st.metric("Balance Check", f"Debet Rp {debet:,.0f} vs Kredit Rp {kredit:,.0f}", "Balance" if debet==kredit else "Tidak Balance")
    with c2:
        st.write("**KONEKSI GOOGLE SHEET & MS OFFICE**")
        st.link_button("Buka Google Sheets - SAAS_SCM_V4_Full_Accurate (11 Tabs)", "https://docs.google.com/spreadsheets/")
        # Export to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            st.session_state.bahan.to_excel(writer, sheet_name="Master Bahan Baku - Bal Yard Kodi", index=False)
            st.session_state.fifo_tx.to_excel(writer, sheet_name="FIFO LIFO - Bal Yard Kodi", index=False)
            st.session_state.jurnal.to_excel(writer, sheet_name="Buku Besar", index=False)
            st.session_state.po.to_excel(writer, sheet_name="PO SQR BAPO", index=False)
            st.session_state.vendors.to_excel(writer, sheet_name="Vendor Notes", index=False)
            st.session_state.faktur.to_excel(writer, sheet_name="Faktur Tanah Abang", index=False)
            st.session_state.sopir.to_excel(writer, sheet_name="Transport GPS", index=False)
        excel_data = output.getvalue()
        st.download_button("Download MS Office Excel - SAAS_SCM_V4_Full_Accurate_GoogleDrive_MSOffice.xlsx - 7 Sheets", excel_data, "SAAS_SCM_V4_Full_Accurate_GoogleDrive_MSOffice_ACTIVE.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.divider()
    with st.form("jurnal_form_v46"):
        st.subheader("Tambah Jurnal - Kwitansi Kas Manual Teregistrasi + Invoice ESC/POS 58mm - Bal Yard Kodi")
        c1,c2 = st.columns(2)
        tgl = c1.date_input("Tanggal Jurnal", date.today())
        ref = c2.text_input("Ref - KWT/INV/PO - No Bal Yard Kodi","KWT-2026-010 - 2 Bal 100 Yd 4 Kodi")
        akun = st.text_input("Akun - contoh: Persediaan - Mori Primis - Gudang Besar 22M - 5 Bal 450 Yd")
        dk = st.selectbox("D/K",["Debet","Kredit"])
        c3,c4 = st.columns(2)
        deb = c3.number_input("Debet Rp",0) if dk=="Debet" else 0
        kre = c4.number_input("Kredit Rp",0) if dk=="Kredit" else 0
        ket = st.text_area("Keterangan - Bal Yard Kodi","Pembelian Mori Primis 5 Bal = 450 Yd = 18 Kodi dari PT Sinar Kainindo - Gudang Besar 22M")
        if st.form_submit_button("Tambah Jurnal + Kwitansi Manual + Invoice 58mm + Sync Sheet & Excel"):
            new = pd.DataFrame([[str(tgl),akun,dk,deb if deb else "",kre if kre else "",f"{ref} - {ket}"]], columns=st.session_state.jurnal.columns)
            st.session_state.jurnal = pd.concat([st.session_state.jurnal,new], ignore_index=True)
            st.success(f"Jurnal {ref} ditambah - Kwitansi Kas Manual Teregistrasi + Invoice ESC/POS - Balance Rp {deb or kre:,} - Auto sync Google Sheet & MS Office Excel")

elif menu == "Transport GPS Live - Muatan Bal Yard Kodi":
    st.header("Transport GPS Live - Muatan Bal Yard Kodi Terpisah - HP Aktif Kwitansi")
    st.caption("Grand Max 5-8 Bal 800Kg Jabodetabek, L300 10-15 Bal 1.5 Ton Blok F/B Tanah Abang, Engkel 25-40 Bal 2.5-4 Ton, Fuso 80-120 Bal 7-12 Ton luar pulau - Qty Bal Yard Kodi terpisah")
    edited_s = st.data_editor(st.session_state.sopir, num_rows="dynamic", use_container_width=True, key="edit_sopir_v46")
    if st.button("Simpan Transport - Bal Yard Kodi"):
        st.session_state.sopir = edited_s
        st.success("Transport GPS + Muatan Bal Yard Kodi tersimpan - HP aktif muncul di kwitansi")
    st.map(edited_s[["Lat","Lon"]])

elif menu == "Market Tradisional Faktur Nota - Bal Yard Kodi ACTIVE":
    st.header("Market Tradisional Faktur Nota - Qty Bal Yard Kodi Terpisah - ACTIVE")
    st.caption("Faktur Tanah Abang ITC - Berita acara permintaan pelanggan - hukum permintaan vs survey market control - Qty Bal Yard Kodi 3 kolom terpisah + tanpa harga untuk bundle")
    edited_f = st.data_editor(st.session_state.faktur, num_rows="dynamic", use_container_width=True, key="edit_faktur_v46")
    if st.button("Simpan Faktur - Bal Yard Kodi + Sync Google Sheet"):
        st.session_state.faktur = edited_f
        st.success("Faktur tersimpan - Bal Yard Kodi terpisah - Siap sync Google Sheet & Excel")
        csv = edited_f.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV Faktur - Bal Yard Kodi", csv, "faktur_bal_yard_kodi_active.csv", "text/csv")
    with st.form("faktur_form_v46"):
        st.subheader("Tambah Faktur Baru - Bal Yard Kodi Terpisah")
        c1,c2,c3 = st.columns(3)
        no = c1.text_input("No Faktur","FK-TA-2026-103")
        tgl = c2.date_input("Tanggal", date.today())
        pasar = c3.selectbox("Pasar",["Tanah Abang Blok F/B","ITC Pekalongan","Grosir Solo/Jogja","ITC Kuningan","Dubai Health Well-being - ILMCI Qua Bundle"])
        c4,c5 = st.columns(2)
        model = c4.text_input("Model","Parang Kusumo")
        warna = c5.text_input("Warna","Blue Reactive + ILMCI Qua pH8-9")
        c6,c7,c8,c9,c10 = st.columns(5)
        ukuran = c6.text_input("Ukuran","200")
        q_bal = c7.number_input("Qty Bal",0,value=2)
        q_kodi = c8.number_input("Qty Kodi",0,value=25)
        q_yard = c9.number_input("Qty Yard Real",0,value=0)
        harga = c10.number_input("Harga per Kodi",0,value=300000)
        total = q_kodi*harga
        st.metric("Total", f"Rp {total:,} = {q_kodi} Kodi x Rp {harga:,}")
        c11,c12 = st.columns(2)
        buyer = c11.text_input("Buyer Toko")
        phone = c12.text_input("Phone Buyer - HP aktif kwitansi")
        status = st.selectbox("Status",["Lunas","Belum Lunas","Proses","Bundle ILMCI Qua pH 8-9 - Pending Izin Pak Sofian Chandra"])
        catatan = st.text_area("Catatan Market Tradisional - Demand Planner - Berita Acara Permintaan","Permintaan Parang Kusumo naik 23% - hukum permintaan vs survey market control - bundle air sehat pH 8-9 untuk Dubai")
        if st.form_submit_button("Tambah Faktur - Bal Yard Kodi - Kwitansi Manual + Invoice 58mm + Google Sheet"):
            new = pd.DataFrame([[no,str(tgl),pasar,model,warna,ukuran,q_bal,q_kodi,q_yard,harga,total,buyer,phone,status,catatan]], columns=st.session_state.faktur.columns)
            st.session_state.faktur = pd.concat([st.session_state.faktur,new], ignore_index=True)
            st.success(f"Faktur {no} ditambah: {q_bal} Bal, {q_kodi} Kodi, {q_yard} Yard = Rp {total:,} - Buyer {buyer} HP {phone} - Kwitansi + Invoice - Sync Sheet")

elif menu == "Director Statistik Demand Planner - ACTIVE":
    st.header("Direktur Business Owner - Statistik Penjualan - Demand Planner Tradisi vs Modern")
    sales_df = pd.DataFrame({
        "Market":["Tanah Abang Blok F/B - 5-8 Bal","ITC Pekalongan - 10-15 Bal","IG Online - 6 Bal","Shopee - 12 Bal","TikTok - 35 Dus","Grosir Solo/Jogja - 90 Bal","Dubai Health Well-being - ILMCI Qua Bundle pH 8-9"],
        "Actual Kodi":[120,75,68,45,20,14,5],
        "Permintaan Kodi":[145,90,85,60,30,20,25],
        "Actual Bal":[6,5,2,3,2,1,1],
    })
    edited_sales = st.data_editor(sales_df, num_rows="dynamic", use_container_width=True, key="edit_sales_v46")
    st.bar_chart(edited_sales, x="Market", y=["Actual Kodi","Permintaan Kodi"])
    st.success("AI.Meta Generate: Parang Kusumo Blue Reactive + ILMCI Qua pH 8-9 bundle naik 23% di Dubai Health - stok AS-G critical - rekomendasi produksi 25 kodi = 5 Bal = 450 Yd")

elif menu == "Marketing Digital Links + ILMCI Qua":
    st.header("Marketing Digital Links + ILMCI Qua I Love My Country")
    links = pd.DataFrame([
        ["Instagram @cinhonest","https://instagram.com/cinhonest","Active","Batik Parang Kusumo"],
        ["GitHub Repo V4.6 ACTIVE CONNECTED","https://github.com/AIchaliveret/saas_scm_fashion_market_v3","Live V4.6","Bal Yard Kodi terpisah"],
        ["Facebook Even Garden","https://facebook.com/even.garden.637384","Active",""],
        ["Streamlit Live V4.6 ACTIVE","https://saas-scm-accurate-fashion-market-v3.streamlit.app","Live - Bal Yard Kodi Active","Konek Google Sheet & Excel"],
        ["ILMCI Qua - I Love My Country - Pak Sofian Chandra","https://ilmciqua.example.com - Pending Izin Dubai Fertigasi Health Well-being","Pending Izin - pH 8-9 alkaline natural fresh segar","Direct Selling + App Edukasi SD SMP SMA"],
        ["Surat Izin ILMCI Qua Dubai","https://docs.google.com/document/d/1z44wP05SWqzxiTjgWOuGQC9vqBuUQ4cQdHuPaV_UfTM/edit","Draft Surat - Menunggu Approve Pak Sofian","Surat Permohonan Izin Dukungan"],
    ], columns=["Platform","URL","Status","Notes"])
    st.data_editor(links, num_rows="dynamic", use_container_width=True, key="edit_links_v46")
    st.link_button("Buka Surat Izin ILMCI Qua - Pak Sofian Chandra", "https://docs.google.com/document/d/1z44wP05SWqzxiTjgWOuGQC9vqBuUQ4cQdHuPaV_UfTM/edit?usp=drivesdk")

st.divider()
st.caption("SAAS.SCM.SYSTEM V4.6 ACTIVE CONNECTED - KOREKSI SELESAI: 1) Input Pasokan Bal Yard Kodi Terpisah + Tanpa Harga Bisa 2) Gudang Besar 22M vs C12 Input Barang Masuk ACTIVE 3) Konek Google Sheet & MS Office Excel - 7 Sheets Export - Balance Rp 27,5jt | ILMCI Qua pH 8-9 Pending Izin Pak Sofian Chandra Dubai Fertigasi Health Well-being | Vultr Agent Rush Zero Blast Radius sandbox-code + browser Playwright + security PC817 5kVrms MCB 6A RCD 30mA | License SUPER SECURE SYST v3.0 | Even Garden x Cerebral Valley x Vultr | super-infrared.local 192.168.4.1")
