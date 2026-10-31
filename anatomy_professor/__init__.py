"""
Gemma Interactive Anatomy Professor Package.
Integrates Gemma AI reasoning with verified TA2 anatomy and Z-Anatomy Blender 3D models.
"""

from .agent.core import AnatomyProfessorAgent
from .kb.database import AnatomyDatabase
from .kb.builder import build_knowledge_base

__all__ = ["AnatomyProfessorAgent", "AnatomyDatabase", "build_knowledge_base"]

