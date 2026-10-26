import sqlite3

DB_NAME = "network_agent.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_created TEXT,
            network_input TEXT,
            analysis TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_incident(
    date_created,
    network_input,
    analysis
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents
        (
            date_created,
            network_input,
            analysis
        )
        VALUES (?, ?, ?)
    """, (
        date_created,
        network_input,
        analysis
    ))

    conn.commit()
    conn.close()


def get_all_incidents():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM incidents
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def count_incidents():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM incidents"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total