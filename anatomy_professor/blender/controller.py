"""
Blender 3D Viewport Controller for Z-Anatomy.
Handles highlighting, layer peeling, camera framing, and material assignment.
"""

import re
from typing import List, Dict, Any, Optional

try:
    import bpy
    import mathutils
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False


class BlenderViewportController:
    """Controls the 3D viewport in Blender for Z-Anatomy models."""

    HIGHLIGHT_MAT_PREFIX = "Anatomy_Prof_Mat_"

    @classmethod
    def is_available(cls) -> bool:
        return BLENDER_AVAILABLE

    @classmethod
    def get_or_create_material(cls, color: tuple, name_suffix: str = "custom") -> Optional[Any]:
        """Creates or retrieves an emissive highlight material."""
        if not BLENDER_AVAILABLE:
            return None

        mat_name = f"{cls.HIGHLIGHT_MAT_PREFIX}{name_suffix}"
        mat = bpy.data.materials.get(mat_name)
        if mat is None:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()

            # Create Principled BSDF with emission for clear visual pop
            output_node = nodes.new(type="ShaderNodeOutputMaterial")
            principled = nodes.new(type="ShaderNodeBsdfPrincipled")
            principled.location = (0, 0)
            output_node.location = (300, 0)

            # Set base color and emission
            # Handles Blender 4.0+ / 5.0+ Principled BSDF socket changes
            if "Base Color" in principled.inputs:
                principled.inputs["Base Color"].default_value = color
            
            emission_input = principled.inputs.get("Emission Color") or principled.inputs.get("Emission")
            if emission_input:
                emission_input.default_value = color
            
            emission_strength = principled.inputs.get("Emission Strength")
            if emission_strength:
                emission_strength.default_value = 0.6

            mat.node_tree.links.new(principled.outputs["BSDF"], output_node.inputs["Surface"])

        return mat

    @classmethod
    def find_objects_by_patterns(cls, patterns: List[str]) -> List[Any]:
        """Finds all Blender objects matching a list of name patterns."""
        if not BLENDER_AVAILABLE:
            return []

        matched = []
        for obj in bpy.data.objects:
            obj_name = obj.name

            # Skip helper objects like curve bevel profiles or text/empties
            if "-profile" in obj_name.lower():
                continue

            clean_base = re.sub(r'\.[a-z0-9]+$', '', obj_name).strip()

            for pattern in patterns:
                pat_clean = re.sub(r'\.[a-z0-9]+$', '', pattern).strip()
                if (obj_name == pattern or
                    clean_base.lower() == pat_clean.lower() or
                    pat_clean.lower() in clean_base.lower()):
                    if obj not in matched:
                        matched.append(obj)
                    break

        return matched

    @classmethod
    def enable_collections_for_objects(cls, objects: List[Any]):
        """
        Automatically enables and unhides all Scene and Layer collections containing
        the target objects, walking from the collection up to the root View Layer.
        Guarantees that the highlighted objects become immediately visible even if
        their system collection (e.g. Visceral, Muscular, Cardiovascular) was hidden.
        """
        if not BLENDER_AVAILABLE or not objects:
            return

        if not hasattr(bpy.context, "view_layer") or not hasattr(bpy.context.view_layer, "layer_collection"):
            return

        root_layer_col = bpy.context.view_layer.layer_collection

        def unhide_layer_collection_recursive(layer_col, target_col):
            if layer_col.collection == target_col:
                layer_col.exclude = False
                layer_col.hide_viewport = False
                return True
            for child in layer_col.children:
                if unhide_layer_collection_recursive(child, target_col):
                    layer_col.exclude = False
                    layer_col.hide_viewport = False
                    return True
            return False

        for obj in objects:
            for col in getattr(obj, "users_collection", []):
                unhide_layer_collection_recursive(root_layer_col, col)

        try:
            bpy.context.view_layer.update()
        except Exception:
            pass

    @classmethod
    def highlight_structures(cls, target_patterns: List[str], color_map: Optional[Dict[str, tuple]] = None) -> int:
        """
        Highlights and selects the target structures.
        Automatically enables any hidden Scene/Layer collections containing them,
        unhides the meshes, and centers the 3D viewport.
        """
        if not BLENDER_AVAILABLE:
            return 0

        # Deselect current selection safely
        for obj in bpy.context.selected_objects:
            try:
                obj.select_set(False)
            except (RuntimeError, Exception):
                pass

        matched_objects = cls.find_objects_by_patterns(target_patterns)

        # Automatically enable and unhide collections containing the target objects
        cls.enable_collections_for_objects(matched_objects)

        count = 0
        valid_selected = []

        default_color = (1.0, 0.85, 0.1, 1.0) # Yellow/Gold

        # View Layer set for fast membership check after enabling collections
        view_layer_objects = bpy.context.view_layer.objects if hasattr(bpy.context, "view_layer") else None

        for obj in matched_objects:
            # Guard against objects not in the active view layer
            if view_layer_objects and obj.name not in view_layer_objects:
                continue

            try:
                obj.hide_viewport = False
                obj.hide_set(False)
                if obj.parent and (obj.parent.hide_viewport or obj.parent.hide_get()):
                    obj.parent.hide_viewport = False
                    obj.parent.hide_set(False)
                obj.select_set(True)
                valid_selected.append(obj)
            except (RuntimeError, Exception):
                continue

            # Determine color
            obj_color = default_color
            if color_map:
                for target_name, col in color_map.items():
                    if target_name.lower() in obj.name.lower():
                        obj_color = col
                        break

            # Assign highlight material if object supports materials
            if hasattr(obj, "data") and hasattr(obj.data, "materials"):
                mat = cls.get_or_create_material(obj_color, name_suffix=f"{int(obj_color[0]*10)}_{int(obj_color[1]*10)}")
                if mat:
                    if len(obj.data.materials) == 0:
                        obj.data.materials.append(mat)
                    else:
                        obj.data.materials[0] = mat

            count += 1

        if valid_selected:
            try:
                bpy.context.view_layer.objects.active = valid_selected[0]
                cls.frame_camera_on_selected()
            except (RuntimeError, Exception):
                pass

        return count

    @classmethod
    def peel_superficial_layers(cls) -> str:
        """Hides superficial fascia and outer muscle layers to reveal deep rotator cuff & skeletal anatomy."""
        if not BLENDER_AVAILABLE:
            return "Blender unavailable"

        peeled_count = 0
        superficial_keywords = ["fascia", "integument", "platysma", "skin", "subdeltoid"]
        for obj in bpy.data.objects:
            name_lower = obj.name.lower()
            if any(k in name_lower for k in superficial_keywords):
                if not obj.hide_viewport:
                    obj.hide_viewport = True
                    obj.hide_set(True)
                    peeled_count += 1

        return f"Peeled {peeled_count} superficial structures."

    @classmethod
    def frame_camera_on_selected(cls):
        """Frames the 3D viewport on the selected objects."""
        if not BLENDER_AVAILABLE:
            return

        for area in getattr(bpy.context.screen, 'areas', []):
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region}
                        try:
                            with bpy.context.temp_override(**override):
                                bpy.ops.view3d.view_selected()
                        except Exception:
                            pass
                        break

    @classmethod
    def peel_structures_by_keywords(cls, keywords: List[str]) -> int:
        """Hides structures matching specific keywords (e.g. ribs, pectoralis) to reveal deep viscera."""
        if not BLENDER_AVAILABLE or not keywords:
            return 0
        peeled = 0
        for obj in bpy.data.objects:
            name_lower = obj.name.lower()
            if any(k.lower() in name_lower for k in keywords):
                if not obj.hide_viewport:
                    obj.hide_viewport = True
                    obj.hide_set(True)
                    peeled += 1
        return peeled

    @classmethod
    def reset_visibility(cls):
        """Restores normal visibility to all objects."""
        if not BLENDER_AVAILABLE:
            return

        for obj in bpy.data.objects:
            obj.hide_viewport = False
            obj.hide_set(False)
            obj.select_set(False)

    @classmethod
    def execute_commands(cls, commands: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Dispatches commands generated by the Gemma Agent."""
        results = []
        for cmd in commands:
            action = cmd.get("command")
            if action == "highlight":
                peel_kws = cmd.get("peel_keywords")
                if peel_kws:
                    cls.peel_structures_by_keywords(peel_kws)
                targets = cmd.get("resolved_mesh_patterns") or cmd.get("target_muscles", [])
                color_map = cmd.get("color_map", {})
                count = cls.highlight_structures(targets, color_map)
                results.append(f"Highlighted {count} objects matching {len(targets)} targets.")
            elif action == "peel":
                res = cls.peel_superficial_layers()
                results.append(res)
            elif action == "reset":
                cls.reset_visibility()
                results.append("Reset viewport visibility.")

        return {"status": "success", "executed": results}

