import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = "C:\\Users\\Lenovo\\Documents\\AI Projects\\final-\\Object-oriented programming in C++-Sams Publishing (2002).pdf"


def chat_with_pdf():
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Using API Key: {api_key[:5]}... (partial for security)")  # Print partial key to verify
    if not api_key:
        print(
            "API Key not loaded. Check .env file and environment variables. Make sure .env is in the correct directory.")
        return

    if not os.path.exists(PDF_PATH):
        print("PDF not found. Update PDF_PATH.")
        return

    url_base = f"http://{os.getenv('AI_HOST', '127.0.0.1')}:{os.getenv('AI_PORT', '5001')}"
    print("🚀 Starting PDF Chat...")
    print("==================================================")

    # Improved health check with retry
    max_retries = 3
    for attempt in range(max_retries):
        try:
            health_response = requests.get(f"{url_base}/health/", timeout=10)
            if health_response.status_code == 200 and health_response.json().get("model_loaded"):
                break
            print(f"Health check failed (Attempt {attempt + 1}/{max_retries}). Retrying...")
            time.sleep(2 ** attempt)
        except Exception:
            if attempt == max_retries - 1:
                print("Server not responding. Ensure it’s running on port 5001.")
                return

    print("🚀 Attempting to upload PDF...")
    try:
        with open(PDF_PATH, "rb") as f:
            response = requests.post(f"{url_base}/upload/", files={"file": f}, timeout=60)
            if response.status_code != 200:
                print("Upload error:", response.json())
                return
            print(
                "PDF uploaded successfully. Ask questions or 'summarize' (e.g., 'who is the author' or 'summarize detailed') (or 'quit' to exit):")
    except Exception as e:
        print(f"Upload failed: {e}. Check file size, server, or API key.")
        return

    while True:
        action = input("> ").strip().lower()
        if action == "quit":
            print("Chat ended.")
            break
        if not action:
            print("Enter a question or 'summarize' with type (e.g., 'summarize detailed').")
            continue
        data = {}
        if action.startswith("summarize"):
            summary_type = action.replace("summarize", "").strip() or "detailed"
            data = {"summary_type": summary_type}
            url = f"{url_base}/summarize/"
        else:
            data = {"question": action}
            url = f"{url_base}/ask/"

        max_retries = 5  # Increased retries
        for attempt in range(max_retries):
            try:
                response = requests.post(url, data=data, timeout=120)
                if response.status_code == 200:
                    result = response.json()
                    if "answer" in result:
                        print(f"Me: {action}")
                        print(f"AI: {result['answer']}")
                    elif "summary" in result:
                        print(f"Summary: {result['summary']}")
                    break
                elif response.status_code == 429:
                    retry_delay = 54  # Based on API response
                    print(
                        f"Quota exceeded (429). Retrying in {retry_delay} seconds (Attempt {attempt + 1}/{max_retries})...")
                    time.sleep(retry_delay)
                else:
                    print(f"Error on attempt {attempt + 1}: {response.json()}")
                    break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Request failed after {max_retries} attempts: {e}")
                else:
                    print(f"Attempt {attempt + 1}/{max_retries} failed: {e}. Retrying in {2 ** attempt} seconds...")
                    time.sleep(2 ** attempt)


if __name__ == "__main__":
    chat_with_pdf()