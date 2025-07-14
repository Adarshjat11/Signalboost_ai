import os
import httpx
from dotenv import load_dotenv

load_dotenv()
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

BASE_URL = "https://api.hunter.io/v2/domain-search"


def enrich_lead(lead: dict) -> dict:
    """
    Enrich a lead dictionary with email addresses using Hunter.io API.
    Adds multiple fields: email, verified status, position, and source.
    """
    domain = lead.get("domain")
    if not domain or not HUNTER_API_KEY:
        lead.update({
            "email": None,
            "email_verified": False,
            "email_position": None,
            "email_source": None
        })
        return lead

    try:
        response = httpx.get(BASE_URL, params={
            "domain": domain,
            "api_key": HUNTER_API_KEY
        })
        response.raise_for_status()

        data = response.json()
        emails = data.get("data", {}).get("emails", [])

        if emails:
            top_email = emails[0]
            lead.update({
                "email": top_email.get("value"),
                "email_verified": top_email.get("verification") == "verified",
                "email_position": top_email.get("position"),
                "email_source": top_email.get("sources", [{}])[0].get("uri")
            })
        else:
            lead.update({
                "email": None,
                "email_verified": False,
                "email_position": None,
                "email_source": None
            })

    except Exception as e:
        print(f"[ERROR] Hunter enrichment failed for {domain}: {e}")
        lead.update({
            "email": None,
            "email_verified": False,
            "email_position": None,
            "email_source": None
        })

    return lead


# Run for test
if __name__ == "__main__":
    test_lead = {
        "company": "NeuroAI Labs",
        "domain": "neuroai.io"
    }
    enriched = enrich_lead(test_lead)
    print(enriched)