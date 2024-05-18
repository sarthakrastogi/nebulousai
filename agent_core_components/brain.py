from ..utils.llm import llm_call

class Brain:
    def __init__(self, brain_system_prompt:str):
        self.brain_system_prompt = brain_system_prompt

    def reason(self, thought):
        messages = [{"role" : "system", "content" : self.brain_system_prompt},
                    {"role" : "user", "content" : thought}]
        return llm_call(messages)