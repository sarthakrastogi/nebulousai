chain_of_thought_prompt = """
Plan out a series of steps that allow you to complete this task. In each step, name the ability to be used, and its input and expected output.
Return your response in the below format. Do not add any comments in your response or it will not be parsed correctly!

Step 1:
Function, reason for using this function, input to function, expected output.

Step 2:
Function, reason for using this function, input to function, expected output.
"""
# Think step by step
# Show your thinking process
# https://arxiv.org/abs/2201.11903

tree_of_thought_prompt = """"""
 # exploring multiple reasoning possibilities at each step. It first decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS (breadth-first search) or DFS (depth-first search) with each state evaluated by a classifier (via a prompt) or majority vote.

# https://arxiv.org/abs/2305.10601

planning_methods_prompts_map = {"chain_of_thought" : chain_of_thought_prompt,
                            
                            "tree_of_thought" : tree_of_thought_prompt
                            }