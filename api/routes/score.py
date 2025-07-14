from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import traceback
from fastapi.responses import JSONResponse

# Import functions from main modules
from ..rule_based import score_leads

router = APIRouter(prefix="/score", tags=["score"])

class ScoreRequest(BaseModel):
    leads: List[dict]

@router.post("/leads")
def score_leads_endpoint(req: ScoreRequest):
    """
    Score a list of leads using the rule-based scoring system.
    """
    try:
        scored_leads = score_leads(req.leads)
        
        # Sort by score (highest first)
        scored_leads.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return {
            "scored_leads": scored_leads,
            "count": len(scored_leads),
            "summary": {
                "high_priority": len([l for l in scored_leads if l.get("priority") == "high"]),
                "medium_priority": len([l for l in scored_leads if l.get("priority") == "medium"]),
                "low_priority": len([l for l in scored_leads if l.get("priority") == "low"]),
                "average_score": sum(l.get("score", 0) for l in scored_leads) / len(scored_leads) if scored_leads else 0
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "trace": traceback.format_exc()
        })

@router.get("/rules")
def get_scoring_rules():
    """
    Get information about the scoring rules used.
    """
    return {
        "scoring_rules": {
            "employee_size": {
                "10-50": "10 points - Ideal team size",
                "51-200": "8 points - Scalable team", 
                "200+": "5 points - Established company"
            },
            "revenue": {
                "$1M-$2M": "8 points - Strong early-stage revenue",
                "$3M-$4M": "6 points - Mid-growth revenue",
                "$5M+": "4 points - Healthy revenue"
            },
            "email_verified": "10 points - Verified email found",
            "role": {
                "CEO/Founder": "8 points - Top-level decision maker",
                "COO/VP": "5 points - Senior leadership"
            },
            "funding": {
                "$5M+": "10 points - Well-funded startup",
                "$1M+": "5 points - Seed-funded company"
            },
            "keywords": "2 points each - AI, automation, analytics, machine learning"
        },
        "priority_tiers": {
            "high": "80+ points",
            "medium": "60-79 points", 
            "low": "<60 points"
        }
    } 