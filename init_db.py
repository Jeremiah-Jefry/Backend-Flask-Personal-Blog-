import sqlite3

# Create/connect to database
conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# Create posts table (Session 3)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("✅ Blog database initialized! Run 'python app.py' to start.")
