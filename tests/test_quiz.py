"""Testing the Quiz class."""

from pathlib import Path

from pubquiz import Quiz


def test_from_yaml():
    """Test the :classmethod:Quiz.from_yaml() classmethod."""
    Quiz.from_yaml(Path(__file__).parents[1] / "docs/source/example_quiz.yaml")
