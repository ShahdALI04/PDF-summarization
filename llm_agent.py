# 📁 llm_agent.py
import google.generativeai as genai

class GeminiBot:
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def answer_with_context(self, query, chunks):
        context = "\n".join(chunks)
        prompt = f"""
        بناءً على محتوى هذا الملف:
        {context}

        أجب بدقة ووضوح على السؤال التالي:
        {query}
        """
        response = self.model.generate_content(prompt)
        return response.text.strip() if hasattr(response, 'text') else response
