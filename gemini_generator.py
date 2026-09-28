import requests

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = "AIzaSyDeL1_kuS6ZWhlKxH4ApiFw9jCTsF_VfcI"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={self.api_key}"

    def generate_document(self, doc_type, parties, terms, dates):
        prompt = f"""
        Generate a legal document of type {doc_type}.
        Parties involved: {parties}
        Terms & Conditions: {terms}
        Effective Date: {dates}
        """
        
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(self.url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"API Error Details: {response.text}")
            
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected API response structure: {response.text}")