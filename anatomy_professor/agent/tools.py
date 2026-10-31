"""
Tool definitions and execution dispatch for Professor Gemma.
"""

from typing import Dict, Any, List, Optional
from ..kb.database import AnatomyDatabase

db = AnatomyDatabase()

TOOL_SCHEMAS = [
    {
        "name": "query_anatomy_kb",
        "description": "Fetch verified anatomical relationships (actions, innervations, spinal roots, TA2) from the verified database.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Movement action, e.g. 'abduction', 'flexion'"},
                "joint": {"type": "string", "description": "Target joint, e.g. 'glenohumeral', 'elbow', 'hip'"},
                "muscle_name": {"type": "string", "description": "Specific muscle to check innervation for"},
                "search_term": {"type": "string", "description": "Term to search in TA2"}
            }
        }
    },
    {
        "name": "blender_control",
        "description": "Control the Blender 3D viewport: isolate, highlight, peel layers, or frame camera.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "enum": ["highlight", "isolate", "peel", "reset"]},
                "target_muscles": {"type": "array", "items": {"type": "string"}},
                "camera_preset": {"type": "string", "enum": ["auto", "anterior", "posterior", "lateral", "superior"]},
                "color_map": {"type": "object", "description": "Map of muscle name to color (e.g. 'yellow', 'cyan', 'green')"}
            },
            "required": ["command", "target_muscles"]
        }
    },
    {
        "name": "get_clinical_quiz",
        "description": "Retrieve a clinical case quiz vignette based on verified anatomical facts.",
        "parameters": {
            "type": "object",
            "properties": {
                "case_id": {"type": "string", "description": "Optional specific case ID"}
            }
        }
    }
]


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatches a tool call to the database or subsystem."""
    if tool_name == "query_anatomy_kb":
        action = arguments.get("action")
        joint = arguments.get("joint")
        muscle_name = arguments.get("muscle_name")
        search_term = arguments.get("search_term")

        if action:
            results = db.find_muscles_by_action(action, joint)
            return {"status": "success", "type": "action_muscles", "data": results}
        elif muscle_name:
            results = db.get_structure_innervation(muscle_name)
            return {"status": "success", "type": "innervations", "data": results}
        elif search_term:
            results = db.search_structures(search_term)
            return {"status": "success", "type": "structures", "data": results}
        else:
            return {"status": "error", "message": "No query parameters specified"}

    elif tool_name == "blender_control":
        command = arguments.get("command", "highlight")
        targets = arguments.get("target_muscles", [])
        camera = arguments.get("camera_preset", "auto")
        color_map = arguments.get("color_map", {})

        # Resolve clinical names to Blender mesh object patterns
        resolved_objects = []
        for target in targets:
            candidates = db.resolve_mesh_candidates(target)
            resolved_objects.extend(candidates)

        return {
            "status": "success",
            "command": command,
            "target_muscles": targets,
            "resolved_mesh_patterns": resolved_objects,
            "camera_preset": camera,
            "color_map": color_map
        }

    elif tool_name == "get_clinical_quiz":
        case_id = arguments.get("case_id")
        keyword = arguments.get("keyword")
        case = db.get_clinical_case(case_id=case_id, keyword=keyword)
        if case:
            return {"status": "success", "quiz": case}
        return {"status": "error", "message": "No quiz cases found"}

    return {"status": "error", "message": f"Unknown tool: {tool_name}"}
