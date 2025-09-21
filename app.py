import os
import sqlite3
import json
import requests
from tavily import TavilyClient
from langchain_groq import ChatGroq
import streamlit as st

TAVILY_API_KEY = "Tavily_api"
GROQ_API_KEY = "Groq_api"


class DatabaseManager:
    def __init__(self, db_path="reports.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                content TEXT,
                sources TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit(); conn.close()

    def save(self, query, content, sources):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO reports (query, content, sources) VALUES (?,?,?)",
                  (query, content, json.dumps(sources)))
        rid = c.lastrowid
        conn.commit(); conn.close()
        return rid

    def all(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, query, created_at FROM reports ORDER BY created_at DESC")
        rows = c.fetchall(); conn.close()
        return rows

    def get(self, rid):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM reports WHERE id=?", (rid,))
        r = c.fetchone(); conn.close()
        if not r: return None
        return {"id": r[0], "query": r[1], "content": r[2], "sources": json.loads(r[3]), "created_at": r[4]}

class ResearchAgent:
    def __init__(self):
        self.db = DatabaseManager()
        self.search = TavilyClient(api_key=TAVILY_API_KEY)
        self.llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY,
                            model_name="llama-3.3-70b-versatile")

    def extract_content(self, url):
        try:
            r = requests.get(url, timeout=10)
            if "pdf" in url.lower() or "pdf" in r.headers.get("Content-Type", ""):
                reader = PdfReader(io.BytesIO(r.content))
                text = "\n".join([p.extract_text() or "" for p in reader.pages])
                return text
            return trafilatura.extract(r.text) or ""
        except Exception as e:
            return f"[Error extracting {url}: {e}]"

    def run(self, query):
        try:
            results = self.search.search(query, search_depth="advanced", max_results=3)["results"]
        except Exception as e:
            return None, f"Search failed: {e}"

        sources = []
        info = ""
        for r in results:
            url, title = r["url"], r.get("title","No title")
            text = self.extract_content(url)[:5000]
            info += f"\n--- {title} ({url}) ---\n{text}\n"
            sources.append({"title": title, "url": url})

        prompt = f"""
# Research Report: {query}

Summarize the following info into a structured report:

{info}

## Executive Summary
## Key Findings
## Detailed Analysis
## Sources Referenced
## Conclusion
"""
        try:
            report = self.llm.invoke(prompt).content
            rid = self.db.save(query, report, sources)
            return rid, None
        except Exception as e:
            return None, f"LLM failed: {e}"


agent = ResearchAgent()
st.title("AI Research Agent")

menu = ["New Report", "All Reports"]
choice = st.sidebar.radio("Menu", menu)

if choice == "New Report":
    q = st.text_input("Enter your research query")
    if st.button("Run Research"):
        if q:
          rid, err = agent.run(q)
          if err:
            st.error(err)
          else:
            st.success(f"Report saved with ID {rid}")
            report = agent.db.get(rid)
            st.subheader("Generated Report")
            st.markdown(report["content"])
            st.subheader("Sources")
            for s in report["sources"]:
              st.markdown(f"- [{s['title']}]({s['url']})")
        else:
            st.warning("Please enter a query.")

if choice == "All Reports":
    rows = agent.db.all()
    if not rows:
        st.info("No reports saved yet.")
    for r in rows:
        if st.button(f"[{r[0]}] {r[1]} ({r[2]})"):
            rep = agent.db.get(r[0])
            st.subheader(rep["query"])
            st.write(rep["created_at"])
            st.markdown(rep["content"])
            st.subheader("Sources")
            for s in rep["sources"]:
                st.markdown(f"- [{s['title']}]({s['url']})")
