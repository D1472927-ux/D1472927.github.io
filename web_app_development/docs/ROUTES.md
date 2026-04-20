# 路由設計 — 線上算命系統

> **文件版本：** v1.0
> **建立日期：** 2026-04-16
> **對應文件：** [PRD.md](./PRD.md) ｜ [ARCHITECTURE.md](./ARCHITECTURE.md) ｜ [DB_DESIGN.md](./DB_DESIGN.md) ｜ [FLOWCHART.md](./FLOWCHART.md)

---

## 1. 路由總覽表格

### 1.1 首頁與每日運勢（`main.py`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 需登入 | 說明 |
|------|-----------|---------|----------|--------|------|
| 首頁 | GET | `/` | `index.html` | ❌ | 系統入口，展示功能選單與今日運勢摘要 |
| 每日運勢 | GET | `/fortune` | `fortune/daily.html` | ❌ | 顯示今日運勢（整體、愛情、事業、財運） |

---

### 1.2 使用者帳號（`auth.py`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 需登入 | 說明 |
|------|-----------|---------|----------|--------|------|
| 註冊頁面 | GET | `/register` | `auth/register.html` | ❌ | 顯示註冊表單 |
| 註冊處理 | POST | `/register` | — | ❌ | 接收表單，建立使用者，重導向至登入頁 |
| 登入頁面 | GET | `/login` | `auth/login.html` | ❌ | 顯示登入表單 |
| 登入處理 | POST | `/login` | — | ❌ | 驗證帳密，建立 Session，重導向至首頁 |
| 登出 | GET | `/logout` | — | ✅ | 清除 Session，重導向至首頁 |
| 個人中心 | GET | `/profile` | `profile/index.html` | ✅ | 顯示個人資訊與統計數據 |

---

### 1.3 抽籤求籤（`draw.py`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 需登入 | 說明 |
|------|-----------|---------|----------|--------|------|
| 抽籤頁面 | GET | `/draw` | `draw/index.html` | ❌ | 選擇類別、輸入問題 |
| 抽籤處理 | POST | `/draw` | — | ❌ | 隨機抽籤，儲存結果，重導向至結果頁 |
| 籤詩結果 | GET | `/draw/result/<id>` | `draw/result.html` | ❌ | 顯示籤詩結果與解釋 |

---

### 1.4 塔羅占卜（`tarot.py`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 需登入 | 說明 |
|------|-----------|---------|----------|--------|------|
| 塔羅占卜頁面 | GET | `/tarot` | `tarot/index.html` | ❌ | 選擇占卜主題 |
| 塔羅占卜處理 | POST | `/tarot` | — | ❌ | 隨機翻牌，儲存結果，重導向至結果頁 |
| 塔羅結果 | GET | `/tarot/result/<id>` | `tarot/result.html` | ❌ | 顯示塔羅牌義與解讀 |

---

### 1.5 歷史紀錄（`history.py`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 需登入 | 說明 |
|------|-----------|---------|----------|--------|------|
| 歷史紀錄列表 | GET | `/history` | `history/index.html` | ✅ | 顯示算命歷史紀錄（支援篩選） |
| 刪除紀錄 | POST | `/history/delete/<id>` | — | ✅ | 刪除指定紀錄，重導向至歷史紀錄頁 |

---

### 1.6 捐獻香油錢（`donate.py`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 需登入 | 說明 |
|------|-----------|---------|----------|--------|------|
| 捐獻頁面 | GET | `/donate` | `donate/index.html` | ✅ | 顯示捐獻表單（金額選擇、祈願） |
| 捐獻處理 | POST | `/donate` | — | ✅ | 記錄捐獻，重導向至感謝頁 |
| 感謝頁面 | GET | `/donate/thanks/<id>` | `donate/thanks.html` | ✅ | 顯示捐獻感謝訊息與摘要 |
| 捐獻紀錄 | GET | `/donate/history` | `donate/history.html` | ✅ | 顯示個人捐獻紀錄 |

---

### 1.7 分享功能（`share.py`）

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 需登入 | 說明 |
|------|-----------|---------|----------|--------|------|
| 分享結果頁 | GET | `/share/<token>` | `share/result.html` | ❌ | 公開的籤詩分享頁面（卡片格式） |

---

## 2. 每個路由的詳細說明

### 2.1 首頁與每日運勢

#### `GET /` — 首頁

- **輸入：** 無
- **處理邏輯：**
  1. 產生今日運勢摘要（根據日期 seed 產生固定的每日數值）
  2. 渲染首頁模板
- **輸出：** 渲染 `index.html`，傳遞 `daily_summary` 資料
- **錯誤處理：** 無特殊處理

#### `GET /fortune` — 每日運勢

- **輸入：** 無
- **處理邏輯：**
  1. 以今天日期為種子，產生各面向運勢（整體、愛情、事業、財運，各 1~5 星）
  2. 產生幸運色與幸運數字
- **輸出：** 渲染 `fortune/daily.html`，傳遞完整運勢資料
- **錯誤處理：** 無特殊處理

---

### 2.2 使用者帳號

#### `GET /register` — 註冊頁面

- **輸入：** 無
- **處理邏輯：** 若已登入則重導向至首頁
- **輸出：** 渲染 `auth/register.html`
- **錯誤處理：** 無

#### `POST /register` — 註冊處理

- **輸入（表單欄位）：**
  - `username`（必填，文字）
  - `password`（必填，文字）
  - `password_confirm`（必填，文字）
- **處理邏輯：**
  1. 驗證欄位非空
  2. 驗證 `password` 與 `password_confirm` 一致
  3. 呼叫 `user.get_by_username(username)` 檢查帳號是否已存在
  4. 呼叫 `user.create(username, password)` 建立使用者
- **輸出：** 成功 → 重導向至 `/login`，顯示 flash 訊息「註冊成功，請登入」
- **錯誤處理：**
  - 欄位驗證失敗 → 重新渲染表單，顯示錯誤訊息
  - 帳號已存在 → 重新渲染表單，顯示「帳號已被使用」

#### `GET /login` — 登入頁面

- **輸入：** 無
- **處理邏輯：** 若已登入則重導向至首頁
- **輸出：** 渲染 `auth/login.html`
- **錯誤處理：** 無

#### `POST /login` — 登入處理

- **輸入（表單欄位）：**
  - `username`（必填）
  - `password`（必填）
- **處理邏輯：**
  1. 呼叫 `user.verify_password(username, password)` 驗證
  2. 驗證成功 → 設定 `session['user_id']` 與 `session['username']`
- **輸出：** 成功 → 重導向至首頁
- **錯誤處理：** 帳號或密碼錯誤 → 重新渲染登入頁，顯示「帳號或密碼錯誤」

#### `GET /logout` — 登出

- **輸入：** 無
- **處理邏輯：** 清除 session（`session.clear()`）
- **輸出：** 重導向至首頁
- **錯誤處理：** 無

#### `GET /profile` — 個人中心

- **輸入：** 無（從 session 取得 `user_id`）
- **處理邏輯：**
  1. 呼叫 `user.get_by_id(user_id)` 取得個人資訊
  2. 呼叫 `user.get_stats(user_id)` 取得統計資料
- **輸出：** 渲染 `profile/index.html`，傳遞 `user` 與 `stats` 資料
- **錯誤處理：** 未登入 → 重導向至 `/login`

---

### 2.3 抽籤求籤

#### `GET /draw` — 抽籤頁面

- **輸入：** 無
- **處理邏輯：**
  1. 呼叫 `poem.get_categories()` 取得可用類別
- **輸出：** 渲染 `draw/index.html`，傳遞 `categories` 清單
- **錯誤處理：** 無

#### `POST /draw` — 抽籤處理

- **輸入（表單欄位）：**
  - `category`（必填，選擇欄位）
  - `question`（選填，文字）
- **處理邏輯：**
  1. 呼叫 `poem.get_random(category)` 隨機取得籤詩
  2. 呼叫 `fortune.create(type='draw', category, question, poem_id, user_id)` 儲存結果
     - `user_id` 從 session 取得，未登入時為 None
  3. 組合 `result_summary`（如「上籤 — 龍飛九天」）
- **輸出：** 重導向至 `/draw/result/<fortune_id>`
- **錯誤處理：** 無籤詩資料 → 顯示錯誤訊息

#### `GET /draw/result/<id>` — 籤詩結果

- **輸入：** URL 參數 `id`（fortune ID）
- **處理邏輯：**
  1. 呼叫 `fortune.get_by_id(id)` 取得結果（含 JOIN 籤詩資料）
- **輸出：** 渲染 `draw/result.html`，傳遞完整籤詩結果
- **錯誤處理：** 紀錄不存在 → 回傳 404

---

### 2.4 塔羅占卜

#### `GET /tarot` — 塔羅占卜頁面

- **輸入：** 無
- **處理邏輯：** 渲染占卜主題選擇頁
- **輸出：** 渲染 `tarot/index.html`，傳遞主題清單（今日運勢/感情問題/工作抉擇）
- **錯誤處理：** 無

#### `POST /tarot` — 塔羅占卜處理

- **輸入（表單欄位）：**
  - `topic`（必填，占卜主題）
  - `spread`（必填，牌陣類型：`single` 或 `three`）
- **處理邏輯：**
  1. 根據 `spread` 決定抽牌數量（1 或 3）
  2. 呼叫 `tarot.draw_cards(count)` 隨機抽牌
  3. 將結果序列化為 JSON
  4. 呼叫 `fortune.create(type='tarot', category=topic, tarot_cards_json=json_str, user_id)` 儲存
- **輸出：** 重導向至 `/tarot/result/<fortune_id>`
- **錯誤處理：** 無塔羅牌資料 → 顯示錯誤訊息

#### `GET /tarot/result/<id>` — 塔羅結果

- **輸入：** URL 參數 `id`（fortune ID）
- **處理邏輯：**
  1. 呼叫 `fortune.get_by_id(id)` 取得結果
  2. 呼叫 `fortune.parse_tarot_json()` 解析塔羅 JSON
  3. 對每張牌呼叫 `tarot.get_by_id()` 取得完整牌資料
- **輸出：** 渲染 `tarot/result.html`，傳遞牌陣結果
- **錯誤處理：** 紀錄不存在 → 回傳 404

---

### 2.5 歷史紀錄

#### `GET /history` — 歷史紀錄列表

- **輸入（Query 參數）：**
  - `type`（選填，篩選類型：`draw` / `tarot`）
  - `date`（選填，篩選起始日期）
- **處理邏輯：**
  1. 從 session 取得 `user_id`
  2. 呼叫 `fortune.get_by_user(user_id, type_filter, date_from)` 取得紀錄
- **輸出：** 渲染 `history/index.html`，傳遞 `records` 清單與篩選條件
- **錯誤處理：** 未登入 → 重導向至 `/login`

#### `POST /history/delete/<id>` — 刪除紀錄

- **輸入：** URL 參數 `id`（fortune ID）
- **處理邏輯：**
  1. 驗證該紀錄屬於當前使用者
  2. 呼叫 `fortune.delete(id)` 刪除
- **輸出：** 重導向至 `/history`，顯示 flash 訊息「紀錄已刪除」
- **錯誤處理：**
  - 紀錄不存在 → 回傳 404
  - 非本人紀錄 → 回傳 403

---

### 2.6 捐獻香油錢

#### `GET /donate` — 捐獻頁面

- **輸入：** 無
- **處理邏輯：** 渲染捐獻表單（預設金額 100/300/500/1000）
- **輸出：** 渲染 `donate/index.html`
- **錯誤處理：** 未登入 → 重導向至 `/login`

#### `POST /donate` — 捐獻處理

- **輸入（表單欄位）：**
  - `amount`（必填，正整數）
  - `custom_amount`（選填，自訂金額）
  - `wish`（選填，文字）
  - `is_anonymous`（選填，checkbox）
- **處理邏輯：**
  1. 決定最終金額（預設或自訂）
  2. 驗證金額為正整數
  3. 呼叫 `donation.create(user_id, amount, wish, is_anonymous)` 儲存
- **輸出：** 重導向至 `/donate/thanks/<donation_id>`
- **錯誤處理：**
  - 金額驗證失敗 → 重新渲染表單，顯示錯誤
  - 未登入 → 重導向至 `/login`

#### `GET /donate/thanks/<id>` — 感謝頁面

- **輸入：** URL 參數 `id`（donation ID）
- **處理邏輯：**
  1. 呼叫 `donation.get_by_id(id)` 取得捐獻資料
- **輸出：** 渲染 `donate/thanks.html`，傳遞捐獻摘要
- **錯誤處理：** 紀錄不存在 → 回傳 404

#### `GET /donate/history` — 捐獻紀錄

- **輸入：** 無（從 session 取得 `user_id`）
- **處理邏輯：**
  1. 呼叫 `donation.get_by_user(user_id)` 取得紀錄
  2. 呼叫 `donation.get_user_total(user_id)` 取得總額
- **輸出：** 渲染 `donate/history.html`，傳遞 `records` 與 `total`
- **錯誤處理：** 未登入 → 重導向至 `/login`

---

### 2.7 分享功能

#### `GET /share/<token>` — 分享結果頁

- **輸入：** URL 參數 `token`（share_token）
- **處理邏輯：**
  1. 呼叫 `fortune.get_by_share_token(token)` 取得結果
  2. 若為塔羅類型，解析 JSON 並取得牌資料
- **輸出：** 渲染 `share/result.html`，以卡片格式呈現
- **錯誤處理：** token 不存在 → 回傳 404

---

## 3. Jinja2 模板清單

所有模板都繼承 `base.html` 基礎模板。

```
app/templates/
├── base.html                  ← 基礎模板（header、navbar、footer、共用 CSS/JS）
├── index.html                 ← 首頁
│
├── auth/
│   ├── login.html             ← 登入頁
│   └── register.html          ← 註冊頁
│
├── draw/
│   ├── index.html             ← 抽籤主頁（選類別、輸入問題）
│   └── result.html            ← 籤詩結果頁
│
├── tarot/
│   ├── index.html             ← 塔羅占卜主頁（選主題、選牌陣）
│   └── result.html            ← 塔羅結果頁
│
├── fortune/
│   └── daily.html             ← 每日運勢頁
│
├── history/
│   └── index.html             ← 歷史紀錄頁（含篩選功能）
│
├── donate/
│   ├── index.html             ← 捐獻頁（金額選擇、祈願）
│   ├── thanks.html            ← 捐獻感謝頁
│   └── history.html           ← 捐獻紀錄頁
│
├── profile/
│   └── index.html             ← 個人中心
│
└── share/
    └── result.html            ← 分享結果頁（公開、卡片格式）
```

---

## 4. Blueprint 註冊方式

```python
# app/__init__.py 中註冊所有 Blueprint
from app.routes.main import main_bp       # url_prefix: 無
from app.routes.auth import auth_bp       # url_prefix: 無
from app.routes.draw import draw_bp       # url_prefix: /draw
from app.routes.tarot import tarot_bp     # url_prefix: /tarot
from app.routes.history import history_bp # url_prefix: /history
from app.routes.donate import donate_bp   # url_prefix: /donate
from app.routes.share import share_bp     # url_prefix: /share
```

---

## 5. 登入保護裝飾器

需要登入的路由統一使用 `login_required` 裝飾器：

```python
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

---

> 📝 **下一步：** 路由設計確認後，請進入 **階段六：程式碼實作**，使用 `/implementation` skill 逐步實作完整應用程式。
