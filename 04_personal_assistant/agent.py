from openai import OpenAI
import streamlit as st
import json, math, requests

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

#les 3 outils
def get_meteo(city):
    response = requests.get("https://api.openweathermap.org/data/2.5/weather", params={
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric", 
        "lang": "en"
    })
    d = response.json()
    return json.dumps({
        "city": city,
        "description": d["weather"][0]["description"],
        "temperature": d["main"]["temp"],
        "feels_like": d["main"]["feels_like"],
        "humidity": d["main"]["humidity"]
    })

def web_search(query):
    response = requests.post("https://api.tavily.com/search", json={
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": 3})
    results = response.json()["results"]
    return json.dumps([{"title": r["title"], "content": r["content"]} for r in results])

def calculer(expression: str) -> float:
    expression = expression.replace("^", "**").replace("pi", str(math.pi))
    result = eval(expression, {"__builtins__": {}}, {
        "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
        "log": math.log10, "ln": math.log, "pi": math.pi, "e": math.e, "abs": abs
        })
    return json.dumps({"expression": expression, "result": round(result, 8)})

#definition des outils pour l'agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_meteo",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city to get the weather for."}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculer",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "The mathematical expression to calculate."}
                },
                "required": ["expression"]
            }
        }
    }
]

def execute_tool(name, args):
    if name == "get_meteo":
        return get_meteo(**args)
    elif name == "web_search":
        return web_search(**args)
    elif name == "calculer":
        return calculer(**args)
    else:
        return json.dumps({"error": "Unknown tool"})
    
#l'agent avec memoire
conversation_history = []

def assistant(question):
    conversation_history.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant that can use tools to answer questions."}] + conversation_history,
        tools=tools,
    )
    msg = response.choices[0].message
    
    #si l'agent appelle un outil
    if msg.tool_calls:
        conversation_history.append(msg)  # message de l'agent avant l'appel de l'outil
        
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"Executing tool: {tc.function.name} with arguments {args}")
            result = execute_tool(tc.function.name, args)
            conversation_history.append({"role": "tool", "tool_call_id": tc.id, "content": result})  # résultat de l'outil
        
        #reponse finale après exécution des outils
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant that can use tools to answer questions."}] + conversation_history,
            tools=tools,
        )
        reply = final_response.choices[0].message.content
    else:
        reply = msg.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

#Test
print(assistant("What is the weather in Paris?"))
print(assistant("Search the web for recent news about OpenAI."))
print(assistant("Calculate the expression: (5^2 + sqrt(16)) * pi"))
print(assistant("What is the weather in New York?"))
print(assistant("summarize our conversation so far."))