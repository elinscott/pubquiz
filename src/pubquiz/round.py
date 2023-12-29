"""Module for the Round class."""

from collections import UserList
from random import shuffle
from typing import List, Optional

from pubquiz.question import Question


class Round(UserList):
    """Class representing a round in a pub quiz."""

    def __init__(self, title, description="", questions: Optional[List[Question]] = None, sheet: Optional[List[str]] = None):
        """Initialize the round."""
        questions = questions or []
        super().__init__(questions)
        self.title = title
        self.description = description

    def __repr__(self):
        return f"Round(title={self.title})"

    @classmethod
    def from_dict(cls, dct):
        """Create a round object from a dictionary."""
        questions = dct.pop("questions", [])
        return cls(**dct, questions=[Question.from_dict(q) for q in questions])

    def shuffle(self):
        """Shuffle the questions in the round."""
        shuffle(self.questions)

    def to_sheets(self, with_answers=True, index=1) -> List[str]:
        """Generate the LaTeX code for the quiz sheets."""
        lines = [
            r"\newpage",
            r"\begin{center}",
            r"\Huge",
            f"Round {index}: {self.title}"
            r"\end{center}",
            r"\LARGE",
        ]
        if len(self.description) > 0:
            if not with_answers:
                lines += [r"\vspace{-1cm}"]
            lines += [self.description]
        if with_answers:
            lines += [r"\large", r"\begin{enumerate}"]
            lines += [r"\item " + str(q) for q in self]
            lines += [r"\end{enumerate}", r"\LARGE"]
        else:
            lines += [r"\Huge", r"\begin{enumerate}"]
            lines += [r"\item" for q in self]
            lines += [r"\end{enumerate}", ""]
        return lines

    def to_slides(self, with_answers=True) -> List[str]:
        """Generate the LaTeX code for the slides."""
        lines = []
        for iq, q in enumerate(self):
            lines.append(q.to_slide(index=iq + 1, with_answer=with_answers))
        return lines