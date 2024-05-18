from .ability_search import search_ability
from .core.ability import Ability, Instruction
from .core.short_term_memory import ShortTermMemory
from .all_abilities import reasonAbility
from .utils.utils import *

class Agent:
    def __init__(self, agent_type, brain, long_term_memory, planner, name="", purpose="", instructions=[], plan_steps=[], task=""):
        self.name = name
        self.purpose = purpose
        self.agent_type = agent_type
        self.brain = brain
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = long_term_memory
        self.abilities = []
        self.planner = planner
        self.plan_steps = []
        self.add_ability(reasonAbility)


    def add_ability(self, ability):
        self.abilities.append(ability)


    def add_point_of_contact(point_of_contact):
        #Add point of contact
        pass


    def act(self, task=None, plan_steps=[], instructions=[]):
        if task:
            # Scenario 1: User provides a task which needs to be planned
            self.task = task
            
            if self.agent_type == "plan_in_advance":
                self.plan()
                return self.act_on_plan()

            else:
                chosen_ability = search_ability(self.abilities, self.task, self.ability_search_method)
                result = chosen_ability.func(**chosen_ability.args) #execute ability
                print(f"""Performed '{self.task}' using '{chosen_ability.ability_name}' ability.
                      Result: {result}""")


        elif plan_steps or self.plan_steps:
            # Scenario 2: User provides a plan or calls the plan() method before act()
            # Assume a multi-step agent flow since planning isn't required.
            if plan_steps: self.plan_steps = plan_steps
            self.act_on_plan()

        '''elif instructions:
            # Scenario 3: User provides direct instructions
            # Assume a multi-step agent flow since planning isn't required.
            self.instructions = instructions
            self.execute_instructions()'''


    def plan(self):
        self.planner.plan_task(self.abilities)
        self.plan_steps = self.planner.agent_plan_steps


    def act_on_plan(self):
        prev_step = ""
        for plan_step in self.plan_steps:
            plan_step = prev_step + plan_step
            instructions_llm_response = self.planner.convert_plan_step_to_instruction(plan_step, self.abilities)
            instruction_function = [ability.action for ability in self.abilities if ability.ability_name == instructions_llm_response['ability_name']][0]
            instruction_arguments = instructions_llm_response['arguments']
            result = instruction_function(**instruction_arguments)
            print(f"""Performed '{instruction_function.__name__}'.\nResult: {result}""")
            prev_step = f"""The previous step was:\n{plan_step}\nThe previous step's output was:\n{result}"""
        return result

    def convert_plan_to_instructions(self):
        instructions_llm_response = self.planner.convert_plan_to_instructions_llm_call(self.plan_steps, self.abilities)
        print("instructions_llm_response", instructions_llm_response)
        instructions = []    
        for instruction in instructions_llm_response:
            instruction_function_calls = parse_function_call(instruction) 
            instruction_func = [ability.func for ability in self.abilities if ability.func.__name__ == instruction_function_calls['function_name']][0]
            print("instruction_function_calls", instruction_function_calls)
            instruction = Instruction(instruction_name="",
                                      description="",
                                      func=instruction_func,
                                      args=instruction_function_calls['args'],
                                      response_variable = instruction_function_calls['response_variable'])
            instructions.append(instruction)
        self.instructions = instructions

    def execute_instructions(self):
        for instruction in self.instructions:
            print(instruction.func, instruction.args)
            # Execute the chosen ability function with arguments
            result = instruction.func(**instruction.args)
            print(f"""Performed '{instruction.func.__name__}'.\nResult: {result}""")
