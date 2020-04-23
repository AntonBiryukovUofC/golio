from typing import List
from collections import Counter
import random


class Cell:
    @staticmethod
    def birth_from_parents(parents: List['Cell']):
        parent_id_count = Counter([cell.team_id for cell in parents])
        if len(parent_id_count) == 1:
            new_id = parent_id_count.most_common(1)[0][0]
        else:
            highest_count = parent_id_count.most_common(1)[0][1]
            possible_parents = [key for key in parent_id_count if parent_id_count[key] == highest_count]
            new_id = random.choice(possible_parents)

        return Cell(team_id=new_id)

    def __init__(self, team_id):
        self.team_id = team_id
