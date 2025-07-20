# 📁 llm_agent.py (باستخدام Gemini API)
class GeminiAnswerAgent:
    def __init__(self, model):
        self.model = model

    def answer_question(self, question, chunks):
        for chunk in chunks[:3]:  # إرسال أول 3 قطع فقط
            prompt = f"""
            📄 محتوى PDF:
            {chunk}

            ❓ السؤال:
            {question}
            """
            try:
                response = self.model.generate_content(prompt)
                answer = response.text.strip()
                if answer:
                    return answer
            except Exception as e:
                continue
        return "لم أتمكن من العثور على إجابة مناسبة من محتوى الملف."
