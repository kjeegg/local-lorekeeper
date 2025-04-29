import sqlite3
import os

DB_PATH = 'memory/memory_store.sqlite'

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    # Ensure the directory exists before trying to create the database file
    if not os.path.exists('memory'):
        os.makedirs('memory')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            chapter TEXT,
            mood TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_memory(content, chapter=None, mood=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memories (content, chapter, mood) VALUES (?, ?, ?)", (content, chapter, mood))
    conn.commit()
    conn.close()

def get_all_memories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, timestamp, chapter, mood FROM memories ORDER BY timestamp ASC")
    memories = cursor.fetchall()
    conn.close()
    return memories

def get_memory_by_id(memory_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, timestamp, chapter, mood FROM memories WHERE id = ?", (memory_id,))
    memory = cursor.fetchone()
    conn.close()
    return memory

def update_memory(memory_id, content, chapter, mood):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE memories SET content = ?, chapter = ?, mood = ? WHERE id = ?", (content, chapter, mood, memory_id))
    conn.commit()
    conn.close()

def delete_memory(memory_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
    conn.commit()
    conn.close()

# Call init_db to create the database and table when the script is run or imported
init_db()
