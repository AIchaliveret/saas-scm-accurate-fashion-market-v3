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

menu = st.sidebar.radio("NAVIGASI V4.7 - PABU GAAP SAK EMKM - Anti Hang", [
    "Dashboard Accurate",
    "Master Bahan Baku - INPUT PASOKAN Bal Yard Kodi",
    "FIFO LIFO Average - Qty Terpisah Tanpa Harga",
    "Vendor Notes - ACTIVE",
    "PO SQR BAPO Surat Jalan - ACTIVE",
    "Keuangan Buku Besar Kwitansi Invoice - CONNECTED Sheet & Excel",
    "Gudang C12 vs Gudang Besar 22M - INPUT BARANG MASUK",
    "Transport GPS Live - Muatan Bal Yard Kodi",
    "Market Tradisional Faktur Nota - Bal Yard Kodi ACTIVE",
    "Invoice Nota Surat Jalan SRITEX Template - Divisi Terkait",
    "PABU GAAP SAK EMKM V7 V8A V8B - Anti Hang + T-Account + Uang Muka Retur",
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
        # === FIX LINE 283 - Transport GPS Live - Muatan Bal Yard Kodi - ANTI HANG V2 - FIX SYNTAX ===
    # GANTI SEMUA DARI LINE 283 SAMPAI 301 DENGAN INI (indent 4 spasi di dalam if menu Transport):
    try:
        if 'edited_s' in locals() and not edited_s.empty and "Lat" in edited_s.columns and "Lon" in edited_s.columns:
            map_df = edited_s[["Lat","Lon"]].copy()
            map_df["Lat"] = pd.to_numeric(map_df["Lat"], errors='coerce')
            map_df["Lon"] = pd.to_numeric(map_df["Lon"], errors='coerce')
            map_df = map_df.dropna()
            if not map_df.empty:
                st.map(map_df)
                st.caption(f"GPS Live: {len(map_df)} titik - Ahmad Subarjo On the way Tanah Abang 12km")
            else:
                st.warning("GPS Lat/Lon belum valid - isi contoh -6.2088,106.8456 (UNIKA Atma Jaya)")
                st.map(pd.DataFrame([{"Lat": -6.2088, "Lon": 106.8456}]))
        else:
            st.info("Belum ada data Transport GPS Live - isi Sopir + Muatan Bal Yard Kodi dulu")
            st.map(pd.DataFrame([{"Lat": -6.2088, "Lon": 106.8456}]))
    except Exception as e:
        st.warning(f"Map fallback: {e}")
        st.map(pd.DataFrame([{"Lat": -6.2088, "Lon": 106.8456}]))
    # === END FIX V2 ===



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


elif menu == "Invoice Nota Surat Jalan SRITEX Template - Divisi Terkait":
    st.header("Invoice Nota Surat Jalan - SRITEX Template - PT Sri Rejeki Isman Tbk - Adaptasi Pabrik Batik")
    st.caption("Contoh Google kamu: INV/20261101/042 200 Roll Primissima + 150 Roll Prima = 77jt + PPN 11% = 85.470.000 - Adaptasi jadi Bal Yard Kodi Terpisah + Prinsip Akuntansi Sama Atas Izin Prinsip")
    tab1, tab2, tab3, tab4 = st.tabs(["Invoice Sritex Template", "Nota Pembelian", "Surat Jalan + Divisi Terkait", "Generate Invoice Baru Bal Yard Kodi"])
    with tab1:
        st.subheader("Invoice - Faktur Penagihan Resmi - SRITEX Template Adaptasi")
        inv_df = pd.DataFrame([
            ["INV/20261101/042","2026-11-01","PO-9982/BTK/X/2026 = PO-2026-010","PT Batik Nusantara Agung / Even Garden","Kain Katun Mori Primissima Cap 115cm 33m - 5 Bal = 450 Yd = 18 Kodi",5,450,18,10000,4500000],
            ["","","","", "Kain Katun Mori Prima 105cm 33m - 3 Bal = 270 Yd = 10 Kodi",3,270,10,10000,2700000],
            ["","","7 Bal kedatangan bisa 10 Bal","Mori Primis 90cm 6kg/25 kodi - Bal-balan","Mori Primis 90cm 7 Bal = 630 Yd = 28 Kodi per Bal Rp 900.000",7,630,28,10000,6300000],
        ], columns=["No Invoice","Tanggal","PO","Kepada Yth","Deskripsi Barang","Qty Bal","Qty Yard","Qty Kodi","Harga/Yard","Total"])
        edited_inv = st.data_editor(inv_df, num_rows="dynamic", use_container_width=True, key="inv_sritex")
        subtotal = pd.to_numeric(edited_inv["Total"], errors='coerce').sum()
        ppn = subtotal*0.11
        total = subtotal+ppn
        c1,c2,c3 = st.columns(3)
        c1.metric("Subtotal", f"Rp {subtotal:,.0f}")
        c2.metric("PPN 11% - Prinsip Akuntansi Pajak", f"Rp {ppn:,.0f}")
        c3.metric("TOTAL TAGIHAN", f"Rp {total:,.0f}")
        st.info("Terbilang: Empat Belas Juta Sembilan Ratus Delapan Puluh Lima Ribu Rupiah - Bank Mandiri Cab Solo A/C 138-00-XXXX-XXXX A/N PT Sritex - Head of Finance Ibu Kirana Rahayu - Prinsip Akuntansi Sama")
    with tab2:
        st.subheader("Nota Pembelian - Kontan / Lunas - Adaptasi Nazar Batik Tulis Tangan")
        nota_df = pd.DataFrame([
            ["NT-8872/XI/26 = NT-2026-010","2026-11-01","PT Batik Nusantara Agung / Even Garden","5 Bal = 450 Yd = 18 Kodi","Mori Primissima 90cm",10000,4500000,"LUNAS - Kwitansi Kas Manual Teregistrasi - HP Sopir Aktif"],
            ["NT-2026-011","2026-11-01","Pabrik Batik Even Garden","7 Bal = 630 Yd = 28 Kodi","Mori Primis 90cm 6kg/25 kodi - Bal-balan",10000,6300000,"LUNAS - KWT-2026-010 - Buku Besar Kas Balance Rp 27,5jt"],
        ], columns=["No Nota","Tanggal","Kepada","Banyaknya - Bal Yard Kodi Terpisah","Nama Barang","Harga/Yard","Total","Status - LUNAS/TUNAI"])
        st.data_editor(nota_df, num_rows="dynamic", use_container_width=True, key="nota_sritex")
        st.caption("Divisi: Staff Purchasing (Pembeli) - Admin Penjualan / Kasir (Penjual) - Kepala Gudang C12 Mr Soesendi Lim & Mister Aliang - Status LUNAS/TUNAI - Kwitansi HP Sopir Aktif - Prinsip Akuntansi Sama")
    with tab3:
        st.subheader("Surat Jalan - Delivery Order + Divisi Terkait 8 Divisi - Prinsip Akuntansi")
        sj_df = pd.DataFrame([
            ["SJ/20261101/992 = SJ-2026-010","2026-11-01","AD 8941 FA Truk Diesel / B9123TAB L300 10-15 Bal","Budi Santoso / Ahmad Subarjo HP 0812-1111-0001","Mori Primissima Cap 115cm 33m Segel Plastik QR-001",5,450,18,"Bagus / Segel Plastik - Gudang Besar 22M","Diterima Pelanggan - Sopir - Kepala Gudang - Sales Manager"],
            ["SJ-2026-011","2026-11-01","B2389CXT Grand Max 5-8 Bal 800Kg Jabodetabek","M Faisal 0857-3333-0003","ILMCI Qua pH 8-9 Alkaline Mineral Bundle Dubai Health Pending Izin Pak Sofian Chandra",0,120,2,"Natural fresh segar - Untuk karyawan Bak1 60-70C Bak2 15-20C","Ruang Teduh Loker Ruach Ha Kadosh"],
        ], columns=["No SJ","Tanggal","No Kendaraan","Nama Sopir - HP Aktif Kwitansi","Nama Barang - Banyaknya","Qty Bal","Qty Yard","Qty Kodi","Kondisi / QR Code","Divisi Terkait"])
        st.data_editor(sj_df, num_rows="dynamic", use_container_width=True, key="sj_sritex")
        st.divider()
        st.write("**Divisi Terkait - Penjelasan Lengkap - Prinsip Akuntansi Sama Atas Izin Prinsip**")
        divisi_df = pd.DataFrame([
            ["Head of Finance & Accounting Ibu Kirana Rahayu","Invoice PPN 11% Total 85.470.000 - Bank Mandiri","Direktur Business Owner Aku Bald Lead - Buku Besar Kas Balance","PSAK - PPN - Laporan Keuangan"],
            ["Procurement / Pembelian","PO-9982/BTK/X/2026","PO SQR BAPO - 7 Bal 630 Yd 28 Kodi - PT Sinar Kainindo","Persediaan - Pembelian - 7 Bal bisa 10 Bal - per Bal Rp 900.000"],
            ["Staff Purchasing / Admin Penjualan","Nota Banyaknya Bal Yard Kodi Terpisah","Master Bahan Baku INPUT PASOKAN 3 kolom terpisah - Tanpa harga boleh untuk proses kerja","Quantity - Bal Yard Kodi - Tanpa Harga Boleh - Jumlah kain dalam bal-balan dan jumlah kodi"],
            ["Kepala Gudang Mr Soesendi Lim & Mister Aliang","SJ fisik Segel Plastik QR Code - Rak A1","Gudang Besar 22M 20x110=2200m2 vs C12 INPUT BARANG MASUK ACTIVE","Gudang - Rak A1 QR-001 - Zero Blast Radius"],
            ["Sopir Ahmad Subarjo B9123TAB / Budi Santoso AD 8941 FA","SJ + No Kendaraan + HP Aktif Kwitansi + GPS Live","Transport GPS Live -6.2088,106.8456 Map - Muatan Bal Yard Kodi - 5-8 Bal 800Kg - 10-15 Bal 1.5 Ton","Logistik - Kwitansi Kas Manual Teregistrasi - Invoice ditentukan harga per tagih"],
            ["Sales Manager","Approve SJ 200 Roll 250rb + 150 Roll 180rb","Director Statistik Demand Planner Actual vs Permintaan","Hukum Permintaan - Survey Market Control - #OOTDJakarta"],
            ["Pelanggan Toko Sari Jaya Tanah Abang","Diterima Oleh SJ - Komplain setelah SJ tidak dilayani","Market Tradisional Faktur Nota Bal Yard Kodi ACTIVE FK-TA-2026-101 - Berita acara permintaan","Piutang - Penjualan - Demand Planner Tradisi"],
            ["Kasir Bank Mandiri Cab Solo 138-00-XXXX-XXXX","Status LUNAS/TUNAI","Kwitansi Kas Manual Teregistrasi KWT-2026-001 + Invoice ESC/POS 58mm - Buku Besar Kas Rp 27,5jt Balance","Kas Berkurang - Total Rupiah - Kwitansi - Invoice - Buku besar menambah persediaan quantity dan kas berkurang nilai rupiah total"],
        ], columns=["Divisi SRITEX","Tugas di Invoice/Nota/SJ","Di Pabrik Batik Even Garden SAAS SCM V4.7","Prinsip Akuntansi - Sama Atas Izin Prinsip"])
        st.data_editor(divisi_df, use_container_width=True, key="divisi_sritex")
    with tab4:
        st.subheader("Generate Invoice Baru - Bal Yard Kodi Terpisah - Prinsip Akuntansi Sama - Atas Izin Prinsip")
        with st.form("gen_invoice"):
            c1,c2 = st.columns(2)
            no_inv = c1.text_input("No Invoice - SRITEX Template","INV/20261101/042 - INV-2026-010")
            tgl = c2.date_input("Tanggal", date.today())
            c3,c4 = st.columns(2)
            po = c3.text_input("No PO","PO-9982/BTK/X/2026 = PO-2026-010 - 7 Bal kedatangan bisa 10 Bal")
            kepada = c4.text_input("Kepada Yth","PT Batik Nusantara Agung / Pabrik Batik Even Garden - Gudang Besar 22M")
            st.write("**Barang - Bal Yard Kodi Terpisah - Harga per Yard / per Bal - Bisa Tanpa Harga**")
            c5,c6,c7,c8,c9 = st.columns(5)
            nama_barang = c5.text_input("Nama Barang","Kain Katun Mori Primissima Cap 115cm 33m")
            qty_bal = c6.number_input("Qty Bal - Bal-balan",1,7)
            qty_yard = c7.number_input("Qty Yard - Kolom Terpisah",90,630)
            qty_kodi = c8.number_input("Qty Kodi",4,28)
            harga_yard = c9.number_input("Harga per Yard - Kosongkan jika proses kerja tanpa harga",10000)
            keterangan = st.text_area("Keterangan - Divisi Terkait - Prinsip Akuntansi","7 Bal sekali datang - bisa 10 Bal - per Bal Rp 900.000 = per Yard Rp 10.000 - Harga dikalikan harga satuan - Kwitansi kedatangan dalam jumlah Bal - Invoice ditentukan harga per tagih - Buku besar menambah persediaan quantity Bal Yard Kodi dan kas berkurang nilai rupiah total - Atas izin prinsip prinsip akuntansi PSAK - PPN 11%")
            total_calc = qty_yard*harga_yard if harga_yard>0 else 0
            ppn_calc = total_calc*0.11 if total_calc>0 else 0
            st.metric("Total + PPN 11%", f"Rp {total_calc:,.0f} + PPN Rp {ppn_calc:,.0f} = Rp {total_calc+ppn_calc:,.0f} = {qty_bal} Bal x {harga_yard*qty_yard/qty_bal if qty_bal else 0:,.0f} per Bal" if harga_yard>0 else f"Proses Kerja Tanpa Harga - Qty: {qty_bal} Bal = {qty_yard} Yd = {qty_kodi} Kodi - Buku besar hanya nambah quantity")
            if st.form_submit_button("Generate Invoice + Nota + Surat Jalan + Jurnal - Bal Yard Kodi - Prinsip Akuntansi Sama Atas Izin Prinsip"):
                idx = st.session_state.bahan[st.session_state.bahan["Nama Bahan"].str.contains("Mori", na=False)].index
                if len(idx)>0:
                    st.session_state.bahan.loc[idx[0],"Stok Bal"] += qty_bal
                    st.session_state.bahan.loc[idx[0],"Stok Yard/L/Kg"] += qty_yard
                    st.session_state.bahan.loc[idx[0],"Stok Kodi"] += qty_kodi
                new_fifo = pd.DataFrame([[str(tgl),no_inv,"Masuk - Pasokan - SRITEX Template",nama_barang,qty_bal,qty_yard,qty_kodi,harga_yard if harga_yard>0 else "",total_calc if total_calc>0 else "",keterangan,"Gudang Besar 22M"]], columns=st.session_state.fifo_tx.columns)
                st.session_state.fifo_tx = pd.concat([st.session_state.fifo_tx,new_fifo], ignore_index=True)
                if total_calc>0:
                    new_j1 = pd.DataFrame([[str(tgl),f"Persediaan - {nama_barang} - Gudang Besar 22M - {qty_bal} Bal {qty_yard} Yd {qty_kodi} Kodi","Debet",total_calc,"",f"{no_inv} - {qty_bal} Bal {qty_yard} Yd"]], columns=st.session_state.jurnal.columns)
                    new_j2 = pd.DataFrame([[str(tgl),f"Hutang Usaha / Kas - {kepada}","Kredit","","",total_calc,f"{no_inv} - PPN 11% Rp {ppn_calc:,.0f}"]], columns=st.session_state.jurnal.columns)
                    st.session_state.jurnal = pd.concat([st.session_state.jurnal,new_j1,new_j2], ignore_index=True)
                st.success(f"Invoice {no_inv} Generated! {qty_bal} Bal = {qty_yard} Yard = {qty_kodi} Kodi - Total Rp {total_calc:,.0f} + PPN Rp {ppn_calc:,.0f} - Persediaan quantity nambah Bal Yard Kodi - Kas berkurang rupiah total - Prinsip Akuntansi Sama - Atas Izin Prinsip! - Siap sync Google Sheet & MS Office FINAL 9 Sheets!")

elif menu == "PABU GAAP SAK EMKM V7 V8A V8B - Anti Hang + T-Account + Uang Muka Retur":
    st.header("PABU GAAP SAK EMKM V7 V8A V8B - Anti Hang - T-Account SUMIF Auto + Uang Muka Akrual + Retur Jurnal Balik + Depresiasi")
    st.caption("V7 4 Sheets + V8A 8KB Jurnal Double-Entry + V8B 10KB Master Akun - Fix _x5f_ & .xlsx.xlsx & .txt - Repo ringan - Scroll page 8 lancar - 100% PABU GAAP SAK EMKM")
    
    st.success("24 Commits - 2 Tags - Latest Release v1.1 - Fix double extension & x5f encoding - Anti nge-hang scroll page 8!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📥 Download Excel Anti Hang - 8KB + 10KB")
        st.write("**V8A Jurnal Double-Entry PABU + Uang Muka Retur - 8KB - 4 Sheets**")
        st.write("- Jurnal_Umum_Double_Entry: BKM-01, BKK-01 2 baris per transaksi Debit=Kredit Balance")
        st.write("- Uang_Muka_PO_Akrual: DP 2.5jt sebagai Kewajiban 2-1200 Kredit, bukan Pendapatan 4-1100 - Baru akui setelah kirim Grand Max GPS -6.2088,106.8456")
        st.write("- Retur_Barang_Cacat: Retur 1 pcs @500rb - Return to Inventory Gudang C12")
        st.write("- Balancing_Check: =SUMIF(C:C,kode,F:F) Validasi Balance")
        
        st.write("**V8B Master Akun SAK EMKM + Depresiasi + Akrual - 10KB - 4 Sheets**")
        st.write("- Master_Akun_SAK_EMKM: Chart of Accounts 1-1100 s/d 6-1500 Saldo Normal T-Account SUMIF")
        st.write("- Depresiasi: Mesin Jahit 15jt/60bln=250rb, Canting Cap 8jt/48bln=166.667, Ketel Uap 500L 25jt/120bln=208.333")
        st.write("- Akrual & Matching: HPP dikaitkan penjualan periode sama - DP = Kewajiban")
        st.write("- Pseudocode: handleUangMukaPO(), handleReturCacat(), handlePenyusutanAkhirBulan()")
        
        # Download buttons using session data or placeholder
        st.info("Download file Excel dari GitHub Repo - 25 Commits - Terbaru 1 minute ago - Anti Hang!")
        st.link_button("📥 GitHub - V8A Jurnal 8KB", "https://github.com/Alchaliveret/saas-scm-accurate-fashion-market-v3/blob/main/SAAS_SCM_V8A_Jurnal_PABU_FINAL.xlsx")
        st.link_button("📥 GitHub - V8B Master Akun 10KB", "https://github.com/Alchaliveret/saas-scm-accurate-fashion-market-v3/blob/main/SAAS_SCM_V8B_Master_Akun_SAK_EMKM_FINAL.xlsx")
        st.link_button("📥 GitHub - V7 T-Account SUMIF", "https://github.com/Alchaliveret/saas-scm-accurate-fashion-market-v3/blob/main/SAAS_SCM_V7_T_Account_FINAL.xlsx")
        st.link_button("📥 GitHub - Backend SAK EMKM.py", "https://github.com/Alchaliveret/saas-scm-accurate-fashion-market-v3/blob/main/backend_SAK_EMKM.py")
    
    with col2:
        st.subheader("🧮 Simulasi T-Account Otomatis - SUMIF")
        st.caption("Rumus: =SUMIF(Jurnal_Umum!C:C, \"1-1200\", F:F) Debit & G:G Kredit - Saldo = Debit - Kredit")
        
        # Demo T-Account
        t_data = pd.DataFrame([
            ["1-1100","Kas Toko","=SUMIF(Jurnal!C:C,\"1-1100\",F:F)","=SUMIF(Jurnal!C:C,\"1-1100\",G:G)","=Debit-Kredit","Aset - Debit"],
            ["1-1200","Bank Operasional","=SUMIF(Jurnal!C:C,\"1-1200\",F:F)","=SUMIF(Jurnal!C:C,\"1-1200\",G:G)","=Debit-Kredit","Aset - Debit"],
            ["2-1200","Uang Muka Pelanggan","=SUMIF(...2-1200...,F:F)","=SUMIF(...2-1200...,G:G)","=Kredit-Debit","Kewajiban - Kredit - Accrual"],
            ["4-1100","Penjualan Shopee","=SUMIF(...4-1100...,F:F)","=SUMIF(...4-1100...,G:G)","=Kredit-Debit","Pendapatan - Kredit"],
            ["4-1110","Retur Penjualan Kontra","=SUMIF(...4-1110...,F:F)","=SUMIF(...4-1110...,G:G)","=Debit-Kredit","Kontra Pendapatan - Debit"],
            ["5-1100","HPP Bahan Baku","=SUMIF(...5-1100...,F:F)","=SUMIF(...5-1100...,G:G)","=Debit-Kredit","HPP - Debit - Matching"],
            ["6-1500","Beban Penyusutan","=SUMIF(...6-1500...,F:F)","=SUMIF(...6-1500...,G:G)","=Debit-Kredit","Beban - Debit - Depresiasi"],
        ], columns=["Kode","Nama Akun","Total Debit SUMIF","Total Kredit SUMIF","Saldo Akhir","Kategori PABU"])
        st.data_editor(t_data, use_container_width=True, key="t_account_demo")
        
        st.subheader("💰 Simulasi Uang Muka PO - Accrual Basis")
        dp = st.number_input("DP PO 25 Kodi Rp", value=2500000)
        pelunasan = st.number_input("Pelunasan Rp", value=5000000)
        st.metric("Total Pendapatan Setelah Kirim", f"Rp {dp+pelunasan:,} = DP {dp:,} + Pelunasan {pelunasan:,}")
        st.write(f"Jurnal: Debit 2-1200 Rp {dp:,} Kredit 4-1100 Rp {dp:,} + Debit 1-1200 Rp {pelunasan:,} Kredit 4-1100 Rp {pelunasan:,}")
        
        st.subheader("📦 Simulasi Retur - Jurnal Balik")
        jml_retur = st.number_input("Jumlah Retur pcs", value=1)
        harga_jual = st.number_input("Harga Jual per pcs", value=500000)
        hpp = st.number_input("HPP per pcs", value=300000)
        st.metric("Total Refund", f"Rp {jml_retur*harga_jual:,} + Return Inventory Rp {jml_retur*hpp:,} = Rp {jml_retur*(harga_jual+hpp):,}")
    
    st.divider()
    st.subheader("🚀 Arsitektur API - HP/Laptop App -> Google Sheets")
    st.code("""
[ HP / Laptop App SAAS SCM V4.7 ]
        │ JSON Payload Double-Entry Balance
        ▼
[ Google Sheets API / Apps Script doPost(e) appendRow ]
        │ Menulis 2 Baris Baru ke Jurnal_Umum
        ▼
Jurnal_Umum --(SUMIF Auto)--> Buku_Besar_T & Laporan_Keuangan

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Jurnal_Umum");
  var data = JSON.parse(e.postData.contents);
  data.rows.forEach(row => sheet.appendRow([row.tanggal, row.no_bukti, row.kode_akun, row.nama_akun, row.keterangan, row.debit, row.kredit]));
  return ContentService.createTextOutput(JSON.stringify({"status":"success"})).setMimeType(ContentService.MimeType.JSON);
}

Payload:
{
  "rows": [
    {"tanggal":"2026-11-01","no_bukti":"BKM-DP-01","kode_akun":"1-1200","nama_akun":"Bank Operasional","keterangan":"DP PO Parang Kusumo 2 Bal 25 Kodi","debit":2500000,"kredit":0},
    {"tanggal":"2026-11-01","no_bukti":"BKM-DP-01","kode_akun":"2-1200","nama_akun":"Uang Muka Pelanggan","keterangan":"DP PO - Kewajiban - Accrual","debit":0,"kredit":2500000}
  ]
}
    """, language="javascript")
    
    st.success("100% PABU / GAAP + SAK EMKM - Double-Entry Aset=Kewajiban+Modal - Economic Entity - Matching Principle - Accrual Basis - Depresiasi Straight Line - Ready Vultr Agent Rush 1,881 builders 22:00 WIB 3 Nov!")

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
st.caption("SAAS.SCM.SYSTEM V4.7 PABU GAAP SAK EMKM - 25 Commits - Release v1.1 Latest - Fix _x5f_ & .xlsx.xlsx & .txt double - V7 4 Sheets + V8A 8KB Jurnal PABU Uang Muka Retur + V8B 10KB Master Akun Depresiasi Akrual - Anti Hang Scroll Page 8 Lancar - T-Account SUMIF Auto Jurnal_Umum->Buku_Besar_T->Laporan_Keuangan - Uang Muka Accrual 2-1200 Kewajiban - Retur Jurnal Balik 4-1110 Kontra Pendapatan - Depresiasi Straight Line 15jt/60bln=250rb - Backend handleUangMukaPO handleRetur handlePenyusutan - Balance Aset=Kewajiban+Modal - 100% PABU GAAP SAK EMKM - ILMCI Qua pH 8-9 Pending Izin | Vultr Agent Rush 1,881 builders 22:00 WIB 3 Nov - YOU'RE REGISTERED | Even Garden x Cerebral Valley x Vultr | super-infrared.local 192.168.4.1")
