from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import discord
import asyncio
import os
from bot import bot

app = FastAPI()

# הגדרת תיקיות סטטיות ותבניות
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "env": {
            "VERCEL": os.getenv("VERCEL"),
            "PYTHONPATH": os.getenv("PYTHONPATH")
        }
    }

@app.on_event("startup")
async def startup_event():
    try:
        if os.getenv("VERCEL") != "1":  # רק אם לא על Vercel
            asyncio.create_task(bot.start())
    except Exception as e:
        print(f"Error starting bot: {e}") 
