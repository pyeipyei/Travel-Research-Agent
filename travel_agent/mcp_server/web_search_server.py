import os
import sys
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

load_dotenv()

# Initialize FastMCP
mcp = FastMCP("advanced-web-search")

# Initialize Tavily Client
api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    print("WARNING: TAVILY_API_KEY is missing from environment variables.", file=sys.stderr)
    tavily = None
else:
    tavily = TavilyClient(api_key=api_key)


@mcp.tool()
def search_web(query: str) -> str:
    """
    Search the live web for recent, factual, or deeply analytical information.
    """
    # Safe logging to stderr so stdio transport doesn't break!
    print(f"Executing Tavily search for: {query}", file=sys.stderr)

    if not tavily:
        return "Error: Search API key not configured on the server."

    try:
        # Executes the search optimizing results specifically for AI agents
        response = tavily.search(query=query, max_results=5)
        results = response.get("results", [])

        if not results:
            return "No relevant web results found."

        output = []
        for r in results:
            output.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}")

        return "\n\n---\n\n".join(output)

    except Exception as e:
        print(f"Search failed: {str(e)}", file=sys.stderr)
        return f"Search failed due to an internal error."


if __name__ == "__main__":
    mcp.run()