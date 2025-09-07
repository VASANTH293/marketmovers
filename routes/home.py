from fastapi import APIRouter, Form, Request , Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import requests
from bsedata.bse import BSE

from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_submissions_collection
import time
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# =========================
# NSE API Setup
# =========================
NSE_API = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
NSE_HOME = "https://www.nseindia.com/"

headers_nse = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": NSE_HOME,
    "Connection": "keep-alive"
 
 }

def fetch_nse():
    import time

    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds between retries

    session = requests.Session()
    for attempt in range(MAX_RETRIES):
        try:
            # Step 1: Get home page cookies
            home_res = session.get(NSE_HOME, headers=headers_nse, timeout=5)

            # Step 2: Make the actual API call
            res = session.get(NSE_API, headers=headers_nse, cookies=home_res.cookies, timeout=5)
            res.raise_for_status()

            # Step 3: Parse the JSON data
            data = res.json()
            stocks = data.get("data", [])
            if not stocks:
                raise ValueError("No stock data received.")

            # Step 4: Create DataFrame and ensure required columns
            df = pd.DataFrame(stocks)
            for col in ['symbol', 'open', 'dayHigh', 'dayLow', 'lastPrice', 'previousClose', 'pChange']:
                if col not in df.columns:
                    df[col] = 0

            df['pChange'] = pd.to_numeric(df['pChange'], errors='coerce').fillna(0)

            # Step 5: Sort gainers and losers
            gainers = df.sort_values("pChange", ascending=False).head(20)
            losers = df.sort_values("pChange", ascending=True).head(20)
            return gainers, losers

        except Exception:
            # Wait before retrying
            time.sleep(RETRY_DELAY)

    # If all retries fail:
    columns = ['symbol', 'open', 'dayHigh', 'dayLow', 'lastPrice', 'previousClose', 'pChange']
    error_row = {
        'symbol': 'NSE not available, you can refer to it later',
        'open': '', 'dayHigh': '', 'dayLow': '', 'lastPrice': '', 'previousClose': '', 'pChange': ''
    }
    error_df = pd.DataFrame([error_row])

    return error_df, error_df


def fetch_bse(retries: int = 3, delay: float = 2):
    for attempt in range(1, retries + 1):
        try:
           
            b = BSE(update_codes=True)
            gainers = pd.DataFrame(b.topGainers()).head(20)
            losers = pd.DataFrame(b.topLosers()).head(20)

            if gainers.empty or losers.empty:
                raise ValueError("BSE data not available")

            return gainers, losers

        except Exception as e:
            if attempt < retries:
                time.sleep(delay)

    # All attempts failed or data was invalid
    return None, None



# -------------------------
# Routes
# -------------------------


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


