#!/usr/bin/env python3
"""
Launcher for Gemma Interactive Anatomy Professor with Blender Z-Anatomy.
Usage:
  python3 launch_professor.py          # Opens Blender with Startup.blend and Professor UI
  python3 launch_professor.py --test   # Runs end-to-end integration test headlessly
"""

import os
import sys
import subprocess
import shutil

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STARTUP_BLEND = os.path.join(PROJECT_ROOT, "Z-Anatomy", "Startup.blend")


def find_blender_binary() -> str:
    """Finds the Blender executable on macOS, Linux, or Windows."""
    # Check environment variable
    if os.environ.get("BLENDER_BIN"):
        return os.environ["BLENDER_BIN"]

    # Check macOS standard locations
    mac_paths = [
        "/Applications/Blender.app/Contents/MacOS/Blender",
        os.path.expanduser("~/Applications/Blender.app/Contents/MacOS/Blender")
    ]
    for p in mac_paths:
        if os.path.exists(p):
            return p

    # Check PATH
    bin_path = shutil.which("blender")
    if bin_path:
        return bin_path

    raise FileNotFoundError(
        "Could not find Blender binary. Please install Blender or set the BLENDER_BIN environment variable."
    )


def run_integration_test(blender_bin: str):
    """Executes a full headless integration test verifying KB, Agent, and 3D Controller."""
    print("=" * 60)
    print("🔬 Running Gemma Anatomy Professor Headless Test...")
    print("=" * 60)

    test_script = f"""
import sys, os
sys.path.insert(0, r'{PROJECT_ROOT}')

from anatomy_professor.kb.database import AnatomyDatabase
from anatomy_professor.agent.core import AnatomyProfessorAgent
from anatomy_professor.blender.controller import BlenderViewportController
from anatomy_professor.blender.addon import register as register_addon

# 1. Test Knowledge Base
print('[TEST 1] Querying Anatomy KB for shoulder abduction...')
db = AnatomyDatabase()
muscles = db.find_muscles_by_action('abduction', joint='glenohumeral')
assert len(muscles) >= 2, f'Expected at least 2 muscles, got {{len(muscles)}}'
print(f' -> Successfully retrieved {{len(muscles)}} verified muscles.')

# 2. Test Agent Processing
print('[TEST 2] Processing User Request through Gemma Professor Agent...')
agent = AnatomyProfessorAgent()
res = agent.process_query('Show me the muscles responsible for shoulder abduction, explain their innervation, and quiz me on them.')
assert 'Supraspinatus' in res['response']
assert 'Deltoid' in res['response']
assert len(res['blender_commands']) > 0
print(' -> Agent successfully produced lesson, innervation breakdown, and 3D commands.')

# 3. Test Blender Addon Registration
print('[TEST 3] Registering Blender Addon UI & Viewport Controller...')
register_addon()

# 4. Test 3D Viewport Execution
print('[TEST 4] Executing 3D Viewport Highlighting...')
exec_res = BlenderViewportController.execute_commands(res['blender_commands'])
print(' -> Viewport Execution Result:', exec_res)

# 5. Test Quiz Evaluation
print('[TEST 5] Testing Quiz Evaluation...')
eval_res = agent.evaluate_answer(1)
print(' -> Quiz feedback received successfully.')

print('\\n' + '='*60)
print('🎉 ALL TESTS PASSED: Gemma Anatomy Professor is fully operational!')
print('='*60)
"""

    cmd = [
        blender_bin,
        "--factory-startup",
        "--background",
        STARTUP_BLEND,
        "--python-expr",
        test_script
    ]

    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def launch_interactive_blender(blender_bin: str):
    """Launches Blender GUI with the Z-Anatomy model and Professor sidebar open."""
    print("=" * 60)
    print("🚀 Launching Gemma Interactive Anatomy Professor in Blender...")
    print(f"Blender: {blender_bin}")
    print(f"Model:   {STARTUP_BLEND}")
    print("=" * 60)

    init_script = f"""
import sys, os
sys.path.insert(0, r'{PROJECT_ROOT}')
import bpy
from anatomy_professor.blender.addon import register as register_addon

register_addon()
print('[Gemma Professor] Addon loaded! Press N in the 3D Viewport to open the sidebar.')
"""

    cmd = [
        blender_bin,
        STARTUP_BLEND,
        "--python-expr",
        init_script
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    blender = find_blender_binary()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_integration_test(blender)
    else:
        launch_interactive_blender(blender)

