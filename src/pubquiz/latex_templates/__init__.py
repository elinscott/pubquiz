"""Module containing various LaTeX templates."""

from pathlib import Path


def get_template(filename):
    """Load a template file from this directory."""
    with open(Path(__file__).parent / filename, "r") as f:
        lines = f.readlines()
    return lines


beamer_header = get_template("beamer_header.tex")
beamer_preamble = get_template("beamer_preamble.tex")
latex_header = get_template("latex_header.tex")
