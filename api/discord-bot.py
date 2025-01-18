from http.server import BaseHTTPRequestHandler
from bot import DiscordBot
import os
import json

# יצירת אובייקט הבוט
bot = DiscordBot()

def handler(request, response):
    """
    פונקציית Serverless של Vercel
    """
    if request.method == 'GET':
        # בדיקת חיבור
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'success',
                'message': 'Discord Bot is running!'
            })
        }
    
    elif request.method == 'POST':
        # הפעלת הבוט
        try:
            bot.start()
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'success',
                    'message': 'Bot started successfully!'
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'status': 'error',
                    'message': str(e)
                })
            }
    
    return {
        'statusCode': 405,
        'body': json.dumps({
            'status': 'error',
            'message': 'Method not allowed'
        })
    } 
