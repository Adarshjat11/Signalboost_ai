from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import traceback
from fastapi.responses import JSONResponse

# Import functions from main modules
from ..linkedin_scraper import get_leads_from_linkedin
from ..crunchbase_scraper import get_company_funding_data
from ..job_board_scraper import get_job_postings
from ..hunter import enrich_lead
from ..rule_based import score_leads

router = APIRouter(prefix="/leads", tags=["leads"])

# Pydantic Models
class LeadRequest(BaseModel):
    industry: str
    location: str
    keywords: List[str] = []

def generate_comprehensive_leads(industry: str, location: str, keywords: List[str]) -> List[dict]:
    """
    Generate leads using multiple data sources and enrich them with additional information.
    """
    # Get base leads from LinkedIn
    raw_leads = get_leads_from_linkedin(industry, location, keywords)
    
    # Get additional data sources
    funding_data = get_company_funding_data(industry, location, keywords)
    job_data = get_job_postings(industry, location, keywords)
    
    # Create lookup dictionaries for additional data
    funding_lookup = {item["company"]: item for item in funding_data}
    job_lookup = {item["company"]: item for item in job_data}
    
    # Enrich leads with additional data
    enriched_leads = []
    for lead in raw_leads:
        company_name = lead.get("company", "")
        
        # Add funding data if available
        if company_name in funding_lookup:
            funding_info = funding_lookup[company_name]
            lead.update({
                "funding_rounds": funding_info.get("funding_rounds", 0),
                "total_funding": funding_info.get("total_funding", 0),
                "last_funding_date": funding_info.get("last_funding_date", ""),
                "investors": funding_info.get("investors", []),
                "funding_stage": funding_info.get("stage", "")
            })
        
        # Add job posting data if available
        if company_name in job_lookup:
            job_info = job_lookup[company_name]
            lead.update({
                "open_roles": job_info.get("roles", []),
                "job_postings_count": job_info.get("postings", 0),
                "recent_hiring_activity": job_info.get("recent_activity", "")
            })
        
        enriched_leads.append(lead)
    
    return enriched_leads

@router.post("/generate")
def generate_leads(req: LeadRequest):
    """
    Generate and score leads based on industry, location, and keywords.
    """
    try:
        # Generate comprehensive leads with all data sources
        raw_leads = generate_comprehensive_leads(req.industry, req.location, req.keywords)
        
        # Enrich with email data
        enriched_leads = [enrich_lead(lead) for lead in raw_leads]
        
        # Score the leads
        scored_leads = score_leads(enriched_leads)
        
        # Sort by score (highest first)
        scored_leads.sort(key=lambda x: x.get("score", 0), reverse=True)

        return {
            "leads": scored_leads, 
            "count": len(scored_leads),
            "summary": {
                "high_priority": len([l for l in scored_leads if l.get("priority") == "high"]),
                "medium_priority": len([l for l in scored_leads if l.get("priority") == "medium"]),
                "low_priority": len([l for l in scored_leads if l.get("priority") == "low"])
            }
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "trace": traceback.format_exc()
        })

@router.get("/funding-data")
def get_funding_data(industry: str, location: str, keywords: str = ""):
    """
    Get funding data for companies in specified industry and location.
    """
    try:
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []
        funding_data = get_company_funding_data(industry, location, keyword_list)
        return {"funding_data": funding_data, "count": len(funding_data)}
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "trace": traceback.format_exc()
        })

@router.get("/job-postings")
def get_job_data(industry: str, location: str, keywords: str = ""):
    """
    Get job posting data for companies in specified industry and location.
    """
    try:
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []
        job_data = get_job_postings(industry, location, keyword_list)
        return {"job_data": job_data, "count": len(job_data)}
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "trace": traceback.format_exc()
        }) 