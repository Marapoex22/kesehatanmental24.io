import streamlit as st

def main():
    st.title('Simple Login App')

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
            # Lanjutkan ke halaman lain atau tampilkan konten setelah login
        else:
            st.error('Username atau password salah')

if __name__ == '__main__':
    main()
