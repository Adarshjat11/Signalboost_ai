from typing import List

def get_company_funding_data(industry: str, location: str, keywords: List[str]) -> List[dict]:
    """
    Simulated Crunchbase-like data. Replace with real scraping/API from Crunchbase Pro or CB API.
    """
    mock_funding_data = [
        {
            "company": "NeuroAI Labs",
            "funding_rounds": 2,
            "total_funding": 4500000,
            "last_funding_date": "2023-12-10",
            "investors": ["Sequoia", "Index Ventures"],
            "stage": "Seed"
        },
        {
            "company": "Datavine Systems",
            "funding_rounds": 1,
            "total_funding": 2000000,
            "last_funding_date": "2024-06-01",
            "investors": ["Accel"],
            "stage": "Pre-Seed"
        }
    ]

    return mock_funding_data