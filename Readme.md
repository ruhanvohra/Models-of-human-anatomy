# Z-Anatomy: Gemma Interactive Anatomy Professor

[![CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-sa/4.0/)
[![Blender 4.0+](https://img.shields.io/badge/Blender-4.0%20%7C%205.x-orange.svg)](https://www.blender.org/)
[![Gemma AI](https://img.shields.io/badge/AI-Gemma%204%20Integrated-blue.svg)](https://ai.google.dev/gemma)
[![Tests Passing](https://img.shields.io/badge/Tests-Passing%20(100%25)-brightgreen.svg)](tests/test_anatomy_professor.py)

An open-source, interactive 3D human anatomy atlas integrated with an AI **Anatomy Professor** powered by **Gemma**. The system connects natural language medical queries to a 3D anatomical viewer in Blender, strictly grounded in verified anatomical nomenclature (**Terminologia Anatomica 2 / TA2**).

[![Z-Anatomy video](https://img.youtube.com/vi/NNNUPDoFMYw/0.jpg)](https://www.youtube.com/watch?v=NNNUPDoFMYw)

---

## 🌟 Key Capabilities

- **Natural-Language Anatomical Navigation**: Ask questions across all major organ systems (Respiratory, Digestive, Cardiovascular, Nervous, Musculoskeletal, Urinary).
- **Strict Medical Grounding (No Hallucinations)**: Queries a structured SQLite database indexing 7,192 official TA2 structures, biomechanical relationships, and neuroanatomical nerve roots.
- **Automated Scene Collection & Viewport Toggling**: Asking a question automatically enables, un-excludes, and unhides the required system collections (e.g. Visceral, Muscular, Cardiovascular) and frames the camera on the target organs.
- **Interactive Multi-Color Highlighting**: Applies emissive Principled BSDF shaders to distinguish functional units (e.g. Cyan for initiators, Gold for prime movers, Red for arteries, Blue for veins).
- **Automated Layer Peeling**: Strips obscuring structures (e.g., ribs and pectoralis muscles for lungs; abdominal wall muscles for retroperitoneal organs like the pancreas and kidneys).
- **Interactive Socratic Quizzes**: Administers clinical vignettes with instant grading via multiple choice buttons or by **clicking 3D meshes directly in the viewport**.

---

## 🛠️ Technical Changes from the Original Project

This fork addresses critical bugs in the original Z-Anatomy template and integrates the complete Gemma Anatomy Professor subsystem:

### 1. Z-Anatomy Core Bug Fixes
- **Keymap File Resolution**: Fixed a broken hardcoded path in `Z-Anatomy/__init__.py` looking for `Z-Anatomy.py` instead of `Anatomy-shortcuts.py`. Added fallback search and compatibility symlinks.
- **Infinite Registration Timer Loop**: Removed an uncontrolled `bpy.app.timers.register` retry loop that spammed exceptions every 0.1s on keymap import failure.
- **Operator Registration Order**: Corrected the lifecycle order in `register()` so classes and scene properties are registered *before* keymaps, preventing `'OperatorProperties' object has no attribute 'unselected'` errors.
- **Keymap Indexing Safeguards**: Guarded against `IndexError: list index out of range` and `UnboundLocalError` when Blender initializes with factory defaults.
- **Headless / Startup Crash Guard**: Added null-guards for `bpy.context.screen.areas` during background/headless execution.
- **Circular Dependency Cycle Elimination**: Removed a circular parent-bevel dependency in `Startup.blend` where `Oesophagus-profile` was parented to `Oesophagus` while serving as its curve bevel object.
- **View Layer Selection Safety**: Protected against `RuntimeError: Object cannot be selected because it is not in View Layer` by checking `bpy.context.view_layer.objects` and filtering out curve bevel helper objects (`*-profile`).
- **Blender Operator Property Caching Fix**: Separated preset masterclass loading from live user query inputs to prevent cached preset queries from overriding new text inputs.

### 2. New Subsystems & Architecture
```
Models-of-human-anatomy/
├── anatomy_professor/
│   ├── kb/
│   │   ├── seed_data.py          # Ground-truth biomechanics, innervations, systems & clinical cases
│   │   ├── builder.py            # SQLite indexer parsing 7,192 TA2 structures
│   │   ├── database.py           # Thread-safe grounded query API
│   │   └── anatomy_kb.db         # Indexed SQLite knowledge base
│   ├── agent/
│   │   ├── prompts.py            # Socratic pedagogy system prompts
│   │   ├── tools.py              # Function calling schemas (KB query, Blender control, Quiz)
│   │   └── core.py               # Gemma Agent core with multi-system physiological reasoning
│   └── blender/
│       ├── controller.py         # 3D Viewport controller with auto-collection toggling
│       ├── ui.py                 # N-Panel Sidebar UI (Chat, presets, quiz card, mesh submission)
│       └── addon.py              # Standard Blender addon registration entry point
├── launch_professor.py           # One-command CLI/GUI runner with automated setup
└── tests/
    └── test_anatomy_professor.py # Automated test suite (100% passing)
```

### 3. Repository & Storage Optimization
- Added `.gitignore` to keep uncompressed 286 MB `.blend` files local on disk while keeping the git commit history lightweight.
- Re-compressed `Z-Anatomy.zip` at level 9 deflate down to **82.65 MB** (comfortably under GitHub's 100 MB hard limit).

---

## 🚀 Installation & Setup

### Prerequisites
- **Blender 4.0, 4.2, 5.0, or newer**: [Download Blender](https://www.blender.org/download/)
- **Python 3.10+** (standard on modern operating systems)

### Method 1: One-Command Launcher (Recommended)

Clone the repository and launch the application directly:

```bash
git clone https://github.com/ruhanvohra/Models-of-human-anatomy.git
cd Models-of-human-anatomy
python3 launch_professor.py
```

`launch_professor.py` will automatically:
1. Locate your Blender installation (macOS, Linux, or Windows).
2. Load `Z-Anatomy/Startup.blend`.
3. Register the **Gemma Anatomy Professor** addon and open the 3D Viewport.

### Method 2: Manual Installation as Blender Application Template

1. Open Blender.
2. Click the Blender icon in the upper-left corner of the window.
3. Choose **Install Application Template** and select `Z-Anatomy.zip`.
4. Go to **File > New > Z-Anatomy**.

---

## 📖 How to Use Professor Gemma in Blender

1. **Open the Professor Panel**:
   - In Blender's 3D Viewport, press **`N`** (or click the small arrow on the right edge) to expand the sidebar tabs.
   - Click the **`Anatomy Professor`** tab.

2. **Ask Any Anatomical or Physiological Question**:
   Type your question into the input box and click **`Ask Professor Gemma`**. For example:
   - *"Show me the parts of the respiratory system responsible for oxygen infusion into the blood"*
   - *"Show me the parts of the digestive system responsible for lowering blood sugar"*
   - *"Show me the muscles responsible for shoulder abduction, explain their innervation, and quiz me on them."*
   - *"Show me the heart chambers, aorta, and pulmonary vessels"*
   - *"Where is the femur located?"*

3. **Automatic Viewport Behavior**:
   - The scene collection containing the target organs (e.g. `8: Visceral systems`, `4: Muscular system`) will automatically be enabled and unhidden in the Outliner.
   - Obscuring structures (like ribs or abdominal muscles) will be automatically peeled away.
   - The target organs illuminate with functional color-coding.
   - The camera automatically centers and frames the target anatomy.

4. **Interactive Clinical Quizzing**:
   - When asking for a quiz (e.g., *"Quiz me on shoulder abduction"*), a clinical scenario appears in the sidebar.
   - **Option A (Multiple Choice)**: Click buttons **`1`**, **`2`**, **`3`**, or **`4`**.
   - **Option B (3D Selection)**: Left-click any muscle or organ directly in the 3D model, then click **`🎯 Submit Clicked 3D Structure`**.
   - Professor Gemma provides immediate feedback and highlights the correct structure.

5. **Manual Viewport Controls**:
   - **`Peel Layers`**: Successively hides superficial fascia and outer layers to reveal deeper anatomy.
   - **`Reset View`**: Restores default visibility and resets materials.

---

## 🧪 Testing

To run the full suite of unit and integration tests:

```bash
# Run unit tests
python3 -m unittest discover tests

# Run full headless integration test through Blender
python3 launch_professor.py --test
```

---

## 📄 License

All code and content shared by 'Z-Anatomy' is under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png

---

## 👥 Attributions & Authors

### Original Models & Project
- **BodyParts3D**: The Database Center for Life Science (CC-BY-SA 2.1 Japan)
- **Z-Anatomy Atlas**: Gauthier KERVYN (Design, 3D, anatomy), Marcin ZIELINSKI (Python Blender addon), Lluis VINENT (Unity development).
- Additional reference models:
  - *"Brainder" and "White matter"*: University of Washington
  - *"Cranial Nerves and Foramina"*: University of Dundee, CAHID (CC-BY 4.0)
  - *"Anatomy of the Inner Ear"*: University of Dundee School of Medicine (CC-BY-NC-SA 4.0)
  - *"Kidney"*: Lissie Cowley (CC-BY-NC 4.0)

### Definitions & Nomenclature
- **Terminologia Anatomica 2 (TA2)**: Federative International Programme on Anatomical Terminologies (FIPAT).
- **Wikipedia**: (CC-BY-SA 3.0)

### Translations
- Ana Teresa BIGIO (Portuguese)
- Carlos TORRES VILLAR (Spanish)
- Paola Perin, Daniele Cossellu, Elisa Vivado (Italian)
- Jadwiga Palosz (Polish)
- Shariar Ahmadpour (Parsi)

### Contributors
- Ruhan Vohra (Gemma Interactive Anatomy Professor, TA2 Knowledge Base, Blender Viewport Controller, Bug Fixes)
- Esteban Fuentes
- Noah Lucas
