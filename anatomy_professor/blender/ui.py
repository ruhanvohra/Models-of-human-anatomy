"""
Blender UI Panels and Operators for Professor Gemma.
Provides an interactive learning interface directly inside Blender's 3D Viewport.
"""

import bpy
from ..agent.core import AnatomyProfessorAgent
from .controller import BlenderViewportController

# Persistent agent instance inside Blender session
_AGENT = None

def get_agent() -> AnatomyProfessorAgent:
    global _AGENT
    if _AGENT is None:
        _AGENT = AnatomyProfessorAgent()
    return _AGENT


class AnatomyProfessorProperties(bpy.types.PropertyGroup):
    """Stores UI state and chat history for the Anatomy Professor."""
    user_query: bpy.props.StringProperty(
        name="Ask Professor",
        description="Type any anatomical question or command for Professor Gemma",
        default="Show me the muscles responsible for shoulder abduction, explain their innervation, and quiz me on them."
    )
    last_response: bpy.props.StringProperty(
        name="Professor Response",
        default="Welcome! Ask a question or click a preset below to explore anatomy."
    )
    quiz_in_progress: bpy.props.BoolProperty(default=False)
    quiz_scenario: bpy.props.StringProperty(default="")
    quiz_question: bpy.props.StringProperty(default="")
    quiz_opt_1: bpy.props.StringProperty(default="")
    quiz_opt_2: bpy.props.StringProperty(default="")
    quiz_opt_3: bpy.props.StringProperty(default="")
    quiz_opt_4: bpy.props.StringProperty(default="")
    quiz_feedback: bpy.props.StringProperty(default="")


class ANATOMY_OT_load_preset(bpy.types.Operator):
    """Load and execute a guided masterclass preset."""
    bl_idname = "anatomy.load_preset"
    bl_label = "Load Guided Lesson"
    bl_description = "Loads a curated anatomical masterclass and runs it"

    preset_query: bpy.props.StringProperty(default="")

    def execute(self, context):
        props = context.scene.anatomy_professor
        props.user_query = self.preset_query
        bpy.ops.anatomy.ask_professor()
        return {'FINISHED'}


class ANATOMY_OT_ask_professor(bpy.types.Operator):
    """Send question to Professor Gemma."""
    bl_idname = "anatomy.ask_professor"
    bl_label = "Ask Professor Gemma"
    bl_description = "Process natural language prompt with Gemma and verified TA2 data"

    def execute(self, context):
        props = context.scene.anatomy_professor
        query = props.user_query.strip()

        if not query:
            self.report({'WARNING'}, "Please enter an anatomical question or command.")
            return {'CANCELLED'}

        agent = get_agent()
        result = agent.process_query(query)

        props.last_response = result.get("response", "")

        # Execute 3D viewport commands
        blender_cmds = result.get("blender_commands", [])
        if blender_cmds:
            BlenderViewportController.execute_commands(blender_cmds)

        # Handle active quiz
        quiz = result.get("quiz")
        if quiz:
            props.quiz_in_progress = True
            props.quiz_scenario = quiz.get("scenario", "")
            props.quiz_question = quiz.get("question", "")
            opts = quiz.get("options", [])
            props.quiz_opt_1 = opts[0] if len(opts) > 0 else ""
            props.quiz_opt_2 = opts[1] if len(opts) > 1 else ""
            props.quiz_opt_3 = opts[2] if len(opts) > 2 else ""
            props.quiz_opt_4 = opts[3] if len(opts) > 3 else ""
            props.quiz_feedback = ""
        else:
            props.quiz_in_progress = False
            props.quiz_feedback = ""

        self.report({'INFO'}, "Professor Gemma answered.")
        return {'FINISHED'}


class ANATOMY_OT_answer_quiz(bpy.types.Operator):
    """Submit an answer to the active quiz."""
    bl_idname = "anatomy.answer_quiz"
    bl_label = "Answer Quiz"
    bl_description = "Submit option choice to Professor Gemma"

    choice_index: bpy.props.IntProperty(default=1)

    def execute(self, context):
        props = context.scene.anatomy_professor
        agent = get_agent()
        eval_result = agent.evaluate_answer(self.choice_index)

        props.quiz_feedback = eval_result.get("feedback", "")

        # Highlight answer in 3D
        blender_cmds = eval_result.get("blender_commands", [])
        if blender_cmds:
            BlenderViewportController.execute_commands(blender_cmds)

        return {'FINISHED'}


class ANATOMY_OT_submit_mesh_answer(bpy.types.Operator):
    """Use the currently selected 3D mesh as the quiz answer."""
    bl_idname = "anatomy.submit_mesh_answer"
    bl_label = "Submit Clicked 3D Mesh as Answer"
    bl_description = "Tests if your selected 3D anatomical structure is the correct answer"

    def execute(self, context):
        active_obj = context.active_object
        if not active_obj:
            self.report({'WARNING'}, "Please select a 3D structure in the viewport first.")
            return {'CANCELLED'}

        props = context.scene.anatomy_professor
        agent = get_agent()
        eval_result = agent.evaluate_answer(active_obj.name)

        props.quiz_feedback = eval_result.get("feedback", "")
        blender_cmds = eval_result.get("blender_commands", [])
        if blender_cmds:
            BlenderViewportController.execute_commands(blender_cmds)

        return {'FINISHED'}


class ANATOMY_OT_peel_layers(bpy.types.Operator):
    """Peel superficial layers to reveal deep anatomy."""
    bl_idname = "anatomy.peel_layers"
    bl_label = "Peel Superficial Layers"

    def execute(self, context):
        msg = BlenderViewportController.peel_superficial_layers()
        self.report({'INFO'}, msg)
        return {'FINISHED'}


class ANATOMY_OT_reset_view(bpy.types.Operator):
    """Reset visibility and materials in viewport."""
    bl_idname = "anatomy.reset_view"
    bl_label = "Reset Viewport"

    def execute(self, context):
        BlenderViewportController.reset_visibility()
        self.report({'INFO'}, "Viewport reset.")
        return {'FINISHED'}


class ANATOMY_PT_professor_panel(bpy.types.Panel):
    """Main Sidebar Panel for the Interactive Anatomy Professor."""
    bl_label = "Gemma Anatomy Professor"
    bl_idname = "ANATOMY_PT_professor_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Anatomy Professor'

    def draw(self, context):
        layout = self.layout
        props = context.scene.anatomy_professor

        # Header Box
        box = layout.box()
        col = box.column(align=True)
        col.label(text="🧠 Professor Gemma", icon='BOOKMARKS')
        col.label(text="Grounded in Terminologia Anatomica (TA2)", icon='CHECKMARK')

        # Input Area
        layout.separator()
        layout.label(text="Ask Question or Command:")
        layout.prop(props, "user_query", text="")
        layout.operator("anatomy.ask_professor", text="Ask Professor Gemma", icon='PLAY')

        # Guided Lesson Quick Presets
        layout.separator()
        layout.label(text="Quick Masterclass Presets:")
        col = layout.column(align=True)
        op = col.operator("anatomy.load_preset", text="🫁 Respiratory System & Gas Exchange", icon='OUTLINER_OB_FORCE_FIELD')
        op.preset_query = "Show me the parts of the respiratory system responsible for oxygen infusion into the blood"

        op = col.operator("anatomy.load_preset", text="🎯 Shoulder Abduction & Innervation", icon='ORIENTATION_GIMBAL')
        op.preset_query = "Show me the muscles responsible for shoulder abduction, explain their innervation, and quiz me on them."

        op = col.operator("anatomy.load_preset", text="❤️ Cardiovascular System & Heart", icon='HEART' if hasattr(bpy.types, "HEART") else 'EXPERIMENTAL')
        op.preset_query = "Show me the heart chambers, aorta, and pulmonary vessels"

        op = col.operator("anatomy.load_preset", text="⚡ Brachial Plexus & Axillary Nerve", icon='NETWORK_DRIVE')
        op.preset_query = "Explain the innervation and spinal roots of the deltoid and rotator cuff."

        op = col.operator("anatomy.load_preset", text="🚶 Hip Abduction & Trendelenburg", icon='MOD_ARMATURE')
        op.preset_query = "Explain the muscles of hip abduction and quiz me on gait stabilization."

        # Viewport Tools
        layout.separator()
        layout.label(text="3D Viewport Controls:")
        row = layout.row(align=True)
        row.operator("anatomy.peel_layers", text="Peel Layers", icon='MOD_SOLIDIFY')
        row.operator("anatomy.reset_view", text="Reset View", icon='FILE_REFRESH')

        # Active Quiz Section
        if props.quiz_in_progress:
            layout.separator()
            qbox = layout.box()
            qbox.label(text="📝 Active Clinical Quiz", icon='HELP')
            if props.quiz_scenario:
                # Wrap scenario lines
                for sc_line in props.quiz_scenario.split(". "):
                    if sc_line:
                        qbox.label(text=sc_line.strip() + ".")

            qbox.separator()
            qbox.label(text=f"Question: {props.quiz_question}", icon='QUESTION')

            col_opts = qbox.column(align=True)
            if props.quiz_opt_1:
                op = col_opts.operator("anatomy.answer_quiz", text=f"1. {props.quiz_opt_1}")
                op.choice_index = 1
            if props.quiz_opt_2:
                op = col_opts.operator("anatomy.answer_quiz", text=f"2. {props.quiz_opt_2}")
                op.choice_index = 2
            if props.quiz_opt_3:
                op = col_opts.operator("anatomy.answer_quiz", text=f"3. {props.quiz_opt_3}")
                op.choice_index = 3
            if props.quiz_opt_4:
                op = col_opts.operator("anatomy.answer_quiz", text=f"4. {props.quiz_opt_4}")
                op.choice_index = 4

            qbox.separator()
            qbox.operator("anatomy.submit_mesh_answer", text="🎯 Submit Clicked 3D Structure", icon='RESTRICT_SELECT_OFF')

            if props.quiz_feedback:
                fbox = qbox.box()
                for fb_line in props.quiz_feedback.split("\n"):
                    if fb_line.strip():
                        fbox.label(text=fb_line.replace("#", "").strip())

        # Response Output Box
        layout.separator()
        res_box = layout.box()
        res_box.label(text="📖 Professor's Lesson Output:", icon='TEXT')
        for line in props.last_response.split("\n"):
            clean = line.replace("#", "").strip()
            if clean:
                res_box.label(text=clean)


classes = [
    AnatomyProfessorProperties,
    ANATOMY_OT_load_preset,
    ANATOMY_OT_ask_professor,
    ANATOMY_OT_answer_quiz,
    ANATOMY_OT_submit_mesh_answer,
    ANATOMY_OT_peel_layers,
    ANATOMY_OT_reset_view,
    ANATOMY_PT_professor_panel
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.anatomy_professor = bpy.props.PointerProperty(type=AnatomyProfessorProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.anatomy_professor

