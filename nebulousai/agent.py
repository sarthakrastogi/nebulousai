from .ability_search import search_ability
from .core.ability import Ability, Instruction
from .core.planning import Planner
from .core.short_term_memory import ShortTermMemory
from .all_abilities import reasonAbility, webSearchAbility, getWebpageContentAbility

class Agent:
    def __init__(self, brain, long_term_memory, planner=None, name="", purpose="", instructions=[], plan_steps=[], task=""):
        self.name = name
        self.purpose = purpose
        self.brain = brain
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = long_term_memory
        self.abilities = []
        self.planner = planner
        self.task = task
        self.plan_steps = plan_steps
        self.add_ability(reasonAbility)
        self.add_ability(webSearchAbility)
        self.add_ability(getWebpageContentAbility)

    def add_ability(self, ability):
        self.abilities.append(ability)

    def add_point_of_contact(point_of_contact):
        #Add point of contact
        pass




class PlannerAgent(Agent):
    def __init__(self, brain, long_term_memory, planner=None, name="", purpose="", instructions=[], plan_steps=[], task=""):
        super().__init__(brain, long_term_memory, planner, name, purpose, instructions, plan_steps, task)

    def act(self, instructions=[]):
        if self.plan_steps and not self.planner:
            self.planner = Planner(agent_goal=self.task)
            self.planner.from_preplanned_steps(self.plan_steps)

        elif not self.plan_steps and self.planner:
            self.planner.plan_task(self.abilities, brain=self.brain)
            self.plan_steps = self.planner.agent_plan_steps

        elif not self.plan_steps and not self.planner:
            raise Exception("Provide either a Planner class object or plan_steps to the Agent class.")
        return self.execute_plan()
            
    def execute_plan(self):
        for step in self.plan_steps:
            print(step)
        prev_step, result = "", ""
        for plan_step in self.plan_steps:
            plan_step = prev_step + plan_step
            instructions_llm_response = self.planner.convert_plan_step_to_instruction(plan_step, self.abilities)
            instruction_function = [ability.action for ability in self.abilities if ability.ability_name == instructions_llm_response['ability_name']][0]
            instruction_arguments = instructions_llm_response['arguments']
            result = instruction_function(**instruction_arguments)
            print(f"""Performed {instruction_function.__name__} with args {str(instruction_arguments)}.\nResult: {result}""")
            prev_step = f"""The previous step was:\n{plan_step}\nThe previous step's output was:\n{result}"""
        return result
    


class ReActAgent(Agent):
    def __init__(self, brain, task, long_term_memory, name="", purpose="", instructions=[]):
        super().__init__(brain, task, long_term_memory, name, purpose, instructions)

    def create_ReAct_thought(previous_iteration):
        create_ReAct_thought_system_prompt = f"""
        You are part of an AI agent.
        This is the process the agent has completed so far:
        {previous_iteration}
        """

    def create_ReAct_action(ReAct_thought):
        pass

    def create_ReAct_observation(ReAct_thought, ReAct_action):
        pass

    def act(self):
        previous_iteration = ""
        while True:
            ReAct_thought = self.create_ReAct_thought(previous_iteration)
            ReAct_action = self.create_ReAct_action(ReAct_thought=ReAct_thought)
            ReAct_observation = self.create_ReAct_observation(ReAct_thought=ReAct_thought, ReAct_action=ReAct_action)
            

        if self.plan_steps and not self.planner:
            self.planner = Planner(agent_goal=self.task)
            self.planner.from_preplanned_steps(self.plan_steps)
 
        elif not self.plan_steps and self.planner:
            self.planner.plan_task(self.abilities, brain=self.brain)
            self.plan_steps = self.planner.agent_plan_steps

        elif not self.plan_steps and not self.planner:
            raise Exception("Provide either a Planner class object or plan_steps to the Agent class.")
        return self.execute_plan()
            
    def execute_plan(self):
        for step in self.plan_steps:
            print(step)
        prev_step, result = "", ""
        for plan_step in self.plan_steps:
            plan_step = prev_step + plan_step
            instructions_llm_response = self.planner.convert_plan_step_to_instruction(plan_step, self.abilities)
            instruction_function = [ability.action for ability in self.abilities if ability.ability_name == instructions_llm_response['ability_name']][0]
            instruction_arguments = instructions_llm_response['arguments']
            result = instruction_function(**instruction_arguments)
            print(f"""Performed {instruction_function.__name__} with args {str(instruction_arguments)}.\nResult: {result}""")
            prev_step = f"""The previous step was:\n{plan_step}\nThe previous step's output was:\n{result}"""
        return result
    
