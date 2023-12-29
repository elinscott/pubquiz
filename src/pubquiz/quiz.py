"""Module containing the Quiz class."""

from collections import UserList
from pathlib import Path
from typing import List, Optional
import shutil

from yaml import safe_load

from pubquiz.round import Round
from pubquiz.latex_templates import path as latex_templates_path


class Quiz(UserList):
    """Class representing a pub quiz."""

    def __init__( self, title, author: str, date: str = r'\today', rounds: Optional[List[Round]] = None):
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

    def to_sheets(self, answers=False):
        """
        Generate the latex code for the quiz sheets.

        :param answers: if True, the answers to the questions will be included in the sheets.
        :type answers: bool

        :returns: a list of strings containing the latex code for the quiz sheets
        """

        # Make sure we have sheets_header.tex in the current directory
        if not Path("sheets_header.tex").exists():
            shutil.copy(latex_templates_path / 'sheets_header.tex', '.')
            print('Generating a default sheets_header.tex file. Please edit this file to suit your needs.')

            
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
                r"Picture: Overpaid & \\",
                r"Puzzles: Connect four & \\",
                r"TOTAL \\",
                r"\hline",
                r"\end{tabular}",
                r"\thispagestyle{empty}",
                r"\Huge",
            ]
        )

        # Header
        lines = [r"\input{sheets_header}"]
        if not answers:
            lines += [r"\rhead{\huge \fbox{\parbox{3.5cm}{Score}}}"]
        lines += [r"\begin{document}"]

        if not answers:
            lines += titlepage

        # Standard rounds
        for i, r in enumerate(self):
            lines += [
                r"\newpage",
                r"\begin{center}",
                r"\Huge",
                "Round {0}: {1}".format(i + 1, r.title),
                r"\end{center}",
                r"\LARGE",
            ]
            if len(r.description) > 0:
                if not answers:
                    lines += [r"\vspace{-1cm}"]
                lines += [r.description]
            if answers:
                lines += [r"\large", r"\begin{enumerate}"]
                lines += [r"\item " + str(q) for q in r]
                lines += [r"\end{enumerate}", r"\LARGE"]
            else:
                lines += [r"\Huge", r"\begin{enumerate}"]
                lines += [r"\item" for q in r]
                lines += [r"\end{enumerate}", ""]

        # # Picture and puzzle
        # for _ in ["pictures", "puzzles"]:
        #     # if answers:
        #     #     os.system(f"cp {r}.tex {r}_with_answers.tex")
        #     #     os.system(f"sed -i -e 's/%%//g' {r}_with_answers.tex")
        #     #     os.system(f"sed -i -e 's/Large/large/g' {r}_with_answers.tex")
        #     #     r += "_with_answers"
        #     # lines += [r"\newpage", r"\Huge", "\input{" + r + ".tex}"]

        # Footer
        lines += [r"\end{document}"]

        # if answers:
        #    fname = "questions.tex"
        # else:
        #    fname = "answer_sheets.tex"
        # with open(fname, "w") as f:
        #    f.write("\n".join(lines))
        return '\n'.join(lines)

    def to_slides(self):
        """Generate the latex code for the quiz slides."""

        # Ensure we have the header and preamble
        if not Path("slides_header.tex").exists():
            shutil.copy(latex_templates_path / 'slides_header.tex', '.')
            print('Generating a default slides_header.tex file. Please edit this file to suit your needs.')
        if not Path("photo.png").exists():
            shutil.copy(latex_templates_path / 'photo.png', '.')
            print('Generating a default photo.png file to use in the title slide. Please replace this file to suit your needs.')
        if not Path("slides_preamble.tex").exists():
            shutil.copy(latex_templates_path / 'slides_preamble.tex', '.')
            print('Generating a default slides_preamble.tex file. Please edit this file to suit your needs.')

        # Header
        lines = [r"\input{slides_header}", r"\title{" + self.title + "}", r"\author{" + self.author + "}"]
        date = self.date or r"\today"
        lines += [r"\date{" + date + "}"]
        lines += [r"\begin{document}", r"\include{slides_preamble}", r"\frame{\titlepage}"]

        # Standard rounds
        for i, r in enumerate(self):
            # Questions
            lines += [
                r"\begin{frame}",
                r"\begin{center}",
                r"\Huge",
                f"Round {i+1}: {r.title}",
                r"\end{center}",
                r"\end{frame}",
            ]
            for iq, q in enumerate(r):
                lines.append(q.to_slide(index=iq + 1))

            # Answers
            lines += [
                r"\begin{frame}",
                r"\begin{center}",
                r"\Huge",
                "Answers",
                r"\end{center}",
                r"\end{frame}",
            ]
            if r.title == "Underworked":
                continue
            for iq, q in enumerate(r):
                lines.append(q.to_slide(index=iq + 1, with_answer=True))

        # Footer
        lines += [r"\include{picture_slides}"]
        lines += [r"\end{document}"]

        return "\n".join(lines)
