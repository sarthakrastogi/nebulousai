from .llm import llm_call
import re

def plan_task_llm_call(task, abilities):
    abilities = '\n\n'.join([f"- {ability.ability_name}\n{ability.description}" for ability in abilities])
    plan_task_system_prompt = f"""
    You are given a task the user wants to accomplish.
    You have the following abilities you can use to complete this task:
    {abilities}

    Plan out a series of steps that allow you to complete this task. In each step, name the ability to be used, and its input and expected output.
    Return your response in the below format. Do not add any comments in your response or it will not be parsed correctly!

    Step 1:
    Function, reason for using this function, input to function, expected output.

    Step 2:
    Function, reason for using this function, input to function, expected output.
    """
    plan_task_system_prompt = plan_task_system_prompt.replace("    ", "")
    #print("plan_task_system_prompt", plan_task_system_prompt)

    messages = [{"role" : "system", "content" : plan_task_system_prompt},
                {"role" : "user", "content" : task}]
    
    llm_response_plan = llm_call(messages)
    steps = re.findall(r'Step \d+:(.*?)(?=Step \d+|$)', llm_response_plan, re.DOTALL)
    plan = [step.strip() for step in steps]
    #print("plan", plan)
    return plan

def convert_plan_to_instructions_llm_call(plan, abilities):
    plan = "\n\n- ".join(plan)
    abilities = '\n\n'.join([f"Function: {ability.func}\nArguments:{str(ability.args)}" for ability in abilities])
    convert_plan_to_instructions_system_prompt = f"""
    You are given a plan the user wants to execute.
    You have to translate each step of this plan into one of the pre-defined Python function given to you.

    <functions to be used>
    - {abilities}
    </functions to be used>

    <plan>
    - {plan}
    </plan>

    Return your response in the below format. Do not add any comments in your response or it will not be parsed correctly!
    response = function_name(arg_name="arg_value", arg_name="arg_value")
    response = function_name(arg_name=response, arg_name="arg_value")
    """
    convert_plan_to_instructions_system_prompt = convert_plan_to_instructions_system_prompt.replace("    ", "")
    #print("convert_plan_to_instructions_system_prompt", convert_plan_to_instructions_system_prompt)

    messages = [{"role" : "system", "content" : convert_plan_to_instructions_system_prompt},
                {"role" : "user", "content" : plan}]
    
    instructions_llm_response = llm_call(messages)
    #print("instructions", instructions)
    instructions_llm_response = instructions_llm_response.split("\n")
    return instructions_llm_response