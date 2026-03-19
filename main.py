from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
import io

# Import des templates
from templates.cv import generate_cv
from templates.business import generate_business
from templates.tiktok import generate_tiktok
from templates.formation import generate_formation
from templates.guide import generate_guide
from templates.ebook import generate_ebook

app = FastAPI(title="PDF Cash IA — Render API", version="1.0.0")

# CORS — autoriser Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MODÈLES DE DONNÉES ──
class FacebookAds(BaseModel):
    titre_pub: Optional[str] = ""
    texte_principal: Optional[str] = ""
    description: Optional[str] = ""
    cta_bouton: Optional[str] = ""
    ciblage_suggere: Optional[str] = ""

class Chapter(BaseModel):
    title: Optional[str] = ""
    content: Optional[str] = ""

class ColorConfig(BaseModel):
    c1: Optional[str] = "#7c3aed"
    c2: Optional[str] = "#0d1030"
    ac: Optional[str] = "#7c3aed"

class ContentData(BaseModel):
    title: Optional[str] = ""
    subtitle: Optional[str] = ""
    author: Optional[str] = ""
    tagline: Optional[str] = ""
    description: Optional[str] = ""
    price_suggested: Optional[str] = "5 000 FCFA"
    table_of_contents: Optional[List[str]] = []
    chapters: Optional[List[Chapter]] = []
    key_takeaways: Optional[List[str]] = []
    call_to_action: Optional[str] = ""
    sales_message: Optional[str] = ""
    viral_hook: Optional[str] = ""
    facebook_ads: Optional[FacebookAds] = None

class PDFRequest(BaseModel):
    content: ContentData
    docType: Optional[str] = "ebook"
    docLabel: Optional[str] = "Ebook"
    color: Optional[ColorConfig] = None
    authorName: Optional[str] = ""

# ── ROUTES ──

@app.get("/")
def root():
    return {
        "status": "PDF Cash IA — Render API en ligne",
        "version": "1.0.0",
        "endpoints": ["/generate", "/health"]
    }

@app.get("/health")
def health():
    return { "status": "ok" }

@app.post("/generate")
def generate_pdf(req: PDFRequest):
    """
    Génère un PDF selon le type de document demandé.
    Retourne le PDF binaire directement.
    """
    doc_type = req.docType or "ebook"
    content  = req.content
    color    = req.color
    author   = req.authorName or content.author or "Expert Digital Afrique"

    try:
        # Routing par type
        if doc_type == "cv":
            pdf_bytes = generate_cv(content, color, author)
        elif doc_type == "business_plan":
            pdf_bytes = generate_business(content, color, author)
        elif doc_type == "tiktok":
            pdf_bytes = generate_tiktok(content, color, author)
        elif doc_type == "formation":
            pdf_bytes = generate_formation(content, color, author)
        elif doc_type == "guide":
            pdf_bytes = generate_guide(content, color, author)
        else:
            # ebook par défaut
            pdf_bytes = generate_ebook(content, color, author)

        # Nom du fichier
        safe_title = (content.title or "document") \
            .encode("ascii", "ignore").decode() \
            .replace(" ", "_")[:40]
        filename = f"{safe_title}_{doc_type}.pdf"

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Length": str(len(pdf_bytes))
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur generation PDF: {str(e)}")
