from pathlib import Path

def get_template(filename):
    with open(Path(__file__).parent / filename, "r") as f:
        return f.readlines()
    
beamer_header = get_template("beamer_header.tex")
beamer_preamble = get_template("beamer_preamble.tex")
latex_header = get_template("latex_header.tex")
