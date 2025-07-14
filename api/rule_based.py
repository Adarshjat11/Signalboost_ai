from typing import List

def score_leads(leads: List[dict]) -> List[dict]:
    """
    Apply an enhanced rule-based scoring system to each lead.
    Adds 'score', 'priority', and 'score_rationale' fields.
    """
    scored_leads = []

    for lead in leads:
        score = 0
        rationale = []

        # Rule 1: Employee size bonus
        emp_count = lead.get("employees", 0)
        if isinstance(emp_count, str):
            try:
                emp_count = int(emp_count.replace(",", ""))
            except:
                emp_count = 0

        if 10 <= emp_count <= 50:
            score += 10
            rationale.append("Ideal team size (10–50)")
        elif 51 <= emp_count <= 200:
            score += 8
            rationale.append("Scalable team (51–200)")
        elif emp_count > 200:
            score += 5
            rationale.append("Established company (>200)")

        # Rule 2: Revenue bonus
        revenue = str(lead.get("revenue", "")).replace(",", "")
        if "$1M" in revenue or "$2" in revenue:
            score += 8
            rationale.append("Strong early-stage revenue")
        elif "$3" in revenue or "$4" in revenue:
            score += 6
            rationale.append("Mid-growth revenue")
        elif "$5" in revenue or "$25" in revenue:
            score += 4
            rationale.append("Healthy revenue")

        # Rule 3: Email verified
        if lead.get("email_verified"):
            score += 10
            rationale.append("Verified email found")

        # Rule 4: Role bonus
        title = str(lead.get("title", "")).lower()
        if "ceo" in title or "founder" in title:
            score += 8
            rationale.append("Top-level decision maker")
        elif "coo" in title or "vp" in title:
            score += 5
            rationale.append("Senior leadership")

        # Rule 5: Funding influence (optional)
        funding = lead.get("total_funding", 0)
        try:
            funding = float(funding)
        except:
            funding = 0

        if funding > 5_000_000:
            score += 10
            rationale.append("Well-funded startup ($5M+)")
        elif funding > 1_000_000:
            score += 5
            rationale.append("Seed-funded company ($1M+)")

        # Rule 6: Keywords boost
        keywords = lead.get("keywords", [])
        for keyword in ["AI", "automation", "analytics", "machine learning"]:
            if any(keyword.lower() in str(k).lower() for k in keywords):
                score += 2
                rationale.append(f"Contains keyword: {keyword}")

        # Determine priority tier
        if score >= 80:
            priority = "high"
        elif score >= 60:
            priority = "medium"
        else:
            priority = "low"

        lead.update({
            "score": score,
            "priority": priority,
            "score_rationale": rationale
        })