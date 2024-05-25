from .tool_search import search_tool
from .core.tool import Tool, Instruction
from .core.planning import Planner
from .core.memory import ShortTermMemory, LongTermMemory
from .all_tools import reasonTool, webSearchTool, getWebpageContentTool
from .utils.llm import llm_call

class Agent:
    def __init__(self, brain, long_term_memory=None, planner=None, name="", purpose="", instructions=[], plan_steps=[], task="", verbose=2):
        self.name = name
        self.purpose = purpose
        self.brain = brain
        self.short_term_memory = ShortTermMemory()
        self.long_term_memory = long_term_memory
        self.tools = []
        self.planner = planner
        self.task = task
        self.plan_steps = plan_steps
        self.verbose = verbose
        self.add_tool(reasonTool)
        self.add_tool(webSearchTool)
        self.add_tool(getWebpageContentTool)

    def add_tool(self, tool):
        self.tools.append(tool)

    def add_point_of_contact(point_of_contact):
        #Add point of contact
        pass

    def execute_instruction(self, instructions_llm_response):
        instruction_function = [tool.action for tool in self.tools if tool.tool_name == instructions_llm_response['tool_name']][0]
        instruction_arguments = instructions_llm_response['arguments']
        result = instruction_function(**instruction_arguments)
        if self.verbose >= 2: print(f"""Performed {instruction_function.__name__} with args {str(instruction_arguments)}.\nResult: {result}""")
        return result




class PlannerAgent(Agent):
    def __init__(self, brain, long_term_memory=None, planner=None, name="", purpose="", instructions=[], plan_steps=[], task="", verbose=2):
        super().__init__(brain, long_term_memory, planner, name, purpose, instructions, plan_steps, task, verbose)

    def act(self):
        if self.plan_steps and not self.planner:
            self.planner = Planner(agent_goal=self.task)
            self.planner.from_preplanned_steps(self.plan_steps)

        elif not self.plan_steps and self.planner:
            self.planner.plan_task(self.tools, brain=self.brain)
            self.plan_steps = self.planner.agent_plan_steps

        elif not self.plan_steps and not self.planner:
            raise Exception("Provide either a Planner class object or plan_steps to the Agent class.")
        return self.execute_plan()
            
    def execute_plan(self):
        prev_step, result = "", ""
        for plan_step in self.plan_steps:
            plan_step = prev_step + plan_step
            instructions_llm_response = self.planner.convert_plan_step_to_instruction(plan_step, self.tools)
            result = self.execute_instruction(instructions_llm_response=instructions_llm_response)
            prev_step = f"""The previous step was:\n{plan_step}\nThe previous step's output was:\n{result}"""
        return result
    



class ReActAgent(Agent):
    """ https://arxiv.org/abs/2210.03629 """

    def __init__(self, brain, task, max_iterations, long_term_memory=None, name="", purpose="", instructions=[], verbose=2):
        super().__init__(brain=brain, task=task, long_term_memory=long_term_memory, name=name, purpose=purpose, instructions=instructions, verbose=verbose)
        self.max_iterations = max_iterations
        self.short_term_memory = ShortTermMemory()

        self.ReAct_preprompt = f"""You are part of an AI agent.
        The AI agent is built on this principle:
        {self.brain.brain_system_prompt}

        The agent is working on the below task/question given by the user:
        "{task}"

        The agent iterates in 3 steps: Think, Act, Observe.
        Remember that the agent can only iterate {str(self.max_iterations)} times -- after which, the current observation will be given to the user as the answer."""

        self.ReAct_postprompt = f"""If you think we already have the complete answer to the user's question or have finished their task, then present this answer or conclusion by responding in the following format:
        "BREAK | [Place the complete answer to user's question along with sources here]"
        """

    def create_ReAct_thought(self, iteration_count:int):
        tools = '\n\n'.join([f"- {tool.tool_name}\n{tool.description}" for tool in self.tools])
        
        create_ReAct_thought_system_prompt = f"""
        {self.ReAct_preprompt}
        You're current on iteration {str(iteration_count)}/{str(self.max_iterations)}.
        Your subtask is think about the best course of action for the agent.

        The agent has access to a set of tools it can use for the "action" in this iteration:
        {tools}
        
        {'This is the process the agent has completed so far:' + self.short_term_memory.formatted() if self.short_term_memory.is_not_empty() else ''}
        
        Think about the immediate next step the agent should take.
        {self.ReAct_postprompt}
        """
        return self.process_ReAct_llm_output(system_prompt=create_ReAct_thought_system_prompt)

    def create_ReAct_action(self, ReAct_thought):
        instructions_llm_response = Planner(agent_goal=ReAct_thought).convert_plan_step_to_instruction(ReAct_thought, self.tools)
        return instructions_llm_response

    def create_ReAct_observation(self, iteration_count, ReAct_thought, ReAct_action, instruction_execution_result):
        create_ReAct_observation_system_prompt = f"""
        {self.ReAct_preprompt}
        You're current on iteration {str(iteration_count)}/{str(self.max_iterations)}.
        
        {'This is the process the agent has completed so far:' + self.short_term_memory.formatted() if self.short_term_memory.is_not_empty() else ''}
        
        This was the agent's thought:
        {ReAct_thought}
        The agent decided to take this action:
        {ReAct_action}
        The action gave the following result:
        {instruction_execution_result}
        Your task is to understand the result of executing the response and write your observation.
        Remember that your response will be stored in the memory of the agent and will be used by subsequent agent iterations to finally answer the user's question. So, you must include any relevant information you find, in your response.
        {self.ReAct_postprompt}
        """
        return self.process_ReAct_llm_output(system_prompt=create_ReAct_observation_system_prompt)


    def summarise_ReAct_iteration(self, iteration_count, ReAct_thought, ReAct_action, ReAct_observation):
        return f""" Iteration {str(iteration_count)}
        This was the agent's thought:
        {ReAct_thought}
        The agent decided to take this action:
        {ReAct_action}
        After executing this action, the following result was observed:
        {ReAct_observation}
        """
    
    def process_ReAct_llm_output(self, system_prompt):
        messages = [{"role" : "system", "content" : system_prompt}]
        llm_response = llm_call(messages)
        if self.verbose >=2: print(llm_response)
        if llm_response.split("|")[0].strip() == "BREAK": return False, llm_response.split("|")[1].strip()
        else: return True, llm_response

    def compile_answer_from_short_term_memory(self):
        compile_answer_from_short_term_memory_system_prompt = f"""
        An AI agent has been working on the below task/question given by the user:
        "{self.task}"
        The AI agent is built on this principle:
        {self.brain.brain_system_prompt}

        The agent iterates in 3 steps: Think, Act, Observe.
        You are given the agent's work. You must use it as reference to answer the user's question.
        """
        messages = [{"role" : "system", "content" : compile_answer_from_short_term_memory_system_prompt},
                    {"role" : "user", "content" : self.short_term_memory.formatted()}]
        llm_response = llm_call(messages)
        return llm_response

    def act(self):
        for iteration_count in range(1, self.max_iterations+1):

            # Think
            continue_ReAct, ReAct_thought = self.create_ReAct_thought(iteration_count=iteration_count)
            if not continue_ReAct: return ReAct_thought

            # Act
            ReAct_action = self.create_ReAct_action(ReAct_thought=ReAct_thought)
            instruction_execution_result = self.execute_instruction(instructions_llm_response=ReAct_action)
            if self.long_term_memory: self.long_term_memory.add_new_memory(instruction_execution_result)

            # Observe
            continue_ReAct, ReAct_observation = self.create_ReAct_observation(iteration_count=iteration_count, ReAct_thought=ReAct_thought, ReAct_action=ReAct_action, instruction_execution_result=instruction_execution_result)
            if not continue_ReAct: return ReAct_observation

            self.short_term_memory.add_new_memory(self.summarise_ReAct_iteration(iteration_count=iteration_count, ReAct_thought=ReAct_action, ReAct_action=ReAct_action, ReAct_observation=ReAct_observation))
        
        #If the agent could not provide the answer in the given number of iterations, summarise the short term memory.
        return self.compile_answer_from_short_term_memory()