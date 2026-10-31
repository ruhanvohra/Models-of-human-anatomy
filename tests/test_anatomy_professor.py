"""
Unit and Integration Tests for Gemma Anatomy Professor.
"""

import unittest
from anatomy_professor.kb.database import AnatomyDatabase
from anatomy_professor.agent.core import AnatomyProfessorAgent
from anatomy_professor.agent.tools import execute_tool


class TestAnatomyKnowledgeBase(unittest.TestCase):
    def setUp(self):
        self.db = AnatomyDatabase()

    def test_shoulder_abduction_query(self):
        muscles = self.db.find_muscles_by_action("abduction", joint="glenohumeral")
        names = [m["muscle_name"] for m in muscles]
        self.assertIn("Supraspinatus muscle", names)
        self.assertIn("Deltoid muscle", names)

    def test_innervation_accuracy(self):
        deltoid_data = self.db.get_structure_innervation("deltoid")
        self.assertTrue(len(deltoid_data) > 0)
        self.assertEqual(deltoid_data[0]["nerve_name"], "Axillary nerve")
        self.assertIn("C5", deltoid_data[0]["spinal_roots"])
        self.assertIn("C6", deltoid_data[0]["spinal_roots"])

    def test_clinical_case_retrieval(self):
        case = self.db.get_clinical_case("case_shoulder_dislocation")
        self.assertIsNotNone(case)
        self.assertEqual(case["target_structure"], "Deltoid muscle")
        self.assertEqual(case["target_nerve"], "Axillary nerve")


class TestGemmaProfessorAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AnatomyProfessorAgent()

    def test_user_example_query(self):
        prompt = "Show me the muscles responsible for shoulder abduction, explain their innervation, and quiz me on them."
        res = self.agent.process_query(prompt)

        self.assertIn("Supraspinatus", res["response"])
        self.assertIn("Deltoid", res["response"])
        self.assertIn("Axillary nerve", res["response"])
        self.assertIn("Suprascapular nerve", res["response"])
        self.assertTrue(len(res["blender_commands"]) > 0)
        self.assertIsNotNone(res["quiz"])

    def test_quiz_evaluation_option_and_mesh(self):
        self.agent.process_query("Quiz me on shoulder dislocation")
        # Test numeric option 1 (1-based index)
        eval_res = self.agent.evaluate_answer(1)
        self.assertTrue(eval_res["correct"])
        self.assertIn("Correct", eval_res["feedback"])

        # Test mesh name evaluation
        mesh_eval = self.agent.evaluate_answer("Deltoid muscle.l")
        self.assertTrue(mesh_eval["correct"])


if __name__ == "__main__":
    unittest.main()

