#entity_extractor.py

import spacy
from typing import List

nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2000000  # Increased to handle large texts (e.g., 1000+ pages)

def extract_entities(text: str) -> List[str]:
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ["DATE", "GPE", "ORG", "PERSON"]]
#nlp = spacy.load("en_core_web_sm")

#def extract_entities(text: str) -> List[str]:
  #  """Extract named entities (e.g., dates, organizations, people) from text."""
  #  doc = nlp(text)
  #  entities = []
   # for ent in doc.ents:
    #    if ent.label_ in ["DATE", "TIME", "GPE", "ORG", "PERSON", "NORP"]:
      #      entities.append(ent.text)
  #  return entities