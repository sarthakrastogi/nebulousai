import re
import json
import inspect

from ..utils.llm import llm_call
from ..agent_core_components.planning_methods import planning_methods_prompts_map


class Planner:
    def __init__(self, agent_goal, decomposition_method="chain_of_thought", refine_plan=False):
        self.agent_goal = agent_goal
        self.refine_plan = refine_plan
        self.decomposition_method = decomposition_method
        self.agent_plan_steps = []

    #Decomposition into subgoals
    def decompose_tasks_into_subtasks(self, abilities, decomposition_method):
                
        abilities = '\n\n'.join([f"- {ability.ability_name}\n{ability.description}" for ability in abilities])
        plan_task_system_prompt = f"""
        You are given a task the user wants to accomplish.
        You have the following abilities you can use to complete this task:
        {abilities}""" + planning_methods_prompts_map[decomposition_method]

        messages = [{"role" : "system", "content" : plan_task_system_prompt},
                    {"role" : "user", "content" : self.agent_goal}]
        
        llm_response_plan = llm_call(messages)
        steps = re.findall(r'Step \d+:(.*?)(?=Step \d+|$)', llm_response_plan, re.DOTALL)
        self.agent_plan_steps = [step.strip() for step in steps]


    def convert_plan_step_to_instruction(self, plan_step, abilities):
        abilities_definition_str = ""
        for ability in abilities:
            params = inspect.signature(ability.action).parameters.values()
            params_str = "\n".join([f'Name: {param.name}, Default: {param.default}, Kind: {param.kind}' for param in params])
            abilities_definition_str += f"""\n\nTool: {ability.ability_name}\nDescription: {ability.description}\nArguments: {params_str}"""
        
        #print(abilities_definition_str)
        convert_plan_to_instructions_system_prompt = f"""
        You are part of an AI agent flow. The user will give you an action they want to perform.
        You also have a set of tools to perform it.
        FIgure out the appropriate tool and the input to be given to it.

        <available tools>
        - {abilities_definition_str}
        </available tools>

        Return your response in the below JSON format. Do not add any comments in your response or it will not be parsed correctly!
        """ + """{"ability_name" : "abilityName1",
         "arguments" : {"argument_1_name" : "argument_1_value", "argument_2_name" : "argument_2_value"}
        }"""
        #"expected_response" : ["expected_response_1"],

        convert_plan_to_instructions_system_prompt = convert_plan_to_instructions_system_prompt.replace("    ", "")
        #print("convert_plan_to_instructions_system_prompt", convert_plan_to_instructions_system_prompt)

        messages = [{"role" : "system", "content" : convert_plan_to_instructions_system_prompt},
                    {"role" : "user", "content" : plan_step}]
        
        instructions_llm_response = llm_call(messages)
        #print("instructions", instructions)
        instructions_llm_response = json.loads(instructions_llm_response)
        print(instructions_llm_response)
        return instructions_llm_response
    

    #Reflection and refinement
    def reflect_upon_and_refine_plan_llm_call(plan, abilities):

        reflect_upon_and_refine_plan_system_prompt = ""

        messages = [{"role" : "system", "content" : reflect_upon_and_refine_plan_system_prompt},
                    {"role" : "user", "content" : plan}]
        
        instructions_llm_response = llm_call(messages)
        #print("instructions", instructions)
        instructions_llm_response = instructions_llm_response.split("\n")
        return instructions_llm_response
    

    def plan_task(self, abilities):
        self.decompose_tasks_into_subtasks(abilities=abilities, decomposition_method=self.decomposition_method)
        if self.refine_plan: self.reflect_upon_and_refine_plan_llm_call()