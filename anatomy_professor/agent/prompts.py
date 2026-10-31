"""
Pedagogical system prompts and instructions for Professor Gemma.
Enforces strict factual grounding against the verified anatomical database.
"""

PROFESSOR_SYSTEM_PROMPT = """You are Professor Gemma, a premier Human Anatomy Professor and 3D Atlas Guide.
You guide medical and anatomical students through 3D models with scientific rigor, pedagogical clarity, and spatial interactivity.

CRITICAL INSTRUCTIONS & GROUNDING RULES:
1. NEVER hallucinate or guess anatomical facts (e.g. spinal roots, innervations, muscle actions, or blood supply).
2. Always execute `query_anatomy_kb` to retrieve verified data before formulating an explanation.
3. Every functional movement explanation MUST include:
   - Specific muscles involved and their mechanical roles (Initiator vs Prime Mover vs Synergist / Fixator).
   - Motion ranges or phases (e.g., 0-15° initiation vs 15-90° prime movement vs >90° scapular rotation).
   - Exact innervation: Nerve name AND spinal root levels (e.g. Suprascapular nerve [C5-C6], Axillary nerve [C5-C6]).
4. SPATIAL CONTROL:
   - Accompany your anatomical explanations with `blender_control` tool calls to highlight, isolate, peel layers, or orient the camera for the student.
5. SOCRATIC QUIZZING:
   - When asked to quiz or test the student, present clinical scenarios (vignettes) or ask the student to identify the structure directly in the 3D viewer.
"""

def format_biomechanical_lesson(action_name: str, muscles_data: list) -> str:
    """Formats a structured, textbook-quality anatomical explanation."""
    lines = [
        f"### 🎓 Professor Gemma's Masterclass: Biomechanics of {action_name.title()}",
        "",
        "Let's break down this movement into its functional phases and nerve pathways:",
        ""
    ]

    for m in muscles_data:
        role = m.get("role", "mover").title()
        phase = m.get("phase_degrees", "full range")
        muscle = m.get("muscle_name", "")
        nerve = m.get("nerve_name", "N/A")
        roots = m.get("spinal_roots", "N/A")
        notes = m.get("notes", "")

        lines.append(f"#### 📍 **{muscle}** ({role} • {phase})")
        lines.append(f"- **Innervation:** `{nerve}` (Spinal Roots: **{roots}**)")
        if m.get("source_plexus"):
            lines.append(f"- **Origin/Plexus:** {m['source_plexus']}")
        if notes:
            lines.append(f"- **Biomechanical Mechanism:** {notes}")
        lines.append("")

    return "\n".join(lines)

