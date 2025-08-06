import os
from fastapi import FastAPI, UploadFile, HTTPException, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from agents.llm_agent import GeminiAnswerAgent
from utils.utils import extract_text_from_pdf, clean_text
from utils.text_chunker import chunk_text
from storage.chat_history import save_history
import uuid
import time

app = FastAPI(
    title="PDF Chat Bot API",
    description="Intelligent PDF document interaction system using Gemini AI",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Load model with retry
def load_model_with_retry():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            bot_model = GeminiAnswerAgent.load_gemini_model()
            bot = GeminiAnswerAgent(bot_model)
            return bot_model, bot, True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed to load model: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    print("Failed to load model after retries.")
    return None, None, False


bot_model, bot, model_loaded = load_model_with_retry()

# Store uploaded PDFs
uploaded_docs = {}


@app.post("/upload/")
async def upload_pdf(file: UploadFile):
    """Upload PDF file for processing"""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    session_id = str(uuid.uuid4())
    pdf_bytes = await file.read()

    if len(pdf_bytes) > 500 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum 500MB allowed.")

    text = extract_text_from_pdf(pdf_bytes)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Failed to extract text.")

    cleaned_text = clean_text(text)
    text_length = len(cleaned_text)

    # Adaptive chunking
    if text_length > 500000:
        chunk_size = 500
        overlap = 50
        max_chunks = 500  # Increased for larger files
    elif text_length > 200000:
        chunk_size = 400
        overlap = 40
        max_chunks = 300
    elif text_length > 100000:
        chunk_size = 300
        overlap = 30
        max_chunks = 200
    else:
        chunk_size = 200
        overlap = 20
        max_chunks = 100

    chunks = chunk_text(cleaned_text, chunk_size=chunk_size, overlap=overlap)
    chunks = chunks[:max_chunks]

    uploaded_docs[session_id] = {
        "chunks": chunks,
        "total_length": text_length,
        "chunk_count": len(chunks),
        "full_text": cleaned_text[:500000]  # Increased to 500,000 chars
    }

    save_history(session_id, "Uploaded", f"PDF processed. {len(chunks)} chunks created.")
    return {
        "session_id": session_id,
        "message": "PDF uploaded successfully.",
        "stats": {
            "total_chars": text_length,
            "chunks_created": len(chunks),
            "chunk_size": chunk_size
        }
    }


@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    if not uploaded_docs:
        raise HTTPException(status_code=400, detail="Upload a PDF first.")
    if not model_loaded:
        raise HTTPException(status_code=500, detail="AI model not loaded. Check API key.")

    session_id = list(uploaded_docs.keys())[0]
    doc_data = uploaded_docs[session_id]
    chunks = doc_data["chunks"]

    context_chunks = chunks[:15] if len(chunks) >= 15 else chunks  # Increased to 15 chunks
    answer = bot.answer_question(question, context_chunks)

    save_history(session_id, question, answer)
    return {"question": question, "answer": answer}


@app.get("/ask/")
async def ask_question_get(question: str = Query(...)):
    if not uploaded_docs:
        raise HTTPException(status_code=400, detail="Upload a PDF first.")
    if not model_loaded:
        raise HTTPException(status_code=500, detail="AI model not loaded. Check API key.")

    session_id = list(uploaded_docs.keys())[0]
    doc_data = uploaded_docs[session_id]
    chunks = doc_data["chunks"]

    context_chunks = chunks[:15] if len(chunks) >= 15 else chunks  # Increased to 15 chunks
    answer = bot.answer_question(question, context_chunks)

    save_history(session_id, question, answer)
    return {"question": question, "answer": answer}


@app.post("/summarize/")
async def summarize_pdf(summary_type: str = Form("detailed")):
    if not uploaded_docs:
        raise HTTPException(status_code=400, detail="Upload a PDF first.")
    if not model_loaded:
        raise HTTPException(status_code=500, detail="AI model not loaded. Check API key.")

    session_id = list(uploaded_docs.keys())[0]
    doc_data = uploaded_docs[session_id]
    full_text = doc_data["full_text"]  # Use full 500,000 chars

    summary = bot.summarize_document(full_text, summary_type)
    save_history(session_id, f"Summary ({summary_type})", summary)
    return {"summary": summary}


@app.get("/summarize/")
async def summarize_pdf_get(summary_type: str = Query("detailed")):
    if not uploaded_docs:
        raise HTTPException(status_code=400, detail="Upload a PDF first.")
    if not model_loaded:
        raise HTTPException(status_code=500, detail="AI model not loaded. Check API key.")

    session_id = list(uploaded_docs.keys())[0]
    doc_data = uploaded_docs[session_id]
    full_text = doc_data["full_text"]  # Use full 500,000 chars

    summary = bot.summarize_document(full_text, summary_type)
    save_history(session_id, f"Summary ({summary_type})", summary)
    return {"summary": summary}


@app.get("/health/")
async def health_check():
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "docs_uploaded": len(uploaded_docs),
        "api_version": "2.0.0"
    }


@app.get("/")
async def root():
    return {
        "message": "PDF Chat Bot API",
        "version": "2.0.0",
        "docs": "/redoc",
        "health": "/health"
    }