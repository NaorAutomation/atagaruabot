from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f'<h1>שגיאה בטעינת הדף: {str(e)}</h1>'

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/health')
def health():
    return {
        "status": "ok",
        "cwd": os.getcwd(),
        "files": os.listdir('.')
    }

# נקודת כניסה עבור Vercel
handler = app 
