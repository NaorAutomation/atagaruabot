from flask import Flask, render_template
from app import bot
import asyncio
import threading
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', stats=bot.stats)

def run_flask():
    # Replit משתמש בפורט 8080
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run_flask)
    server.start()

def run_bot():
    asyncio.run(bot.start())

if __name__ == "__main__":
    # הפעלת שרת הווב כדי לשמור על הבוט פעיל
    keep_alive()
    
    # הפעלת הבוט
    run_bot() 
