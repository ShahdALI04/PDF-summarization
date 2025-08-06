import os
import google.generativeai as genai
from typing import List


class GeminiAnswerAgent:
    @staticmethod
    def load_gemini_model():
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY missing. Please set your Gemini API key in environment variables.")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")

    def __init__(self, model):
        self.model = model

    def answer_question(self, question: str, chunks: List[str]) -> str:
        if not chunks:
            return "No content available to answer the question."

        context_chunks = chunks[:15] if len(chunks) >= 15 else chunks
        context = "\n".join(context_chunks)

        prompt = f"""You are an intelligent assistant specialized in document analysis. Understand the user's intent and provide a relevant response based on the provided content, even if the question is not exact. If the intent is unclear, ask for clarification.

Document Content:
{context}

User Input: {question}

Response:"""

        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )
            return response.text.strip() or "I couldn't find a relevant answer. Please clarify your request."
        except Exception as e:
            return f"Error: {str(e)}"

    def summarize_document(self, full_text: str, summary_type: str = "detailed") -> str:
        if not full_text.strip():
            return "No text for summarization."

        if len(full_text) > 500000:  # Adjust to handle up to 500,000 chars
            chunk_size = 500000 // 5
            samples = [full_text[i * chunk_size:(i + 1) * chunk_size] for i in range(5)]
            full_text = "\n\n[Content omitted]\n\n".join(samples)

        prompt = f"""You are an intelligent assistant. Provide a summary based on the user's request. If 'detailed' or similar is mentioned, give a comprehensive summary (500-1000 words) covering main topics, key points, core concepts, and conclusions. If 'brief' or similar, give a concise summary (200-400 words). Adapt to any other request intelligently, ensuring the summary reflects the full document as much as possible.

Document Content:
{full_text}

User Request: {summary_type}

Summary:"""

        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.7,
                    "top_k": 30
                }
            )
            return response.text.strip() or "Summary failed. Please try a different request."
        except Exception as e:
            return f"Summary error: {str(e)}"