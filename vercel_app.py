from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>שלום! האפליקציה עובדת!</h1>'

@app.route('/health')
def health():
    return {"status": "ok"}

# נקודת כניסה עבור Vercel
app.debug = True 
