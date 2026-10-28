## Architecture


This is a small Python app for analyzing **uploaded network-device output**, not for collecting network data itself.



- **`app.py`** is the Streamlit UI: it accepts a text upload, calls Ollama with a troubleshooting prompt, displays and downloads the analysis, and shows incident history.

- **`database.py`** provides SQLite persistence for incidents, including the dashboard’s counts, recent items, and full-history view.

- **`main.py`** is a separate command-line-style runner that reads `router_output.txt` and calls the same model independently of the UI.

- **`memory/incidents.txt`** is a second, plain-text incident store. The app writes each analysis there and uses the whole file as model context.

- **Tech stack:** Python, Streamlit, Ollama’s Python client with the `llama3.2` model, and Python’s built-in `sqlite3`. There is no dependency manifest or automated test suite in the tracked files; the README only embeds an image.



## Three improvements to prioritize



1. **Use one incident source of truth.** `app.py` writes to both SQLite and the text file, but reads memory from the text file and displays database history from SQLite. These stores can diverge. Consolidating persistence behind `database.py` would make history and model context consistent.

2. **Retrieve relevant history instead of sending all of it.** `load_memory()` adds the entire incident file to every prompt, so context grows with usage and can include unrelated or conflicting advice. Select a small set of relevant incidents and impose a context limit to improve response quality and keep latency predictable.

3. **Make the analysis path testable and reproducible.** The Streamlit flow and `main.py` have separate model-call logic, while dependencies and runtime configuration are undocumented. A shared analysis function, declared dependencies, and focused tests for persistence and model-call behavior would make changes safer and setup more reliable.