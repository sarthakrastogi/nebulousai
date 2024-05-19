import wikipedia
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

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




def reason(input_text:str):
    return llm_call([{"role" : "user", "content" : input_text}])

reason_ability_description = """Makes an LLM call to figure out an answer.
In the input text string, make sure that you include all the relevant context and clearly mention your question and the expected output from the LLM.
"""

reasonAbility = Ability(ability_name = "Reason",
                        description = reason_ability_description,
                        action=reason)



def web_search_ddg(search_term:str):
    results = DDGS().text(search_term, max_results=5)
    return str(results)

web_search_ddg_ability_description = """Given a search query, searches the DuckDuckGo search engine.
Returns 5 search results with the title, URL and a few sentences of the body, of each search result.
After getting the search results, the agent should usually use the getWebpageContentAbility to visit the most relevant URL, read its content, and answer the user's question.
"""

webSearchAbility = Ability(ability_name="Web Search",
                           description=web_search_ddg_ability_description,
                           action=web_search_ddg)



def get_webpage_content(url:str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'
        text_content = ' '.join(soup.stripped_strings)
        return f"{title}\n{text_content}"
    except requests.exceptions.RequestException as e:
        return "There was an error reading this webpage."

get_webpage_content_ability_description = """Given the URL to a webpage, returns the page content if it is accessible.
Before using this ability, you would usually have searched the web to have your search results' URLs ready.
The Web Search Ability's response only contains page titles and a few sentences. So, if these sentences do not answer the user's question, you must visit one of the webpage URLs to get the full text.
After using this ability, you can use the Reasoning ability to filter / summarise the text to generate the final answer for the user.
If a certain webpage's content is not accessible, the agent must try another search result URL.
"""

getWebpageContentAbility = Ability(ability_name = "Get Webpage Content",
                        description = get_webpage_content_ability_description,
                        action=get_webpage_content)




#Human Feedback

def send_email(name:str, email_address:str, email_subject:str, email_body:str):
    return "sent email"

def poll_for_email_reply():
    return "received email"