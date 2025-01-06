import sqlite3

def create_db():
    # Connect to SQLite database (it will create the database if it doesn't exist)
    conn = sqlite3.connect('telemetry.db')
    c = conn.cursor()

    # Create a table for telemetry data if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    altitude REAL NOT NULL,
                    temperature REAL NOT NULL,
                    pressure REAL NOT NULL,
                    power REAL NOT NULL,
                    system_status TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
