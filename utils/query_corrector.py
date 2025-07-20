from textblob import TextBlob

def correct_query(text):
    try:
        blob = TextBlob(text)
        return str(blob.correct())
    except Exception:
        return text
