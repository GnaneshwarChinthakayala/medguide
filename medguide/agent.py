import os
from pathlib import Path

from strands import Agent, AgentSkills
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models import BedrockModel
from strands.session.file_session_manager import FileSessionManager

from .hooks import AuditLogHook, RateLimiterHook
from .steering import InteractionFirstHandler, SafetyGuardrailHandler
from .tools import (check_interactions, emergency_check, get_drug_info,
                    parse_prescription, translate_text)

SKILLS_DIR = str(Path(__file__).resolve().parent.parent / "skills")

# Event credits only cover Amazon Nova models. Override with MEDGUIDE_MODEL if needed
# (for example "us.amazon.nova-pro-v1:0" if your account needs an inference profile).
MODEL_ID = os.environ.get("MEDGUIDE_MODEL", "amazon.nova-pro-v1:0")

SYSTEM_PROMPT = """You are MedGuide, a medicine explainer for people with low health literacy.
Rules:
- Use simple words (about grade 6 reading level) and short sentences.
- Workflow: parse_prescription, then check_interactions (always, even for one medicine), then get_drug_info for each medicine, then explain.
- Only state facts returned by your tools. If a medicine or a pair is not in the tools' data, say it could not be verified and tell the user to ask a pharmacist.
- Never tell the user to start, stop, skip, or change the dose of any medicine. Never diagnose. Tell them to ask their doctor or pharmacist.
- If the user mentions symptoms, call emergency_check first and follow its result.
- If the user wants another language, call translate_text on your final explanation (te Telugu, hi Hindi, ta Tamil, bn Bengali, mr Marathi, ur Urdu). If translation is unavailable, answer in English and say so.
- Always end with a short reminder that you are not a doctor or pharmacist."""


def build_agent(session_id: str | None = None, llm_steering: bool | None = None,
                audit_path: str | None = "audit.log") -> Agent:
    if llm_steering is None:
        llm_steering = os.environ.get("MEDGUIDE_LLM_STEERING", "0") == "1"

    plugins = [AgentSkills(skills=[SKILLS_DIR]), InteractionFirstHandler()]
    if llm_steering:
        plugins.append(SafetyGuardrailHandler())

    kwargs = dict(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[parse_prescription, check_interactions, get_drug_info,
               emergency_check, translate_text],
        hooks=[RateLimiterHook(max_calls=6), AuditLogHook(path=audit_path)],
        plugins=plugins,
        system_prompt=SYSTEM_PROMPT,
        conversation_manager=SlidingWindowConversationManager(window_size=20),
    )
    if session_id:
        kwargs["session_manager"] = FileSessionManager(
            session_id=session_id, storage_dir="./sessions")
    return Agent(**kwargs)
