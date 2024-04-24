from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from urllib.parse import quote
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import HTMLResponse, RedirectResponse


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

#登出狀態時，不可只用成功頁面URL進入操作  #全改成狀態碼303更一致
async def verify_login(request: Request):
    if not "signed_in" in request.session or not request.session["signed_in"]:
        return RedirectResponse(url="/", status_code=303)
    return


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
#跳轉新的子頁面(驗證時為post請求，依驗證結果再get請求到新頁面)
@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request, message: str = None):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})
    #登入後，管理會員狀態
@app.get("/member", response_class=HTMLResponse)
async def member_page(request: Request):
    if 'signed_in' not in request.session or not request.session['signed_in']:
        return RedirectResponse(url="/", status_code=303)
    response = templates.TemplateResponse("member.html", {"request": request})
    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/signout")
async def signout(request: Request):
    request.session["signed_in"] = False
    response = RedirectResponse(url="/", status_code=303)
    response.headers["Cache-Control"] = "no-store"
    return response


#改成非json格式，以免驗證後URL無法正確重導向子頁面+修改狀態碼
@app.post("/signin")
async def verify_user(request: Request, username: str = Form(None), password: str = Form(None)):
    if not username or not password:
        message = quote("請輸入帳號、密碼")
        return RedirectResponse(url=f"/error?message={message}", status_code=303)
    if username == "test" and password == "test":
        request.session["signed_in"] = True
        return RedirectResponse(url="/member", status_code=303)
    else:
        message = quote("帳號、密碼輸入錯誤")
        return RedirectResponse(url=f"/error?message={message}", status_code=303)
