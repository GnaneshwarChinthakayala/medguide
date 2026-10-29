# MedGuide

A plain-language medicine explainer built with the Strands Agents SDK on Amazon Bedrock.
It helps people with low health literacy understand what their medicines are for, flags
known dangerous combinations, and always sends them to a pharmacist or doctor instead of
giving dosing advice.

**MedGuide is an educational prototype, not a doctor or pharmacist.** Its reference
data is a small demo list and must be replaced with a vetted source before real use.

## Harness features
- Tools: prescription parsing, drug info, interaction check, emergency check, Amazon Translate
- Hooks: per-tool rate limiter and an audit log of every tool call
- Deterministic steering: interactions must be checked before any medicine is explained
- LLM steering: reviews replies for dose-change advice, diagnosis, false reassurance
- Skills: explain-prescription, handle-interaction-flag, emergency-escalation
- Sessions: FileSessionManager remembers the conversation by session id
- Evals: `python evals/run_evals.py`

## Run
```bash
pip install -r requirements.txt
python chat.py --session-id demo
python evals/run_evals.py
```
Defaults to Amazon Nova Pro. Set `MEDGUIDE_MODEL` to change it, and
`MEDGUIDE_LLM_STEERING=0` to turn off the LLM guardrail.

## Deploy
`main.py` is an Amazon Bedrock AgentCore Runtime entrypoint (`agentcore create`, `agentcore add`
with Bring Your Own Code, copy `main.py`, `medguide/` and `skills/`, then `agentcore deploy`).

## License
MIT
