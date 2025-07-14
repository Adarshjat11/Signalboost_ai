from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import traceback
from fastapi.responses import JSONResponse

# Import functions from main modules
from ..hunter import enrich_lead

router = APIRouter(prefix="/enrich", tags=["enrich"])

class EnrichRequest(BaseModel):
    leads: List[dict]

@router.post("/emails")
def enrich_leads_with_emails(req: EnrichRequest):
    """
    Enrich a list of leads with email addresses using Hunter.io API.
    """
    try:
        enriched_leads = [enrich_lead(lead) for lead in req.leads]
        
        return {
            "enriched_leads": enriched_leads,
            "count": len(enriched_leads),
            "summary": {
                "with_emails": len([l for l in enriched_leads if l.get("email")]),
                "verified_emails": len([l for l in enriched_leads if l.get("email_verified")])
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "trace": traceback.format_exc()
        })

@router.post("/single")
def enrich_single_lead(lead: dict):
    """
    Enrich a single lead with email data.
    """
    try:
        enriched_lead = enrich_lead(lead)
        return {"enriched_lead": enriched_lead}
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "trace": traceback.format_exc()
        }) 