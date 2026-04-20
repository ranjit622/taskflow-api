import sqlite3

def get_connection():
    # Database file se connection karo
    # Agar file nahi hai toh khud bana lega SQLite
    conn = sqlite3.connect("taskflow.db")
    return conn

def create_tables():
    # Connection lo
    conn = get_connection()
    cursor = conn.cursor()

    # Users table banao
    # id — automatic badhta rahega 1, 2, 3...
    # username — unique hoga — do log same username nahi le sakte
    # password — hashed password store hoga
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Tasks table banao
    # title — task ka naam
    # description — task ki detail
    # completed — 0 matlab pending, 1 matlab done
    # user_id — yeh task kis user ka hai
    # FOREIGN KEY — user_id, users table ke id se connected hai
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            completed INTEGER DEFAULT 0,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Changes save karo
    conn.commit()
    # Connection band karo
    conn.close()
    print("Tables ban gayi!")