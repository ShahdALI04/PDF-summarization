from fastapi import FastAPI, UploadFile, Form
from utils.utils import extract_text_from_pdf, clean_text, smart_chunk, load_gemini_model
from agents.llm_agent import GeminiAnswerAgent
from utils.query_corrector import correct_query

app = FastAPI()

# Load model
bot_model = load_gemini_model()
bot = GeminiAnswerAgent(bot_model)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile):
    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)
    cleaned = clean_text(text)
    chunks = smart_chunk(cleaned, chunk_size=1000, overlap=100)
    return {"text": cleaned, "chunks": chunks}

@app.post("/ask/")
async def ask_pdf_question(question: str = Form(...), pdf_text: str = Form(...)):
    corrected_question = correct_query(question)
    chunks = smart_chunk(pdf_text, chunk_size=1000, overlap=100)
    answer = bot.answer_question(corrected_question, chunks)
    return {"question": corrected_question, "answer": answer}

@app.post("/summarize/")
async def summarize_pdf(pdf_text: str = Form(...)):
    summary = bot.summarize_document(pdf_text)
    return {"summary": summary}
