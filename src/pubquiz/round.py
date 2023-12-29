"""Module for the Round class."""

from collections import UserList
from random import shuffle
from typing import List, Optional

from pubquiz.question import Question


class Round(UserList):
    """Class representing a round in a pub quiz."""

    def __init__(self, title, description="", questions: Optional[List[Question]] = None):
        """Initialize the round."""
        questions = questions or []
        super().__init__(questions)
        self.title = title
        self.description = description

    def __repr__(self):
        return f'Round(title={self.title})'

    @classmethod
    def from_dict(cls, dct):
        """Create a round object from a dictionary."""
        questions = dct.pop("questions", [])
        return cls(**dct, questions=[Question.from_dict(q) for q in questions])

    def shuffle(self):
        """Shuffle the questions in the round."""
        shuffle(self.questions)
