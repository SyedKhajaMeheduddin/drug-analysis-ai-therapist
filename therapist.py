import re

# Concern classification keywords
CATEGORIES = {
    "safety": [
        "safe", "danger", "harmful", "overdose", "allergic", "allergy",
        "reaction", "child", "pregnant", "pregnancy", "elderly", "interact",
        "combination", "mixing", "expire", "expired",
    ],
    "side_effects": [
        "side effect", "side-effect", "nausea", "vomit", "dizzy", "dizziness",
        "headache", "rash", "itching", "stomach", "pain", "swelling",
        "fatigue", "tired", "sleepy", "constipation", "diarrhea", "adverse",
    ],
    "usage": [
        "how", "dose", "dosage", "take", "use", "when", "often", "frequency",
        "meals", "food", "water", "morning", "night", "before", "after",
        "missed", "forget", "schedule",
    ],
    "information": [
        "what", "which", "ingredient", "generic", "brand", "type", "class",
        "work", "treat", "used for", "purpose", "indication",
    ],
}

RESPONSES = {
    "safety": {
        "intro": "Your concern about safety is completely valid and important.",
        "advice": [
            "Always consult a licensed doctor or pharmacist before combining medications.",
            "Store medicines at recommended temperature away from children.",
            "Check expiry dates before taking any medication.",
            "If you experience an allergic reaction (rash, breathing difficulty), seek emergency help immediately.",
            "Pregnant or breastfeeding individuals should always verify safety with their OB/GYN.",
        ],
        "disclaimer": "This is general guidance only. Please consult a healthcare professional for personal medical advice.",
    },
    "side_effects": {
        "intro": "Side effects are a natural concern when taking any medication.",
        "advice": [
            "Mild side effects often subside within a few days as your body adjusts.",
            "Take the medication with food or water if stomach upset occurs.",
            "Never stop a prescribed medication abruptly without consulting your doctor.",
            "Keep a symptom diary to help your doctor understand patterns.",
            "Serious side effects (difficulty breathing, chest pain) require immediate medical attention.",
        ],
        "disclaimer": "Side effect experiences vary by individual. A qualified medical professional can give personalised guidance.",
    },
    "usage": {
        "intro": "Taking medicines correctly is key to effective treatment.",
        "advice": [
            "Follow the dosage instructions on the label or as prescribed.",
            "Take at evenly spaced intervals to maintain consistent levels in your body.",
            "If you miss a dose, take it as soon as you remember — unless it is almost time for the next dose.",
            "Do not double the dose to make up for a missed one.",
            "Complete the full prescribed course even if symptoms improve early.",
        ],
        "disclaimer": "Dosage instructions on your specific prescription or packaging always take priority over general guidance.",
    },
    "information": {
        "intro": "Understanding your medication empowers better health decisions.",
        "advice": [
            "Generic and brand-name drugs contain the same active ingredient and are equally effective.",
            "Drug class tells you how the medication works — antibiotics kill bacteria, analgesics relieve pain.",
            "Your pharmacist is a great resource for quick medication questions.",
            "Always keep a list of all medications you take to share with any new healthcare provider.",
            "Look for the drug's leaflet (package insert) for complete information.",
        ],
        "disclaimer": "For specific questions about your prescription, your doctor or pharmacist is the best source.",
    },
}

def classify_concern(concern: str) -> str:
    """Classify user's concern into one of the therapy categories."""
    text = concern.lower()
    scores = {cat: 0 for cat in CATEGORIES}
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in text:
                scores[cat] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "information"

def generate_response(concern: str, drug_name: str = None) -> dict:
    """
    Generate a structured AI therapist response.
    Returns category, intro, personalized advice, and disclaimer.
    """
    category = classify_concern(concern)
    template = RESPONSES[category]
    drug_ref = f" about {drug_name}" if drug_name else ""

    response = {
        "category": category,
        "category_label": category.replace("_", " ").title(),
        "intro": template["intro"],
        "drug_context": f"Based on your question{drug_ref}, here is what you should know:",
        "advice": template["advice"],
        "disclaimer": template["disclaimer"],
        "concern_echo": concern,
    }
    return response

def save_session(concern: str, response: dict, analysis_id: int = None) -> int | None:
    """Save therapy session to database and return session ID."""
    try:
        from modules.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO therapy_sessions
               (user_concern, concern_category, ai_response, analysis_id)
               VALUES (%s, %s, %s, %s)""",
            (concern, response["category"], str(response["advice"]), analysis_id),
        )
        conn.commit()
        session_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return session_id
    except Exception:
        return None
