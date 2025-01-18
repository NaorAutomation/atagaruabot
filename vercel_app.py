from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return HTMLResponse(content="<h1>שלום! האפליקציה עובדת!</h1>")

@app.get("/health")
async def health_check():
    return {"status": "ok"} 
