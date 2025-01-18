import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from bot import DiscordBot
import uvicorn
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

# הגדרת נתיבים לתיקיות
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# הגדרת תבניות וקבצים סטטיים
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# יצירת הבוט
bot = DiscordBot()

# רשימת חיבורי WebSocket פעילים
active_connections = []

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)

@app.get("/health")
async def health_check():
    """נקודת קצה לבדיקת תקינות"""
    return {"status": "healthy", "templates_dir": str(TEMPLATES_DIR), "static_dir": str(STATIC_DIR)}

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

if __name__ == "__main__":
    # הפעלת הבוט בתהליך נפרד
    asyncio.create_task(bot.start())
    
    # הפעלת שרת הווב
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
