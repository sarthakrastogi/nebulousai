from .llm import llm_call
def reason(input_text:str):
    return llm_call([{"role" : "user", "content" : input_text}])

def web_search(search_query:str):
    return "sample web search results here"