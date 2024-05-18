from .prompts import AbilitySearchPrompt
from .utils.llm import llm_call
from .vectordb import vector_search, get_embedding

import json

def search_ability(abilities, task, method):
    # Placeholder for different search mechanisms
    if method == "llm_call":
        ability_search_prompt = AbilitySearchPrompt(abilities).generate_prompt()
        messages = [{"role" : "system", "content" : ability_search_prompt},
                    {"role" : "user", "content" : task}]
        best_matching_ability_object = llm_call(messages, "gpt-3.5-turbo")
        best_matching_ability_object = json.loads(best_matching_ability_object)
        print(best_matching_ability_object)

        ability_name = best_matching_ability_object.pop("ability_name")
        best_matching_ability = [ability for ability in abilities if ability.ability_name == ability_name][0]
        best_matching_ability.args = best_matching_ability_object

        return best_matching_ability

    elif method == "vector_search":
        task_embedding = get_embedding(task)
        best_matching_ability = vector_search(abilities, task_embedding)
        return best_matching_ability
    
