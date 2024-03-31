from .llm import llm_call

def plan_task_llm_call(task, abilities):
    abilities = '\n- '.join(abilities)
    plan_task_system_prompt = f"""
    You are given a task the user wants to accomplish.
    You have the following abilities you can use to complete this task:
    - {abilities}

    Plan out a series of steps that allow you to complete this task.
    Return your response with one step in each new line. Do not add any comments in your response.
    """

    messages = [{"role" : "system", "content" : plan_task_system_prompt},
                {"role" : "user", "content" : task}]
    
    llm_response_plan = llm_call(messages)
    plan = llm_response_plan.split("\n")

    return plan

def convert_plan_to_instructions_llm_call(plan, abilities):
    plan = "\n- ".join(plan)
    abilities = "\n- ".join(abilities)
    convert_plan_to_instructions_system_prompt = f"""
    You are given a plan the user wants to execute.
    You have to translate each step of this plan into one of the pre-defined Python function given to you.

    <functions to be used>
    - {abilities}
    </functions to be used>

    <plan>
    - {plan}
    </plan>

    Return your response with one step in each new line. Do not add any comments in your response or it will not be parsed correctly!
    """

    messages = [{"role" : "system", "content" : convert_plan_to_instructions_system_prompt},
                {"role" : "user", "content" : plan}]
    
    llm_response_plan = llm_call(messages)
    instructions = llm_response_plan.split("\n")

    return instructions