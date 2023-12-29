"""Module for the Round class."""

from collections import UserList
from random import shuffle
from typing import List, Optional

from pubquiz.question import Question


class Round(UserList):
    """Class representing a round in a pub quiz."""

    def __init__(self, title, description="", questions: Optional[List[Question]] = None):
        questions = questions or []
        super().__init__(questions)
        self.title = title
        self.description = description

    def __repr__(self):
        return "\n".join([self.title] + [self.description] + [str(q) for q in self])

    def shuffle(self):
        """Shuffle the questions in the round."""
        shuffle(self.questions)
