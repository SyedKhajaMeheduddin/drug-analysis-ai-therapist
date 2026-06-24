import requests
from difflib import SequenceMatcher

OPENFDA_BASE = "https://api.fda.gov/drug/ndc.json"

# Local fallback drug dictionary for offline/quick matching
LOCAL_DRUG_DB = {
    "paracetamol": "Paracetamol", "acetaminophen": "Acetaminophen",
    "ibuprofen": "Ibuprofen", "aspirin": "Aspirin",
    "amoxicillin": "Amoxicillin", "metformin": "Metformin",
    "atorvastatin": "Atorvastatin", "omeprazole": "Omeprazole",
    "cetirizine": "Cetirizine", "azithromycin": "Azithromycin",
    "dolo": "Paracetamol", "crocin": "Paracetamol",
    "brufen": "Ibuprofen", "combiflam": "Ibuprofen + Paracetamol",
    "pan": "Pantoprazole", "pantoprazole": "Pantoprazole",
    "doxycycline": "Doxycycline", "ciprofloxacin": "Ciprofloxacin",
    "metronidazole": "Metronidazole", "ranitidine": "Ranitidine",
}

def exact_match(tokens: list) -> dict | None:
    """Check tokens against local drug dictionary (exact, case-insensitive)."""
    for token in tokens:
        key = token.lower()
        if key in LOCAL_DRUG_DB:
            return {"drug_name": LOCAL_DRUG_DB[key], "match_type": "exact", "token": token}
    return None

def fuzzy_match(tokens: list, threshold: float = 0.75) -> dict | None:
    """Fuzzy match tokens against local DB using SequenceMatcher."""
    best = None
    best_score = 0
    for token in tokens:
        for key, name in LOCAL_DRUG_DB.items():
            score = SequenceMatcher(None, token.lower(), key).ratio()
            if score > best_score and score >= threshold:
                best_score = score
                best = {"drug_name": name, "match_type": "fuzzy", "score": round(score, 3), "token": token}
    return best

def api_match(tokens: list) -> dict | None:
    """Query openFDA NDC API for each token."""
    for token in tokens:
        if len(token) < 3:
            continue
        try:
            params = {
                "search": f'brand_name:"{token}"+generic_name:"{token}"',
                "limit": 1,
            }
            resp = requests.get(OPENFDA_BASE, params=params, timeout=5)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    r = results[0]
                    return {
                        "drug_name": r.get("brand_name", token),
                        "match_type": "api",
                        "token": token,
                        "raw": r,
                    }
        except Exception:
            continue
    return None

def identify_drug(tokens: list) -> dict:
    """
    Multi-level drug identification:
    1. Exact local match
    2. Fuzzy local match
    3. openFDA API match
    4. Return top candidates if nothing found
    """
    result = exact_match(tokens)
    if result:
        return result

    result = fuzzy_match(tokens)
    if result:
        return result

    result = api_match(tokens)
    if result:
        return result

    # Return top candidates as fallback
    candidates = []
    for token in tokens[:5]:
        best_score = 0
        best_name = token
        for key, name in LOCAL_DRUG_DB.items():
            score = SequenceMatcher(None, token.lower(), key).ratio()
            if score > best_score:
                best_score = score
                best_name = name
        candidates.append({"token": token, "candidate": best_name, "score": round(best_score, 3)})

    return {
        "drug_name": None,
        "match_type": "no_match",
        "candidates": sorted(candidates, key=lambda x: x["score"], reverse=True),
    }
