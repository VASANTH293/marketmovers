from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routes import home, signup
from routes.login import router as login_router
import os
import uvicorn
from dotenv import load_dotenv
import requests

# Step 1: Load environment variables from .env early in the file
load_dotenv()

# Step 2: Get the API URL from environment variables
api_url = os.getenv("API_URL")
print("Your API URL is:", api_url)

# Step 3: Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Step 4: Include routers
app.include_router(login_router)
app.include_router(home.router)
app.include_router(signup.router)

# Step 5: Example of using the api_url inside an endpoint
@app.post("/login")
async def login(request: Request):
    # Here you can use the api_url to make requests if needed
    # Example: call some API endpoint before rendering dashboard
    # response = requests.get(f"{api_url}/api/some-data")
    # data = response.json()

    message = "Login successful!"
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": message})

# Step 6: Run the app with uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Port from environment or default 10000
    uvicorn.run(app, host="0.0.0.0", port=port)
