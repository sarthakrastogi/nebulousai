import re
import json
import inspect
from json import JSONDecodeError

from ..utils.llm import llm_call

class Planner:
    def __init__(self, agent_goal, refine_plan=False):
        self.agent_goal = agent_goal
        self.refine_plan = refine_plan
        self.agent_plan_steps = []

    #Decomposition into subgoals
    def decompose_tasks_into_subtasks(self, tools, brain):
                
        tools = '\n\n'.join([f"- {tool.tool_name}\n{tool.description}" for tool in tools])
        chain_of_thought_planning_prompt = f"""
        You are given a task the user wants to accomplish. These are the guidelines the user has set for you:
        {brain.brain_system_prompt}

        You have the following tools you can use to complete this task:
        {tools}

        Plan out a series of steps that allow you to complete this task. You can plan any number of tasks.
        In each step, name the tool to be used, and its input and expected output.
        Return your response in the below format. Do not add any comments in your response or it will not be parsed correctly!

        Step 1:
        Function, reason for using this function, input to function, expected output.

        Step 2:
        Function, reason for using this function, input to function, expected output.

        Step 3:
        Function, reason for using this function, input to function, expected output.
        """
        # https://arxiv.org/abs/2201.11903

        messages = [{"role" : "system", "content" : chain_of_thought_planning_prompt},
                    {"role" : "user", "content" : self.agent_goal}]
        
        llm_response_plan = llm_call(messages)
        steps = re.findall(r'Step \d+:(.*?)(?=Step \d+|$)', llm_response_plan, re.DOTALL)
        self.agent_plan_steps = [step.strip() for step in steps]


    def convert_plan_step_to_instruction(self, plan_step, tools, retries=5):
        tools_definition_str = ""
        for tool in tools:
            params = inspect.signature(tool.action).parameters.values()
            params_str = "\n".join([f'Name: {param.name}, Default: {param.default}, Kind: {param.kind}' for param in params])
            tools_definition_str += f"""\n\nTool: {tool.tool_name}\nDescription: {tool.description}\nArguments: {params_str}"""
        
        convert_plan_to_instructions_system_prompt = f"""
        You are part of an AI agent flow. The user will give you an action they want to perform.
        You also have a set of tools to perform it.
        FIgure out the appropriate tool and the input to be given to it.

        <available tools>
        - {tools_definition_str}
        </available tools>

        Return your response in the below JSON format. Do not add any comments in your response or it will not be parsed correctly!
        """ + """{"tool_name" : "toolName1",
         "arguments" : {"argument_1_name" : "argument_1_value", "argument_2_name" : "argument_2_value"}
        }"""
        
        convert_plan_to_instructions_system_prompt = convert_plan_to_instructions_system_prompt.replace("    ", "")
        try:
            messages = [{"role" : "system", "content" : convert_plan_to_instructions_system_prompt},
                        {"role" : "user", "content" : plan_step}]
            
            instructions_llm_response = llm_call(messages)
            instructions_llm_response_parsed = json.loads(instructions_llm_response)
        except JSONDecodeError:
            if retries > 0: return self.convert_plan_step_to_instruction(plan_step, tools, retries-1)
        return instructions_llm_response_parsed
    

    #Reflection and refinement
    def reflect_upon_and_refine_plan_llm_call(plan, tools):
        reflect_upon_and_refine_plan_system_prompt = ""
        messages = [{"role" : "system", "content" : reflect_upon_and_refine_plan_system_prompt},
                    {"role" : "user", "content" : plan}]
        
        instructions_llm_response = llm_call(messages)
        instructions_llm_response = instructions_llm_response.split("\n")
        return instructions_llm_response
    

    def plan_task(self, tools, brain):
        self.decompose_tasks_into_subtasks(tools=tools, brain=brain)
        if self.refine_plan: self.reflect_upon_and_refine_plan_llm_call()

    
    def from_preplanned_steps(self, plan_steps):
        self.agent_plan_steps = plan_steps




class TreeOfThoughtPlanner:
    def __init__(self, agent_goal, refine_plan=False):
        self.agent_goal = agent_goal
        self.refine_plan = refine_plan
        self.agent_plan_steps = []

    def decompose_tasks_into_subtasks(self, tools):
        tree_of_thought_prompt = """"""
        # exploring multiple reasoning possibilities at each step. It first decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS (breadth-first search) or DFS (depth-first search) with each state evaluated by a classifier (via a prompt) or majority vote.
        # https://arxiv.org/abs/2305.10601
        pass