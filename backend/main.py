import os
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Direct MCP tool imports
from mcp_server import (
    scrape_github,
    analyze_profile,
    generate_card_html,
    save_card,
)

app = FastAPI(title="GitHub Dev Card Generator")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static directories
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
CARDS_DIR = os.path.join(STATIC_DIR, "cards")

os.makedirs(CARDS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# Request model
class GenerateRequest(BaseModel):
    username: str


# Generate endpoint
@app.post("/generate")
async def generate_card(request: GenerateRequest):
    username = request.username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username is required"
        )

    try:
        # Step 1 - Scrape GitHub
        github_data = await scrape_github(username)

        if github_data.get("error"):
            raise HTTPException(
                status_code=404,
                detail=github_data["error"]
            )

        # Step 2 - Analyze profile
        analysis = await analyze_profile(github_data)

        # Step 3 - Generate HTML
        html = await generate_card_html(
            username,
            github_data,
            analysis
        )

        # Step 4 - Save card
        card_url = await save_card(
            username,
            html
        )

        return {
            "status": "success",
            "username": username,
            "card_url": card_url,
            "analysis": analysis
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# Serve generated cards
@app.get("/card/{username}")
async def get_card(username: str):
    file_path = os.path.join(
        CARDS_DIR,
        f"{username}.html"
    )

    if os.path.exists(file_path):
        return FileResponse(file_path)

    raise HTTPException(
        status_code=404,
        detail="Card not found. Generate it first."
    )


# Health endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Run app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )