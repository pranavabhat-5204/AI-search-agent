from tavily import TavilyClient
# This part of the program acts as the searching agent which takes the user input and searches on the web
print('Please provide your search query')
Query=str(input())
# Replace "YOUR_TAVILY_API_KEY" with your actual Tavily API key
tavily_client = TavilyClient(api_key="key")

# Step 2. Executing the search request
response = tavily_client.search(Query, search_depth = "advanced", max_results=5)
# Step 3. Printing the search results
urls=[]
for result in response['results']:
  url=result['url']
  urls.append(url)
response = tavily_client.extract(urls=urls, include_images=False)
Information=''
for result in response['results']:
  Information=Information+result['raw_content']

from langchain_groq import ChatGroq
# Replace "YOUR_GROQ_API_KEY" with your actual Groq API key
llm= ChatGroq(temperature=0, groq_api_key="key", model_name="llama-3.3-70b-versatile" )
result=llm.invoke("use" + str(Information[:1000])+ ", summarize and Create a short, structured report with key points and links.")
result.content
