from ..vectordb import get_embedding
class Tool:
    def __init__(self, tool_name, description, action, args=[]):
        self.tool_name = tool_name
        self.description = description
        #self.description_embedding = get_embedding(description)
        self.action = action
        self.args = args

class Instruction(Tool):
    def __init__(self, instruction_name, description, func, args, response_variable):
        self.instruction_name = instruction_name
        self.description = description
        self.func = func
        self.args = args
        self.response_variable = response_variable
