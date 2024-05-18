#all the relevant research findings get stored as constituent objects of this class.
from ..utils.llm import llm_call

class ShortTermMemory:
    def __init__(self):
        self.short_term_memories = []

    def add_new_memory(self, new_short_term_memory:str):
        self.short_term_memories += [new_short_term_memory]