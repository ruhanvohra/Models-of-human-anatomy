"""
Anatomical Knowledge Base Query Interface.
Provides strict, verified factual retrieval for the Gemma Professor.
"""

import os
import sqlite3
import json
import random
from typing import List, Dict, Any, Optional
from .seed_data import VERIFIED_SYSTEMS, VERIFIED_PHYSIOLOGY_PATHWAYS

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "anatomy_kb.db")


class AnatomyDatabase:
    """Thread-safe interface to the verified anatomical SQLite knowledge base."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            from .builder import build_knowledge_base
            build_knowledge_base(self.db_path)

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def find_physiology_pathway(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves specific functional mechanisms (e.g. lowering blood sugar / insulin,
        bile synthesis, gastric acid secretion) matching terms in the query.
        """
        q_lower = query.lower()
        for pathway in VERIFIED_PHYSIOLOGY_PATHWAYS:
            if any(kw in q_lower for kw in pathway["keywords"]):
                return pathway
        return None

    def get_system_info(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves verified system knowledge (e.g. respiratory, cardiovascular, digestive)
        matching keywords in the query.
        """
        q_lower = query.lower()
        for sys_key, sys_data in VERIFIED_SYSTEMS.items():
            if sys_key in q_lower or any(kw in q_lower for kw in sys_data.get("keywords", [])):
                return sys_data
        return None

    def find_muscles_by_action(self, action: str, joint: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves all verified muscles that perform the given action.
        Automatically joins with innervation data to provide comprehensive functional units.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            a.muscle_name,
            a.action,
            a.joint,
            a.phase_degrees,
            a.role,
            a.notes,
            i.nerve_name,
            i.spinal_roots,
            i.source_plexus
        FROM actions a
        LEFT JOIN innervations i ON lower(a.muscle_name) = lower(i.muscle_name)
        WHERE lower(a.action) LIKE ?
        """
        params = [f"%{action.strip().lower()}%"]
        if joint:
            query += " AND lower(a.joint) LIKE ?"
            params.append(f"%{joint.strip().lower()}%")

        query += " ORDER BY CASE a.role WHEN 'initiator' THEN 1 WHEN 'prime mover' THEN 2 WHEN 'synergist' THEN 3 ELSE 4 END"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results

    def get_structure_innervation(self, muscle_name: str) -> List[Dict[str, Any]]:
        """Retrieves verified nerve supply and spinal root segments for a muscle."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT muscle_name, nerve_name, spinal_roots, source_plexus
        FROM innervations
        WHERE lower(muscle_name) LIKE ?
        """, (f"%{muscle_name.strip().lower()}%",))

        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results

    def search_structures(self, query_str: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Searches Terminologia Anatomica (TA2) structures in English and Latin."""
        conn = self._get_connection()
        cursor = conn.cursor()

        pattern = f"%{query_str.strip()}%"
        cursor.execute("""
        SELECT ta2_id, english_name, latin_name, french_name, spanish_name
        FROM structures
        WHERE english_name LIKE ? OR latin_name LIKE ?
        LIMIT ?
        """, (pattern, pattern, limit))

        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results

    def get_clinical_case(self, case_id: Optional[str] = None, keyword: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Retrieves a verified clinical vignette for interactive testing."""
        conn = self._get_connection()
        cursor = conn.cursor()

        if case_id:
            cursor.execute("SELECT * FROM clinical_cases WHERE id = ?", (case_id,))
            row = cursor.fetchone()
        elif keyword:
            pattern = f"%{keyword.strip().lower()}%"
            cursor.execute("""
            SELECT * FROM clinical_cases
            WHERE lower(title) LIKE ? OR lower(scenario) LIKE ? OR lower(target_structure) LIKE ?
            LIMIT 1
            """, (pattern, pattern, pattern))
            row = cursor.fetchone()
            if not row:
                cursor.execute("SELECT * FROM clinical_cases")
                rows = cursor.fetchall()
                row = random.choice(rows) if rows else None
        else:
            cursor.execute("SELECT * FROM clinical_cases")
            rows = cursor.fetchall()
            row = random.choice(rows) if rows else None

        conn.close()
        if not row:
            return None

        data = dict(row)
        data["options"] = json.loads(data["options_json"])
        return data

    def resolve_mesh_candidates(self, structure_name: str) -> List[str]:
        """
        Maps a clinical/anatomical name to plausible Z-Anatomy Blender object names
        including bilateral symmetry (.l, .r) and common functional partitions.
        """
        name_clean = structure_name.strip()
        candidates = [name_clean]

        # Handle bilateral extensions
        for suffix in [".l", ".r", ".ol", ".or", ".el", ".er"]:
            candidates.append(f"{name_clean}{suffix}")

        # If name has "muscle", also check without "muscle"
        if "muscle" in name_clean.lower():
            without_m = name_clean.lower().replace(" muscle", "").strip().title()
            candidates.append(without_m)
            for suffix in [".l", ".r"]:
                candidates.append(f"{without_m}{suffix}")

        return candidates
