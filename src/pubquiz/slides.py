"""Module containing useful functions for generating LaTeX slides."""


def header_slide(header):
    """Generate a generic header slide with the heading 'header'."""
    return [r"\begin{frame}", r"\begin{center}", r"\Huge", header, r"\end{center}", r"\end{frame}"]
