#all the relevant research findings get stored as constituent objects of this class.
from ..utils.llm import llm_call


class Memory:
    def __init__(self, memories=[]):
        self.memories = memories

    def add_new_memory(self, new_memory:str):
        self.memories += [new_memory]

    def is_not_empty(self):
        return True if self.memories else False
    
    def formatted(self):
        return "\n".join(self.memories)


class ShortTermMemory(Memory):
    def __init__(self, memories=[]):
        super().__init__(memories)
    

class LongTermMemory(Memory):
    def __init__(self, memories=[]):
        super().__init__(memories)