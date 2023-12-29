import os
from typing import List, Optional
from pathlib import Path
from collections import UserList
from pubquiz.latex_templates import beamer_header, beamer_preamble, latex_header
from pubquiz.round import Round

class Quiz(UserList):
   def __init__(self, title, rounds: List[Round]=[], slides_preamble: Optional[Path] = None):
      super().__init__(rounds)
      self.title = title
      if slides_preamble is None:
         slides_preamble = beamer_preamble

   def to_sheets(self, answers=False):
      # N.B. will not do picture and puzzle rounds, these must be contained in pictures.tex and puzzles.tex
      titlepage = [r"\centering",
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
                   r"\hline"] + [r.title + r" & \\" for r in self.rounds] + [r"Picture: Overpaid & \\",
                   r"Puzzles: Connect four & \\",
                   r"TOTAL \\",
                   r"\hline",
                   r"\end{tabular}",
                   r"\thispagestyle{empty}",
                   r"\Huge"]

      # Header
      lines = latex_header + [r"\begin{document}"] 
      
      if not answers:
         lines += titlepage

      # Standard rounds
      for i, r in enumerate(self.rounds):
         lines += [r"\newpage", r"\begin{center}", r"\Huge", "Round {0}: {1}".format(i + 1, r.title), \
                  r"\end{center}", r"\LARGE"]
         if len(r.description) > 0:
            if not answers:
               lines += [r"\vspace{-1cm}"]
            lines += [r.description]
         if answers:
            lines += [r"\large", r"\begin{enumerate}"]
            lines += [r"\item " + str(q) for q in r.questions]
            lines += [r"\end{enumerate}", r"\LARGE"]
         else:
            lines += ["\Huge", r"\begin{enumerate}"]
            lines += [r"\item" for q in r.questions]
            lines += [r"\end{enumerate}", ""]

      # Picture and puzzle
      for r in ["pictures", "puzzles"]:
         if answers:
            os.system(f"cp {r}.tex {r}_with_answers.tex")
            os.system(f"sed -i -e 's/%%//g' {r}_with_answers.tex")
            os.system(f"sed -i -e 's/Large/large/g' {r}_with_answers.tex")
            r += "_with_answers"
         lines += [r"\newpage", r"\Huge", "\input{" + r + ".tex}"]
      # Hacky way of getting puzzles answers to appear in master copy without having to code up
         
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

      # Header
      lines = beamer_header + [r"\begin{document}", "\include{preamble}"]

      # Standard rounds
      for i, r in enumerate(self.rounds):

         # Questions
         lines += [r"\begin{frame}", r"\begin{center}", r"\Huge", f"Round {i+1}: {r.title}",
                  r"\end{center}", r"\end{frame}"]
         for iq, q in enumerate(r.questions):
            lines += q.as_slide(index=iq + 1)

         # Answers
         lines += [r"\begin{frame}", r"\begin{center}", r"\Huge", "Answers",
                  r"\end{center}", r"\end{frame}"]
         if r.title == "Underworked":
            continue
         for iq, q in enumerate(r.questions):
            lines += q.as_slide(index=iq + 1, with_answer=True)
         
      # Footer
      lines += [r"\include{picture_slides}"]
      lines += [r"\end{document}"]

      with open("slides.tex", "w") as f:
         f.write("\n".join(lines))