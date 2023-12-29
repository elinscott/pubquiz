"""Module containing the Quiz class."""

from collections import UserList
from pathlib import Path
from typing import List, Optional

from yaml import safe_load

from pubquiz.latex_templates import beamer_header, beamer_preamble, latex_header
from pubquiz.round import Round


class Quiz(UserList):
    """Class representing a pub quiz."""

    def __init__(
        self, title, rounds: Optional[List[Round]] = None, slides_preamble: Optional[Path] = None
    ):
        """Initialize the quiz."""
        rounds = rounds or []
        super().__init__(rounds)
        self.title = title
        if slides_preamble is None:
            slides_preamble = beamer_preamble

    @classmethod
    def from_yaml(cls, filename: Path):
        """Create a quiz object from a yaml file."""
        with open(filename, "r") as f:
            data = safe_load(f)
        return cls(**data)

    def to_sheets(self, answers=False):
        """
        Generate the latex code for the quiz sheets.

        :param answers: if True, the answers to the questions will be included in the sheets.
        :type answers: bool

        :returns: a list of strings containing the latex code for the quiz sheets
        """
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
            + [r.title + r" & \\" for r in self.rounds]
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
        lines = latex_header + [r"\begin{document}"]

        if not answers:
            lines += titlepage

        # Standard rounds
        for i, r in enumerate(self.rounds):
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
                lines += [r"\item " + str(q) for q in r.questions]
                lines += [r"\end{enumerate}", r"\LARGE"]
            else:
                lines += [r"\Huge", r"\begin{enumerate}"]
                lines += [r"\item" for q in r.questions]
                lines += [r"\end{enumerate}", ""]

        # Picture and puzzle
        for _ in ["pictures", "puzzles"]:
            raise NotImplementedError()  # noqa
            # if answers:
            #     os.system(f"cp {r}.tex {r}_with_answers.tex")
            #     os.system(f"sed -i -e 's/%%//g' {r}_with_answers.tex")
            #     os.system(f"sed -i -e 's/Large/large/g' {r}_with_answers.tex")
            #     r += "_with_answers"
            # lines += [r"\newpage", r"\Huge", "\input{" + r + ".tex}"]

        # Footer
        lines += [r"\end{document}"]

        # if answers:
        #    fname = "questions.tex"
        # else:
        #    fname = "answer_sheets.tex"
        # with open(fname, "w") as f:
        #    f.write("\n".join(lines))
        return lines

    def to_slides(self):
        """Generate the latex code for the quiz slides."""
        # Header
        lines = beamer_header + [r"\begin{document}", r"\include{preamble}"]

        # Standard rounds
        for i, r in enumerate(self.rounds):
            # Questions
            lines += [
                r"\begin{frame}",
                r"\begin{center}",
                r"\Huge",
                f"Round {i+1}: {r.title}",
                r"\end{center}",
                r"\end{frame}",
            ]
            for iq, q in enumerate(r.questions):
                lines += q.as_slide(index=iq + 1)

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
            for iq, q in enumerate(r.questions):
                lines += q.as_slide(index=iq + 1, with_answer=True)

        # Footer
        lines += [r"\include{picture_slides}"]
        lines += [r"\end{document}"]

        with open("slides.tex", "w") as f:
            f.write("\n".join(lines))
