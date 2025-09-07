from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routes import home, signup
from routes.signin import router as login_router
import os
import uvicorn
from routes.home import fetch_nse, fetch_bse  
from routes.ReachUs import router as ReachUs_router 

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    nse_g, nse_l = fetch_nse()
    bse_g, bse_l = fetch_bse()

    def to_html_safe(df):
        return df.to_html(index=False, classes="table table-striped", border=0) if df is not None else "<p>Data not available</p>"

    return templates.TemplateResponse("home.html", {
        "request": request,
        "nse_g": to_html_safe(nse_g),
        "nse_l": to_html_safe(nse_l),
        "bse_g": to_html_safe(bse_g),
        "bse_l": to_html_safe(bse_l),
    })


@app.post("/signin")
async def signin(request: Request):
     message = "Login successful!"
     return templates.TemplateResponse( {"request": request, "message": message})

# Include routers
app.include_router(login_router)
app.include_router(home.router)
app.include_router(signup.router)
app.include_router(ReachUs_router)
 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
