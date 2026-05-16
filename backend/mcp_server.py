from dotenv import load_dotenv

load_dotenv()

from mcp.server.fastmcp import FastMCP
import httpx
import os
import json
from google import generativeai as genai
from typing import Dict, List, Any
from collections import Counter

mcp = FastMCP("GitHub Card Tools")

# Initialize Gemini for analysis
GEN_API_KEY = os.getenv("GEMINI_API_KEY")
if GEN_API_KEY:
    genai.configure(api_key=GEN_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
else:
    model = None

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@mcp.tool()
async def scrape_github(username: str) -> Dict[str, Any]:
    """Fetch user profile information and top repositories from GitHub REST API."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    async with httpx.AsyncClient() as client:
        # Profile Info
        profile_res = await client.get(f"https://api.github.com/users/{username}", headers=headers)
        if profile_res.status_code != 200:
            return {"error": f"User {username} not found"}
        
        profile = profile_res.json()
        
        # Repositories
        repos_res = await client.get(f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100", headers=headers)
        repos = repos_res.json() if repos_res.status_code == 200 else []
        
        # Process Repos: Sort by stars and get top 6
        sorted_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)
        top_6 = []
        languages = []
        for r in sorted_repos[:6]:
            top_6.append({
                "name": r.get("name"),
                "stars": r.get("stargazers_count"),
                "language": r.get("language"),
                "description": r.get("description")
            })
        
        # Aggregate Languages
        for r in repos:
            if r.get("language"):
                languages.append(r.get("language"))
        
        most_used_langs = [lang for lang, count in Counter(languages).most_common(5)]

        return {
            "name": profile.get("name") or profile.get("login"),
            "avatar_url": profile.get("avatar_url"),
            "bio": profile.get("bio"),
            "location": profile.get("location"),
            "public_repos": profile.get("public_repos"),
            "followers": profile.get("followers"),
            "top_6_repos": top_6,
            "most_used_languages": most_used_langs
        }

@mcp.tool()
async def analyze_profile(github_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze GitHub data using Gemini 2.0 Flash to determine developer vibe and theme."""
    if not model:
        return {
            "developer_vibe": "A mysterious coder roaming the digital void (No API Key).",
            "top_skills": ["Python", "Git", "Problem Solving"],
            "fun_fact": "They once wrote a script that worked on the first try.",
            "card_theme": "builder"
        }
    
    prompt = f"""
    Analyze this GitHub profile data and return a JSON object with:
    - developer_vibe: (1 sentence personality description)
    - top_skills: (list of exactly 3 skills)
    - fun_fact: (something clever inferred from their repos or bio)
    - card_theme: (one of: "hacker", "builder", "researcher", "designer", "open-source-hero")

    Data:
    {json.dumps(github_data)}
    
    Return ONLY JSON.
    """
    
    response = model.generate_content(prompt)
    try:
        # Simple JSON extraction from response text
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        return json.loads(text.strip())
    except Exception as e:
        return {
            "developer_vibe": "A mysterious coder roaming the digital void.",
            "top_skills": ["Python", "Git", "Problem Solving"],
            "fun_fact": "They once wrote a script that worked on the first try.",
            "card_theme": "builder"
        }

@mcp.tool()
async def generate_card_html(username: str, github_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
    """Generate a beautiful, self-contained HTML string for a dev card."""
    theme = analysis.get("card_theme", "builder")
    
    themes = {
        "hacker": {"bg": "#0d1117", "text": "#c9d1d9", "accent": "#238636", "border": "#30363d"},
        "builder": {"bg": "#ffffff", "text": "#24292e", "accent": "#0366d6", "border": "#e1e4e8"},
        "researcher": {"bg": "#f6f8fa", "text": "#24292e", "accent": "#6f42c1", "border": "#d1d5da"},
        "designer": {"bg": "#fff5f5", "text": "#2d3748", "accent": "#e53e3e", "border": "#feb2b2"},
        "open-source-hero": {"bg": "#f0f9ff", "text": "#0c4a6e", "accent": "#0ea5e9", "border": "#bae6fd"}
    }
    
    t = themes.get(theme, themes["builder"])
    
    repos_html = "".join([
        f'<div style="margin-bottom: 8px; font-size: 0.9em;">'
        f'<strong>{r["name"]}</strong> ⭐ {r["stars"]} - <span style="color: {t["accent"]}">{r["language"]}</span>'
        f'</div>' for r in github_data.get("top_6_repos", [])[:3]
    ])
    
    skills_html = "".join([
        f'<span style="background: {t["accent"]}; color: white; padding: 2px 8px; border-radius: 12px; margin-right: 5px; font-size: 0.8em;">{s}</span>'
        for s in analysis.get("top_skills", [])
    ])

    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; 
                background: {t["bg"]}; color: {t["text"]}; border: 1px solid {t["border"]}; 
                border-radius: 12px; padding: 24px; width: 400px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <img src="{github_data.get("avatar_url")}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid {t["accent"]}; margin-right: 16px;">
            <div>
                <h2 style="margin: 0;">{github_data.get("name")}</h2>
                <div style="font-size: 0.9em; opacity: 0.8;">@{username}</div>
            </div>
        </div>
        <p style="font-style: italic; margin: 12px 0;">"{analysis.get("developer_vibe")}"</p>
        <div style="margin: 16px 0;">{skills_html}</div>
        <div style="display: flex; gap: 20px; margin: 16px 0; font-size: 0.9em;">
            <div><strong>{github_data.get("public_repos")}</strong> Repos</div>
            <div><strong>{github_data.get("followers")}</strong> Followers</div>
        </div>
        <div style="border-top: 1px solid {t["border"]}; padding-top: 16px;">
            <h4 style="margin: 0 0 10px 0;">Top Repos</h4>
            {repos_html}
        </div>
        <div style="margin-top: 16px; font-size: 0.8em; opacity: 0.7; text-align: right;">
            {analysis.get("fun_fact")}
        </div>
    </div>
    """
    return html

@mcp.tool()
async def save_card(username: str, html: str) -> str:
    """Save the HTML dev card to the static directory."""
    path = f"static/cards/{username}.html"
    full_path = os.path.join(os.path.dirname(__file__), path)
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return f"/static/cards/{username}.html"

if __name__ == "__main__":
    mcp.run(transport="stdio")
