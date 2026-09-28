from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str

@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        # Indha line-a try-kku ulle potadhaal ipo ovvoru muraiyum pudhu key load aagum!
        generator = GeminiDocumentGenerator()
        
        response = generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates
        )
        return {"document": response}
    except Exception as e:
        print("===============================")
        print("GEMINI ERROR DETAILS:", str(e))
        print("===============================")
        raise HTTPException(status_code=500, detail=str(e))