import re
import sqlite3

DB_NAME = "network_agent.db"
HISTORY_CANDIDATE_LIMIT = 50
DEFAULT_HISTORY_LIMIT = 3
DEFAULT_HISTORY_MAX_CHARS = 6000


def _terms(text):
    return set(re.findall(r"[a-z0-9][a-z0-9_.:/-]{2,}", text.casefold()))


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

def get_recent_incidents(limit=5):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, date_created
        FROM incidents
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_relevant_incidents(
    network_input,
    limit=DEFAULT_HISTORY_LIMIT,
    max_chars=DEFAULT_HISTORY_MAX_CHARS,
):
    if limit < 1:
        raise ValueError("limit must be at least 1")
    if max_chars < 1:
        raise ValueError("max_chars must be at least 1")

    input_terms = _terms(network_input)
    if not input_terms:
        return "No relevant previous incidents."

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, date_created, network_input, analysis
        FROM incidents
        ORDER BY id DESC
        LIMIT ?
        """,
        (HISTORY_CANDIDATE_LIMIT,)
    )
    incidents = cursor.fetchall()
    conn.close()

    scored_incidents = []
    for incident in incidents:
        incident_terms = _terms(f"{incident[2]} {incident[3]}")
        score = len(input_terms & incident_terms)
        if score:
            scored_incidents.append((score, incident))

    scored_incidents.sort(key=lambda item: (-item[0], -item[1][0]))

    sections = []
    remaining_chars = max_chars
    for _, incident in scored_incidents[:limit]:
        incident_id, date_created, incident_input, analysis = incident
        section = (
            f"Incident {incident_id} ({date_created})\n"
            f"Input: {incident_input}\n"
            f"Analysis: {analysis}"
        )
        if len(section) > remaining_chars:
            if not sections and remaining_chars > 3:
                sections.append(section[:remaining_chars - 3] + "...")
            break
        sections.append(section)
        remaining_chars -= len(section) + 2
        if remaining_chars <= 0:
            break

    if not sections:
        return "No relevant previous incidents."

    return "\n\n".join(sections)