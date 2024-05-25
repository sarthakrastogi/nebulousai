import wikipedia
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from .utils.llm import llm_call
from .core.tool import Tool

# Symbolic Modules

def search_wikipedia(search_term:str):
    search_results = wikipedia.search(search_term)
    selected_search_result = search_results[0]
    page_summary = wikipedia.summary(selected_search_result)
    #page = wikipedia.page(search_term)
    return page_summary #page.content#, , page.links

search_wikipedia_tool_description = """Searches Wikipedia using the API to return the page summary, page content and list of links.
You must ensure that a page for your entered search term exists on Wikipedia.
Use the returned page content, pass it through the reasoning step with a question to get your answer."""

searchWikipediaTool = Tool(tool_name="Wikipedia Search",
                                 description=search_wikipedia_tool_description,
                                 action=search_wikipedia)




def reason(input_text:str):
    return llm_call([{"role" : "user", "content" : input_text}])

reason_tool_description = """Makes an LLM call to figure out an answer.
In the input text string, make sure that you include all the relevant context and clearly mention your question and the expected output from the LLM.
"""

reasonTool = Tool(tool_name = "Reason",
                        description = reason_tool_description,
                        action=reason)



def web_search_ddg(search_term:str):
    results = DDGS().text(search_term, max_results=5)
    return str(results)

web_search_ddg_tool_description = """Given a search query, searches the DuckDuckGo search engine.
Returns 5 search results with the title, URL and a few sentences of the body, of each search result.
The search results are only useful if, after searching, the agent uses the getWebpageContentTool to visit the most relevant URL, reads its content, and finds the answer to the user's question.
"""

webSearchTool = Tool(tool_name="Web Search",
                           description=web_search_ddg_tool_description,
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

get_webpage_content_tool_description = """Given the URL to a webpage, returns the page content if it is accessible.
Before using this tool, you would usually have searched the web to have your search results' URLs ready.
The Web Search Tool's response only contains page titles and a few sentences. So, if these sentences do not answer the user's question, you must visit one of the webpage URLs to get the full text.
After using this tool, you can use the Reasoning tool to filter / summarise the text to generate the final answer for the user.
If a certain webpage's content is not accessible, the agent must try another search result URL.
"""

getWebpageContentTool = Tool(tool_name = "Get Webpage Content",
                        description = get_webpage_content_tool_description,
                        action=get_webpage_content)




#Human Feedback

def send_email(name:str, email_address:str, email_subject:str, email_body:str):
    pass #TODO

def poll_for_email_reply():
    pass #TODO