import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Video Stream Portal")

# Define the absolute path to index.html
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "index.html")

@app.get("/video", response_class=HTMLResponse)
async def get_video_portal():
    """Serves the main video player page."""
    try:
        with open(TEMPLATE_PATH, "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: Template not found</h1>", 
            status_code=404
        )

@app.get("/video/", response_class=HTMLResponse)
async def get_video_portal_slash():
    """Serves the main video player page for trailing slash requests."""
    return await get_video_portal()

if __name__ == "__main__":
    # Run the server locally on port 8080
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
