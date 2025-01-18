from http.server import BaseHTTPRequestHandler
from bot import DiscordBot
import os
import asyncio

bot = DiscordBot()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Discord Bot is running!'.encode())
        
        # הפעלת הבוט אם הוא עדיין לא רץ
        if not hasattr(handler, 'bot_running'):
            handler.bot_running = True
            asyncio.run(bot.start())

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Webhook received!'.encode()) 
