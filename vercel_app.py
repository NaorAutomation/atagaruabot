import uvicorn
from main import app

if __name__ == "__main__":
    # הפעלת השרת המקומי
    uvicorn.run(app, host="localhost", port=8000) 
