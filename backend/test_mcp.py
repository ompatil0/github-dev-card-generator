import asyncio
import os
import json
from dotenv import load_dotenv
from mcp_server import scrape_github, analyze_profile, generate_card_html

# Load environment variables from .env
load_dotenv()

async def test_end_to_end():
    username = "torvalds"
    print(f"--- Starting End-to-End Test for user: {username} ---")
    
    # 1. Scrape GitHub
    print("Step 1: Scraping GitHub data...")
    github_data = await scrape_github(username)
    if "error" in github_data:
        print(f"FAILED: scrape_github error: {github_data['error']}")
        return
    print("SUCCESS: Data scraped.")

    # 2. Analyze Profile
    print("Step 2: Analyzing profile with Gemini...")
    analysis = await analyze_profile(github_data)
    if not analysis or "developer_vibe" not in analysis:
        print("FAILED: analyze_profile failed to return valid JSON.")
        return
    print("SUCCESS: Profile analyzed.")

    # 3. Generate HTML Card
    print("Step 3: Generating HTML card...")
    html = await generate_card_html(username, github_data, analysis)
    if not html:
        print("FAILED: generate_card_html returned empty string.")
        return
    print("SUCCESS: HTML card generated.")

    # 4. Results
    print("\n--- RESULTS ---")
    print(f"Card Theme: {analysis.get('card_theme')}")
    print(f"Developer Vibe: {analysis.get('developer_vibe')}")
    print("----------------")

if __name__ == "__main__":
    asyncio.run(test_end_to_end())
