from openai import OpenAI
import streamlit as st
import json
import requests


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
#on definit l'outil de recherche web (on va utiliser Tavily ouisque c'est gratuit)
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    }        
]

def web_search(query):
    response = requests.post("https://api.tavily.com/search", json={
        "api_key": TAVILY_API_KEY,
        "query": query,
        "num_results": 3})
    if response.status_code == 200:
        results = response.json()["results"]
        return "\n".join([r["content"] for r in results])
        
    else:
        return {"error": "Failed to retrieve search results"}

def agent_search(question):
    messages = [{"role": "user", "content": question}]
    
    #l'agent décide s'il doit chercher
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        tools=tools,
        tool_choice="auto",
        messages=messages
    )
    
    #si l'agent appelle l'outil
    if response.choices[0].finish_reason == "tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]
        query = json.loads(tool_call.function.arguments)["query"]
        
        print(f"Searching the web for: {query}")
        search_results = web_search(query)
        
        #on renvoie les résultats à l'agent
        messages.append(response.choices[0].message)  # message de l'agent avant l'appel de l'outil
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": search_results
        })
        
        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final.choices[0].message.content
    
    return response.choices[0].message.content

#Test
print(agent_search("Quelles sont les dernières avancées en IA en 2025 ?"))

