import sqlite3

def init_db(db_name="call_logs.db"):
    """Initializes the local SQLite relational file schema layout."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sim_slot TEXT,
            phone_number TEXT,
            status TEXT,
            duration INTEGER,
            citizen_speech TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_log(slot, phone, status, duration, speech, db_name="call_logs.db"):
    """Inserts an active network call interaction record safely into the disk file."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO calls (sim_slot, phone_number, status, duration, citizen_speech) VALUES (?, ?, ?, ?, ?)",
        (slot, phone, status, duration, speech)
    )
    conn.commit()
    conn.close()
