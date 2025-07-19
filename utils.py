# 📁 utils.py
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # إزالة التكرارات والمسافات الزائدة
    text = re.sub(r'[\u200f\u200e]', '', text)  # إزالة رموز تنسيق الاتجاه
    return text.strip()

def smart_chunk(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
