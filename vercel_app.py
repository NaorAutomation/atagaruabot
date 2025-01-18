from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from bot import DiscordBot
import asyncio
import uvicorn

app = FastAPI()

# הגדרת תיקיות סטטיות ותבניות
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# יצירת אובייקט הבוט
bot = DiscordBot()

@app.on_event("startup")
async def startup_event():
    # הפעלת הבוט בתהליך נפרד
    asyncio.create_task(bot.start())

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "cwd": os.getcwd(),
        "files": os.listdir('.')
    }

# נקודת כניסה עבור פיתוח מקומי
if __name__ == "__main__":
    uvicorn.run("vercel_app:app", host="0.0.0.0", port=8000, reload=True) 