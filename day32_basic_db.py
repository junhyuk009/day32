# day32_basic_db.py
import os
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
SQL_DIR = Path(__file__).resolve().parent / "sql"

def execute(name, params=()):
    url = os.getenv("DATABASE_URL", '').strip()
    if not url:
        raise ValueError('DATABASE_URL 환경변수를 설정하세요.')
    sql = (SQL_DIR / name).read_text(encoding='utf-8')
    with psycopg.connect(url, connect_timeout=15, row_factory=dict_row) as conn:
        return conn.execute(sql, params).fetchall()

def save_quote(quote, request_key):
    rows = execute('basic_save.sql', (
        quote['title'],
        quote['weight'],
        quote['fee'],
        quote['version'],
        request_key,
    ))
    # 중복 요청이면 RETURNING 결과가 없으므로 None
    return rows[0]['id'] if rows else None

def list_quotes():
    return execute('basic_list.sql')