class GeminiAnswerAgent:
    def __init__(self, model):
        self.model = model

    def answer_question(self, question, chunks):
        for chunk in chunks[:3]:
            prompt = f"""
            PDF Content:
            {chunk}

            Question:
            {question}
            """
            try:
                response = self.model.generate_content(prompt)
                answer = response.text.strip()
                if answer:
                    return answer
            except Exception:
                continue
        return "I could not find a suitable answer from the document."

    def summarize_document(self, full_text):
        words = full_text.split()
        chunk_size = 2000
        summaries = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            prompt = f"""
            Please summarize the following part of the document in clear bullet points:

            {chunk}
            """
            try:
                response = self.model.generate_content(prompt)
                summary = response.text.strip()
                summaries.append(summary)
            except Exception:
                summaries.append("⚠️ Failed to summarize this part.")

        final_summary = "\n\n".join(summaries)
        return final_summary or "Summary not available."
