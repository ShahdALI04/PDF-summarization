import fitz  # PyMuPDF
import os
from google.generativeai import GenerativeModel
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_bytes):
    """استخراج النص من ملف PDF من البايتات"""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_text(text):
    """تنظيف النص: إزالة التكرارات والفراغات"""
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
    """تقطيع النص إلى مقاطع ذكية مع تداخل"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks
import os
import google.generativeai as genai

def load_gemini_model():
    """تحميل نموذج Gemini بعد تهيئة المفتاح"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("⚠️ يرجى تحديد متغير البيئة GEMINI_API_KEY")

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")
