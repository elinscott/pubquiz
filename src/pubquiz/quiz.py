"""Module containing the Quiz class."""

import shutil
from collections import UserList
from pathlib import Path
from typing import List, Optional

from yaml import safe_load

from pubquiz.latex_templates import path as latex_templates_path
from pubquiz.round import Round


class Quiz(UserList):
    """Class representing a pub quiz."""

    def __init__(
        self, title, author: str, date: str = r"\today", rounds: Optional[List[Round]] = None
    ):
        """Initialize the quiz."""
        rounds = rounds or []
        super().__init__(rounds)
        self.title = title
        self.author = author
        self.date = date

    def __repr__(self) -> str:
        return f"Quiz(title={self.title}, rounds=[{', '.join([r.title for r in self])}])"

    @classmethod
    def from_dict(cls, dct):
        """Create a quiz object from a dictionary."""
        rounds = dct.pop("rounds", [])
        return cls(**dct, rounds=[Round.from_dict(r) for r in rounds])

    @classmethod
    def from_yaml(cls, filename: Path):
        """Create a quiz object from a yaml file."""
        with open(filename, "r") as f:
            dct = safe_load(f)
        return cls.from_dict(dct)

    def to_sheets(self, with_answers=False) -> str:
        """
        Generate the latex code for the quiz sheets.

        :param with_answers: if True, the answers to the questions will be included in the sheets.
        :type with_answers: bool

        :returns: a list of strings containing the latex code for the quiz sheets
        """
        # Make sure we have sheets_header.tex in the current directory
        if not Path("sheets_header.tex").exists():
            shutil.copy(latex_templates_path / "sheets_header.tex", ".")
            print(
                "Generating a default sheets_header.tex file. Please edit this file to suit your needs."
            )

        # N.B. will not do picture and puzzle rounds, these must be contained in pictures.tex and puzzles.tex
        titlepage = (
            [
                r"\centering",
                r"\Huge",
                self.title,
                r"\vspace{2cm}",
                r"",
                r"\LARGE",
                r"Team Name: \underline{\hphantom{XXXXXXXXXXXXXXXXXXXXXXXXXX}}",
                r"",
                r"\vspace{3cm}",
                r"",
                r"\LARGE",
                r"\begin{tabular}{ll}",
                r"\hline",
                r"Round & Score \\",
                r"\hline",
            ]
            + [r.title + r" & \\" for r in self]
            + [
                r"TOTAL \\",
                r"\hline",
                r"\end{tabular}",
                r"\thispagestyle{empty}",
                r"\Huge",
            ]
        )

        # Header
        lines = [r"\input{sheets_header}"]
        if not with_answers:
            lines += [r"\rhead{\huge \fbox{\parbox{3.5cm}{Score}}}"]
        lines += [r"\begin{document}"]

        if not with_answers:
            lines += titlepage

        # Standard rounds
        for i, r in enumerate(self):
            lines += r.to_sheets(with_answers=with_answers, index=i + 1)

        # Footer
        lines += [r"\end{document}"]

        return "\n".join(lines)

    def to_slides(self) -> str:
        """Generate the latex code for the quiz slides."""
        # Ensure we have the header and preamble
        if not Path("slides_header.tex").exists():
            shutil.copy(latex_templates_path / "slides_header.tex", ".")
            print(
                "Generating a default slides_header.tex file. Please edit this file to suit your needs."
            )
        if not Path("photo.png").exists():
            shutil.copy(latex_templates_path / "photo.png", ".")
            print(
                "Generating a default photo.png file to use in the title slide. Please replace this file to "
                "suit your needs."
            )
        if not Path("slides_preamble.tex").exists():
            shutil.copy(latex_templates_path / "slides_preamble.tex", ".")
            print(
                "Generating a default slides_preamble.tex file. Please edit this file to suit your needs."
            )

        # Header
        lines = [
            r"\input{slides_header}",
            r"\title{" + self.title + "}",
            r"\author{" + self.author + "}",
        ]
        date = self.date or r"\today"
        lines += [r"\date{" + date + "}"]
        lines += [r"\begin{document}", r"\frame{\titlepage}", r"\include{slides_preamble}"]

        # Loop over rounds and generate slides
        for i, r in enumerate(self):
            lines += r.to_slides(index=i + 1)

        # Footer
        lines += [r"\end{document}"]

        return "\n".join(lines)
