#📁main_gradio.py
import gradio as gr
from utils.utils import clean_text, smart_chunk, load_gemini_model
from agents.llm_agent import GeminiAnswerAgent
from utils.query_corrector import correct_query
from PyPDF2 import PdfReader

# Load model
bot_model = load_gemini_model()
bot = GeminiAnswerAgent(bot_model)

# Functions
def handle_pdf(pdf_file):
    reader = PdfReader(pdf_file.name)
    raw_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    cleaned = clean_text(raw_text)
    chunks = smart_chunk(cleaned, chunk_size=1000, overlap=100)
    return cleaned, chunks

def chat_with_bot(message, chat_history, pdf_text, chunks):
    if not pdf_text or not pdf_text.strip():
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": "❌ Please upload a PDF file first."})
        return chat_history, ""

    # Correct the message
    corrected_message = correct_query(message)

    chat_history.append({"role": "user", "content": corrected_message})

    bot_reply = bot.answer_question(corrected_message, chunks)
    chat_history.append({"role": "assistant", "content": bot_reply})

    return chat_history, ""  # Clear input box after sending

# Interface
with gr.Blocks() as demo:
    gr.Markdown("# 📄 PDF Chatbot")

    pdf_file = gr.File(label="Upload PDF File", file_types=[".pdf"])
    upload_button = gr.Button("📤 Upload PDF")

    chatbot = gr.Chatbot(label="Chat with PDF Bot", type='messages')
    user_input = gr.Textbox(label="Message", placeholder="Type your message here...")

    send_button = gr.Button("Send")

    hidden_pdf_text = gr.Textbox(visible=False)
    hidden_chunks = gr.State()
    chat_history = gr.State([])

    upload_button.click(
        fn=handle_pdf,
        inputs=pdf_file,
        outputs=[hidden_pdf_text, hidden_chunks]
    )

    send_button.click(
        fn=chat_with_bot,
        inputs=[user_input, chat_history, hidden_pdf_text, hidden_chunks],
        outputs=[chatbot, user_input]
    )

demo.launch()

