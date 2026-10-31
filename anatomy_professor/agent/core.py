"""
Gemma Interactive Anatomy Professor Agent Core.
Processes natural language queries, enforces medical ground-truth retrieval,
dispatches 3D viewport operations, and administers interactive quizzes.
"""

import os
import re
from typing import Dict, Any, Optional
from .prompts import PROFESSOR_SYSTEM_PROMPT, format_biomechanical_lesson
from .tools import execute_tool, TOOL_SCHEMAS


class AnatomyProfessorAgent:
    """
    The Interactive Anatomy Professor powered by Gemma.
    Orchestrates grounded anatomical knowledge retrieval with 3D Blender actions.
    """

    def __init__(self, model_name: str = "gemma-4", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("GEMMA_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.active_quiz = None

    def process_query(self, user_prompt: str) -> Dict[str, Any]:
        """
        Main entry point for student interaction.
        Accepts natural language, queries ground-truth knowledge base,
        coordinates 3D Blender actions, and produces an educational response.
        """
        prompt_lower = user_prompt.lower().strip()

        # Step 1: Detect Intent & Extract Entities
        # Check for movement action queries
        action_match = self._extract_movement(prompt_lower)
        is_quiz_requested = any(w in prompt_lower for w in ["quiz", "test", "question", "exam"])

        blender_commands = []
        explanation = ""
        quiz_data = None

        if action_match:
            action, joint = action_match
            # Execute verified DB lookup (Grounding step)
            kb_result = execute_tool("query_anatomy_kb", {"action": action, "joint": joint})
            muscles_data = kb_result.get("data", [])

            if muscles_data:
                # 1. Format pedagogical explanation
                explanation = format_biomechanical_lesson(action, muscles_data)

                # 2. Build 3D Blender commands
                muscle_names = [m["muscle_name"] for m in muscles_data]
                color_map = {}
                for m in muscles_data:
                    role = m.get("role", "")
                    if role == "initiator":
                        color_map[m["muscle_name"]] = (0.2, 0.8, 1.0, 1.0)  # Cyan
                    elif role == "prime mover":
                        color_map[m["muscle_name"]] = (1.0, 0.85, 0.1, 1.0) # Gold/Yellow
                    else:
                        color_map[m["muscle_name"]] = (0.4, 0.9, 0.3, 1.0)  # Green

                blender_cmd = execute_tool("blender_control", {
                    "command": "highlight",
                    "target_muscles": muscle_names,
                    "camera_preset": "auto",
                    "color_map": color_map
                })
                blender_commands.append(blender_cmd)

        # Step 2: Check for specific muscle innervation query if not an action
        elif any(w in prompt_lower for w in ["innervat", "nerve", "root", "nerve supply"]):
            # Extract target muscle name
            cleaned = re.sub(r'[^a-zA-Z\s]', '', prompt_lower)
            candidates = ["deltoid", "supraspinatus", "infraspinatus", "biceps", "triceps", "brachialis",
                          "serratus", "trapezius", "gluteus", "quadriceps", "rectus femoris"]
            found_muscle = next((c for c in candidates if c in cleaned), None)

            if found_muscle:
                kb_result = execute_tool("query_anatomy_kb", {"muscle_name": found_muscle})
                innerv_data = kb_result.get("data", [])
                if innerv_data:
                    info = innerv_data[0]
                    explanation = (
                        f"### ⚡ Innervation of {info['muscle_name']}\n\n"
                        f"- **Nerve Supply:** `{info['nerve_name']}`\n"
                        f"- **Spinal Root Segments:** **{info['spinal_roots']}**\n"
                        f"- **Brachial/Lumbosacral Plexus Origin:** {info.get('source_plexus', 'N/A')}\n"
                    )
                    blender_cmd = execute_tool("blender_control", {
                        "command": "highlight",
                        "target_muscles": [info["muscle_name"]],
                        "camera_preset": "auto",
                        "color_map": {info["muscle_name"]: (1.0, 0.9, 0.1, 1.0)}
                    })
                    blender_commands.append(blender_cmd)

        # Step 3: Handle Quiz Requests
        if is_quiz_requested or not explanation:
            # Match clinical case using prompt keywords
            quiz_kw = None
            for kw in ["dislocation", "impingement", "empty can", "winged", "scapula", "trendelenburg", "gait"]:
                if kw in prompt_lower:
                    quiz_kw = kw
                    break

            quiz_result = execute_tool("get_clinical_quiz", {"keyword": quiz_kw})
            if quiz_result.get("status") == "success":
                quiz_data = quiz_result.get("quiz")
                self.active_quiz = quiz_data

                quiz_prompt_text = (
                    f"\n\n---\n"
                    f"### 📝 Professor Gemma's Clinical Assessment\n\n"
                    f"**Case: {quiz_data['title']}**\n\n"
                    f"{quiz_data['scenario']}\n\n"
                    f"**Question:** {quiz_data['question']}\n\n"
                )
                for idx, opt in enumerate(quiz_data["options"], start=1):
                    quiz_prompt_text += f"**[{idx}]** {opt}\n"

                quiz_prompt_text += (
                    f"\n*💡 Tip: You can answer by choosing the option or clicking the target structure in the 3D Viewport!*"
                )
                explanation += quiz_prompt_text

        if not explanation:
            explanation = (
                "### 🩺 Professor Gemma\n"
                "I am ready. Ask me any anatomical question! For example:\n"
                "- *'Show me the muscles responsible for shoulder abduction, explain their innervation, and quiz me on them.'*\n"
                "- *'What innervates the supraspinatus and deltoid muscles?'*\n"
                "- *'Explain the functional anatomy of the elbow flexors.'*"
            )

        return {
            "response": explanation,
            "blender_commands": blender_commands,
            "quiz": quiz_data
        }

    def evaluate_answer(self, user_answer: Any) -> Dict[str, Any]:
        """
        Evaluates a student's answer to the active quiz.
        Supports both multiple-choice selection and 3D mesh clicking in Blender!
        """
        if not self.active_quiz:
            return {"status": "no_active_quiz", "message": "No active quiz in progress."}

        quiz = self.active_quiz
        correct = False
        feedback = ""

        # Check if user passed an option index or text
        if isinstance(user_answer, int):
            correct = (user_answer == quiz["correct_index"] or user_answer - 1 == quiz["correct_index"])
        elif isinstance(user_answer, str):
            clean_ans = user_answer.strip().lower()
            # Strip mesh suffix if passed from 3D viewport
            clean_mesh_base = re.sub(r'\.[a-z0-9]+$', '', clean_ans).strip()
            correct_opt = quiz["options"][quiz["correct_index"]].lower()
            target_struct = quiz["target_structure"].lower()
            target_nerve = quiz.get("target_nerve", "").lower()

            if (clean_ans in correct_opt or
                target_struct in clean_ans or
                target_struct in clean_mesh_base or
                clean_mesh_base in target_struct or
                (target_nerve and target_nerve in clean_ans)):
                correct = True
            elif clean_ans.isdigit():
                val = int(clean_ans)
                correct = (val == quiz["correct_index"] or val - 1 == quiz["correct_index"])

        if correct:
            feedback = (
                f"### ✅ Correct!\n\n"
                f"**Explanation:** {quiz['explanation']}\n\n"
                f"Notice how the verified ground-truth links the structure **{quiz['target_structure']}** "
                f"to its innervation: **{quiz.get('target_nerve', '')}** ({quiz.get('spinal_roots', '')})."
            )
        else:
            feedback = (
                f"### ❌ Incorrect, but a great learning opportunity!\n\n"
                f"The correct answer is: **{quiz['options'][quiz['correct_index']]}**\n\n"
                f"**Clinical Explanation:** {quiz['explanation']}"
            )

        # Highlight the correct answer structure in 3D
        highlight_cmd = execute_tool("blender_control", {
            "command": "highlight",
            "target_muscles": [quiz["target_structure"]],
            "camera_preset": "auto",
            "color_map": {quiz["target_structure"]: (0.2, 0.9, 0.3, 1.0) if correct else (1.0, 0.3, 0.3, 1.0)}
        })

        return {
            "status": "evaluated",
            "correct": correct,
            "feedback": feedback,
            "blender_commands": [highlight_cmd]
        }

    def _extract_movement(self, prompt: str) -> Optional[tuple]:
        """Extracts movement action and joint from natural language prompt."""
        actions = ["abduction", "adduction", "flexion", "extension", "external rotation", "internal rotation", "pronation", "supination"]
        found_action = next((a for a in actions if a in prompt), None)

        if not found_action:
            if "abduct" in prompt:
                found_action = "abduction"
            elif "adduct" in prompt:
                found_action = "adduction"
            elif "flex" in prompt:
                found_action = "flexion"
            elif "extend" in prompt:
                found_action = "extension"

        if found_action:
            joint = None
            if any(w in prompt for w in ["shoulder", "arm", "glenohumeral"]):
                joint = "glenohumeral"
            elif any(w in prompt for w in ["elbow", "forearm"]):
                joint = "elbow"
            elif any(w in prompt for w in ["hip", "pelvis"]):
                joint = "hip"
            elif any(w in prompt for w in ["knee", "leg"]):
                joint = "knee"
            return found_action, joint

        return None
