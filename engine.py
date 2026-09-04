# engine.py
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rank_bm25 import BM25Okapi
from corpus import GOLD_CORPUS

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class HybridRetriever:
    def __init__(self, corpus):
        self.corpus = corpus
        tokenized_corpus = [doc["text"].lower().split() for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def retrieve(self, query: str, jurisdiction: str, top_k: int = 3):
        # 1. Hard jurisdiction filter
        filtered_indices = [
            i for i, doc in enumerate(self.corpus) 
            if doc["jurisdiction"].lower() == jurisdiction.lower()
        ]
        if not filtered_indices:
            return []

        # 2. Score via BM25 on filtered set
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        
        filtered_results = sorted(
            [(scores[i], self.corpus[i]) for i in filtered_indices],
            key=lambda x: x[0],
            reverse=True
        )
        return [doc for score, doc in filtered_results[:top_k]]

retriever = HybridRetriever(GOLD_CORPUS)

def classify_formulation(user_query: str) -> dict:
    """Classifies formulation type or requests clarification."""
    prompt = f"""
    Analyze the user's Ayurvedic formulation query: "{user_query}"
    Determine if this query maps to:
    - 'classical' (exact formula from 1st Schedule Ayurvedic text)
    - 'proprietary' (new combination/admixture of classical ingredients)
    - 'phytopharmaceutical' (purified extract with >=4 quantified phytochemicals)
    - 'ayurveda_aahara' (food/dietary pathya)
    - 'unclear'

    Output ONLY a JSON object:
    {{
        "is_clear": true/false,
        "formulation_type": "classical" | "proprietary" | "phytopharmaceutical" | "ayurveda_aahara" | "unclear",
        "clarifying_question": "string or null"
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json")
    )
    return json.loads(response.text)

def generate_evidence_answer(query: str, jurisdiction: str, formulation_type: str = "general") -> dict:
    docs = retriever.retrieve(query, jurisdiction, top_k=2)
    
    if not docs:
        return {
            "answer": "No authoritative statutory provisions found in the corpus for the selected jurisdiction.",
            "citations": [],
            "disclaimer": "Information assistant only. Not legal advice."
        }

    context_str = "\n\n".join([
        f"Document: {d['title']} | Section: {d['section']} | Heading: {d['heading']}\nText: {d['text']}"
        for d in docs
    ])

    system_instruction = f"""
    You are IP-SAKTI Sahayak, an information-only legal assistant for Ayurvedic intellectual property.
    Jurisdiction constraint: STRICTLY {jurisdiction}. Never cite documents from other jurisdictions.
    You do NOT provide legal advice. Ground your entire answer strictly in the provided Context.
    
    Format your response in JSON with these exact keys:
    - answer: Concise, factual answer addressing the user's question directly.
    - citations: A list of objects with keys: "statute", "section", "snippet", "doc_id".
    - confidence_score: float (0.80 to 0.99).
    """

    prompt = f"""
    Context:
    {context_str}

    Formulation Focus: {formulation_type}
    User Query: {query}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    result = json.loads(response.text)
    result["raw_docs"] = docs
    return result
