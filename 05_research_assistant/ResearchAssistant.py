import streamlit as st
from openai import OpenAI
import json, requests

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

#recherche web
def web_search(query):
    response = requests.post("https://api.tavily.com/search", json={
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": 5,
        "include_raw_content": True})
    results = response.json().get("results", [])
    return "\n\n".join([f"Title: {r['title']}\nContent: {r['content']}" for r in results])

#synthese des sources
def sources_analysis(topic, sources):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are an assistant that synthesizes information from multiple sources. Extract the most relevent informations from the given sources."},
            {"role": "user", "content": f"Here is the topic: {topic}\n Here are the sources:\n{sources}\n\nPlease provide a concise summary of the key points and insights from these sources."}
        ]
    )
    return response.choices[0].message.content

#redaction du rapport
def write_report(topic, analyse):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Write a structred report in Markdown format:
             ## Introduction
             ## Context
             ## Key Findings
             ## Analysis
             ## Perspective
             ## Conclusion"""},
            {"role": "user", "content": f"Here is the topic: {topic}\n Here is the analysis of the sources: {analyse}\n\nPlease write a detailed report based on this analysis."}
        ]
    )
    return response.choices[0].message.content

#interface Streamlit
st.set_page_config(page_title="Research Assistant", page_icon="🔍")
st.title("🔍 Research Assistant")
st.caption("Enter a topic --> the agent will search the web, analyze the sources and write a report.")
topic = st.text_input("Research topic:", placeholder="e.g. The impact of AI on society")
if st.button("Generate Report", type="primary") and topic:
    with st.status("Searching the web...", expanded=True) as status:
        st.write("🔍 Searching the web for relevant sources...")
        sources = web_search(topic)
        st.write(f"{len(sources.split())} sources found.")
        
        st.write("🧠 Analyzing sources...")
        analyse = sources_analysis(topic, sources)
        st.write("Analysis completed.")
        
        st.write("📝 Writing report...")
        report = write_report(topic, analyse)
        st.write("Report generated.")
        
        status.update(label="Report generated successfully!", state="complete")
        
    st.divider()
    st.markdown(report)
    
    st.download_button(
        "Download Report",
        data=report,
        file_name = f"report_{topic[:30]}.md",
        mime="text/markdown"
    )