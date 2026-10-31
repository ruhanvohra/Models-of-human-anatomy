"""
Knowledge Base Builder.
Parses TA2.csv and seeds verified biomechanics, innervations, and clinical cases
into a unified SQLite database: anatomy_kb.db.
"""

import os
import sqlite3
import json
from .seed_data import VERIFIED_ACTIONS, VERIFIED_INNERVATIONS, VERIFIED_CLINICAL_CASES

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "anatomy_kb.db")
DEFAULT_TA2_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "TA2.csv")


def init_database(db_path=DEFAULT_DB_PATH):
    """Creates the schema for verified anatomical facts."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS structures (
        ta2_id INTEGER PRIMARY KEY,
        english_name TEXT NOT NULL,
        latin_name TEXT,
        french_name TEXT,
        spanish_name TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        muscle_name TEXT NOT NULL,
        action TEXT NOT NULL,
        joint TEXT NOT NULL,
        phase_degrees TEXT,
        role TEXT,
        notes TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS innervations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        muscle_name TEXT NOT NULL,
        nerve_name TEXT NOT NULL,
        spinal_roots TEXT NOT NULL,
        source_plexus TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clinical_cases (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        scenario TEXT NOT NULL,
        target_structure TEXT NOT NULL,
        target_nerve TEXT,
        spinal_roots TEXT,
        question TEXT NOT NULL,
        options_json TEXT NOT NULL,
        correct_index INTEGER NOT NULL,
        explanation TEXT NOT NULL
    )
    """)

    # Indices for high-speed lookup
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_struct_en ON structures(english_name COLLATE NOCASE)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_struct_la ON structures(latin_name COLLATE NOCASE)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_action_act ON actions(action COLLATE NOCASE)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_action_muscle ON actions(muscle_name COLLATE NOCASE)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_innerv_muscle ON innervations(muscle_name COLLATE NOCASE)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_innerv_nerve ON innervations(nerve_name COLLATE NOCASE)")

    conn.commit()
    return conn


def populate_ta2(conn, ta2_path=DEFAULT_TA2_PATH):
    """Parses TA2.csv and populates the structures table."""
    if not os.path.exists(ta2_path):
        print(f"[KB Builder] Warning: TA2.csv not found at {ta2_path}")
        return

    cursor = conn.cursor()
    cursor.execute("DELETE FROM structures")

    count = 0
    with open(ta2_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            parts = line.split(";")
            if not parts or not parts[0].isdigit():
                continue

            ta2_id = int(parts[0])
            english = parts[1].strip() if len(parts) > 1 else ""
            latin = parts[2].strip() if len(parts) > 2 else ""
            french = parts[3].strip() if len(parts) > 3 else ""
            spanish = parts[4].strip() if len(parts) > 4 else ""

            cursor.execute("""
            INSERT OR REPLACE INTO structures (ta2_id, english_name, latin_name, french_name, spanish_name)
            VALUES (?, ?, ?, ?, ?)
            """, (ta2_id, english, latin, french, spanish))
            count += 1

    conn.commit()
    print(f"[KB Builder] Populated {count} anatomical structures from TA2.csv")


def populate_verified_relations(conn):
    """Populates biomechanical actions, innervations, and clinical cases."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM actions")
    cursor.execute("DELETE FROM innervations")
    cursor.execute("DELETE FROM clinical_cases")

    # Insert verified actions
    for item in VERIFIED_ACTIONS:
        cursor.execute("""
        INSERT INTO actions (muscle_name, action, joint, phase_degrees, role, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, item)

    # Insert verified innervations
    for item in VERIFIED_INNERVATIONS:
        cursor.execute("""
        INSERT INTO innervations (muscle_name, nerve_name, spinal_roots, source_plexus)
        VALUES (?, ?, ?, ?)
        """, item)

    # Insert verified clinical cases
    for case in VERIFIED_CLINICAL_CASES:
        cursor.execute("""
        INSERT INTO clinical_cases (id, title, scenario, target_structure, target_nerve, spinal_roots, question, options_json, correct_index, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case["id"],
            case["title"],
            case["scenario"],
            case["target_structure"],
            case.get("target_nerve", ""),
            case.get("spinal_roots", ""),
            case["question"],
            json.dumps(case["options"]),
            case["correct_index"],
            case["explanation"]
        ))

    conn.commit()
    print(f"[KB Builder] Populated {len(VERIFIED_ACTIONS)} actions, {len(VERIFIED_INNERVATIONS)} innervations, {len(VERIFIED_CLINICAL_CASES)} clinical cases.")


def build_knowledge_base(db_path=DEFAULT_DB_PATH, ta2_path=DEFAULT_TA2_PATH):
    """Main build function to generate the knowledge base."""
    conn = init_database(db_path)
    populate_ta2(conn, ta2_path)
    populate_verified_relations(conn)
    conn.close()
    print(f"[KB Builder] Knowledge base ready at: {db_path}")


if __name__ == "__main__":
    build_knowledge_base()

