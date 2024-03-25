from .vectordb import get_embedding
class Ability:
    def __init__(self, ability_name, description, func, args):
        self.ability_name = ability_name
        self.description = description
        self.description_embedding = get_embedding(description)
        self.func = func
        self.args = args
