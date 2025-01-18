from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import discord
import asyncio
import os
import sys
import traceback
from bot import bot

app = FastAPI()

print("Starting application...")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir('.')}")

# בדיקת קיום תיקיות נדרשות
if not os.path.exists('templates'):
    print("Error: templates directory not found!")
    print(f"Current path: {os.getcwd()}")
else:
    print("Templates directory found")
    print(f"Templates contents: {os.listdir('templates')}")

if not os.path.exists('static'):
    print("Error: static directory not found!")
else:
    print("Static directory found")
    print(f"Static contents: {os.listdir('static')}")

# הגדרת תיקיות סטטיות ותבניות
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    templates = Jinja2Templates(directory="templates")
    print("Successfully mounted static files and templates")
except Exception as e:
    print(f"Error mounting directories: {str(e)}")
    traceback.print_exc()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        print("Attempting to render index.html")
        response = templates.TemplateResponse("index.html", {"request": request})
        print("Successfully rendered index.html")
        return response
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc(),
                "cwd": os.getcwd(),
                "files": os.listdir('.')
            }
        )

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "env": dict(os.environ),
        "cwd": os.getcwd(),
        "files": os.listdir('.'),
        "python_version": sys.version
    }

@app.on_event("startup")
async def startup_event():
    print("Application startup...")
    try:
        if os.getenv("VERCEL") != "1":
            print("Starting bot (not on Vercel)")
            asyncio.create_task(bot.start())
        else:
            print("Running on Vercel - bot not started")
    except Exception as e:
        print(f"Error in startup: {str(e)}")
        traceback.print_exc() 
