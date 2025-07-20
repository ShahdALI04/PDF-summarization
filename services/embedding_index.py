# ✅ embedding_index.py
# لا حاجة للفكتور سيرش أو FAISS
# فقط chunking ذكي للنص

def smart_chunk_text(text, max_tokens=300):
    import re
    chunks, current_chunk = [], []
    token_count = 0

    for paragraph in re.split(r'[\n\r]+', text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        paragraph_tokens = paragraph.split()
        if token_count + len(paragraph_tokens) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk, token_count = [], 0

        current_chunk.extend(paragraph_tokens)
        token_count += len(paragraph_tokens)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# ✅ extract text from PDF
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text


def prepare_context_chunks(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    return smart_chunk_text(raw_text)


# ✅ llm_agent.py
import google.generativeai as genai

class GeminiRAG:
    def __init__(self, api_key, model_name='gemini-1.5-flash'):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def answer_with_context(self, query, context_chunks):
        context = "\n\n".join(context_chunks)
        prompt = f"""
        لديك السياق التالي من ملف PDF:
        {context}

        السؤال: {query}
        أجب إجابة دقيقة كأنك قرأت الملف كاملًا.
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()
