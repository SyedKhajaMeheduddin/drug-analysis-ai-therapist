import requests

OPENFDA_NDC = "https://api.fda.gov/drug/ndc.json"
OPENFDA_LABEL = "https://api.fda.gov/drug/label.json"

def fetch_drug_info(drug_name: str) -> dict:
    """
    Fetch enriched drug information from openFDA:
    - Generic name, brand name, dosage form, manufacturer
    - Route of administration, marketing status
    - Warnings and health risks from label API
    """
    info = {
        "brand_name": drug_name,
        "generic_name": "N/A",
        "dosage_form": "N/A",
        "route": "N/A",
        "manufacturer": "N/A",
        "marketing_status": "N/A",
        "warnings": [],
        "indications": "N/A",
        "adverse_reactions": "N/A",
        "source": "local",
    }

    # Query NDC endpoint
    try:
        params = {"search": f'brand_name:"{drug_name}"', "limit": 1}
        resp = requests.get(OPENFDA_NDC, params=params, timeout=6)
        if resp.status_code == 200 and resp.json().get("results"):
            r = resp.json()["results"][0]
            info["brand_name"] = r.get("brand_name", drug_name)
            info["generic_name"] = r.get("generic_name", "N/A")
            info["dosage_form"] = r.get("dosage_form", "N/A")
            info["route"] = ", ".join(r.get("route", ["N/A"]))
            info["manufacturer"] = r.get("labeler_name", "N/A")
            info["marketing_status"] = r.get("marketing_status", "N/A")
            info["source"] = "openFDA NDC"
    except Exception:
        pass

    # Query Label endpoint for warnings and indications
    try:
        params = {"search": f'openfda.brand_name:"{drug_name}"', "limit": 1}
        resp = requests.get(OPENFDA_LABEL, params=params, timeout=6)
        if resp.status_code == 200 and resp.json().get("results"):
            r = resp.json()["results"][0]
            warnings = r.get("warnings", r.get("warnings_and_cautions", []))
            info["warnings"] = warnings[:2] if warnings else []
            indications = r.get("indications_and_usage", [])
            info["indications"] = indications[0][:400] if indications else "N/A"
            adverse = r.get("adverse_reactions", [])
            info["adverse_reactions"] = adverse[0][:400] if adverse else "N/A"
            info["source"] = "openFDA Label"
    except Exception:
        pass

    # Fallback static data for common drugs
    static = _static_drug_info(drug_name)
    for k, v in static.items():
        if info[k] in ("N/A", [], ""):
            info[k] = v

    return info

def _static_drug_info(name: str) -> dict:
    """Static fallback data for common drugs."""
    db = {
        "Paracetamol": {
            "generic_name": "Acetaminophen",
            "dosage_form": "Tablet / Syrup",
            "route": "Oral",
            "manufacturer": "Various",
            "indications": "Relief of mild to moderate pain and reduction of fever.",
            "warnings": ["Do not exceed recommended dose.", "Avoid alcohol while taking this medication."],
            "adverse_reactions": "Rare: liver damage with overdose, skin rash.",
        },
        "Ibuprofen": {
            "generic_name": "Ibuprofen",
            "dosage_form": "Tablet / Capsule",
            "route": "Oral",
            "manufacturer": "Various",
            "indications": "Relief of pain, fever, and inflammation. Used for headache, arthritis, menstrual cramps.",
            "warnings": ["May increase risk of heart attack or stroke.", "Take with food to avoid stomach upset."],
            "adverse_reactions": "Stomach pain, heartburn, nausea, dizziness.",
        },
        "Amoxicillin": {
            "generic_name": "Amoxicillin",
            "dosage_form": "Capsule / Suspension",
            "route": "Oral",
            "manufacturer": "Various",
            "indications": "Bacterial infections of ear, nose, throat, urinary tract, and skin.",
            "warnings": ["Discontinue if allergic reaction occurs.", "Complete the full course."],
            "adverse_reactions": "Diarrhea, nausea, skin rash, vomiting.",
        },
    }
    # Match by partial name
    for k, v in db.items():
        if k.lower() in name.lower() or name.lower() in k.lower():
            return v
    return {}
