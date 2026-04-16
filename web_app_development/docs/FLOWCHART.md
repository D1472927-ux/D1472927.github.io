# 流程圖設計 — 線上算命系統

> **文件版本：** v1.0
> **建立日期：** 2026-04-09
> **對應文件：** [PRD.md](./PRD.md) ｜ [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 1. 使用者流程圖（User Flow）

### 1.1 整體操作流程

```mermaid
flowchart LR
    A(["🌐 使用者開啟網頁"]) --> B["首頁"]
    B --> C{"要執行什麼操作？"}

    C -->|"抽籤求籤"| D["抽籤頁"]
    C -->|"塔羅占卜"| E["塔羅占卜頁"]
    C -->|"查看今日運勢"| F["每日運勢頁"]
    C -->|"登入/註冊"| G["登入/註冊頁"]
    C -->|"捐香油錢"| H["捐獻頁"]
    C -->|"查看歷史紀錄"| I{"是否已登入？"}

    D --> D1["選擇類別"]
    D1 --> D2["輸入問題（選填）"]
    D2 --> D3["點擊抽籤"]
    D3 --> D4["顯示籤詩結果"]
    D4 --> D5{"要儲存結果？"}
    D5 -->|"是"| D6{"是否已登入？"}
    D6 -->|"是"| D7["儲存成功"]
    D6 -->|"否"| G
    D5 -->|"否"| D8["結束或再抽一次"]
    D4 --> D9["分享籤詩"]

    E --> E1["選擇占卜主題"]
    E1 --> E2["翻開塔羅牌"]
    E2 --> E3["顯示牌義結果"]
    E3 --> D5

    F --> F1["顯示今日運勢"]

    G --> G1{"有帳號？"}
    G1 -->|"有"| G2["輸入帳密登入"]
    G1 -->|"沒有"| G3["填寫註冊表單"]
    G3 --> G4["註冊成功"]
    G4 --> G2
    G2 --> G5["登入成功，返回首頁"]

    H --> H1{"是否已登入？"}
    H1 -->|"是"| H2["選擇捐獻金額"]
    H1 -->|"否"| G
    H2 --> H3["填寫祈願（選填）"]
    H3 --> H4["確認捐獻"]
    H4 --> H5["顯示感謝頁"]

    I -->|"是"| I1["歷史紀錄頁"]
    I -->|"否"| G
    I1 --> I2["篩選/瀏覽紀錄"]
```

### 1.2 抽籤（求籤）詳細流程

```mermaid
flowchart TD
    Start(["開始抽籤"]) --> S1["選擇詢問類別"]
    S1 --> S1a{"選擇哪個類別？"}
    S1a -->|"事業"| S2["輸入問題（選填）"]
    S1a -->|"感情"| S2
    S1a -->|"學業"| S2
    S1a -->|"健康"| S2
    S1a -->|"財運"| S2
    S2 --> S3["點擊「抽籤」按鈕"]
    S3 --> S4["🎴 抽籤動畫播放"]
    S4 --> S5["系統隨機選取籤詩"]
    S5 --> S6["顯示結果"]
    S6 --> S6a["籤等級：上上 / 上 / 中 / 下 / 下下"]
    S6 --> S6b["籤詩原文"]
    S6 --> S6c["白話文解釋"]
    S6 --> S7{"下一步？"}
    S7 -->|"儲存結果"| S8{"已登入？"}
    S8 -->|"是"| S9["✅ 儲存至歷史紀錄"]
    S8 -->|"否"| S10["跳轉登入頁"]
    S7 -->|"分享"| S11["產生分享連結"]
    S7 -->|"再抽一次"| S1
    S7 -->|"回首頁"| End(["結束"])
```

### 1.3 塔羅占卜詳細流程

```mermaid
flowchart TD
    Start(["開始塔羅占卜"]) --> T1["選擇占卜主題"]
    T1 --> T1a{"選擇哪個主題？"}
    T1a -->|"今日運勢"| T2["單牌占卜"]
    T1a -->|"感情問題"| T3["三牌占卜"]
    T1a -->|"工作抉擇"| T3
    T2 --> T4["點擊翻牌"]
    T3 --> T4
    T4 --> T5["🃏 翻牌動畫"]
    T5 --> T6{"正位 or 逆位？"}
    T6 -->|"正位"| T7["顯示正位牌義"]
    T6 -->|"逆位"| T8["顯示逆位牌義"]
    T7 --> T9["綜合解讀與建議"]
    T8 --> T9
    T9 --> T10{"下一步？"}
    T10 -->|"儲存"| T11["儲存至歷史紀錄"]
    T10 -->|"再占一次"| T1
    T10 -->|"回首頁"| End(["結束"])
```

### 1.4 捐獻流程

```mermaid
flowchart TD
    Start(["進入捐獻頁"]) --> C1{"是否已登入？"}
    C1 -->|"否"| C2["跳轉登入頁"]
    C2 --> C3["登入成功"]
    C3 --> C4
    C1 -->|"是"| C4["顯示捐獻頁面"]
    C4 --> C5["選擇捐獻金額"]
    C5 --> C5a{"使用預設金額？"}
    C5a -->|"是"| C6["選擇 100/300/500/1000"]
    C5a -->|"否"| C7["輸入自訂金額"]
    C6 --> C8["選擇具名或匿名"]
    C7 --> C8
    C8 --> C9["填寫祈願內容（選填）"]
    C9 --> C10["確認捐獻資訊"]
    C10 --> C11{"確認送出？"}
    C11 -->|"是"| C12["✅ 捐獻紀錄寫入資料庫"]
    C12 --> C13["顯示感謝頁面"]
    C11 -->|"取消"| C4
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 抽籤（求籤）序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(draw.py)
    participant Model as Model<br/>(poem.py / fortune.py)
    participant DB as SQLite

    User->>Browser: 進入抽籤頁面
    Browser->>Flask: GET /draw
    Flask-->>Browser: 回傳 draw/index.html

    User->>Browser: 選擇類別、輸入問題、點擊「抽籤」
    Browser->>Flask: POST /draw
    Flask->>Model: 呼叫 get_random_poem(category)
    Model->>DB: SELECT * FROM poems WHERE category=? ORDER BY RANDOM() LIMIT 1
    DB-->>Model: 回傳籤詩資料
    Model-->>Flask: 回傳籤詩物件

    alt 使用者已登入
        Flask->>Model: 呼叫 save_fortune(user_id, poem_id, question)
        Model->>DB: INSERT INTO fortunes (user_id, poem_id, question, ...)
        DB-->>Model: 儲存成功
    end

    Flask-->>Browser: 回傳 draw/result.html（含籤詩結果）
    Browser-->>User: 顯示籤詩結果頁面
```

### 2.2 使用者註冊序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(auth.py)
    participant Model as Model<br/>(user.py)
    participant DB as SQLite

    User->>Browser: 點擊「註冊」
    Browser->>Flask: GET /register
    Flask-->>Browser: 回傳 auth/register.html

    User->>Browser: 填寫帳號、密碼，點擊「送出」
    Browser->>Flask: POST /register

    Flask->>Model: 呼叫 get_user_by_username(username)
    Model->>DB: SELECT * FROM users WHERE username=?
    DB-->>Model: 回傳結果

    alt 帳號已存在
        Model-->>Flask: 回傳使用者資料
        Flask-->>Browser: 回傳錯誤訊息「帳號已被使用」
    else 帳號可用
        Model-->>Flask: 回傳 None
        Flask->>Flask: 密碼雜湊（hash）
        Flask->>Model: 呼叫 create_user(username, hashed_password)
        Model->>DB: INSERT INTO users (username, password_hash, ...)
        DB-->>Model: 儲存成功
        Model-->>Flask: 回傳新使用者 ID
        Flask-->>Browser: 重導向至登入頁，顯示「註冊成功」
    end
```

### 2.3 使用者登入序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(auth.py)
    participant Model as Model<br/>(user.py)
    participant DB as SQLite

    User->>Browser: 進入登入頁面
    Browser->>Flask: GET /login
    Flask-->>Browser: 回傳 auth/login.html

    User->>Browser: 輸入帳號密碼，點擊「登入」
    Browser->>Flask: POST /login

    Flask->>Model: 呼叫 get_user_by_username(username)
    Model->>DB: SELECT * FROM users WHERE username=?
    DB-->>Model: 回傳使用者資料

    alt 帳號不存在或密碼錯誤
        Flask-->>Browser: 回傳錯誤訊息「帳號或密碼錯誤」
    else 驗證成功
        Flask->>Flask: 建立 Session（session["user_id"] = id）
        Flask-->>Browser: 重導向至首頁
    end
```

### 2.4 捐獻序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(donate.py)
    participant Model as Model<br/>(donation.py)
    participant DB as SQLite

    User->>Browser: 進入捐獻頁面
    Browser->>Flask: GET /donate

    alt 未登入
        Flask-->>Browser: 重導向至 /login
    else 已登入
        Flask-->>Browser: 回傳 donate/index.html
    end

    User->>Browser: 選擇金額、填寫祈願、點擊「確認捐獻」
    Browser->>Flask: POST /donate
    Flask->>Model: 呼叫 create_donation(user_id, amount, wish, anonymous)
    Model->>DB: INSERT INTO donations (user_id, amount, wish, is_anonymous, ...)
    DB-->>Model: 儲存成功
    Model-->>Flask: 回傳捐獻 ID
    Flask-->>Browser: 回傳 donate/thanks.html（感謝頁）
    Browser-->>User: 顯示感謝訊息與捐獻摘要
```

### 2.5 歷史紀錄查詢序列圖

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route<br/>(history.py)
    participant Model as Model<br/>(fortune.py)
    participant DB as SQLite

    User->>Browser: 進入歷史紀錄頁
    Browser->>Flask: GET /history

    alt 未登入
        Flask-->>Browser: 重導向至 /login
    else 已登入
        Flask->>Model: 呼叫 get_fortunes_by_user(user_id)
        Model->>DB: SELECT * FROM fortunes WHERE user_id=? ORDER BY created_at DESC
        DB-->>Model: 回傳紀錄列表
        Model-->>Flask: 回傳紀錄物件列表
        Flask-->>Browser: 回傳 history/index.html（含紀錄資料）
    end

    User->>Browser: 選擇篩選條件（類型/日期）
    Browser->>Flask: GET /history?type=draw&date=2026-04-01
    Flask->>Model: 呼叫 get_fortunes_by_user(user_id, filters)
    Model->>DB: SELECT * FROM fortunes WHERE user_id=? AND type=? AND date>=?
    DB-->>Model: 回傳篩選後紀錄
    Model-->>Flask: 回傳結果
    Flask-->>Browser: 回傳更新後的頁面
```

---

## 3. 功能清單對照表

| # | 功能 | URL 路徑 | HTTP 方法 | 說明 | 需登入 |
|---|------|---------|-----------|------|--------|
| 1 | 首頁 | `/` | GET | 顯示系統入口與功能選單 | ❌ |
| 2 | 註冊頁面 | `/register` | GET | 顯示註冊表單 | ❌ |
| 3 | 註冊處理 | `/register` | POST | 處理註冊請求 | ❌ |
| 4 | 登入頁面 | `/login` | GET | 顯示登入表單 | ❌ |
| 5 | 登入處理 | `/login` | POST | 處理登入請求 | ❌ |
| 6 | 登出 | `/logout` | GET | 清除登入狀態 | ✅ |
| 7 | 抽籤頁面 | `/draw` | GET | 顯示抽籤介面（選類別） | ❌ |
| 8 | 抽籤處理 | `/draw` | POST | 隨機抽籤並回傳結果 | ❌ |
| 9 | 籤詩結果 | `/draw/result/<id>` | GET | 顯示特定籤詩結果 | ❌ |
| 10 | 塔羅占卜頁面 | `/tarot` | GET | 顯示塔羅占卜介面 | ❌ |
| 11 | 塔羅占卜處理 | `/tarot` | POST | 隨機翻牌並回傳結果 | ❌ |
| 12 | 每日運勢 | `/fortune` | GET | 顯示今日運勢 | ❌ |
| 13 | 歷史紀錄 | `/history` | GET | 顯示算命歷史紀錄 | ✅ |
| 14 | 刪除紀錄 | `/history/delete/<id>` | POST | 刪除特定紀錄 | ✅ |
| 15 | 捐獻頁面 | `/donate` | GET | 顯示捐獻表單 | ✅ |
| 16 | 捐獻處理 | `/donate` | POST | 處理捐獻請求 | ✅ |
| 17 | 捐獻紀錄 | `/donate/history` | GET | 顯示捐獻紀錄 | ✅ |
| 18 | 個人中心 | `/profile` | GET | 顯示個人資訊與統計 | ✅ |
| 19 | 分享結果 | `/share/<id>` | GET | 公開的籤詩分享頁面 | ❌ |

---

> 📝 **下一步：** 流程圖確認後，請進入 **階段四：資料庫設計**，使用 `/db-design` skill 產出資料庫設計文件。
