from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    html_content = """
    <!DOCTYPE html>
    <html dir="rtl" lang="he">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discord Bot Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    </head>
    <body class="bg-gray-100">
        <div class="container mx-auto px-4 py-8">
            <h1 class="text-3xl font-bold mb-6 text-center">לוח בקרה - Discord Bot</h1>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div class="bg-white p-4 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-2">משתמשים מחוברים</h2>
                    <p id="connected-users" class="text-2xl text-blue-600">0</p>
                </div>
                <div class="bg-white p-4 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-2">הודעות קוליות היום</h2>
                    <p id="voice-messages" class="text-2xl text-green-600">0</p>
                </div>
                <div class="bg-white p-4 rounded-lg shadow">
                    <h2 class="text-xl font-semibold mb-2">סה"כ פעולות</h2>
                    <p id="total-actions" class="text-2xl text-purple-600">0</p>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-4">
                <h2 class="text-xl font-semibold mb-4">לוגים אחרונים</h2>
                <div id="logs" class="h-96 overflow-y-auto bg-gray-50 p-4 rounded">
                </div>
            </div>
        </div>

        <script>
            function addLog(message) {
                const logsDiv = document.getElementById('logs');
                const logEntry = document.createElement('div');
                logEntry.className = 'mb-2 p-2 bg-white rounded shadow';
                logEntry.textContent = `${new Date().toLocaleTimeString('he-IL')} - ${message}`;
                logsDiv.insertBefore(logEntry, logsDiv.firstChild);
            }

            addLog('ממשק הבקרה נטען בהצלחה');
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "cwd": os.getcwd(),
        "files": os.listdir('.')
    } 
