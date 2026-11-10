"""Opt-in real dependency checks; CI runs these inside the built image."""

import os
from pathlib import Path
import unittest

from sentiment import analyze_text


@unittest.skipUnless(os.environ.get("RUN_DEPENDENCY_TESTS") == "1",
                     "Set RUN_DEPENDENCY_TESTS=1 in an approved dependency environment")
class DependencyTests(unittest.TestCase):
    def test_real_textblob_positive_negative_and_neutral(self):
        for text, label in (("I love this wonderful day", "Positive"),
                            ("I hate this terrible day", "Negative"),
                            ("table", "Neutral")):
            with self.subTest(text=text):
                score, actual = analyze_text(text)
                self.assertEqual(actual, label)
                self.assertTrue(-1 <= score <= 1)

    def test_real_streamlit_app_starts_and_renders_positive_analysis(self):
        from streamlit.testing.v1 import AppTest

        app = Path(__file__).resolve().parents[1] / "app.py"
        at = AppTest.from_file(str(app)).run(timeout=15)
        self.assertFalse(at.exception)
        at.text_area[0].input("I love this wonderful day").run(timeout=15)
        at.button[0].click().run(timeout=15)
        self.assertFalse(at.exception)
        self.assertEqual(len(at.success), 1)
        self.assertIn("Positive", at.success[0].value)

    def test_real_streamlit_blank_negative_and_neutral_inputs(self):
        from streamlit.testing.v1 import AppTest

        app = Path(__file__).resolve().parents[1] / "app.py"
        at = AppTest.from_file(str(app)).run(timeout=15)
        for text, output in ((" \n\t", "warning"),
                             ("I hate this terrible day", "error"),
                             ("table", "info")):
            with self.subTest(output=output):
                at.text_area[0].input(text).run(timeout=15)
                at.button[0].click().run(timeout=15)
                self.assertFalse(at.exception)
                self.assertEqual(len(getattr(at, output)), 1)
                self.assertEqual(len(at.success), 0)


if __name__ == "__main__":
    unittest.main()
