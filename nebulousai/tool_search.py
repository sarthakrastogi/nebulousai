from .prompts import ToolSearchPrompt
from .utils.llm import llm_call
from .vectordb import vector_search, get_embedding

import json

def search_tool(tools, task, method):
    # Placeholder for different search mechanisms
    if method == "llm_call":
        tool_search_prompt = ToolSearchPrompt(tools).generate_prompt()
        messages = [{"role" : "system", "content" : tool_search_prompt},
                    {"role" : "user", "content" : task}]
        best_matching_tool_object = llm_call(messages, "gpt-3.5-turbo")
        best_matching_tool_object = json.loads(best_matching_tool_object)
        print(best_matching_tool_object)

        tool_name = best_matching_tool_object.pop("tool_name")
        best_matching_tool = [tool for tool in tools if tool.tool_name == tool_name][0]
        best_matching_tool.args = best_matching_tool_object

        return best_matching_tool

    elif method == "vector_search":
        task_embedding = get_embedding(task)
        best_matching_tool = vector_search(tools, task_embedding)
        return best_matching_tool
    
