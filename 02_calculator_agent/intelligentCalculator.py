from openai import OpenAI
import streamlit as st
import json, math

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def calculer(expression: str) -> float:
    expression = expression.replace("^", "**").replace("pi", str(math.pi))
    return eval(expression, {"__builtins__": {}}, {
        "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
        "log": math.log10, "ln": math.log, "pi": math.pi, "e": math.e, "abs": abs
        })
    
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculer",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def agent_calculator(question):
    messages = [{"role": "user", "content": question}]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        tools=tools,
        messages=messages
    )
    
    if response.choices[0].finish_reason == "tool_calls":
        tool_call = response.choices[0].message.tool_calls[0]
        expression = json.loads(tool_call.function.arguments)["expression"]
        
        print(f"Calculating: {expression}")
        result = calculer(expression)
        
        messages.append(response.choices[0].message)  # message de l'agent avant l'appel de l'outil
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})  # résultat de l'outil
        
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        return final_response.choices[0].message.content
    
    else:
        return response.choices[0].message.content
    
#Test
print(agent_calculator("What is the value of (2^3 + sqrt(16)) * pi?"))
print(agent_calculator("Calculate the expression: ln (100) + e^2"))
print(agent_calculator("if I want to invest 5000 euros at 7%% interest for 5 years, how much will I have? (use the formula A = P(1 + r/n)^(nt) where P is the principal, r is the annual interest rate, n is the number of times that interest is compounded per year, and t is the time the money is invested for in years)"))