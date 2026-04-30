import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import json, requests, io
from datetime import datetime

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

#Initialisation session state 
if "history" not in st.session_state:
    st.session_state.history = []

#recherche web
def web_search(query):
    response = requests.post("https://api.tavily.com/search", json={
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": 5,
        "include_raw_content": True})
    results = response.json().get("results", [])
    return "\n\n".join([f"Title: {r['title']}\nContent: {r['content']}" for r in results])

#multiple sources search
def multi_source_search(topic):
    """Launch 3 different searches with different angles to get a variety of sources."""
    queries = [
        topic,
        f"{topic} recent developments",
        f"{topic} challenges and opportunities"
    ]
    all_results = []
    for q in queries:
        all_results += f"\n\n--- Search: {q} ---\n"
        all_results += web_search(q)
    return all_results, queries
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

def clean_for_pdf(text):
    """Supprime les caractères non supportés par Helvetica"""
    return text.encode("latin-1", errors="replace").decode("latin-1")

#exporter en PDF
def export_to_pdf(topic, report):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)  # ← marges explicites left, top, right
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", size=16)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 10, clean_for_pdf(topic))
    pdf.ln(2)
    pdf.set_font("Helvetica", "", size=10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="R")
    pdf.ln(4)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)
    
    for line in report.split("\n"):
        clean = (line.replace("**", "").replace("##", "").replace("###", "").replace("- ", " ° ").strip())
        clean = clean_for_pdf(clean)
        if not clean:
            pdf.ln(2)
            continue
        if line.startswith("## "):
            pdf.set_font("Helvetica", "B", size=14)
            pdf.set_text_color(40, 40, 40)
            pdf.ln(3)
        elif line.startswith("### "):
            pdf.set_font("Helvetica", "B", size=12)
            pdf.set_text_color(60, 60, 60)
        else:
            pdf.set_font("Helvetica", size=10)
            pdf.set_text_color(0, 50, 50)
        #Largeur fixe au lieu de 0
        page_width = pdf.w - 30  # 210mm - 15mm*2 marges
        pdf.multi_cell(page_width, 5, clean)
        pdf.ln(1)
    return bytes(pdf.output())

#interface Streamlit
st.set_page_config(page_title="Your research Assistant", page_icon="🔍", layout="centered")
st.title("🔍 Research Assistant")
tab1, tab2 = st.tabs([f"New report", f"History ({len(st.session_state.history)})"])

with tab1:
    topic = st.text_input("Enter a research topic:", placeholder="e.g. The impact of AI on society")
    if st.button("Generate Report", type="primary") and topic:
        with st.status("Generating report...", expanded=True) as status:
            st.write("Searching the web for relevant sources...")
            sources, queries = multi_source_search(topic)
            sources_text = "\n".join(sources) if isinstance(sources, list) else sources
            st.write(f"Search completed with {len(queries)} different queries. {len(sources_text.split())} sources found.")
            st.write("Analyzing sources...")
            st.write("Analysis completed.")
            st.write("Writing report...")
            report = write_report(topic, sources)
            st.write("Report generated.")
            st.write("Preparing PDF...")
            pdf_bytes = export_to_pdf(topic, report)
            st.write("PDF ready.")
            status.update(label="Report generated successfully!", state="complete")
        
        #sauvegarde dans l'historique
        st.session_state.history.append({
            "topic": topic, "report": report, "pdf": pdf_bytes,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sources": len(queries), "words": len(report.split())
        })
        
        st.divider()
        st.markdown(report)
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Download Report (PDF)",
                data=pdf_bytes, file_name = f"report_{topic[:30]}.pdf", mime="application/pdf"
            )
        with col2:
            st.download_button(
                "Download Report (Markdown)",
                data=report, file_name = f"report_{topic[:30]}.md", mime="text/markdown"
            )
with tab2:
    if not st.session_state.history:
        st.info("No reports generated yet. Go to the 'New report' tab to create your first report.")
    else:
        for i, r in enumerate(reversed(st.session_state.history)):
            with st.expander(f"{r['topic']} _ {r['date']}"):
                st.caption(f"{r['sources']} sources - {r['words']} words")
                st.markdown(r["report"])
                st.download_button(
                    "Download Report (PDF)", r["pdf"], file_name = f"report_{r['topic'][:30]}.pdf", mime="application/pdf", key=f"dl_{i}")
# st.caption("Enter a topic --> the agent will search the web, analyze the sources and write a report.")
# topic = st.text_input("Research topic:", placeholder="e.g. The impact of AI on society")
# if st.button("Generate Report", type="primary") and topic:
#     with st.status("Searching the web...", expanded=True) as status:
#         st.write("🔍 Searching the web for relevant sources...")
#         sources = web_search(topic)
#         st.write(f"{len(sources.split())} sources found.")
        
#         st.write("🧠 Analyzing sources...")
#         analyse = sources_analysis(topic, sources)
#         st.write("Analysis completed.")
        
#         st.write("📝 Writing report...")
#         report = write_report(topic, analyse)
#         st.write("Report generated.")
        
#         status.update(label="Report generated successfully!", state="complete")
        
#     st.divider()
#     st.markdown(report)
    
#     st.download_button(
#         "Download Report",
#         data=report,
#         file_name = f"report_{topic[:30]}.md",
#         mime="text/markdown"
#     )