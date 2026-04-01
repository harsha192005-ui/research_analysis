"""
core/database.py
SQLite persistence — papers and analyses.
"""
import os
import sqlite3
import hashlib
import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research_papers.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist (idempotent)."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                filename    TEXT    NOT NULL,
                title       TEXT    NOT NULL,
                file_hash   TEXT    UNIQUE NOT NULL,
                content     TEXT    NOT NULL,
                word_count  INTEGER NOT NULL,
                uploaded_at TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id    INTEGER NOT NULL,
                mode        TEXT    NOT NULL,
                result      TEXT    NOT NULL,
                created_at  TEXT    NOT NULL,
                FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
            )
        """)
        conn.commit()


# ── Helpers ──────────────────────────────────────────────────────────────────

def _file_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def _now() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


# ── Papers ───────────────────────────────────────────────────────────────────

def save_paper(filename: str, title: str, content: str) -> int:
    """Insert paper; return existing id if already stored (deduplication by hash)."""
    fh = _file_hash(content)
    with get_db() as conn:
        row = conn.execute("SELECT id FROM papers WHERE file_hash=?", (fh,)).fetchone()
        if row:
            return row["id"]
        cur = conn.execute(
            "INSERT INTO papers (filename, title, file_hash, content, word_count, uploaded_at)"
            " VALUES (?,?,?,?,?,?)",
            (filename, title, fh, content, len(content.split()), _now()),
        )
        conn.commit()
        return cur.lastrowid


def get_all_papers():
    with get_db() as conn:
        return conn.execute(
            "SELECT id, filename, title, word_count, uploaded_at"
            " FROM papers ORDER BY uploaded_at DESC"
        ).fetchall()


def get_paper_by_id(paper_id: int):
    with get_db() as conn:
        return conn.execute("SELECT * FROM papers WHERE id=?", (paper_id,)).fetchone()


def delete_paper(paper_id: int) -> None:
    with get_db() as conn:
        conn.execute("DELETE FROM papers WHERE id=?", (paper_id,))
        conn.commit()


# ── Analyses ─────────────────────────────────────────────────────────────────

def save_analysis(paper_id: int, mode: str, result: str) -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT INTO analyses (paper_id, mode, result, created_at) VALUES (?,?,?,?)",
            (paper_id, mode, result, _now()),
        )
        conn.commit()


def get_analyses_for_paper(paper_id: int):
    with get_db() as conn:
        return conn.execute(
            "SELECT mode, result, created_at FROM analyses"
            " WHERE paper_id=? ORDER BY created_at DESC",
            (paper_id,),
        ).fetchall()