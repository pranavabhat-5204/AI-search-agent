The file is about a program which has two AI agents with one asking for the query and using Tavily search to gather relevant urls and extract information from those URLs.
The next agent uses Langchain api to connect with Chatgpt 3.5 turbo to answer the query through the extracted information.

About the search agent:
This agent uses both the search and extract fuction of tavily.
The search option is used for getting relevent urls for the query provided as input.
I have kept the search_depth = "advanced" for better results and to keep it below the ratelimit of Open AI free API, I have kept the max_results=5.
Then from the urls collected from the search, I used the extract fuction and then collected the collective information using the Key: "raw_content".
These are stored in a variable for Information.

About the answer drafter and the LLM agent using Langchain:
First I used the OpenAI API for the LLM part.
The chatmodel is the Open AI's gpt-3.5-turbo-instruct.
After this I just aksed the LLM, to invoke a prompt to summarize the Information which was stored.

I have included the screenshots of both the information stored and the answer output of LLM for the query on "who is the greatest war general?".
