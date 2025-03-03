from tavily import TavilyClient
# This part of the program acts as the searching agent which takes the user input and searches on the web
print('Please provide your search query')
Query=str(input())
tavily_client = TavilyClient(api_key="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")

# Step 2. Executing the search request
response = tavily_client.search(Query, search_depth = "advanced", max_results=5)
# Step 3. Printing the search results
Information=''
for result in response['results']:
  content=result['content']
  Information=Information+content
print(Information)
from langchain_openai import OpenAI
from getpass import getpass
import time
import os
os.environ['OPENAI_API_KEY'] = getpass()
llm=OpenAI(temperature=0)
Information=str(Information)

llm.invoke("summerize"+Information)
