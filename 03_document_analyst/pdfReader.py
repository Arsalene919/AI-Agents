from openai import OpenAI
import streamlit as st
import PyPDF2

    
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

#Extraire le texte d'un PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
#l'agent repond aux questions sur le document PDF
def agent_pdf_reader(pdf_path, question):
    print(f"File reading...")
    pdf_text = extract_text_from_pdf(pdf_path)
    
    #on limite à 12 000 caractères pour éviter de dépasser les limites de tokens
    if len(pdf_text) > 12000:
        pdf_text = pdf_text[:12000] + "\n...[truncated]..."
    
    print(f"Document loaded ({len(pdf_text)} characters)")
    print(f"Ongoing analysis...")
    
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant that answers questions based on the content of a PDF document."
                Here is the content of the document: {pdf_text}
                
                Answer the questions based ONLY on the content of the document. If the answer is not in the document, say you do not know."""},
                {"role": "user", "content": question
            }
        ]
    )
    
    return response.choices[0].message.content

#Test
pdf_path = r"C:\Users\Khach\OneDrive\Desktop\WebSearch\iso27001.pdf"
print(agent_pdf_reader(pdf_path, "What is the main topic of the document?"))
print(agent_pdf_reader(pdf_path, "What are the key findings?"))
print(agent_pdf_reader(pdf_path, "Who is the author?"))