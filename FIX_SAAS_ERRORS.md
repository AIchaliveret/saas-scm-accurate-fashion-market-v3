
# FIX 1: ModuleNotFoundError openpyxl
# In requirements.txt tambah:
openpyxl
xlsxwriter

# FIX 2: st.map error
# Ganti:
# st.map(edited_s[["Lat","Lon"]])
# Menjadi:
if not edited_s.empty and "Lat" in edited_s.columns and "Lon" in edited_s.columns:
    map_df = edited_s[["Lat","Lon"]].dropna()
    map_df["Lat"] = pd.to_numeric(map_df["Lat"], errors='coerce')
    map_df["Lon"] = pd.to_numeric(map_df["Lon"], errors='coerce')
    map_df = map_df.dropna()
    if not map_df.empty:
        st.map(map_df)
    else:
        st.warning("GPS Lat/Lon belum ada data valid - cek -6.2088,106.8456")
else:
    st.info("Belum ada data Transport GPS Live - isi dulu di Gudang")
