# 📄 PDF Chatbot System

This project allows users to upload a PDF document, chat with it (ask questions), and receive summaries using Google's Gemini model.

## 🛠️ Technologies Used:
- Python 3.x
- Gradio (for GUI testing)
- FastAPI (for API communication)
- Google Generative AI API (Gemini)
- PyMuPDF (for PDF processing)
- TextBlob (optional spell correction)

## 📦 Installation:

```bash
pip install gradio fastapi uvicorn google-generativeai python-dotenv PyMuPDF textblob

---

Required Libraries:

gradio

requests

numpy

arabic_reshaper

python-bidi

PyMuPDF

google-generativeai

python-dotenv

🚀 Running the Project:
1️⃣ Gradio Interface (for testing):

python main.py
Open the local URL displayed in your terminal.

Upload any PDF file.

Use the chatbot to ask questions or request summaries.

2️⃣ FastAPI (for backend integration):
uvicorn main_fastapi:app --reload

🛠️ Project Structure

project/
│
├── main.py
── app/
│   └── main_fastapi.py
├── agents/
│   └── llm_agent.py
├── utils/
│   └── utils.py
├── requirements.txt
└── README.md


📡 API Endpoints:
/upload-pdf/ : Upload a PDF file, returns cleaned text and chunks.

/ask/ : Submit a question + PDF content to get an answer.

/summarize/ : Get summary for a PDF.


🛡️ Notes
Make sure your GOOGLE_API_KEY is configured via the .env file.

This project is optimized for PDFs in any language and can handle both technical and non-technical content.

