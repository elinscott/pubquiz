"""Module for the Round class."""

from collections import UserList
from pathlib import Path
from random import shuffle
from typing import List, Optional

from pubquiz.question import Question
from pubquiz.slides import header_slide


class Round(UserList):
    """Class representing a round in a pub quiz."""

    def __init__(
        self,
        title,
        description="",
        questions: Optional[List[Question]] = None,
        solve_in_own_time: bool = False,
        randomize: bool = False,
        sheets: Optional[Path] = None,
    ):
        """Initialize the round."""
        questions = questions or []
        if randomize:
            shuffle(questions)
        super().__init__(questions)
        self.title = title
        self.description = description
        self.solve_in_own_time = solve_in_own_time
        self.randomize = randomize
        self.sheets = sheets

    def __repr__(self):
        return f"Round(title={self.title})"

    @classmethod
    def from_dict(cls, dct):
        """Create a round object from a dictionary."""
        questions = dct.pop("questions", [])
        return cls(**dct, questions=[Question.from_dict(q) for q in questions])

    def _sheets_content(self, with_answers: bool = True) -> List[str]:
        """Generate the LaTeX code for the body of the sheet for this round, either with or without the answers."""
        if self.sheets:
            return [r"\input{" + str(self.sheets) + "}"]

        lines = []
        if with_answers:
            lines += [r"\large", r"\begin{enumerate}"]
            lines += [r"\item " + str(q) for q in self]
            lines += [r"\end{enumerate}", r"\LARGE"]
        else:
            if self.solve_in_own_time:
                lines += [r"\large"]
            else:
                lines += [r"\Huge"]
            lines += [r"\begin{enumerate}"]
            if self.solve_in_own_time:
                # Show the questions
                lines += [rf"\item {q.question}" for q in self]
            else:
                lines += [r"\item" for _ in self]
            lines += [r"\end{enumerate}", ""]
        return lines

    def to_sheets(self, with_answers=True, index=1) -> List[str]:
        """Generate the LaTeX code for the quiz sheets."""
        header = self.title if ":" in self.title else f"Round {index}: {self.title}"
        lines = [r"\newpage", r"\begin{center}", r"\Huge", header, r"\end{center}"]

        lines += [r"\large"]

        if len(self.description) > 0:
            lines += [self.description, ""]

        lines += self._sheets_content(with_answers=with_answers)
        return lines

    def _slides_content(self, with_answers: bool = True) -> List[str]:
        """Generate the LaTeX code for the slides, either with or without the answers."""
        lines = []
        for iq, q in enumerate(self):
            lines.append(q.to_slide(index=iq + 1, with_answer=with_answers))
        return lines

    def to_slides(self, index=1) -> List[str]:
        """Generate the LaTeX code for the slides.

        Includes headers and (possibly) first all the questions without and then with the answers

        :param index: the index of the round
        :type index: int

        :returns: a list containing the lines of latex code for the slides
        """
        # Round header
        if ":" not in self.title:
            heading = f"Round {index}: {self.title}"
        else:
            heading = self.title
        lines = header_slide(heading)

        if not self.solve_in_own_time:
            # Questions without answers
            lines += self._slides_content(with_answers=False)

            # Answer header
            lines += header_slide("Answers")

        # Questions with answers
        lines += self._slides_content(with_answers=True)

        return lines
