import json
import requests

from schemas import PlannerOutput


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


SYSTEM_INSTRUCTION = """
You are a planning module for a technical document analysis agent.

Your task is to create a minimal valid execution plan for the user query.

Available steps:
1. search     - retrieve relevant documents
2. summarize  - summarize document sections
3. compare    - compare the top 2 relevant documents
4. report     - generate the final markdown report

Rules:
- Always include "search" first.
- Always include "summarize" before "compare" and before "report".
- Include "compare" only if the query asks for comparison, differences, contrast, or similar intent.
- Always include "report" last.
- Return ONLY valid JSON.
- Do not include markdown fences.
- Do not include any explanation outside JSON.

Return JSON in this exact format:
{
  "plan": ["search", "summarize", "compare", "report"],
  "rationale": "short explanation"
}
""".strip()


def create_fallback_plan(query: str) -> PlannerOutput:
    """
    Rule-based fallback planner.
    """
    q = query.lower()
    plan = ["search", "summarize"]

    if any(word in q for word in ["compare", "difference", "differences", "contrast", "vs"]):
        plan.append("compare")

    plan.append("report")

    return PlannerOutput(
        plan=plan,
        rationale="Fallback rule-based planner used because Ollama planning was unavailable or parsing failed."
    )


def extract_json(text: str) -> dict:
    """
    Try to extract a JSON object from model output.
    Handles cases where the model adds extra text around JSON.
    """
    text = text.strip()

    # Case 1: direct JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Case 2: find first {...} block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        return json.loads(candidate)

    raise ValueError("No valid JSON object found in LLM output.")


def validate_plan(plan: list[str]) -> list[str]:
    """
    Validate and normalize the plan.
    Ensures only supported steps are used and ordering is safe.

    Final enforced order:
    search -> summarize -> compare -> report
    """
    allowed_steps = ["search", "summarize", "compare", "report"]

    # Keep only allowed steps
    cleaned = [step for step in plan if step in allowed_steps]

    # Remove duplicates while preserving original order
    deduped = []
    for step in cleaned:
        if step not in deduped:
            deduped.append(step)

    # Detect whether compare was requested
    has_compare = "compare" in deduped

    # Rebuild plan in strict safe order
    final_plan = ["search", "summarize"]

    if has_compare:
        final_plan.append("compare")

    final_plan.append("report")

    return final_plan


def create_plan(query: str, model: str = OLLAMA_MODEL) -> PlannerOutput:
    """
    Create a plan using a local Ollama model.
    Falls back to rule-based planning if Ollama is unavailable
    or if JSON parsing fails.
    """
    prompt = f"""
{SYSTEM_INSTRUCTION}

User query: {query}
""".strip()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0
                }
            },
            timeout=60
        )
        response.raise_for_status()

        result = response.json()
        output_text = result.get("response", "").strip()

        data = extract_json(output_text)

        raw_plan = data.get("plan", [])
        rationale = data.get("rationale", "LLM planner used.")

        if not isinstance(raw_plan, list):
            raise ValueError("Invalid plan format: plan must be a list.")

        validated_plan = validate_plan(raw_plan)

        return PlannerOutput(
            plan=validated_plan,
            rationale=rationale
        )

    except Exception:
        return create_fallback_plan(query)