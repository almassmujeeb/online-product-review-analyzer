import sqlite3

conn = sqlite3.connect("review.db")
cursor = conn.cursor()

# Reviews Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reviews(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    platform TEXT,
    product_name TEXT,
    rating INTEGER,
    review TEXT,
    sentiment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Visitors Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS visitors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")