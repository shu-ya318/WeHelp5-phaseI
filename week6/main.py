from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from urllib.parse import quote
import os
import mysql.connector


# 密碼設定安全機制
def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="website"
    )
    cursor = db.cursor()
    return db, cursor


class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.add_middleware(CacheControlMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request, message: str = " "):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})


@app.get("/member", response_class=HTMLResponse)
async def member_page(request: Request):
    if 'signed_in' not in request.session or not request.session['signed_in']:
        return RedirectResponse(url="/", status_code=303)
    name = request.session.get("name", "unknown user")  # 設定預設值，考量name意外地沒紀錄在session情形
    _, cursor = get_db()                                # 沒使用返回的db變數
    cursor.execute("""
    SELECT message.id, message.content, member.name, member.id
    FROM message
    JOIN member ON message.member_id = member.id
    ORDER BY message.time DESC
    """)
    messages = cursor.fetchall()
    cursor.close()
    return templates.TemplateResponse("member.html", {"request": request, "name": name, "messages": messages})

# 登出後，清除所有用戶狀態(含 變更登入狀態) ，以防被駭客偽裝身分登入etc安全性問題
@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    request.session["signed_in"] = False
    return RedirectResponse(url="/", status_code=303)


@app.post("/signup")
async def register_user(request: Request, name: str = Form(...), username: str = Form(...), password: str = Form(...)):
    db, cursor = get_db()
    cursor.execute("SELECT * FROM member WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        message = quote("帳號已經被註冊")
        cursor.close()
        return RedirectResponse(url=f"/error?message={message}", status_code=303)
    cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
    db.commit()
    cursor.close()
    return RedirectResponse(url="/", status_code=303)


@app.post("/signin")
async def verify_user(request: Request, username: str = Form(...), password: str = Form(...)):
    _, cursor = get_db()
    cursor.execute("SELECT * FROM member WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()   # 只需找到第一個匹配資料
    if user:  # 代表資料庫有資料，把用戶狀態 (連同登入狀態 更新)存在session
        request.session["id"] = user[0]
        request.session["name"] = user[1]
        request.session["username"] = username
        request.session["signed_in"] = True
        return RedirectResponse(url="/member", status_code=303)
    else:
        message = quote("帳號、密碼輸入錯誤")
        return RedirectResponse(url=f"/error?message={message}", status_code=303)


@app.post("/createMessage")
async def create_message(request: Request, content: str = Form(...)):
    if 'signed_in' not in request.session or not request.session['signed_in']:
        return RedirectResponse(url="/", status_code=303)
    db, cursor = get_db()
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (request.session["id"], content))
    db.commit()
    return RedirectResponse(url="/member", status_code=303)


@app.post("/deleteMessage")
async def delete_message(request: Request, message_id: int = Form(...)):
    if 'signed_in' not in request.session or not request.session['signed_in']:
        return RedirectResponse(url="/", status_code=303)
    db, cursor = get_db()
    cursor.execute("SELECT member_id FROM message WHERE id = %s", (message_id,))
    message = cursor.fetchone()
    if not message or message[0] != request.session["id"]:
        raise HTTPException(status_code=403, detail="Permission denied")

    cursor.execute("DELETE FROM message WHERE id = %s AND member_id = %s", (message_id, request.session["id"]))
    db.commit()
    return RedirectResponse(url="/member", status_code=303)
