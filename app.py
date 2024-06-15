import streamlit as st
import sqlite3
from sqlite3 import Error
import hashlib

# Function to create a connection to SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# Function to create tables if they do not exist
def create_tables(conn):
    if conn is not None:
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
        create_diagnosis_table = """
        CREATE TABLE IF NOT EXISTS diagnosis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symptoms TEXT,
            diagnosis TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """

        try:
            c = conn.cursor()
            c.execute(create_users_table)
            c.execute(create_diagnosis_table)
        except Error as e:
            print(e)

# Function to insert user data into users table
def insert_user(conn, username, password):
    sql = "INSERT INTO users(username, password) VALUES (?, ?)"
    cur = conn.cursor()
    cur.execute(sql, (username, password))
    conn.commit()
    return cur.lastrowid

# Function to retrieve user by username from users table
def get_user_by_username(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    return row

# Function to retrieve user by ID from users table
def get_user_by_id(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    return row

# Function to insert diagnosis data into diagnosis table
def insert_diagnosis(conn, user_id, symptoms, diagnosis):
    sql = "INSERT INTO diagnosis(user_id, symptoms, diagnosis) VALUES (?, ?, ?)"
    cur = conn.cursor()
    cur.execute(sql, (user_id, symptoms, diagnosis))
    conn.commit()
    return cur.lastrowid

# Function to initialize or get connection to SQLite database
def init_db():
    conn = create_connection('health_app.db')
    create_tables(conn)
    return conn

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Streamlit app main function
def main():
    st.title('Aplikasi Kesehatan Mental')

    menu = ['Login', 'Registrasi']
    choice = st.sidebar.selectbox('Menu', menu)

    # Initialize or get connection to database
    conn = init_db()

    if choice == 'Login':
        st.subheader('Login')

        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if st.button('Login'):
            hashed_password = hash_password(password)
            user = get_user_by_username(conn, username)
            if user and user[2] == hashed_password:
                st.success(f'Login berhasil sebagai {username}')
                st.subheader('Form Diagnosa')
                symptoms = st.text_area('Gejala')
                if st.button('Submit Diagnosa'):
                    insert_diagnosis(conn, user[0], symptoms, "Hasil diagnosa akan disimpan di sini")
                    st.success('Diagnosa telah disubmit!')

                st.markdown("---")
                st.subheader('Hasil Diagnosa Terakhir')
                last_diagnosis = st.empty()
                cur = conn.cursor()
                cur.execute("SELECT * FROM diagnosis WHERE user_id=?", (user[0],))
                rows = cur.fetchall()
                for row in rows:
                    last_diagnosis.write(f"Gejala: {row[2]} | Diagnosis: {row[3]}")

            else:
                st.error('Username atau password salah')

    elif choice == 'Registrasi':
        st.subheader('Registrasi')

        new_username = st.text_input('Username')
        new_password = st.text_input('Password', type='password')

        if st.button('Registrasi'):
            hashed_password = hash_password(new_password)
            if get_user_by_username(conn, new_username):
                st.warning('Username sudah ada, silakan gunakan username lain')
            else:
                insert_user(conn, new_username, hashed_password)
                st.success('Registrasi berhasil! Silakan login untuk melanjutkan.')

if __name__ == '__main__':
    main()
