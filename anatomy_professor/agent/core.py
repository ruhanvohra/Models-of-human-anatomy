"""
Gemma Interactive Anatomy Professor Agent Core.
Processes natural language queries across all anatomical systems,
enforces medical ground-truth retrieval, dispatches 3D Blender actions,
and administers interactive quizzes.
"""

import os
import re
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List
from .prompts import PROFESSOR_SYSTEM_PROMPT, format_biomechanical_lesson
from .tools import execute_tool, TOOL_SCHEMAS
from ..kb.database import AnatomyDatabase


class AnatomyProfessorAgent:
    """
    The Interactive Anatomy Professor powered by Gemma.
    Combines general anatomical semantic reasoning with verified TA2 grounding
    and multi-system 3D Blender viewport control.
    """

    def __init__(self, model_name: str = "gemma-4", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("GEMMA_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.ollama_endpoint = os.environ.get("OLLAMA_ENDPOINT", "http://127.0.0.1:11434")
        self.active_quiz = None
        self.db = AnatomyDatabase()

    def process_query(self, user_prompt: str) -> Dict[str, Any]:
        """
        Main entry point for student interaction.
        Accepts any anatomical prompt across all organ systems, queries ground-truth,
        generates rich 3D commands, and formulates textbook-level pedagogical lessons.
        """
        prompt_lower = user_prompt.lower().strip()

        is_quiz_requested = any(w in prompt_lower for w in ["quiz", "test", "exam", "question me", "assess me"])
        blender_commands: List[Dict[str, Any]] = []
        explanation = ""
        quiz_data = None

        # -------------------------------------------------------------
        # 1. Check for Specific Physiological Pathways & Functional Sub-Mechanisms
        # (e.g. "parts of the digestive system responsible for lowering blood sugar")
        # -------------------------------------------------------------
        physio_pathway = self.db.find_physiology_pathway(prompt_lower)

        if physio_pathway:
            explanation, blender_cmds = self._handle_pathway_query(physio_pathway)
            blender_commands.extend(blender_cmds)

        # -------------------------------------------------------------
        # 2. Check for Broad Bodily Systems & General Organ Overview
        # (e.g. "respiratory system", "digestive system")
        # -------------------------------------------------------------
        elif system_info := self.db.get_system_info(prompt_lower):
            explanation, blender_cmds = self._handle_system_query(prompt_lower, system_info)
            blender_commands.extend(blender_cmds)

        # -------------------------------------------------------------
        # 3. Check for Biomechanical Joint Movements
        # (e.g. "muscles responsible for shoulder abduction")
        # -------------------------------------------------------------
        elif action_match := self._extract_movement(prompt_lower):
            action, joint = action_match
            kb_result = execute_tool("query_anatomy_kb", {"action": action, "joint": joint})
            muscles_data = kb_result.get("data", [])

            if muscles_data:
                explanation = format_biomechanical_lesson(action, muscles_data)
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

        # -------------------------------------------------------------
        # 3. Check for Innervation / Nerve Queries
        # -------------------------------------------------------------
        elif any(w in prompt_lower for w in ["innervat", "nerve", "spinal root"]):
            cleaned = re.sub(r'[^a-zA-Z\s]', '', prompt_lower)
            words = [w for w in cleaned.split() if len(w) > 3 and w not in ["show", "what", "which", "explain", "nerve", "innervation", "muscles"]]
            found_struct = None
            for w in words:
                matches = self.db.get_structure_innervation(w)
                if matches:
                    found_struct = matches[0]
                    break

            if found_struct:
                explanation = (
                    f"### ⚡ Innervation of {found_struct['muscle_name']}\n\n"
                    f"- **Nerve Supply:** `{found_struct['nerve_name']}`\n"
                    f"- **Spinal Root Segments:** **{found_struct['spinal_roots']}**\n"
                    f"- **Plexus Origin:** {found_struct.get('source_plexus', 'N/A')}\n"
                )
                blender_cmd = execute_tool("blender_control", {
                    "command": "highlight",
                    "target_muscles": [found_struct["muscle_name"]],
                    "camera_preset": "auto",
                    "color_map": {found_struct["muscle_name"]: (1.0, 0.9, 0.1, 1.0)}
                })
                blender_commands.append(blender_cmd)

        # -------------------------------------------------------------
        # 4. Check for Arbitrary Anatomical Structure Search in TA2
        # (e.g. "Show me the femur", "Where is the thyroid", "Show me the aorta")
        # -------------------------------------------------------------
        elif not is_quiz_requested:
            # Extract search candidate tokens
            clean_tokens = [w for w in prompt_lower.split() if w not in ["show", "me", "the", "parts", "of", "where", "is", "explain", "what", "find"]]
            search_query = " ".join(clean_tokens)

            matches = self.db.search_structures(search_query, limit=5)
            if not matches and clean_tokens:
                matches = self.db.search_structures(clean_tokens[-1], limit=5)

            if matches:
                top_match = matches[0]
                struct_name = top_match["english_name"]
                latin_name = top_match["latin_name"]

                explanation = (
                    f"### 📍 Anatomical Structure: {struct_name}\n\n"
                    f"- **Terminologia Anatomica (TA2 ID):** `{top_match['ta2_id']}`\n"
                    f"- **Latin Nomenclature:** *{latin_name}*\n"
                    f"- **Multilingual:** French: *{top_match.get('french_name', 'N/A')}*, Spanish: *{top_match.get('spanish_name', 'N/A')}*\n\n"
                    f"I have highlighted and centered this structure in the 3D Viewport."
                )

                blender_cmd = execute_tool("blender_control", {
                    "command": "highlight",
                    "target_muscles": [struct_name],
                    "camera_preset": "auto",
                    "color_map": {struct_name: (0.2, 0.8, 1.0, 1.0)}
                })
                blender_commands.append(blender_cmd)

        # -------------------------------------------------------------
        # 5. Handle Quiz Requests (ONLY when explicitly requested!)
        # -------------------------------------------------------------
        if is_quiz_requested:
            quiz_kw = None
            for kw in ["dislocation", "impingement", "empty can", "winged", "scapula", "trendelenburg", "gait", "respiratory", "lung"]:
                if kw in prompt_lower:
                    quiz_kw = kw
                    break

            quiz_result = execute_tool("get_clinical_quiz", {"keyword": quiz_kw})
            if quiz_result.get("status") == "success":
                quiz_data = quiz_result.get("quiz")
                self.active_quiz = quiz_data

                quiz_prompt_text = (
                    f"### 📝 Professor Gemma's Clinical Assessment\n\n"
                    f"**Case: {quiz_data['title']}**\n\n"
                    f"{quiz_data['scenario']}\n\n"
                    f"**Question:** {quiz_data['question']}\n\n"
                )
                for idx, opt in enumerate(quiz_data["options"], start=1):
                    quiz_prompt_text += f"**[{idx}]** {opt}\n"

                quiz_prompt_text += (
                    f"\n*💡 Tip: Choose an option or left-click the target anatomical structure in the 3D Viewport!*"
                )
                explanation = quiz_prompt_text if not explanation else (explanation + "\n\n---\n" + quiz_prompt_text)

        # Fallback if nothing matched
        if not explanation:
            explanation = (
                "### 🩺 Professor Gemma\n"
                "I am ready. You can ask me about any anatomical system or structure, for example:\n"
                "- *'Show me the parts of the respiratory system responsible for oxygen infusion into the blood'*\n"
                "- *'Show me the muscles responsible for shoulder abduction and explain their innervation'*\n"
                "- *'Show me the chambers of the heart and the aorta'*\n"
                "- *'Where are the kidneys and renal vessels located?'*\n"
                "- *'Quiz me on clinical nerve lesions'*"
            )

        return {
            "response": explanation,
            "blender_commands": blender_commands,
            "quiz": quiz_data
        }

    def _handle_pathway_query(self, pathway: Dict[str, Any]) -> tuple:
        """Formulates targeted physiological masterclasses for specific biochemical pathways."""
        title = pathway["title"]
        category = pathway["system_category"]
        primary_organ = pathway["primary_organ"]
        structures = pathway["3d_structures"]
        role = pathway["functional_role"]
        cell_mech = pathway["cellular_mechanism"]
        action_mech = pathway["target_action"]
        peel_kw = pathway.get("peel_keywords", [])
        color_map = pathway.get("color_map", {})

        lines = [
            f"### 🔬 Professor Gemma's Masterclass: {title}",
            f"**System Category:** {category}",
            "",
            f"#### 🎯 **Primary Functional Organ: {primary_organ}**",
            f"- **Role:** {role}",
            "",
            "#### 🧪 **Cellular & Molecular Mechanism:**",
            cell_mech,
            "",
            "#### ⚡ **Physiological Pathway & Target Effectors:**",
            action_mech,
            "",
            "#### 🌐 **3D Structures Displayed in Viewport:**",
            f"I have highlighted the **{primary_organ}** and target effectors in the 3D model:",
        ]
        for s in structures:
            lines.append(f"- `📍 {s}`")

        lines.append("")
        lines.append("*(Superficial abdominal wall muscles have been peeled to reveal retroperitoneal viscera).*")

        full_color_map = {}
        for s in structures:
            for k, col in color_map.items():
                if k.lower() in s.lower():
                    full_color_map[s] = col
                    break
            if s not in full_color_map:
                full_color_map[s] = (1.0, 0.85, 0.1, 1.0)

        blender_cmd = execute_tool("blender_control", {
            "command": "highlight",
            "target_muscles": structures,
            "camera_preset": "anterior",
            "color_map": full_color_map,
            "peel_keywords": peel_kw
        })

        return "\n".join(lines), [blender_cmd]

    def _handle_system_query(self, prompt: str, system_info: Dict[str, Any]) -> tuple:
        """Formulates rich physiological and anatomical lessons for any bodily system."""
        sys_name = system_info["system_name"]
        primary_objs = system_info["primary_3d_structures"]
        subunits = system_info.get("functional_subunits", [])
        peel_kw = system_info.get("peel_keywords", [])

        lines = [
            f"### 🫁 Professor Gemma's Masterclass: {sys_name}",
            "",
            "Here is the functional anatomical architecture for this system:",
            ""
        ]

        # Add functional subunits and physiological mechanisms
        for sub in subunits:
            lines.append(f"#### 🔬 **{sub['name']}** ({sub['type']})")
            lines.append(f"- **Physiological Role:** {sub['role']}")
            lines.append(f"- **Mechanism:** {sub['mechanism']}")
            lines.append("")

        lines.append("#### 🌐 **3D Structures Displayed in Viewport:**")
        lines.append("I have illuminated the primary macroscopic structures in the 3D model:")
        for obj_name in primary_objs[:8]:
            lines.append(f"- `📍 {obj_name}`")
        lines.append("")
        lines.append("*(Superficial anterior chest wall structures have been automatically peeled for clear visibility).*")

        # Color palette for respiratory/cardiovascular structures
        color_map = {}
        for obj in primary_objs:
            if "vein" in obj.lower():
                color_map[obj] = (0.2, 0.4, 1.0, 1.0)   # Blue/Cyan
            elif "artery" in obj.lower() or "trunk" in obj.lower():
                color_map[obj] = (0.9, 0.2, 0.2, 1.0)   # Red
            elif "bronch" in obj.lower() or "trachea" in obj.lower():
                color_map[obj] = (1.0, 0.85, 0.2, 1.0)  # Gold/Yellow
            else:
                color_map[obj] = (0.3, 0.8, 1.0, 1.0)   # Cyan / Lung Parenchyma

        blender_cmd = execute_tool("blender_control", {
            "command": "highlight",
            "target_muscles": primary_objs,
            "camera_preset": system_info.get("default_camera", "anterior"),
            "color_map": color_map,
            "peel_keywords": peel_kw
        })

        return "\n".join(lines), [blender_cmd]

    def evaluate_answer(self, user_answer: Any) -> Dict[str, Any]:
        """Evaluates a student's answer to the active quiz."""
        if not self.active_quiz:
            return {"status": "no_active_quiz", "message": "No active quiz in progress."}

        quiz = self.active_quiz
        correct = False

        if isinstance(user_answer, int):
            correct = (user_answer == quiz["correct_index"] or user_answer - 1 == quiz["correct_index"])
        elif isinstance(user_answer, str):
            clean_ans = user_answer.strip().lower()
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
                f"**Clinical Explanation:** {quiz['explanation']}\n\n"
                f"Notice how the verified ground-truth links **{quiz['target_structure']}** "
                f"to its innervation: **{quiz.get('target_nerve', '')}** ({quiz.get('spinal_roots', '')})."
            )
        else:
            feedback = (
                f"### ❌ Incorrect, but a great learning opportunity!\n\n"
                f"The correct answer is: **{quiz['options'][quiz['correct_index']]}**\n\n"
                f"**Clinical Explanation:** {quiz['explanation']}"
            )

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
