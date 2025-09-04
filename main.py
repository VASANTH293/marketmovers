from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routes import home, signup
from routes.login import router as login_router
import os
import uvicorn

import requests
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.include_router(login_router)

@app.post("/login")
async def login(request: Request):
    # ...your login logic here...
    message = "Login successful!"
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": message})

# include routers
app.include_router(home.router)
app.include_router(signup.router)


if __name__ == "__main__":
        port = int(os.environ.get("PORT", 10000)) # Use environment variable for port
        uvicorn.run(app, host="0.0.0.0",port=port)
