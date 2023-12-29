from random import shuffle
from collections import UserList
from pubquiz.question import Question
from typing import List

class Round(UserList):
   def __init__(self, title, description="", questions: List[Question]=[]):
      super().__init__(questions)
      self.title = title
      self.description = description

   def __repr__(self):
      return "\n".join([self.title] + [self.description] + [str(q) for q in self])

   def shuffle(self):
      shuffle(self.questions)