from .ability_search import search_ability
from .ability import Ability
from .planning import plan_task_llm_call, convert_plan_to_instructions_llm_call

class Agent:
    def __init__(self, name, purpose, ability_search_method="llm_call", instructions=[], plan_steps=[], task=""):
        self.name = name
        self.purpose = purpose
        self.abilities = []
        self.ability_search_method = ability_search_method # "llm_call" by default. can be "vector_search" if functions connected to ability do not require args.
        self.instructions = instructions
        self.plan_steps = plan_steps
        self.task = task


    def add_ability(self, ability_name, description, func, args):
        ability = Ability(ability_name, description, func, args)
        self.abilities.append(ability)


    def perform_task(self):
        if self.task:
            # Scenario 3: User provides a task
            self.plan_task()
            self.convert_plan_to_instructions()
            self.execute_instructions()

        elif self.plan_steps:
            # Scenario 2: User provides a plan
            self.convert_plan_to_instructions()
            self.execute_instructions()

        elif self.instructions:
            # Scenario 1: User provides direct instructions
            self.execute_instructions()

    def plan_task(self):
        self.plan_steps = plan_task_llm_call(self.task, self.abilities)

    def convert_plan_to_instructions(self):
        self.instructions = convert_plan_to_instructions_llm_call(self.task, self.abilities)

    def execute_instructions(self):
        if self.multi_step:
            for instruction in self.instructions:
                chosen_ability = search_ability(self.abilities, instruction, self.ability_search_method)

                # Execute the chosen ability function with arguments
                result = chosen_ability.func(**chosen_ability.args)
                print(f"Performed '{instruction}' using '{chosen_ability.ability_name}' ability. Result: {result}")


        else:
            # Search for the relevant ability based on the instruction
            chosen_ability = search_ability(self.abilities, instruction, self.ability_search_method)

            # Execute the chosen ability function with arguments
            result = chosen_ability.func(**chosen_ability.args)
            print(f"Performed '{instruction}' using '{chosen_ability.ability_name}' ability. Result: {result}")
