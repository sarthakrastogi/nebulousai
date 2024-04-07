from endgoal import Agent

name = "wikisearch"
purpose = "Disambiguate wiki search and get content"
ability_search_method = "llm_call"
wiki_agent = Agent(name, purpose, ability_search_method)


def wikipedia_search(search_term):
    return wikipedia.search(search_term)

def get_wikipedia_page_content(page_name):
    return wikipedia.page(page_name).content

wiki_agent.add_ability("Search Wikipedia", "", wikipedia_search, {"search_term": ""})
wiki_agent.add_ability("Get Content from a Wikipedia Page", "", get_wikipedia_page_content, {"page_name": ""})


wiki_agent.act(task="can you search wikipedia for the latest kdramas of April 2024 and then use an llm to write a summary of the search results")
