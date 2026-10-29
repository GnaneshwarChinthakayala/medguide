"""Small DEMO reference data for MedGuide.

This is NOT a complete or clinically validated database. Replace it with a
vetted source (for example openFDA or DrugBank) before any real-world use.
No dosing information is stored on purpose.
"""
import re

DISCLAIMER = (
    "MedGuide is an educational tool, not a doctor or a pharmacist. It cannot "
    "diagnose you or change your treatment. Please check with a pharmacist or "
    "doctor before you change anything about your medicines."
)

DRUGS = {
    "paracetamol": {
        "aliases": ["acetaminophen", "dolo", "crocin", "calpol"],
        "purpose": "Relieves mild to moderate pain and brings down fever.",
        "notes": "Many cold and flu products also contain paracetamol. Taking more than the label or your doctor allows can seriously harm the liver.",
        "call_doctor_if": "you have yellowing of the skin or eyes, or you are unsure how much you have taken.",
    },
    "ibuprofen": {
        "aliases": ["brufen", "advil"],
        "purpose": "Relieves pain, swelling and fever (an NSAID pain reliever).",
        "notes": "It can upset the stomach and is usually taken with food. It can affect the kidneys and raise blood pressure.",
        "call_doctor_if": "you have black stools, stomach pain that does not go away, or swelling in your legs.",
    },
    "aspirin": {
        "aliases": ["ecosprin", "disprin"],
        "purpose": "Relieves pain and fever. Low-dose aspirin is also prescribed to lower the risk of blood clots.",
        "notes": "It makes bleeding more likely and can irritate the stomach.",
        "call_doctor_if": "you have black stools, vomit blood, or bleed easily.",
    },
    "warfarin": {
        "aliases": [],
        "purpose": "A blood thinner that helps prevent dangerous blood clots.",
        "notes": "It needs regular blood tests. Changes in diet, other medicines and alcohol can change how strongly it works.",
        "call_doctor_if": "you notice unusual bruising, bleeding gums, blood in urine or stool, or you fall and hit your head.",
    },
    "metformin": {
        "aliases": ["glycomet"],
        "purpose": "Lowers blood sugar in people with type 2 diabetes.",
        "notes": "Stomach upset is common at first. It is often taken with meals.",
        "call_doctor_if": "you have repeated vomiting, severe stomach pain, or unusual tiredness with fast breathing.",
    },
    "lisinopril": {
        "aliases": [],
        "purpose": "Lowers blood pressure and helps protect the heart and kidneys.",
        "notes": "A dry cough is a common side effect.",
        "call_doctor_if": "you have swelling of the face, lips or tongue (get emergency help), or you feel very dizzy or faint.",
    },
    "amlodipine": {
        "aliases": [],
        "purpose": "Lowers blood pressure and can help with chest pain from angina.",
        "notes": "Ankle swelling and flushing can happen.",
        "call_doctor_if": "swelling gets worse or you feel faint.",
    },
    "atorvastatin": {
        "aliases": [],
        "purpose": "Lowers cholesterol to reduce the risk of heart attack and stroke.",
        "notes": "Tell your doctor about unexplained muscle pain or weakness.",
        "call_doctor_if": "you have severe muscle pain, weakness, or dark urine.",
    },
    "simvastatin": {
        "aliases": [],
        "purpose": "Lowers cholesterol to reduce the risk of heart attack and stroke.",
        "notes": "Tell your doctor about unexplained muscle pain or weakness.",
        "call_doctor_if": "you have severe muscle pain, weakness, or dark urine.",
    },
    "omeprazole": {
        "aliases": [],
        "purpose": "Reduces stomach acid for acid reflux and stomach ulcers.",
        "notes": "It is often taken before a meal.",
        "call_doctor_if": "you have trouble swallowing, vomiting blood, or black stools.",
    },
    "sildenafil": {
        "aliases": [],
        "purpose": "Treats erectile dysfunction, and in some brands a lung blood pressure problem.",
        "notes": "It must never be combined with nitrate medicines.",
        "call_doctor_if": "you have chest pain, sudden vision or hearing loss, or an erection lasting a long time.",
    },
    "nitroglycerin": {
        "aliases": ["glyceryl trinitrate", "gtn"],
        "purpose": "Relieves or prevents chest pain from angina by opening blood vessels.",
        "notes": "It can cause headache and dizziness. It must never be combined with sildenafil-type medicines.",
        "call_doctor_if": "chest pain is not relieved as your doctor told you (call emergency services).",
    },
    "sertraline": {
        "aliases": [],
        "purpose": "An antidepressant used for depression and anxiety.",
        "notes": "It can take weeks to work. Stopping suddenly can cause unpleasant effects, so changes should be guided by a doctor.",
        "call_doctor_if": "your mood gets worse, you have thoughts of self-harm, or you feel very agitated or confused.",
    },
    "tramadol": {
        "aliases": [],
        "purpose": "A strong pain reliever.",
        "notes": "It can cause drowsiness and dizziness, and can be habit-forming.",
        "call_doctor_if": "you feel very sleepy, confused, or have trouble breathing (get emergency help).",
    },
    "clarithromycin": {
        "aliases": [],
        "purpose": "An antibiotic for bacterial infections.",
        "notes": "It can change how other medicines work in the body.",
        "call_doctor_if": "you have severe diarrhea, a rash, or a very fast heartbeat.",
    },
    "potassium chloride": {
        "aliases": ["potassium"],
        "purpose": "A supplement used to treat or prevent low potassium.",
        "notes": "Too much potassium can affect the heart rhythm.",
        "call_doctor_if": "you have muscle weakness or an irregular heartbeat.",
    },
}

INTERACTIONS = [
    {"pair": ("warfarin", "aspirin"), "severity": "major",
     "effect": "Together they raise the chance of serious bleeding.",
     "advice": "Do not combine unless your doctor planned it. Ask your doctor or pharmacist today."},
    {"pair": ("warfarin", "ibuprofen"), "severity": "major",
     "effect": "Together they raise the chance of serious bleeding, including stomach bleeding.",
     "advice": "Ask your doctor or pharmacist about a safer pain reliever."},
    {"pair": ("sildenafil", "nitroglycerin"), "severity": "contraindicated",
     "effect": "Together they can cause a sudden, dangerous drop in blood pressure.",
     "advice": "This combination should not be used. Contact your doctor or pharmacist right away."},
    {"pair": ("simvastatin", "clarithromycin"), "severity": "major",
     "effect": "The antibiotic can raise simvastatin levels in the body and increase the risk of serious muscle damage.",
     "advice": "Tell your doctor or pharmacist before taking both."},
    {"pair": ("sertraline", "tramadol"), "severity": "major",
     "effect": "Together they can cause a dangerous reaction called serotonin syndrome and raise the risk of seizures.",
     "advice": "Ask your doctor or pharmacist before taking both."},
    {"pair": ("lisinopril", "potassium chloride"), "severity": "major",
     "effect": "Together they can push potassium in the blood too high, which can affect the heart.",
     "advice": "Your doctor should check your blood potassium. Ask them or your pharmacist."},
    {"pair": ("lisinopril", "ibuprofen"), "severity": "moderate",
     "effect": "Ibuprofen can weaken the blood pressure effect and strain the kidneys.",
     "advice": "Ask your pharmacist before using ibuprofen regularly."},
    {"pair": ("aspirin", "ibuprofen"), "severity": "moderate",
     "effect": "Together they raise the chance of stomach bleeding, and ibuprofen can reduce the heart-protecting effect of low-dose aspirin.",
     "advice": "Ask your pharmacist how to use them safely."},
    {"pair": ("warfarin", "clarithromycin"), "severity": "major",
     "effect": "The antibiotic can make warfarin stronger and raise the chance of bleeding.",
     "advice": "Your doctor may need to check your blood more often. Ask them or your pharmacist."},
]

SOURCE_NOTE = ("Source: MedGuide demo reference list (general drug-labeling "
               "knowledge, not a complete or validated database).")

INDEX = {}
for _canon, _d in DRUGS.items():
    INDEX[_canon] = _canon
    for _a in _d["aliases"]:
        INDEX[_a] = _canon


def resolve(name):
    """Return the canonical drug name for a typed name or brand, or None."""
    n = " ".join(re.sub(r"[^a-z ]", " ", name.lower()).split())
    if n in INDEX:
        return INDEX[n]
    for tok in n.split():
        if tok in INDEX:
            return INDEX[tok]
    return None


def find_in_text(text):
    t = text.lower()
    found = []
    for term, canon in INDEX.items():
        if re.search(r"\b" + re.escape(term) + r"\b", t) and canon not in found:
            found.append(canon)
    return found


def lookup_pair(a, b):
    key = frozenset((a, b))
    for item in INTERACTIONS:
        if frozenset(item["pair"]) == key:
            return item
    return None
