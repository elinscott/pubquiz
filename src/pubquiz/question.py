"""Module defining the Question class."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Question:
    """Class representing a question in a pub quiz."""

    question: Optional[str] = None
    answer: Optional[str] = None
    question_pic: Optional[Path] = None
    question_pic_height: float = 0.6
    question_pic_credit: Optional[str] = None
    question_slide: Optional[Path] = None
    answer_pic: Optional[Path] = None
    answer_pic_height: float = 0.6
    answer_pic_credit: Optional[str] = None
    answer_slide: Optional[Path] = None

    def __post_init__(self):
        if self.question and Path(self.question).exists():
            self.question = r"\input{" + self.question + "}"
        if self.answer and Path(self.answer).exists():
            self.answer = r"\input{" + self.answer + "}"
        if self.question_slide and Path(self.question_slide).exists():
            self.question_slide = r"\input{" + self.question_slide + "}"
        if self.answer_slide and Path(self.answer_slide).exists():
            self.answer_slide = r"\input{" + self.answer_slide + "}"

    def __repr__(self):
        return self.question + " (" + self.answer + ")"

    @classmethod
    def from_dict(cls, dct):
        """Create a question object from a dictionary."""
        return cls(**dct)

    def to_slide(self, index, with_answer=False):
        """Generate the LaTeX code for a slide presenting this question."""
        # Allow manual override of as_slide(), to allow for more complex slides to be generated by hand
        if self.question_slide and not with_answer:
            return "\n".join([r"\begin{frame}", self.question_slide, r"\end{frame}"])
        elif self.answer_slide and with_answer:
            return "\n".join([r"\begin{frame}", self.answer_slide, r"\end{frame}"])

        lines = [r"\begin{frame}", r"\begin{center}", r"\Large", f"{index}. {self.question}"]
        if self.question_pic:
            pic = r"\vspace{0.5em}"
            pic += (
                r"\includegraphics[height="
                + str(self.question_pic_height)
                + r"\paperheight]{"
                + self.question_pic
                + "}"
            )
            if self.question_pic_credit:
                lines.append(r"\blfootnote{photo credit: " + self.question_pic_credit + "}")
            if with_answer and self.answer_pic:
                lines += [r"\\", r"\only<1>{" + pic + "}"]
            else:
                lines += [r"\\", pic]
        if with_answer:
            if self.answer_pic:
                pic = r"\vspace{0.5em}"
                pic += (
                    r"\includegraphics[height="
                    + str(self.answer_pic_height)
                    + r"\paperheight]{"
                    + self.answer_pic
                    + "}"
                )
                if self.question_pic_credit:
                    lines.append(r"\blfootnote{photo credit: " + self.answer_pic_credit + "}")
                if self.question_pic:
                    lines += [r"\only<2>{" + pic + "}"]
                else:
                    lines += [r"\\", r"\onslide<2>{" + pic + "}"]
            if r"\input" not in lines[-1]:
                lines += [r"\\"]
            if self.answer:
                lines += [r"\onslide<2->{\vspace{1em}\textit{" + self.answer + "}}"]
        lines += [r"\end{center}", r"\end{frame}"]

        return "\n".join(lines)
