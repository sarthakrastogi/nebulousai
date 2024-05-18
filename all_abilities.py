import wikipedia
from .utils.llm import llm_call
from .core.ability import Ability

def search_wikipedia(search_term:str):
    search_results = wikipedia.search(search_term)
    selected_search_result = search_results[0]
    page_summary = wikipedia.summary(selected_search_result)
    #page = wikipedia.page(search_term)
    return page_summary #page.content#, , page.links

search_wikipedia_ability_description = """Searches Wikipedia using the API to return the page summary, page content and list of links.
You must ensure that a page for your entered search term exists on Wikipedia.
Use the returned page content, pass it through the reasoning step with a question to get your answer."""
searchWikipediaAbility = Ability(ability_name="Wikipedia Search",
                                 description=search_wikipedia_ability_description,
                                 action=search_wikipedia)

reason_ability_description = """Makes an LLM call to figure out an answer.
Make sure that you include all the relevant context and clearly mention your question and the expected output from the LLM.
"""

def reason(input_text:str):
    return llm_call([{"role" : "user", "content" : input_text}])

reasonAbility = Ability(ability_name = "Reason",
                        description = reason_ability_description,
                        action=reason)




def web_search(search_query:str):
    return "sample web search results here"

#Human Feedback

def send_email(name:str, email_address:str, email_subject:str, email_body:str):
    return "sent email"

def poll_for_email_reply():
    return "received email"