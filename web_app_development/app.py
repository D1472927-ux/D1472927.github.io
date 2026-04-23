"""
app.py — 應用程式入口點（啟動 Flask 伺服器）

使用方式：
    開發模式：python app.py
    或者：flask run

此檔案呼叫 create_app() 工廠函式來建立 Flask 應用程式。
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
