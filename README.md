This project is a **Streamlit-based AI Research Agent** that:
- Takes a research query from the user.
- Uses **Tavily API** to fetch relevant information from the web.
- Summarizes results into a **structured research report** using **Groq LLMs**.
- Saves reports in a **SQLite database** for later retrieval.
- Provides a simple **web interface via Streamlit**.
- Supports deployment with **ngrok** for public access.

app.py # Main Streamlit app
├── Run.py # Script to launch the app with ngrok
├── reports.db # Auto-created SQLite database for saved reports
├── README.md # Project documentation


The installations you have to make are:
**pip install pyngrok streamlit flask langchain-groq tavily-python requests**

At last after you have app.py ready, you have to run the Run.py script to run the Ngrok App
If you are using local machine with python, sqlite3 is mostly already installed.



