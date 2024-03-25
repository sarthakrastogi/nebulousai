from .ability_search import search_ability
from .ability import Ability

class Agent:
    def __init__(self, name, purpose, ability_search_method="llm_call"):
        self.name = name
        self.purpose = purpose
        self.abilities = []
        self.ability_search_method = ability_search_method # "llm_call" by default. can be "vector_search" if functions connected to ability do not require args.

    def add_ability(self, ability_name, description, func, args):
        ability = Ability(ability_name, description, func, args)
        self.abilities.append(ability)

    def perform_task(self, task):
        # Search for the relevant ability based on the task
        chosen_ability = search_ability(self.abilities, task, self.ability_search_method)

        # Execute the chosen ability function with arguments
        return chosen_ability.func(**chosen_ability.args)
    