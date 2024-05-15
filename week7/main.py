from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from urllib.parse import quote
import os
import mysql.connector


class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response


class UpdateNameRequest(BaseModel):
    name: str


def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="website"
    )
    cursor = db.cursor()
    return db, cursor


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
    name = request.session.get("name", "unknown user")
    _, cursor = get_db()
    cursor.execute("""
    SELECT message.id, message.content, member.name, member.id
    FROM message
    JOIN member ON message.member_id = member.id
    ORDER BY message.time DESC
    """)
    messages = cursor.fetchall()
    cursor.close()
    return templates.TemplateResponse("member.html", {"request": request, "name": name, "messages": messages, "current_member_id": request.session.get("id")})


# 查詢會員功能
@app.get("/api/member")
async def member_query(request: Request, username: str = " "):
    # 排除 非登入狀態
    if 'signed_in' not in request.session or not request.session['signed_in']:
        return {"data": None}
    # 排除  欄位無輸入or輸入空值情形
    if username is None or username == " ":
        return {"data": None}
    # 實際進入資料庫
    else:
        _, cursor = get_db()
        cursor.execute("SELECT * FROM member WHERE username = %s", (username,))
        member = cursor.fetchone()
        cursor.close()
        if member is None:
            return {"data": None}
        else:
            return {"data": {"id": member[0], "name": member[1], "username": member[2]}}


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
    user = cursor.fetchone()
    if user:
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


# 更新姓名功能
@app.patch("/api/member")
async def update_member_name(request: Request, update_name_request: UpdateNameRequest):
    # 排除 非登入狀態
    if 'signed_in' not in request.session or not request.session['signed_in']:
        return {"error": True}
    # 排除  無紀錄會員id狀態(以免 對不存在會員操作而浪費資料庫操作次數)
    member_id = request.session.get("id")
    if member_id is None:
        return {"error": True}
    # 實際進入資料庫
    new_name = update_name_request.name
    try:  # 對有紀錄id狀態的特定會員 更新姓名的值
        db, cursor = get_db()
        cursor.execute("UPDATE member SET name = %s WHERE id = %s", (new_name, member_id))
        db.commit()
        success = cursor.rowcount == 1  # 確認更新: 用rowcount，確認上個執行SQL指令造成影響的行數(update指令無返回紀錄)  (fetchone搭配SQL查詢指令，會返回紀錄)
        cursor.close()
    except Exception as e:
        print(e)
        success = False
    # 寫在異常處理區塊(多為處理資料庫操作)後面
    if success:
        request.session["name"] = new_name
        return {"ok": True}
    else:
        return {"error": True}
