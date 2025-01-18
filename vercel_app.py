from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

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
app.debug = True 
