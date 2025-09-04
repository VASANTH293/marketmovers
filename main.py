from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routes import home, signup
from routes.login import router as login_router
import os
import uvicorn


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Define login route
@app.post("/login")
async def login(request: Request):
    # ...your login logic here...
    message = "Login successful!"
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": message})

# Include routers
app.include_router(login_router)
app.include_router(home.router)
app.include_router(signup.router)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
