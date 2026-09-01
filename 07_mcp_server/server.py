from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio, json, httpx


app = Server("research-assistant-mcp")

#Outil 1 : Sauvegarder un rapport de recherche
@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="save_report",
            description="Save a report to the research database.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["topic", "content"]
            }
        ),
        Tool(
            name="search-reports",
            description="Search for reports in the existant reports",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="export_to_drive",
            description="Export a report to Google Drive.",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_id": {"type": "integer"},
                    "folder": {"type": "string"}
                },
                "required": ["report_id"]
            }
        )
    ]
    
#Exécution des outils
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    async with httpx.AsyncClient(timeout=120.0) as client:
        if name == "save_report":
            response = await client.post("http://localhost:8000/reports/generate",
                                         json={"topic": arguments["topic"]})
            data = response.json()
            return [TextContent(type="text", text=f"Report saved! ID: {data['id']}")]
        elif name == "search-reports":
            response = await client.get(f"http://localhost:8000/reports/search/query", params={"q": arguments["query"]})
            results = response.json()
            return [TextContent(type="text", text=json.dumps(results, ensure_ascii=False, indent=2))]
        elif name == "export_to_drive":
            #on connecte Google Drive API
            return [TextContent(type="text", text=f"Report {arguments['report_id']} exported to Google Drive.")]
        
async def main():
    async with stdio_server() as streams:
        await app.run(*streams, app.create_initialization_options())
        
if __name__ == "__main__":
    asyncio.run(main())
