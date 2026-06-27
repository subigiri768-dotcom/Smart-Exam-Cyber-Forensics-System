import sqlite3
from datetime import datetime

DB_NAME = "exam_system.db"


def get_connection():
    return sqlite3.connect(DB_NAME, timeout=10, check_same_thread=False)


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- Users ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    # ---------------- Violations ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL,

            violation_type TEXT NOT NULL,

            risk_points INTEGER DEFAULT 0,

            evidence_path TEXT,

            timestamp TEXT NOT NULL

        )
    """)

    conn.commit()
    conn.close()


# -------------------------------------------------

def register_user(username, password):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(

            "INSERT INTO users(username,password) VALUES(?,?)",

            (username, password)

        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        return False


# -------------------------------------------------

def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM users WHERE username=? AND password=?",

        (username, password)

    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


# -------------------------------------------------

def add_violation(

        username,

        violation_type,

        risk_points=0,

        evidence_path=""

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO violations(

            username,

            violation_type,

            risk_points,

            evidence_path,

            timestamp

        )

        VALUES(?,?,?,?,?)

    """,

    (

        username,

        violation_type,

        risk_points,

        evidence_path,

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ))

    conn.commit()

    conn.close()


# -------------------------------------------------

def get_user_violations(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            violation_type,

            risk_points,

            evidence_path,

            timestamp

        FROM violations

        WHERE username=?

        ORDER BY timestamp ASC

    """,

    (username,))

    rows = cursor.fetchall()

    conn.close()

    violations = []

    for row in rows:

        if row[1] >= 20:

            severity = "High"

        elif row[1] >= 10:

            severity = "Medium"

        else:

            severity = "Low"

        violations.append({

            "time": row[3],

            "type": row[0],

            "severity": severity,

            "risk": row[1],

            "evidence": row[2]

        })

    return violations


# -------------------------------------------------

def get_total_risk(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT SUM(risk_points)

        FROM violations

        WHERE username=?

    """,

    (username,))

    result = cursor.fetchone()

    conn.close()

    if result and result[0]:

        return result[0]

    return 0


# -------------------------------------------------

def get_evidence(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT evidence_path

        FROM violations

        WHERE username=?

        AND evidence_path!=''

    """,

    (username,))

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]


# -------------------------------------------------

def clear_user_violations(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM violations WHERE username=?",

        (username,)

    )

    conn.commit()

    conn.close()


# -------------------------------------------------

def get_statistics(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            COUNT(*),

            SUM(risk_points)

        FROM violations

        WHERE username=?

    """,

    (username,))

    result = cursor.fetchone()

    conn.close()

    return {

        "total_violations": result[0] if result[0] else 0,

        "risk_score": result[1] if result[1] else 0

    }