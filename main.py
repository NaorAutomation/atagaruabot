import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from bot import DiscordBot
import uvicorn
import json
import os
from pathlib import Path

# יצירת אפליקציית FastAPI
app = FastAPI()

# הגדרת CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# הגדרת תיקיות
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# יצירת הבוט
bot = DiscordBot()

# רשימת חיבורי WebSocket פעילים
active_connections = []

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        active_connections.remove(websocket)

async def broadcast_log(message: str):
    """שליחת לוג לכל הלקוחות המחוברים"""
    for connection in active_connections:
        try:
            await connection.send_json({
                "type": "log",
                "message": message
            })
        except:
            active_connections.remove(connection)

async def broadcast_stats(stats: dict):
    """שליחת סטטיסטיקות לכל הלקוחות המחוברים"""
    for connection in active_connections:
        try:
            await connection.send_json({
                "type": "stats",
                **stats
            })
        except:
            active_connections.remove(connection)

# הוספת הפונקציות לבוט
bot.broadcast_log = broadcast_log
bot.broadcast_stats = broadcast_stats

async def start_bot():
    """הפעלת הבוט והשרת"""
    # הפעלת הבוט
    await bot.start()

if __name__ == "__main__":
    # יצירת Event Loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # הפעלת הבוט בתהליך נפרד
    loop.create_task(start_bot())
    
    # הפעלת שרת הווב
    port = int(os.getenv("PORT", 8000))
    config = uvicorn.Config(app, host="localhost", port=port, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve()) 