import streamlit as st

def main():
    st.title('kesehatan Mental App')

    # Menampilkan halaman login menggunakan HTML
    with open('login.html', 'r') as file:
        login_page = file.read()
    st.markdown(login_page, unsafe_allow_html=True)

    # Memproses input dari form login
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    # Cek login ketika tombol login ditekan
    if st.button('Login'):
        if username == 'admin' and password == 'password':
            st.success('Login berhasil!')
            # Navigasi ke halaman diagnosa setelah login berhasil
            show_diagnosa_page()
        else:
            st.error('Username atau password salah')

def show_diagnosa_page():
    st.title('Halaman Diagnosa')

    # Menampilkan halaman diagnosa menggunakan HTML
    with open('templates/diagnosa.html', 'r') as file:
        diagnosa_page = file.read()
    st.markdown(diagnosa_page, unsafe_allow_html=True)

    # Tambahkan logika dan interaksi tambahan di halaman diagnosa di sini

if __name__ == '__main__':
    main()
