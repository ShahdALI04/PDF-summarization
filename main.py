# 📁 main.py
import os
from PyPDF2 import PdfReader
from utils import clean_text, smart_chunk
from llm_agent import GeminiBot

# ✅ إعداد API (من المطوّر مباشرة)
GEMINI_API_KEY = "AIzaSyBwSVSojcvFfiJxj20w8JRDsLUnETOOgR4"  # ← استبدلها بمفتاحك الثابت

# 📄 قراءة ملف PDF وتحويله لنص
pdf_path = input("\U0001F4C4 Enter path to your PDF file: ")
reader = PdfReader(pdf_path)
raw_text = "\n".join(page.extract_text() or "" for page in reader.pages)

# 🧹 تنظيف النص وتقطيعه
print("\u23F3 Reading and chunking PDF...")
cleaned_text = clean_text(raw_text)
chunks = smart_chunk(cleaned_text, chunk_size=1000, overlap=100)

# 🤖 تهيئة البوت
bot = GeminiBot(api_key=GEMINI_API_KEY)

# 💬 بدء المحادثة
while True:
    user_input = input("\n\U0001F4AC Ask something (or type 'exit'): \nYou: ")
    if user_input.lower() == "exit":
        break
    answer = bot.answer_with_context(user_input, chunks[:3])  # ⚠️ أرسل أول 3 قطع فقط
    print("\U0001F9E0 Answer:", answer)
