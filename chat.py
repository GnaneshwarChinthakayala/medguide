"""Interactive MedGuide chat. Usage: python chat.py [--session-id NAME]"""
import argparse

from medguide.agent import build_agent

parser = argparse.ArgumentParser()
parser.add_argument("--session-id", default="medguide-demo")
args = parser.parse_args()

agent = build_agent(session_id=args.session_id)
print("MedGuide - plain-language medicine explainer. Type 'quit' to exit.")
print('Try: "My prescription says dolo, ecosprin and warfarin. Explain them simply."\n')
while True:
    try:
        text = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break
    if text.lower() in {"quit", "exit", "q"}:
        break
    if not text:
        continue
    print("\nMedGuide: ", end="")
    agent(text)
    print()
