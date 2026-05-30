import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import requests, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ── CSS Custom ─────────────────────────────────────────────
st.set_page_config(page_title="Research Assistant", page_icon="🔍", layout="centered")

st.markdown("""
<style>
/* Base dark blue */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
}

.stApp {
    background-color: #0f172a !important;
}

/* Header */
.ra-header {
    padding: 2rem 0 1rem;
    border-bottom: 1px solid #1e293b;
    margin-bottom: 2rem;
}
.ra-title { font-size: 1.5rem; font-weight: 600; color: #f1f5f9; margin: 0; }
.ra-sub   { font-size: 0.875rem; color: #64748b; margin: 4px 0 0; }

/* Input */
div[data-testid="stTextInput"] input {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #f1f5f9 !important;
    padding: 10px 14px !important;
    font-size: 0.95rem !important;
    box-shadow: none !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #475569 !important; }

/* Bouton principal */
div[data-testid="stButton"] > button[kind="primary"] {
    background: #3b82f6 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    width: 100%;
    transition: background .2s !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #2563eb !important;
}

/* Boutons secondaires (exemples) */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    padding: 8px 16px !important;
    transition: all .2s !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    border-color: #3b82f6 !important;
    color: #3b82f6 !important;
    background: #1e3a5f !important;
}

/* Download buttons */
div[data-testid="stDownloadButton"] > button {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: all .2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    border-color: #3b82f6 !important;
    color: #3b82f6 !important;
    background: #1e3a5f !important;
}

/* Tabs */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #1e293b;
    gap: 0;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: 10px 20px !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom-color: #3b82f6 !important;
}

/* Rapport card */
.report-card {
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 2rem;
    background: #131f33;
    margin: 1.5rem 0;
}
.report-card h2 {
    font-size: 1.1rem; font-weight: 600; color: #f1f5f9;
    margin: 1.5rem 0 0.5rem;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 6px;
}
.report-card h3 { font-size: 1rem; font-weight: 600; color: #cbd5e1; margin: 1rem 0 0.3rem; }
.report-card p  { color: #94a3b8; line-height: 1.75; margin: 0.4rem 0; }
.report-card ul { color: #94a3b8; padding-left: 1.2rem; }
.report-card li { margin-bottom: 4px; line-height: 1.7; }

/* Historique cards */
.hist-card {
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    background: #131f33;
    cursor: pointer;
    transition: border-color .2s, box-shadow .2s;
}
.hist-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 0 0 1px #3b82f6;
}
.hist-topic { font-size: 0.95rem; font-weight: 500; color: #f1f5f9; }
.hist-meta  { font-size: 0.8rem; color: #64748b; margin-top: 3px; }

/* Status */
div[data-testid="stStatus"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
}

/* Info box */
div[data-testid="stAlert"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

/* Divider */
hr { border: none; border-top: 1px solid #1e293b !important; margin: 1.5rem 0 !important; }

/* Masquer menu Streamlit */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Fonctions ─────────────────────────────────────────────
def web_search(query):
    r = requests.post("https://api.tavily.com/search", json={
        "api_key": TAVILY_API_KEY, "query": query, "max_results": 5
    })
    results = r.json().get("results", [])
    return "\n\n".join([f"{x['title']}\n{x['content']}" for x in results])

def multi_source_search(topic):
    queries = [topic, f"{topic} examples 2025", f"{topic} trends future"]
    all_results = ""
    for q in queries:
        all_results += f"\n\n--- {q} ---\n" + web_search(q)
    return all_results, queries

def write_report(topic, sources):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """Write a structured research report in pdf format with the following sections:
## Introduction
## Context
## Key Points
## Analysis
## Trends & Perspectives
## Conclusion
Be factual, precise, minimum 400 words."""},
            {"role": "user", "content": f"Topic: {topic}\n\nSources:\n{sources}"}
        ]
    )
    return response.choices[0].message.content

def clean_for_pdf(text):
    return text.encode("latin-1", errors="replace").decode("latin-1")

def export_to_pdf(topic, report):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(17, 24, 39)
    pdf.multi_cell(0, 9, clean_for_pdf(topic))
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 6, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(4)
    pdf.set_draw_color(229, 231, 235)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(6)
    for line in report.split("\n"):
        clean = line.replace("**","").replace("## ","").replace("### ","").replace("- ","  • ").strip()
        clean = clean_for_pdf(clean)
        if not clean: pdf.ln(2); continue
        if line.startswith("## "):
            pdf.set_font("Helvetica", "B", 13); pdf.set_text_color(17,24,39); pdf.ln(3)
        elif line.startswith("### "):
            pdf.set_font("Helvetica", "B", 11); pdf.set_text_color(55,65,81)
        else:
            pdf.set_font("Helvetica", "", 10); pdf.set_text_color(75,85,99)
        pdf.multi_cell(pdf.w - 30, 5, clean)
        pdf.ln(1)
    return bytes(pdf.output())

# ── Header ────────────────────────────────────────────────
st.set_page_config(page_title="Your research Assistant", page_icon="🔍", layout="centered")
st.title("🔍 Research Assistant")

# ── Tabs ──────────────────────────────────────────────────
tab1, tab2 = st.tabs([
    "New report",
    f"History ({len(st.session_state.history)})"
])

with tab1:
    topic = st.text_input("", placeholder="e.g. The impact of AI agents in 2025", label_visibility="collapsed")

    # col1, col2, col3 = st.columns([1, 1, 1])
    # with col1:
    #     ex1 = st.button("AI Agents 2025", use_container_width=True)
    # with col2:
    #     ex2 = st.button("LangChain vs LlamaIndex", use_container_width=True)
    # with col3:
    #     ex3 = st.button("What is RAG ?", use_container_width=True)

    # if ex1: topic = "AI Agents in 2025"
    # if ex2: topic = "LangChain vs LlamaIndex"
    # if ex3: topic = "What is RAG ?"

    st.write("")
    generate = st.button("Generate Report", type="primary", use_container_width=True)

    if generate and topic:
        with st.status("Generating your report...", expanded=True) as status:
            st.write("Searching the web...")
            sources, queries = multi_source_search(topic)
            st.write(f"✓ {len(queries)} searches completed")
            st.write("Writing the report...")
            report = write_report(topic, sources)
            st.write("✓ Report generated")
            st.write("Preparing PDF...")
            pdf_bytes = export_to_pdf(topic, report)
            st.write("✓ PDF ready")
            status.update(label="Report ready", state="complete")

        st.session_state.history.append({
            "topic": topic, "report": report, "pdf": pdf_bytes,
            "date": datetime.now().strftime("%d %b %Y, %H:%M"),
            "words": len(report.split()), "sources": len(queries)
        })

        # Rapport affiché
        st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("↓ Download PDF", pdf_bytes,
                file_name=f"{topic[:40]}.pdf", mime="application/pdf",
                use_container_width=True)
        with col2:
            st.download_button("↓ Download Markdown", report,
                file_name=f"{topic[:40]}.md", mime="text/markdown",
                use_container_width=True)

with tab2:
    if not st.session_state.history:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("No reports yet. Generate your first report in the New report tab.")
    else:
        for i, r in enumerate(reversed(st.session_state.history)):
            st.markdown(f"""
            <div class="hist-card">
                <div class="hist-topic">{r['topic']}</div>
                <div class="hist-meta">{r['date']} · {r['words']} words · {r['sources']} sources</div>
            </div>""", unsafe_allow_html=True)
            with st.expander("View report"):
                st.markdown(r["report"])
                st.download_button("↓ Download PDF", r["pdf"],
                    file_name=f"{r['topic'][:40]}.pdf",
                    mime="application/pdf", key=f"dl_{i}",
                    use_container_width=True)