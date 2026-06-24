
import streamlit as st
import pandas as pd
import re

# ================= SETTING HALAMAN =================
st.set_page_config(
    page_title="Manajemen Mahasiswa",
    page_icon="",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#f5f7fa,#dfe9f3);
}

h1 {
    text-align:center;
    color:#1e3a8a;
}

.block-container {
    padding-top:2rem;
}

div.stButton > button {
    width:100%;
    border-radius:10px;
    height:45px;
    font-weight:bold;
}

[data-testid="stMetric"]{
    background:white;
    padding:10px;
    border-radius:10px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ================= CLASS INDUK =================
class Orang:
    def __init__(self, nama):
        self.nama = nama

    def info(self):
        return f"Nama : {self.nama}"


# ================= CLASS TURUNAN =================
class Mahasiswa(Orang):

    def __init__(self, nim, nama, jurusan):
        super().__init__(nama)

        self.__nim = nim
        self.__jurusan = jurusan

    def get_nim(self):
        return self.__nim

    def get_nama(self):
        return self.nama

    def get_jurusan(self):
        return self.__jurusan

    def set_nama(self, nama_baru):
        self.nama = nama_baru

    def set_jurusan(self, jurusan_baru):
        self.__jurusan = jurusan_baru

    def info(self):
        return f"NIM : {self.__nim} | Nama : {self.nama} | Jurusan : {self.__jurusan}"


# ================= SESSION =================
if "data_mahasiswa" not in st.session_state:
    st.session_state.data_mahasiswa = []


# ================= HEADER =================
st.markdown("""
<h1> Aplikasi Manajemen Data Mahasiswa</h1>
<p style='text-align:center;color:gray'>
CRUD • Search • Sort • File I/O • OOP
</p>
""", unsafe_allow_html=True)


# ================= STATISTIK =================
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Jumlah Mahasiswa",
              len(st.session_state.data_mahasiswa))

with c2:
    st.metric("Status Sistem", "Aktif")

with c3:
    st.metric("Data Tersimpan",
              len(st.session_state.data_mahasiswa))


# ================= INPUT =================
st.subheader(" Input Data Mahasiswa")

col1, col2 = st.columns(2)

with col1:
    nim = st.text_input("NIM")

with col2:
    nama = st.text_input("Nama")

jurusan = st.text_input("Jurusan")


# ================= TOMBOL BARIS 1 =================
b1, b2, b3 = st.columns(3)

with b1:
    tambah = st.button(" Tambah Data")

with b2:
    edit = st.button(" Edit Data")

with b3:
    hapus = st.button(" Hapus Data")


# ================= TOMBOL BARIS 2 =================
b4, b5, b6 = st.columns(3)

with b4:
    linear = st.button(" Cari Linear")

with b5:
    binary = st.button(" Cari Binary")

with b6:
    simpan = st.button(" Simpan File")


# ================= TOMBOL BARIS 3 =================
b7, b8, b9 = st.columns(3)

with b7:
    baca = st.button(" Baca File")

with b8:
    bubble = st.button("⬆ Bubble Sort")

with b9:
    selection = st.button(" Selection Sort")


# ================= TAMBAH =================
if tambah:

    if not re.fullmatch(r"\d+", nim):
        st.error("NIM harus angka")

    elif not re.fullmatch(r"[A-Za-z ]+", nama):
        st.error("Nama hanya boleh huruf")

    else:
        st.session_state.data_mahasiswa.append(
            Mahasiswa(nim, nama, jurusan)
        )

        st.success("Data berhasil ditambahkan")


# ================= EDIT =================
if edit:

    ditemukan = False

    for mhs in st.session_state.data_mahasiswa:

        if mhs.get_nim() == nim:

            mhs.set_nama(nama)
            mhs.set_jurusan(jurusan)

            ditemukan = True
            st.success("Data berhasil diubah")
            break

    if not ditemukan:
        st.error("Data tidak ditemukan")


# ================= HAPUS =================
if hapus:

    for mhs in st.session_state.data_mahasiswa:

        if mhs.get_nim() == nim:

            st.session_state.data_mahasiswa.remove(mhs)
            st.success("Data berhasil dihapus")
            break


# ================= LINEAR SEARCH =================
if linear:

    ditemukan = False

    for mhs in st.session_state.data_mahasiswa:

        if mhs.get_nim() == nim:

            st.success("Data ditemukan")
            st.write(mhs.info())

            ditemukan = True
            break

    if not ditemukan:
        st.error("Data tidak ditemukan")


# ================= BINARY SEARCH =================
if binary:

    data = sorted(
        st.session_state.data_mahasiswa,
        key=lambda x: x.get_nim()
    )

    kiri = 0
    kanan = len(data) - 1

    ditemukan = False

    while kiri <= kanan:

        tengah = (kiri + kanan) // 2

        if data[tengah].get_nim() == nim:

            st.success("Data ditemukan")
            st.write(data[tengah].info())

            ditemukan = True
            break

        elif data[tengah].get_nim() < nim:
            kiri += 1

        else:
            kanan -= 1

    if not ditemukan:
        st.error("Data tidak ditemukan")


# ================= BUBBLE SORT =================
if bubble:

    data = st.session_state.data_mahasiswa

    for i in range(len(data)):
        for j in range(len(data)-i-1):

            if data[j].get_nama() > data[j+1].get_nama():

                data[j], data[j+1] = data[j+1], data[j]

    st.success("Bubble Sort berhasil")


# ================= SELECTION SORT =================
if selection:

    data = st.session_state.data_mahasiswa

    for i in range(len(data)):

        min_idx = i

        for j in range(i+1, len(data)):

            if data[j].get_nama() < data[min_idx].get_nama():
                min_idx = j

        data[i], data[min_idx] = data[min_idx], data[i]

    st.success("Selection Sort berhasil")


# ================= SIMPAN FILE =================
if simpan:

    with open("mahasiswa.txt", "w") as file:

        for mhs in st.session_state.data_mahasiswa:

            file.write(
                f"{mhs.get_nim()},"
                f"{mhs.get_nama()},"
                f"{mhs.get_jurusan()}\n"
            )

    st.success("Data berhasil disimpan")


# ================= BACA FILE =================
if baca:

    try:

        st.session_state.data_mahasiswa.clear()

        with open("mahasiswa.txt", "r") as file:

            for baris in file:

                nim_file, nama_file, jurusan_file = \
                    baris.strip().split(",")

                st.session_state.data_mahasiswa.append(
                    Mahasiswa(
                        nim_file,
                        nama_file,
                        jurusan_file
                    )
                )

        st.success("Data berhasil dibaca")

    except FileNotFoundError:
        st.error("File tidak ditemukan")


# ================= TABEL DATA =================
st.subheader(" Data Mahasiswa")

if st.session_state.data_mahasiswa:

    data = []

    for mhs in st.session_state.data_mahasiswa:

        data.append({
            "NIM": mhs.get_nim(),
            "Nama": mhs.get_nama(),
            "Jurusan": mhs.get_jurusan()
        })

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Belum ada data mahasiswa")