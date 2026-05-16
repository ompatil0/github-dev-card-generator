import os
import sys

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import McpToolset

from mcp import StdioServerParameters

# Gemini model
model = Gemini(model="gemini-2.5-flash")

# MCP server path
mcp_server_path = os.path.join(
    os.path.dirname(__file__),
    "mcp_server.py"
)

# MCP connection params
server_params = StdioServerParameters(
    command=sys.executable,
    args=[mcp_server_path],
    env=os.environ.copy()
)

# MCP Toolset
toolset = McpToolset(
    connection_params=server_params
)

# Agent
github_card_agent = Agent(
    name="github_card_agent",
    model=model,
    tools=[toolset],   # IMPORTANT
    instruction="""
You are a GitHub profile analyst and dev card generator.

When a user gives a GitHub username:
1. scrape_github
2. analyze_profile
3. generate_card_html
4. save_card

Never skip steps.
"""
)