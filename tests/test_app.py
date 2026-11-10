"""UI branch checks using fake Streamlit calls, without installing Streamlit."""

from pathlib import Path
import runpy
import unittest
from unittest.mock import MagicMock, patch


APP = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def render(self, text, result=(0.5, "Positive"), clicked=True, failure=None):
        ui = MagicMock()
        ui.text_area.return_value = text
        ui.button.return_value = clicked
        with patch.dict("sys.modules", {"streamlit": ui}), patch(
            "sentiment.analyze_text", return_value=result, side_effect=failure
        ) as analyze:
            runpy.run_path(str(APP), run_name="__main__")
        return ui, analyze

    def test_no_analysis_before_button_click(self):
        ui, analyze = self.render("hello", clicked=False)
        analyze.assert_not_called()
        ui.success.assert_not_called()

    def test_blank_input_warns_without_analysis(self):
        for text in ("", " \n\t"):
            with self.subTest(text=text):
                ui, analyze = self.render(text)
                analyze.assert_not_called()
                ui.warning.assert_called_once()

    def test_positive_result_displays_score_and_balloons(self):
        ui, analyze = self.render("good", (0.5, "Positive"))
        analyze.assert_called_once_with("good")
        ui.success.assert_called_once_with(":blush: Positive (Score: 0.50)")
        ui.balloons.assert_called_once()
        ui.error.assert_not_called()
        ui.info.assert_not_called()

    def test_negative_result_displays_score(self):
        ui, _ = self.render("bad", (-0.5, "Negative"))
        ui.error.assert_called_once_with(":rage: Negative (Score: -0.50)")
        ui.success.assert_not_called()
        ui.balloons.assert_not_called()

    def test_analyzer_failure_shows_safe_error_without_result(self):
        ui, analyze = self.render("sample input", failure=RuntimeError("internal detail"))
        analyze.assert_called_once_with("sample input")
        ui.error.assert_called_once_with(
            "Analysis is unavailable. Please try again or check the local installation.")
        ui.success.assert_not_called()
        ui.info.assert_not_called()
        ui.balloons.assert_not_called()
        ui.subheader.assert_not_called()

    def test_neutral_result_displays_zero(self):
        ui, _ = self.render("table", (0.0, "Neutral"))
        ui.info.assert_called_once_with(":neutral_face: Neutral (Score: 0.00)")
        ui.balloons.assert_not_called()


if __name__ == "__main__":
    unittest.main()
