import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from bot import DiscordBot
import uvicorn
import os

# יצירת אפליקציית FastAPI
app = FastAPI()

# הגדרת תיקיות
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

async def start_server():
    """הפעלת השרת והבוט"""
    # הפעלת הבוט
    await bot.start()

def run():
    """פונקציית הפעלה ראשית"""
    port = int(os.getenv("PORT", 8000))
    
    # יצירת event loop חדש
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # הפעלת הבוט בתהליך נפרד
    loop.create_task(start_server())
    
    # בדיקה אם אנחנו בסביבת פיתוח או בענן
    host = "localhost" if os.getenv("VERCEL") is None else "0.0.0.0"
    
    # הפעלת השרת
    config = uvicorn.Config(app=app, host=host, port=port, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())

if __name__ == "__main__":
    run() 
