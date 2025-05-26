# 🧠 AI Job Assistant Agent

This project is an interactive AI Agent built with **LangGraph**, designed to help users better understand job listings and prepare for interviews. It extracts structured job details, summarizes the role, and generates relevant interview questions — all powered by OpenAI.

---

## 🚀 Features

- ✅ Parses raw job descriptions into structured fields
- 📝 Generates a short professional summary of the job
- ❓ Creates interview questions based on the role
- 🧹 Built with modular LangGraph nodes for clear, traceable workflows
- 🤖 LLM-powered with OpenAI

---

## 📁 Project Structure

```plaintext
.
├── main.py                  # Entry point: builds and runs the LangGraph agent
├── prompts.py              # Contains prompt templates (system messages)
├── pyproject.toml          # Project dependencies (used with uv or poetry)
├── uv.lock                 # Lock file for uv-based environment
├── .gitignore              # Specifies files/folders to exclude from Git
├── .python-version         # Optional: specifies Python version
├── README.md               # This file
```


> ⚠️ `.env` is used to store your OpenAI API key and must **not** be committed to GitHub.

---

## 🔧 Setup Instructions

```bash 
# 1. Clone the repo
git clone https://github.com/your-username/your-repo.git
cd your-repo

# 2. Install dependencies with `uv`
uv pip install -r pyproject.toml

# 3. Create a `.env` file
echo "OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" > .env

# 4. Run the agent
python main.py
```


## 📜 License

This project is for educational/demo purposes. Use responsibly when working with LLMs and sensitive data.

---

## 🤝 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph)  
- [LangChain](https://github.com/langchain-ai/langchain)  
- [OpenAI](https://openai.com)
