# 📁 utils/utils.py
import fitz  # PyMuPDF
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_text(text):
    lines = text.split("\n")
    cleaned = []
    seen = set()
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            cleaned.append(line)
    return "\n".join(cleaned)

def smart_chunk(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def load_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("⚠️ GEMINI_API_KEY environment variable not found.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")
