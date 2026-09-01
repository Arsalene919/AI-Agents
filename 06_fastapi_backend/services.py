from openai import OpenAI
import requests, os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def web_search(query):
    r = requests.post("https://api.tavily.com/search", json={
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": 5
    })
    return "\n\n".join([f"{x['title']}\n{x['content']}" for x in r.json().get("results", [])])

def generate_report(topic: str):
    queries = [topic, f"{topic} latest news", f"{topic} recent developments"]
    sources = "\n\n".join([web_search(q) for q in queries])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Write a structured research report in a pdf format:
            ## Introduction
            ## Context
            ## Key Points
            ## Analysis
            ## Trends & Perspectives
            ## Conclusion"""},
            {"role": "user", "content": f"Topic: {topic}\n\nSources:\n{sources}"}
        ]
    )
    content = response.choices[0].message.content
    return content, len(queries)