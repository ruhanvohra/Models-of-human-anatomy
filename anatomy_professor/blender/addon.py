"""
Blender Addon Registration Entry Point for Gemma Anatomy Professor.
"""

bl_info = {
    "name": "Gemma Anatomy Professor",
    "author": "Antigravity & Z-Anatomy",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar (N) > Anatomy Professor",
    "description": "Interactive AI Anatomy Professor powered by Gemma and verified TA2 ground truth.",
    "category": "Education",
}

from .ui import register as ui_register, unregister as ui_unregister


def register():
    ui_register()
    print("[Anatomy Professor] Gemma Anatomy Professor Addon registered successfully.")


def unregister():
    ui_unregister()
    print("[Anatomy Professor] Gemma Anatomy Professor Addon unregistered.")


if __name__ == "__main__":
    register()

