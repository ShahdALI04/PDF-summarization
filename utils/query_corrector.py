from textblob import TextBlob

def correct_query(text):
    try:
        return str(TextBlob(text).correct())
    except:
        return text