import numpy as np 
import pandas as pd 
import pickle
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection

from PIL import Image

image = Image.open('Bobot fitur.jpg')


def main():
    
    choice = option_menu(None, ["Home","Prediksi","Hasil","Penilaian","Tentang"], 
    icons=['house','trophy', 'camera', 'list-task', 'book'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    st.header('Prediksi Performa Akademik Mahasiswa')

    if choice == "Home":
        st.subheader("Definisi dan penjelasan")
        st.write('Performa akademik mahasiswa adalah capaian seorang mahasiswa dalam mendapatkan nilai akademik, indikator performa akademik diperoleh dari nilai Indek Prestasi Sementara (IPS) maupun Indek Prestasi Komulatif (IPK).') 
        st.write('Banyak variabel yang mempengaruhi performa akademik mahasiswa baik variabel perilaku didalam pembelajaran maupun variabel lainnya. Pada sistem informasi prediksi performa akademik mahasiswa ini variabel yang digunakan adalah variabel akademik dan non-akademik.') 
        st.write('Variabel akademik adalah variabel yang diperoleh dari kegiatan akademik yaitu variabel IPK/IPS dan perilaku mahasiswa dalam berinteraksi dengan Learning Management System (LMS). Sedangkan variabel non-akademik terdiri dari faktor ekonomi, domisili, gender dan keikutsertaan mahasiswa dalam berorganisasi kampus.')
        st.write('Prediksi performa akademik mahasiswa merupakan aktivitas yang sangat penting, hal ini dikarenakan dengan memprediksi performa akademik mahasiswa, dapat menciptakan peluang untuk meningkatkan hasil pendidikan. Selain itu dengan pendekatan prediksi performa yang efektif, instruktur dapat mengalokasikan sumber daya dan instruksi yang lebih akurat. Prediksi awal performa mahasiswa dapat membantu pengambil keputusan untuk memberikan tindakan pada saat yang tepat dan untuk merencanakan pembelajaran yang tepat dalam meningkatkan tingkat keberhasilan mahasiswa')
        st.write('Performa akademik mahasiswa perlu dipantau dengan cermat untuk membantu lembaga mengidentifikasi mahasiswa yang berisiko gagal, mencegah mereka DO atau lulus terlambat (Nachouki dan Abou Naaj 2022). Performa akademik yang buruk menjadi indikator mahasiswa kesulitan dalam menyesuaikan diri dengan perguruan tinggi dan berpeluang besar untuk putus sekolah/drop out (DO) (Lau 2003). Beberapa dampak negatif dari buruknya performa akademik dan tingginya DO diantaranya yaitu rendahnya tingkat kelulusan tepat waktu (Delen 2010), membuang biaya Pendidikan yang sia-sia (Costa, Bispo, dan Pereira 2018), pengurangan kesempatan hidup secara profesional dan sosial yang berdampak negatif kepada keluarga dan masyarakat (Casanova dkk. 2021), sulitnya perguruan tinggi dalam mendapatkan akreditasi yang baik (Delen, Topuz, dan Eryarsoy 2020), hilangnya kepercayaan dan motivasi untuk melanjutkan Pendidikan (Coussement dkk. 2020), dan lain sebagainya.')    
        st.write('Sistem informasi Prediksi Performa Akademik Mahasiswa ini sangat penting bagi Mahasiswa, Dosen, Staff Akademik dan lainnya. Berdasarkan data yang digunakan untuk membangun model, maka sistem informasi prediksi performa akademik mahasiswa ini sangat baik digunakan untuk memprediksi performa akademik mahasiswa semester dua dan empat')
        st.write('Untuk melakukan prediksi performa akademik mahasiswa, maka silahkan ke menu :blue[Prediksi], Jangan lupa setelah melakukan prediksi silahkan berikan penilaian dan masukan untuk pengembangan aplikasi selanjutnya di menu :blue[Penilaian]')


    elif choice == "Prediksi":

        st.write('Prediksi performa akademik ini menggunakan dua sumber data yaitu 1). Data Akademik yang berasal dari aktifitas mahasiswa di LMS (Moodle),  2). Data non-akademik (ekonomi, domisili, gender, keikutsertaan mahasiswa dalam berorganisasi kampus). Sistem informasi prediksi ini sangat tepat jika digunakan untuk memprediksi performa akademik mahasiswa semester dua dan empat.')
        
        st.subheader("Masukkan Data Diri Anda")
        nama = st.text_input('Nama :blue[(Nama Anda tidak dipublikasikan)], Data anda tidak termasuk bagian dari Prediksi')

        colus,colkel = st.columns(2)
        with colus:
            status = st.radio(
                    'Status',
                    ('Mahasiswa', 'Dosen', 'Staff Akademik', 'Lainnya'))
        with colkel:
            jenkel = st.radio(
                    'Jenis Kelamin',
                    ('Pria', 'Wanita'))

        kota_tinggal = st.text_input('Kota Tinggal :blue[(Kota tingal Anda)]')

        st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        
        st.write("Ini merupakan bagian Prediksi Performa Akademik Mahasiswa, Anda dapat melakukan percobaan prediksi berulang kali, dengan mengganti nilai-nilai fiturnya")
        st.subheader("Masukkan Data Akademik (Kegiatan di LMS)")
        st.write('Perlu dipahami bahwasanya masing-masing fitur memiliki bobot yang berbeda, masing-masing bobot ditunjukkan pada caption fitur')
        st.write('Untuk menginputkan nilai, silahkan :blue[geser slider kekanan untuk menambah atau kekiri untuk mengurangi]')
        
        col1,col2 = st.columns(2)
        with col1:
            Total_login = st.slider('Jumlah Login LMS :blue[(0,303)]', 0, 140)
            N_access_forum = st.slider('Jumlah Akses Forum LMS :blue[(0,130)]', 0, 3000)
            N_access_didactic_units = st.slider('Jumlah Akses Materi :blue[(0,107)]', 0, 750)
            N_assignments_submitted = st.slider('Jumlah Upload Tugas :blue[(0,128)]', 0, 150)
            
        with col2:
            N_reviews_questionnaire = st.slider('Jumlah Ulasan Quiz :blue[(0,089)]', 0, 500)
            Days_first_access_x = st.slider('Minggu Keberapa Akses LMS :blue[(0,033)]', 0, 3)
            N_entries_course_x = st.slider('Jumlah Masuk Ke Mata Kuliah :blue[(0,089)]', 0, 3000)


        st.subheader("Masukkan Data Non Akademik")

        cols,colss = st.columns(2)
        with cols:
            Gender = st.radio(
                    'Jenis Kelamin :blue[(0,026)]',
                    ('Pria', 'Wanita'))
            if Gender == 'Pria':
                Gender = 1
            else:
                Gender = 0

            Campus_organization = st.slider('Jumlah Organisasi Kampus Yang Diikuti :blue[(0,053)]', 0, 4)

        with colss:
            Economy = st.selectbox(
                    'Pendapatan Orang Tua :blue[(0,026)]',
                    ('100.000 - 600.000', '500.000 - 1.000.000', '1.000.000 - 2.500.000', 
                        '2.500.000 - 5.000.000', '5.000.000 - 7.500.000',
                        '7.500.000 - 10.000.000', '> 10.000.000')) 
            if Economy == '100.000 - 600.000':
                Economy = 1
            elif Economy == '500.000 - 1.000.000':
                Economy = 2
            elif Economy == '1.000.000 - 2.500.000':
                Economy = 3
            elif Economy == '2.500.000 - 5.000.000':
                Economy = 4
            elif Economy == '5.000.000 - 7.500.000':
                Economy = 5
            elif Economy == '7.500.000 - 10.000.000':
                Economy = 6
            else:
                Economy = 7

            Domicile = st.selectbox(
                    'Jarak Kota Domisili dengan Kampus :blue[(0,014)]',
                    ('Dalam Kota', 'Kota Sebelah', 'Jarak Satu Kota', 'Dalam Satu Pulau', 'Diluar Pulau'))

            if Domicile == 'Dalam Kota':
                Domicile = 1
            elif Domicile == 'Kota Sebelah':
                Domicile = 2
            elif Domicile == 'Jarak Satu Kota':
                Domicile = 3
            elif Domicile == 'Dalam Satu Pulau':
                Domicile = 4
            else : Domicile = 5            

        with open("ppakm.sav", "rb") as file:
            model = pickle.load(file)

        predit = ''

        if Gender == 1:
            jekel = "Pria"
        else: 
            jekel ="Wanita"

        if Economy == 1:
            pendap = '100.000 - 600.000'
        elif Economy == 2:
            pendap = '500.000 - 1.000.000'
        elif Economy == 3:
            pendap = '1.000.000 - 2.500.000'
        elif Economy == 4:
            pendap = '2.500.000 - 5.000.000'
        elif Economy == 5:
            pendap = '5.000.000 - 7.500.000'
        elif Economy == 6:
            pendap = '7.500.000 - 10.000.000'
        else:
            pendap = '> 10.000.000'

        if Domicile == 1:
            Domisili = 'Dalam Kota'
        elif Domicile == 2:
            Domisili = 'Kota Sebelah'
        elif Domicile == 3:
            Domisili = 'Jarak Satu Kota'
        elif Domicile == 4:
            Domisili = 'Dalam Satu Pulau'
        else : 
            Domisili = 'Diluar Pulau' 


        if st.button('Prediksi Performa'):
            if not nama or not kota_tinggal:
                st.warning("Pastikan semua textbox terisi.")
            else:
                predit = model.predict(
                    [[Gender, Domicile, Economy, Campus_organization, 
                      Total_login, N_access_forum, N_access_didactic_units, 
                      N_assignments_submitted, N_reviews_questionnaire, 
                      Days_first_access_x, N_entries_course_x]]
                )
                st.success (f"Hasil Prediksi : %.2f" % predit)
    
                #Simpan data
                conn = st.connection("gsheets", type=GSheetsConnection)
                data1 = conn.read(worksheet="HasilPrediksi",usecols=list(range(22)), ttl=5)
                data1 = data1.dropna(how="all")
                
                data_prediksi = pd.DataFrame(
                    [
                        {
                            "Nama":nama, "Status":status, "Jenis_Kelamin":jenkel, "Kota_Tinggal":kota_tinggal, "Jenis Kelamin":jekel, 
                            "Ekonomi":pendap, "Domisili":Domisili, "Organisasi Kampus":Campus_organization,
                            "Jumlah Login LMS":Total_login, "Jumlah Akses Forum":N_access_forum, "Jumlah Akses Materi":N_access_didactic_units, 
                            "Jumlah Upload Tugas":N_assignments_submitted, "Jumlah Ulasan Quiz":N_reviews_questionnaire,  
                            "Minggu Keberapa Akses LMS":Days_first_access_x, "Jumlah Masuk Ke Mata Kuliah":N_entries_course_x, 
                            "Hasil Prediksi":predit,
                        }
                    ]
                )
    
                # Add the new vendor data to the existing data
                updated_df = pd.concat([data1, data_prediksi], ignore_index=True)
                conn.update(worksheet="HasilPrediksi", data=updated_df)
                v_data = data_prediksi.iloc[:, 4:22]
                st.dataframe(v_data)
                st.write('Terima kasih. Untuk mendownload hasil prediksi, silahkan kepojok kanan dari tabel diatas, lalu klik download')
            
       
    elif choice == "Hasil":
        st.subheader("Data Hasil Prediksi")
        conn = st.connection("gsheets", type=GSheetsConnection)
        data1 = conn.read(worksheet="HasilPrediksi",usecols=list(range(16)), ttl=5)
        data1 = data1.dropna(how="all")
        v_data = data1.iloc[:, 4:16]
        st.dataframe(v_data)
        
    elif choice == "Penilaian":

        conn = st.connection("gsheets", type=GSheetsConnection)
        datapenilaian = conn.read(worksheet="HasilPenilaian",usecols=list(range(6)), ttl=5)
        datapenilaian = datapenilaian.dropna(how="all")
 
        st.subheader("Nilai Aplikasi dan Saran")
        st.write('Berikan penilaian terhadap sisterm informasi ini')

        form= st.form("myform",clear_on_submit=True)
        col1,col2 = form.columns(2)
        with col1:

                kemudahan = st.radio(
                    'Kemudahan dalam menggunakan sistem',
                    ('Sangat Baik', 'Baik', 'Cukup Baik','Kurang Baik'))

                if kemudahan == 'Sangat Baik':
                    kemudahan = 4
                elif kemudahan == 'Baik':
                    kemudahan = 3 
                elif kemudahan == 'Cukup Baik':
                    kemudahan = 2 
                else:
                    kemudahan = 1

                kelengkapan = st.radio(
                    'Kelengkapan dalam memprediksi performa akademik',
                    ('Sangat Baik', 'Baik', 'Cukup Baik','Kurang Baik'))

                if kelengkapan == 'Sangat Baik':
                    kelengkapan = 4
                elif kelengkapan == 'Baik':
                    kelengkapan = 3 
                elif kelengkapan == 'Cukup Baik':
                    kelengkapan = 2 
                else:
                    kelengkapan = 1

                informasi = st.radio(
                    'Informasi yang disajikan',
                    ('Sangat Baik', 'Baik', 'Cukup Baik','Kurang Baik'))

                if informasi == 'Sangat Baik':
                    informasi = 4
                elif informasi == 'Baik':
                    informasi = 3 
                elif informasi == 'Cukup Baik':
                    informasi = 2 
                else:
                    informasi = 1

        with col2:

                kualitas = st.radio(
                    'Kualitas sistem informasi',
                    ('Sangat Baik', 'Baik', 'Cukup Baik','Kurang Baik'))

                if kualitas == 'Sangat Baik':
                    kualitas = 4
                elif kualitas == 'Baik':
                    kualitas = 3 
                elif kualitas == 'Cukup Baik':
                    kualitas = 2 
                else:
                    kualitas = 1

                kepuasan = st.radio(
                    'Kepuasan dalam menggunakan',
                    ('Sangat Puas', 'Puas', 'Cukup Puas','Kurang Puas'))

                if kepuasan == 'Sangat Puas':
                    kepuasan = 4
                elif kepuasan == 'Puas':
                    kepuasan = 3 
                elif kepuasan == 'Cukup Puas':
                    kepuasan = 2 
                else:
                    kepuasan = 1

        saran = form.text_area("Berikan saran untuk pengembangan sistem informasi ini dimasa mendatang")

        submit_button=form.form_submit_button("Simpan")

            #Simpan data penilaian
        if submit_button:
            data_penilaian = pd.DataFrame(
                    [
                        {
                            "Kemudahan Penggunaan":kemudahan, 
                            "Kelengkapan Prediksi":kelengkapan, 
                            "Informasi Yang Disajikan":informasi, 
                            "Kualitas Sistem Informasi":kualitas, 
                            "Kepuasan Penggunaan":kepuasan, 
                            "Masukan":saran,
                        }
                    ]
                )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([datapenilaian, data_penilaian], ignore_index=True)
            conn.update(worksheet="HasilPenilaian", data=updated_df)
            form.info("Data berhasil disimpan, Terima kasih atas penialaian dan saran Anda")


        st.write('**Grafik Hasil Penilaian Pengguna**')

        colo1,colo2 = st.columns(2)
        with colo1:
            #Grafik penilaian kemudahan penggunaan
            st.write('*Kemudahan Penggunaan*')
            x= datapenilaian['Kemudahan Penggunaan'].tolist()
            count_value = 1
            counti = x.count(count_value)
            count_value = 2
            counti1 = x.count(count_value)
            count_value = 3
            counti2 = x.count(count_value)
            count_value = 4
            counti3 = x.count(count_value)

            # Pie chart
            labels = 'Kurang Baik', 'Cukup Baik', 'Baik', 'Sangat Baik'
            sizes = [counti, counti1, counti2, counti3]
            explode = (0, 0.05, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            #ax1.set_title("Kemudahan Penggunaan")
            st.pyplot(fig1)

            #Grafik penilaian kelengkapan prediksi
            st.write('*Kelengkapan Prediksi*')
            xs=datapenilaian['Kelengkapan Prediksi'].tolist()
            count_value2 = 1
            counti = xs.count(count_value2)
            count_value2 = 2
            counti1 = xs.count(count_value2)
            count_value2 = 3
            counti2 = xs.count(count_value2)
            count_value2 = 4
            counti3 = xs.count(count_value2)

            # Pie chart
            labels = 'Kurang Baik', 'Cukup Baik', 'Baik', 'Sangat Baik'
            sizes = [counti, counti1, counti2, counti3]
            explode = (0, 0.05, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

            #Grafik penilaian informasi yang disajikan
            st.write('*Informasi Yang Disajikan*')
            xs2=datapenilaian['Informasi Yang Disajikan'].tolist()
            count_value = 1
            counti = xs2.count(count_value)
            count_value = 2
            counti1 = xs2.count(count_value)
            count_value = 3
            counti2 = xs2.count(count_value)
            count_value = 4
            counti3 = xs2.count(count_value)
       
            # Pie chart
            labels = 'Kurang Baik', 'Cukup Baik', 'Baik', 'Sangat Baik'
            sizes = [counti, counti1, counti2, counti3]
            explode = (0, 0.05, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

        with colo2:
            #Grafik penilaian kualitas sistem informasi
            st.write('*Kualitas Sistem Informasi*')
            xs3=datapenilaian['Kualitas Sistem Informasi'].tolist()
            count_value = 1
            counti = xs3.count(count_value)
            count_value = 2
            counti1 = xs3.count(count_value)
            count_value = 3
            counti2 = xs3.count(count_value)
            count_value = 4
            counti3 = xs3.count(count_value)

            #Bar chart
            labels = 'Kurang Baik', 'Cukup Baik', 'Baik', 'Sangat Baik'
            sizes = [counti, counti1, counti2, counti3]
            fig5, ax5 = plt.subplots()
            plt.bar(labels, sizes)
            ax5.set_ylabel("Penilaian")
            #ax5.set_xlabel("Kategori Nilai")
            #ax5.set_title("Layanan")
            #plt.grid(axis='y')
            st.pyplot(fig5)
         
            #Grafik penilaian kepuasan pengguna
            st.write('*Kepuasan Penggunaan*')
            xs4=datapenilaian['Kepuasan Penggunaan'].tolist()
            count_value = 1
            counti = xs4.count(count_value)
            count_value = 2
            counti1 = xs4.count(count_value)
            count_value = 3
            counti2 = xs4.count(count_value)
            count_value = 4
            counti3 = xs4.count(count_value)
           
            #Bae chart
            labels = 'Kurang Puas', 'Cukup Puas', 'Puas', 'Sangat Puas'
            sizes = [counti, counti1, counti2, counti3]
       
            fig5, ax5 = plt.subplots()
            plt.bar(labels, sizes)
            ax5.set_ylabel("Penilaian")
            st.pyplot(fig5)

    elif choice == "Tentang":
        st.subheader("Tentang Aplikasi")
        st.write('Sistem Informasi Prediksi Performa Akademik Mahasiswa ini dibuat dengan menggunakan bahasa pemprograman :blue[Python] dan :blue[Streamlit] sedangkan database yang digunakan adalah :blue[Google Sheets], Sisfo ini menggunakan model yang terbentuk dari algoritma :blue[Gradient Boosting Trees] yang telah dioptimasi hyperparameternya dengan menggunakan algoritma :blue[Gread Search]. Sedangkan data yang digunakan untuk membangun model berasal dari data akademik dan data non-akademikdemik yang diperoleh dari :blue[Universitas Muria Kudus].')
        st.write('Dalam melakukan prediksi Model ini memiliki tingkat kesalahan sebesar :blue[21%], Adapun nilai bobot dari masing-masing fitur ditunjukkan pada halaman prediksi dan pada gambar dibawah ini.')

        st.image(image, caption='Bobot Fitur')

        st.write('Untuk informasi lebih lanjut terkait Prediksi Performa Akademik Mahasiswa ini, dapat menghubungi Email: :blue[arifin.m@umk.ac.id] ')


if __name__ == '__main__':
    main()
