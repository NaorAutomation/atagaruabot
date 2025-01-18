import asyncio
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bot import DiscordBot
import os

# יצירת אפליקציית FastAPI
app = FastAPI()

# הגדרת תיקיות
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# יצירת הבוט
bot = DiscordBot()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """הדף הראשי"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health_check():
    """בדיקת תקינות"""
    return {
        "status": "ok",
        "env": {
            "VERCEL": os.getenv("VERCEL"),
            "PORT": os.getenv("PORT")
        }
    }

# נקודת כניסה עבור Vercel
app.bot = bot  # שמירת הבוט כמשתנה גלובלי 
