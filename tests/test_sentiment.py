import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from sentiment import analyze_text, classify_polarity


class SentimentTests(unittest.TestCase):
    def test_positive_scores_include_upper_boundary(self):
        for score in (0.0001, 0.5, 1.0):
            with self.subTest(score=score):
                self.assertEqual(classify_polarity(score), "Positive")

    def test_negative_scores_include_lower_boundary(self):
        for score in (-0.0001, -0.5, -1.0):
            with self.subTest(score=score):
                self.assertEqual(classify_polarity(score), "Negative")

    def test_zero_is_neutral(self):
        self.assertEqual(classify_polarity(0.0), "Neutral")

    def test_invalid_polarities_are_rejected(self):
        for score in (float("nan"), float("inf"), -float("inf"), -1.01, 1.01):
            with self.subTest(score=score), self.assertRaises(ValueError):
                classify_polarity(score)

    def test_blank_input_is_rejected_before_analyzer_is_called(self):
        analyzer = Mock()
        for text in ("", " ", "\n\t"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                analyze_text(text, analyzer)
        analyzer.assert_not_called()

    def test_analyzer_receives_original_text_and_returns_polarity_and_label(self):
        for score, label in ((0.75, "Positive"), (-0.5, "Negative"), (0, "Neutral")):
            with self.subTest(score=score):
                analyzer = Mock(return_value=SimpleNamespace(
                    sentiment=SimpleNamespace(polarity=score)))
                self.assertEqual(analyze_text("  example  ", analyzer), (score, label))
                analyzer.assert_called_once_with("  example  ")

    def test_invalid_analyzer_output_is_not_displayed_as_a_valid_result(self):
        analyzer = Mock(return_value=SimpleNamespace(
            sentiment=SimpleNamespace(polarity=float("nan"))))
        with self.assertRaises(ValueError):
            analyze_text("example", analyzer)

    def test_analyzer_failure_is_not_silently_changed_to_neutral(self):
        analyzer = Mock(side_effect=RuntimeError("analyzer unavailable"))
        with self.assertRaisesRegex(RuntimeError, "analyzer unavailable"):
            analyze_text("example", analyzer)


if __name__ == "__main__":
    unittest.main()
