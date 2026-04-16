"""
db.py — 資料庫連線與初始化工具

提供統一的資料庫連線管理，以及根據 schema.sql 初始化資料表的功能。
所有 Model 都透過此模組取得資料庫連線。
"""

import sqlite3
import os

# 資料庫檔案路徑（位於專案根目錄的 instance/ 資料夾）
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')
SEED_PATH = os.path.join(BASE_DIR, 'database', 'seed.sql')


def get_connection():
    """
    取得 SQLite 資料庫連線。

    回傳的連線物件已設定：
    - row_factory = sqlite3.Row（讓查詢結果可以用欄位名稱存取）
    - 啟用外部鍵約束（PRAGMA foreign_keys = ON）

    Returns:
        sqlite3.Connection: 資料庫連線物件
    """
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果可以用欄位名稱存取
    conn.execute('PRAGMA foreign_keys = ON')  # 啟用外部鍵
    return conn


def init_db():
    """
    初始化資料庫：執行 schema.sql 建立所有資料表。

    如果資料表已存在（使用 IF NOT EXISTS），不會重複建立。
    """
    conn = get_connection()
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        print('✅ 資料庫初始化完成')
    finally:
        conn.close()


def seed_db():
    """
    匯入種子資料：執行 seed.sql 填充籤詩與塔羅牌的初始資料。

    僅在資料表為空時才匯入（避免重複匯入）。
    """
    if not os.path.exists(SEED_PATH):
        print('⚠️ seed.sql 尚未建立，跳過種子資料匯入')
        return

    conn = get_connection()
    try:
        # 檢查是否已有資料
        poem_count = conn.execute('SELECT COUNT(*) FROM poems').fetchone()[0]
        if poem_count > 0:
            print('ℹ️ 資料庫已有資料，跳過種子資料匯入')
            return

        with open(SEED_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        print('✅ 種子資料匯入完成')
    finally:
        conn.close()


def close_connection(conn):
    """
    關閉資料庫連線。

    Args:
        conn (sqlite3.Connection): 要關閉的連線物件
    """
    if conn:
        conn.close()
