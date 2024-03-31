from .llm import llm_call
def LLM(instruction:str):
    return llm_call([{"role" : "user", "content" : instruction}])