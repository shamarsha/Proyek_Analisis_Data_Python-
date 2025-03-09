import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
bikes_hourly = pd.read_csv("dashboard/hour_cleaned.csv")

# Sidebar Filters
view_option = st.sidebar.selectbox("Pilih Filter", ["Perkembangan Jumlah Sewa Sepeda", "Pengaruh Musim dan Cuaca", "Pengguna Terdaftar vs Tidak Terdaftar", "Pemakaian per Jam"])

st.title("Dashboard Analisis Data Bike Sharing")

# Filter 1
if view_option == "Perkembangan Jumlah Sewa Sepeda":
    st.subheader("Perkembangan Jumlah Sewa Sepeda dari tahun 2011 ke 2012")
    yearly_counts = bikes_hourly.groupby("yr")["cnt"].sum()
    st.bar_chart(yearly_counts)

# Filter 2
elif view_option == "Pengaruh Musim dan Cuaca":
    st.subheader("Pengaruh Musim dan Cuaca terhadap Jumlah Sewa Sepeda")
    workday_option = st.radio("Pilih Jenis Hari", ["Hari Kerja", "Hari Libur"])
    
    if workday_option == "Hari Kerja":
        filtered_df = bikes_hourly[bikes_hourly["workingday"] == 1]
    else:
        filtered_df = bikes_hourly[bikes_hourly["holiday"] == 1]
    
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_df, x="season", y="cnt", hue="weathersit", ax=ax, ci=None)
    plt.xlabel("Musim")
    plt.ylabel("Rata-rata Jumlah Sewa Sepeda")
    plt.title(f"Sewa Sepeda berdasarkan Musim & Cuaca pada {workday_option}")
    st.pyplot(fig)
    
    st.markdown("""
    **Kondisi Cuaca:**
    - **1:** Cerah, Berawan sebagian
    - **2:** Kabut + Berawan, Kabut + Sedikit awan, Kabut
    - **3:** Salju ringan, Hujan ringan + Awan berserakan
    - **4:** Hujan lebat + Salju Lebat + Petir + Kabut
    """)

# Filter 3
elif view_option == "Pengguna Terdaftar vs Tidak Terdaftar":
    st.subheader("Perbandingan Jumlah Sewa Pengguna Terdaftar dengan Tidak Terdaftar")

    # Urutan nama bulan dengan kategori
    month_order = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]

    # Konversi angka bulan ke nama bulan dengan tipe kategori
    bikes_hourly["mnth"] = pd.Categorical(bikes_hourly["mnth"].replace(dict(enumerate(month_order, start=1))),
                                          categories=month_order, ordered=True)

    # Agregasi data berdasarkan bulan
    monthly_shared = bikes_hourly.groupby("mnth")[["casual", "registered"]].sum().sort_index()

    st.line_chart(monthly_shared)

# Filter 4
elif view_option == "Pemakaian per Jam":
    st.subheader("Tren Penyewaan Sepeda per Jam")
    yr_selected = st.selectbox("Pilih Tahun", [2011, 2012])
    hourly_avg = bikes_hourly[bikes_hourly["yr"] == yr_selected].groupby("hr")["cnt"].mean()
    st.line_chart(hourly_avg)

st.sidebar.write("Sumber: Bike Sharing Dataset")