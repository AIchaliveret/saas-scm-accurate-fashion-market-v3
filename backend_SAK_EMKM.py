
# SAAS_SCM_V8_BACKEND_PABU_SAK_EMKM - Uang Muka PO + Retur + Penyusutan - Python Requests - SAK EMKM
import requests, json
from datetime import datetime

GOOGLE_SHEETS_WEB_APP_URL = "https://script.google.com/macros/s/YOUR_WEB_APP_ID/exec"  # Ganti dengan URL deploy Apps Script Anda

def send_to_google_sheets(rows):
    """Kirim jurnal double-entry ke Google Sheets via Apps Script doPost - Validasi Balancing Check"""
    total_debit = sum(r['debit'] for r in rows)
    total_kredit = sum(r['kredit'] for r in rows)
    if total_debit != total_kredit:
        raise ValueError(f"Jurnal Tidak Balance! Debit {total_debit} != Kredit {total_kredit} - PABU / GAAP - Aset = Kewajiban + Modal")
    payload = {"rows": rows}
    r = requests.post(GOOGLE_SHEETS_WEB_APP_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    print(f"✅ Sent to Google Sheets: Debit={total_debit} Kredit={total_kredit} - Response: {r.text}")
    return r.text

# 1. UANG MUKA PO - ACCRUAL BASIS - DP sebagai Kewajiban 2-1200 Bukan Pendapatan 4-1100
def handle_uang_muka_po(tanggal, no_bukti, kode_po, jumlah_bal, jumlah_kodi, total_order, dp_amount, nama_pembeli):
    print(f"\n=== UANG MUKA PO - {kode_po} - DP Rp {dp_amount} - {nama_pembeli} ===")
    jurnal_dp = [
        {"tanggal": tanggal, "no_bukti": f"BKM-DP-{no_bukti}", "kode_akun": "1-1200", "nama_akun": "Bank Operasional", "keterangan": f"Terima DP 50% {kode_po} - {nama_pembeli} - {jumlah_bal} Bal {jumlah_kodi} Kodi", "debit": dp_amount, "kredit": 0},
        {"tanggal": tanggal, "no_bukti": f"BKM-DP-{no_bukti}", "kode_akun": "2-1200", "nama_akun": "Uang Muka Pelanggan / Utang Pendapatan", "keterangan": f"DP PO {kode_po} - Kewajiban - Belum boleh diakui Pendapatan - SAK EMKM Accrual - Economic Entity", "debit": 0, "kredit": dp_amount}
    ]
    send_to_google_sheets(jurnal_dp)
    
    def handle_pelunasan_dan_pengiriman(tanggal_kirim, no_bukti_lunas, pelunasan_amount, sopir, gps="-6.2088,106.8456"):
        print(f"=== PELUNASAN & PENGIRIMAN - {kode_po} - Dikirim {sopir} GPS {gps} ===")
        jurnal_lunas = [
            {"tanggal": tanggal_kirim, "no_bukti": f"BKM-LNS-{no_bukti_lunas}", "kode_akun": "2-1200", "nama_akun": "Uang Muka Pelanggan", "keterangan": f"Reklasifikasi DP menjadi Pendapatan - PO Selesai - Dikirim {sopir} GPS {gps} - Matching Principle", "debit": dp_amount, "kredit": 0},
            {"tanggal": tanggal_kirim, "no_bukti": f"BKM-LNS-{no_bukti_lunas}", "kode_akun": "4-1100", "nama_akun": "Penjualan Shopee/TikTok", "keterangan": f"Akui Pendapatan PO {kode_po} - Tanah Abang Blok F/B", "debit": 0, "kredit": dp_amount},
            {"tanggal": tanggal_kirim, "no_bukti": f"BKM-LNS-{no_bukti_lunas}", "kode_akun": "1-1200", "nama_akun": "Bank Operasional", "keterangan": f"Terima Pelunasan {kode_po} - {nama_pembeli} - Total {total_order}", "debit": pelunasan_amount, "kredit": 0},
            {"tanggal": tanggal_kirim, "no_bukti": f"BKM-LNS-{no_bukti_lunas}", "kode_akun": "4-1100", "nama_akun": "Penjualan Shopee/TikTok", "keterangan": f"Pelunasan Pendapatan {kode_po} - {jumlah_kodi} Kodi @300rb", "debit": 0, "kredit": pelunasan_amount}
        ]
        send_to_google_sheets(jurnal_lunas)
    
    return handle_pelunasan_dan_pengiriman

# Contoh pakai:
# handle_dp = handle_uang_muka_po("2026-11-01", "001", "ORD-2026-001 Parang Kusumo", 2, 25, 7500000, 2500000, "Toko Sari Jaya Tanah Abang")
# handle_dp("2026-11-05", "001", 5000000, "Ahmad Subarjo Grand Max 5-8 Bal 800Kg")

# 2. RETUR BARANG CACAT - JURNAL BALIK OTOMATIS
def handle_retur_cacat(tanggal_retur, no_bukti_retur, no_bukti_jual_asal, sku, jumlah_retur, harga_jual_per_pcs, hpp_per_pcs, alasan):
    print(f"\n=== RETUR BARANG CACAT - {sku} - {jumlah_retur} pcs - {alasan} ===")
    total_refund = jumlah_retur * harga_jual_per_pcs
    total_hpp_retur = jumlah_retur * hpp_per_pcs
    jurnal_retur = [
        {"tanggal": tanggal_retur, "no_bukti": f"RTR-{no_bukti_retur}", "kode_akun": "4-1110", "nama_akun": "Retur Penjualan - Kontra Pendapatan", "keterangan": f"Retur {jumlah_retur} pcs {sku} - {alasan} - Kembali ke Gudang C12 - {no_bukti_jual_asal}", "debit": total_refund, "kredit": 0},
        {"tanggal": tanggal_retur, "no_bukti": f"RTR-{no_bukti_retur}", "kode_akun": "1-1100", "nama_akun": "Kas Toko / Piutang Usaha", "keterangan": f"Refund {jumlah_retur} pcs {sku} - {alasan} - Toko Sari Jaya", "debit": 0, "kredit": total_refund},
        {"tanggal": tanggal_retur, "no_bukti": f"RTR-{no_bukti_retur}", "kode_akun": "1-1420", "nama_akun": "Persediaan Barang Jadi", "keterangan": f"Barang Retur Kembali ke Stok - Gudang C12 Rak B1 QR-010 - Return to Inventory - {sku} - Bal Yard Kodi", "debit": total_hpp_retur, "kredit": 0},
        {"tanggal": tanggal_retur, "no_bukti": f"RTR-{no_bukti_retur}", "kode_akun": "5-1100", "nama_akun": "Biaya Bahan Baku - HPP", "keterangan": f"Penyesuaian HPP Retur - HPP Berkurang - Matching Principle - Persediaan Awal + Pembelian - Akhir", "debit": 0, "kredit": total_hpp_retur}
    ]
    send_to_google_sheets(jurnal_retur)
    print(f"✅ Stok Bal Yard Kodi bertambah kembali: {jumlah_retur} pcs {sku} ke Gudang C12")

# Contoh:
# handle_retur_cacat("2026-11-03", "001", "TRM-001", "BATIK-PK-200 Parang Kusumo", 1, 500000, 300000, "Cacat Kain / Salah Ukuran")

# 3. PENYUSUTAN ASET TETAP - JURNAL PENYESUAIAN OTOMATIS AKHIR BULAN
def handle_penyusutan_akhir_bulan(tanggal_akhir_bulan="2026-11-30"):
    print(f"\n=== PENYUSUTAN ASET TETAP - {tanggal_akhir_bulan} - Straight Line - SAK EMKM ===")
    assets = [
        {"nama": "Mesin Jahit 5 unit - CMT Cut Make Trim", "harga": 15000000, "umur_bulan": 60, "kode_beban": "6-1500", "kode_akumulasi": "1-1601"},
        {"nama": "Canting Cap Tembaga 20 pcs - Mister Budi Sandy", "harga": 8000000, "umur_bulan": 48, "kode_beban": "6-1500", "kode_akumulasi": "1-1601"},
        {"nama": "Wajan + Bak Semen 90x120x18cm + Bak1 60-70C Bak2 15-20C", "harga": 5000000, "umur_bulan": 36, "kode_beban": "6-1500", "kode_akumulasi": "1-1601"},
        {"nama": "Ketel Uap 500L 2.5 bar 90kg/jam + Turbine Francis 1000W x4 + Thermal Battery 500L", "harga": 25000000, "umur_bulan": 120, "kode_beban": "6-1500", "kode_akumulasi": "1-1601"}
    ]
    jurnal = []
    total_beban = 0
    for a in assets:
        beban = a['harga'] / a['umur_bulan']
        total_beban += beban
        jurnal.append({"tanggal": tanggal_akhir_bulan, "no_bukti": f"ADJ-DEP-{tanggal_akhir_bulan}", "kode_akun": a['kode_beban'], "nama_akun": "Beban Penyusutan Peralatan", "keterangan": f"Penyusutan {a['nama']} - {beban:.0f}/bln", "debit": round(beban), "kredit": 0})
        jurnal.append({"tanggal": tanggal_akhir_bulan, "no_bukti": f"ADJ-DEP-{tanggal_akhir_bulan}", "kode_akun": a['kode_akumulasi'], "nama_akun": "Akumulasi Penyusutan Peralatan - Kontra Aset", "keterangan": f"Akumulasi Penyusutan {a['nama']}", "debit": 0, "kredit": round(beban)})
    send_to_google_sheets(jurnal)
    print(f"✅ Total Beban Penyusutan Bulan Ini: Rp {total_beban:.0f} - Aset Bersih = Harga - Akumulasi - Neraca Balance Aset = Kewajiban + Modal")

# handle_penyusutan_akhir_bulan("2026-11-30")
