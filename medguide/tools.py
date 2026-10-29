import os
from itertools import combinations

from strands import tool

from .data import (DISCLAIMER, DRUGS, SOURCE_NOTE, find_in_text, lookup_pair,
                   resolve)

RED_FLAGS = [
    "chest pain", "trouble breathing", "difficulty breathing", "can't breathe",
    "cannot breathe", "swelling of face", "swelling of the face",
    "swollen face", "swollen lips", "swelling of lips", "severe bleeding",
    "vomiting blood", "vomited blood", "black stool", "black stools",
    "fainted", "fainting", "passed out", "seizure", "overdose",
    "took too many", "suicid", "want to die", "hurt myself",
]


@tool
def parse_prescription(text: str) -> str:
    """Find known medicine names or brand names in prescription text the user typed.

    Args:
        text: The prescription text or list of medicines as the user typed it
    """
    found = find_in_text(text)
    if not found:
        return ("No medicines from MedGuide's reference list were recognized. "
                "Tell the user these could not be verified and to ask a pharmacist.")
    return ("Recognized medicines: " + ", ".join(found) + ". Any other medicine "
            "the user mentioned could not be verified; say so and suggest a pharmacist.")


@tool
def check_interactions(drugs: str) -> str:
    """Check a list of medicines for known interactions. ALWAYS call this before explaining medicines, even for one medicine.

    Args:
        drugs: Comma-separated medicine names, for example "warfarin, aspirin"
    """
    names, unknown = [], []
    for raw in drugs.split(","):
        raw = raw.strip()
        if not raw:
            continue
        canon = resolve(raw)
        if canon and canon not in names:
            names.append(canon)
        elif not canon:
            unknown.append(raw)

    lines = []
    if unknown:
        lines.append("NOT VERIFIED (not in reference list): " + ", ".join(unknown) + ".")
    if len(names) < 2:
        lines.append("Fewer than two known medicines, so no pair could be checked.")
    flagged = 0
    for a, b in combinations(names, 2):
        hit = lookup_pair(a, b)
        if hit:
            flagged += 1
            lines.append(f"FLAG [{hit['severity'].upper()}] {a} + {b}: "
                         f"{hit['effect']} {hit['advice']}")
    if len(names) >= 2 and not flagged:
        lines.append("No interaction was found in MedGuide's small reference list for "
                     "these medicines. This does NOT prove they are safe. Ask a pharmacist.")
    lines.append(SOURCE_NOTE)
    return "\n".join(lines)


@tool
def get_drug_info(drug: str) -> str:
    """Get plain-language information about one medicine: what it is for and what to watch for. Never includes doses.

    Args:
        drug: The medicine name or brand name
    """
    canon = resolve(drug)
    if not canon:
        return (f"'{drug}' is not in MedGuide's reference list. Say it could not be "
                "verified and suggest asking a pharmacist.")
    d = DRUGS[canon]
    return (f"{canon.title()}\nWhat it is for: {d['purpose']}\nGood to know: {d['notes']}\n"
            f"Call your doctor if: {d['call_doctor_if']}\n{DISCLAIMER}")


@tool
def emergency_check(symptoms: str) -> str:
    """Check what the user described for emergency warning signs. Call this whenever the user mentions symptoms.

    Args:
        symptoms: The symptoms or situation as the user described them
    """
    s = symptoms.lower()
    hits = [f for f in RED_FLAGS if f in s]
    if hits:
        return ("URGENT: the user mentioned possible emergency signs (" + ", ".join(hits) +
                "). Tell them to contact their local emergency number now (112 in India) "
                "or go to the nearest hospital, or ask someone nearby to help. "
                "Do not give medicine advice first.")
    return "No emergency keywords detected. This is not a medical assessment."


@tool
def translate_text(text: str, target_language_code: str) -> str:
    """Translate text into the user's language with Amazon Translate. Codes: te Telugu, hi Hindi, ta Tamil, bn Bengali, mr Marathi, ur Urdu.

    Args:
        text: The text to translate
        target_language_code: The language code to translate into, for example te or hi
    """
    try:
        import boto3
        client = boto3.client("translate", region_name=os.environ.get("AWS_REGION", "us-east-1"))
        out = client.translate_text(Text=text, SourceLanguageCode="auto",
                                    TargetLanguageCode=target_language_code)
        return out["TranslatedText"]
    except Exception as e:  # permissions, region, bad code
        return (f"TRANSLATION_UNAVAILABLE ({type(e).__name__}). Answer in English and "
                "tell the user translation is not available right now.")
