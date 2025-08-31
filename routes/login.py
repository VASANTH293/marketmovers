from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from database import db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    user = await db["users"].find_one({"username": username})

    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "❌ Invalid username"})
    
    if not bcrypt.verify(password, user["password"]):
        return templates.TemplateResponse("login.html", {"request": request, "error": "❌ Incorrect password"})

    message = "Login successful!"
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": message})
