from .ability_search import search_ability
from .ability import Ability, Instruction
from .planning import plan_task_llm_call, convert_plan_to_instructions_llm_call
from .all_abilities import *
from .utils import *

class Agent:
    def __init__(self, name, purpose, multi_step, ability_search_method="llm_call", instructions=[], plan_steps=[], task=""):
        self.name = name
        self.purpose = purpose
        self.multi_step = multi_step
        self.abilities = []
        self.ability_search_method = ability_search_method # "llm_call" by default. can be "vector_search" if functions connected to ability do not require args.

        self.add_ability("Reasoning", "Makes an LLM call to figure out an answer.", reason, {"input_text" : ""})
        self.add_ability("Web Search", "Searches the web using the Brave Search API", web_search, {"search_query" : ""})


    def add_ability(self, ability_name, description, func, args):
        ability = Ability(ability_name, description, func, args)
        self.abilities.append(ability)


    def act(self, task=None, plan_steps=[], instructions=[]):
        if task:
            # Scenario 1: User provides a task
            self.task = task
            
            if self.multi_step:
                self.plan_task()
                self.convert_plan_to_instructions()
                self.execute_instructions()

            else:
                chosen_ability = search_ability(self.abilities, self.task, self.ability_search_method)
                result = chosen_ability.func(**chosen_ability.args) #execute ability
                print(f"Performed '{self.task}' using '{chosen_ability.ability_name}' ability. Result: {result}")


        elif plan_steps:
            # Scenario 2: User provides a plan
            # Assume a multi-step agent flow since planning isn't required.
            self.plan_steps = plan_steps

            self.convert_plan_to_instructions()
            self.execute_instructions()

        elif instructions:
            # Scenario 3: User provides direct instructions
            # Assume a multi-step agent flow since planning isn't required.
            self.instructions = instructions

            self.execute_instructions()


    def plan_task(self):
        self.plan_steps = plan_task_llm_call(self.task, self.abilities)


    def convert_plan_to_instructions(self):
        instructions_llm_response = convert_plan_to_instructions_llm_call(self.plan_steps, self.abilities)
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
            print(f"Performed '{instruction}'. Result: {result}")
