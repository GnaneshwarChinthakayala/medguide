---
name: explain-prescription
description: Steps for explaining a prescription or list of medicines in plain language. Use when the user shares medicines and wants to understand them.
---

# Explain a prescription

1. Call parse_prescription on what the user typed.
2. Call check_interactions with ALL recognized medicines (even if only one).
3. Call get_drug_info for each recognized medicine.
4. Write the explanation in short sentences: what each medicine is for, one thing to know, when to call a doctor.
5. Put any interaction FLAG first, before the individual explanations.
6. List any medicine that could not be verified and tell the user to ask a pharmacist.
7. If the user asked for another language, call translate_text on the final text.
8. End with the reminder that you are not a doctor or pharmacist.

Never give doses and never tell the user to start, stop or change a medicine.
