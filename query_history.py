import sqlite3


DB_NAME = "database.db"


def create_history_table():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            sql TEXT NOT NULL,
            corrected INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_query(question, sql, corrected):

    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO query_history
        (question, sql, corrected)
        VALUES (?, ?, ?)
        """,
        (question, sql, int(corrected))
    )

    conn.commit()
    conn.close()


def get_query_history():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        """
        SELECT question, sql, corrected, created_at
        FROM query_history
        ORDER BY id DESC
        """
    )

    history = cursor.fetchall()

    conn.close()

    return history

def clear_query_history():

    conn = sqlite3.connect(DB_NAME)

    conn.execute("DELETE FROM query_history")

    conn.commit()
    conn.close()