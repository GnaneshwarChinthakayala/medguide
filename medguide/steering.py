from strands.vended_plugins.steering import (Guide, LedgerProvider,
                                             LLMSteeringHandler, Proceed,
                                             SteeringHandler,
                                             ToolSteeringAction)


class InteractionFirstHandler(SteeringHandler):
    """Deterministic rule: interactions must be checked BEFORE any medicine is explained."""

    name = "interaction-first"

    def __init__(self):
        super().__init__(context_providers=[LedgerProvider()])

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        if tool_use.get("name") != "get_drug_info":
            return Proceed(reason="Not an explanation step")
        ledger = self.steering_context.data.get("ledger", {})
        calls = ledger.get("tool_calls", [])
        checked = any(c["tool_name"] == "check_interactions" and c["status"] == "success"
                      for c in calls)
        if not checked:
            return Guide(reason="Safety first: call check_interactions with ALL of the "
                                "user's medicines before explaining any medicine.")
        return Proceed(reason="Interactions were checked first")


class SafetyGuardrailHandler(LLMSteeringHandler):
    """LLM review of each drafted reply for medical-safety rules."""

    name = "safety-guardrail"

    def __init__(self):
        super().__init__(
            system_prompt="""You review replies from MedGuide, a medicine explainer for people with low health literacy.
The reply must:
- NEVER tell the user to start, stop, skip, increase, decrease or change the dose of any medicine
- NEVER diagnose a condition
- Say a pharmacist or doctor should be asked whenever something is flagged, unclear or not verified
- Not claim two medicines are 'safe together' just because no interaction was found
- Use simple words and short sentences
- Include the reminder that MedGuide is not a doctor or pharmacist
If the reply breaks any rule, give specific guidance on how to fix it."""
        )
