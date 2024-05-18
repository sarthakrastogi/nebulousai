import re

def parse_function_call(string):
    function_name = re.search(r'(\w+)\(', string).group(1)
    args = re.findall(r'(\w+)=(.*?)(?=\s\w+=|\))', string)
    args_dict = {arg[0] : arg[1] for arg in args}
    response_variable = re.search(r'\b(\w+)\s*=', string).group(1)
    
    return {"function_name": function_name, "args": args_dict, "response_variable": response_variable}
