-- ============================================
-- 線上算命系統 — SQLite 資料庫建表語法
-- 建立日期：2026-04-16
-- 對應文件：docs/DB_DESIGN.md
-- ============================================

-- 啟用外部鍵約束（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- ============================================
-- 1. users — 使用者資料表
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT    NOT NULL UNIQUE,
    password_hash  TEXT    NOT NULL,
    created_at     TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ============================================
-- 2. poems — 籤詩資料表
-- ============================================
CREATE TABLE IF NOT EXISTS poems (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category        TEXT    NOT NULL CHECK (category IN ('事業', '感情', '學業', '健康', '財運')),
    level           TEXT    NOT NULL CHECK (level IN ('上上籤', '上籤', '中籤', '下籤', '下下籤')),
    title           TEXT    NOT NULL,
    poem_text       TEXT    NOT NULL,
    interpretation  TEXT    NOT NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ============================================
-- 3. tarot_cards — 塔羅牌資料表
-- ============================================
CREATE TABLE IF NOT EXISTS tarot_cards (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    name                  TEXT    NOT NULL,
    image_url             TEXT,
    upright_meaning       TEXT    NOT NULL,
    reversed_meaning      TEXT    NOT NULL,
    upright_description   TEXT    NOT NULL,
    reversed_description  TEXT    NOT NULL,
    created_at            TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ============================================
-- 4. fortunes — 算命結果資料表
-- ============================================
CREATE TABLE IF NOT EXISTS fortunes (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER,
    type             TEXT    NOT NULL CHECK (type IN ('draw', 'tarot')),
    category         TEXT,
    question         TEXT,
    poem_id          INTEGER,
    tarot_cards_json TEXT,
    result_summary   TEXT,
    share_token      TEXT    UNIQUE,
    created_at       TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),

    FOREIGN KEY (user_id) REFERENCES users(id)  ON DELETE SET NULL,
    FOREIGN KEY (poem_id) REFERENCES poems(id)   ON DELETE SET NULL
);

-- ============================================
-- 5. donations — 捐獻紀錄資料表
-- ============================================
CREATE TABLE IF NOT EXISTS donations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    amount        INTEGER NOT NULL CHECK (amount > 0),
    wish          TEXT,
    is_anonymous  INTEGER NOT NULL DEFAULT 0 CHECK (is_anonymous IN (0, 1)),
    created_at    TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================
-- 建立索引
-- ============================================
CREATE INDEX IF NOT EXISTS idx_fortunes_user_id    ON fortunes(user_id);
CREATE INDEX IF NOT EXISTS idx_fortunes_type       ON fortunes(type);
CREATE INDEX IF NOT EXISTS idx_fortunes_share_token ON fortunes(share_token);
CREATE INDEX IF NOT EXISTS idx_donations_user_id   ON donations(user_id);
CREATE INDEX IF NOT EXISTS idx_poems_category      ON poems(category);
