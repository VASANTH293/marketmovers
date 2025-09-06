# register.py

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import get_submissions_collection  # Your MongoDB logic

templates = Jinja2Templates(directory="templates")
router = APIRouter()  # ✅ Only define router here

@router.get("/ReachUs", response_class=HTMLResponse)
async def reachus(request: Request):
    return templates.TemplateResponse("ReachUs.html", {"request": request})

@router.post("/submit")
async def submit(
    name: str = Form(...),
    phone: str = Form(...),
    whatsapp: str = Form(""),
    insurance: str = Form(...),
    mutualfund: str = Form(...),
    stockresearch: str = Form(...),
    expertcall: str = Form(...)
):
    submissions = get_submissions_collection()
    doc = {
        "name": name,
        "phone": phone,
        "whatsapp": whatsapp,
        "insurance": insurance,
        "mutualfund": mutualfund,
        "stockresearch": stockresearch,
        "expertcall": expertcall
    }
    await submissions.insert_one(doc)
    return RedirectResponse("/thankyou", status_code=303)

@router.get("/thankyou", response_class=HTMLResponse)
async def thankyou(request: Request):
    return templates.TemplateResponse("thankyou.html", {"request": request})
