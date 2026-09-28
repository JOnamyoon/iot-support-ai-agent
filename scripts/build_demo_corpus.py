from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

SUMMARIES = {
"OWASP_LLM_TOP10": "Prompt injection occurs when instructions in user input or external content manipulate an LLM into unintended behavior. LLM applications should treat retrieved or user-supplied content as untrusted data and apply controls around model actions. The OWASP LLM risk guidance also covers insecure output handling, excessive agency, sensitive information disclosure, vector and embedding weaknesses, and related GenAI risks.",
"OWASP_WEB_TOP10": "The OWASP Top 10 is an awareness document for common web application security risks. The 2025 edition includes categories such as broken access control, security misconfiguration, software supply chain failures, cryptographic failures, injection, insecure design, authentication failures, software or data integrity failures, security logging and alerting failures, and mishandling of exceptional conditions.",
"OWASP_API_TOP10": "The OWASP API Security Top 10 focuses on risks that are especially important for APIs. Typical themes include authorization mistakes, authentication problems, unrestricted resource consumption, security misconfiguration, unsafe inventory management, and unsafe consumption of third-party APIs. API security requires validating who can access which object and operation, not only whether a user is logged in.",
"OWASP_MCP_TOP10": "OWASP MCP security guidance addresses risks in systems that connect AI models to external tools and context through the Model Context Protocol. Threats include command execution from untrusted context, tool or model misbinding, context spoofing, insecure memory references, and other failures that can turn model instructions into unsafe external actions.",
"NIST_AI_RMF": "The NIST AI Risk Management Framework is voluntary guidance intended to help organizations manage risks from AI systems while considering trustworthy AI characteristics. Its core functions are Govern, Map, Measure, and Manage. It emphasizes that AI risk management should be continuous and connected to organizational processes rather than treated as a one-time checklist.",
"NIST_CSF20": "The NIST Cybersecurity Framework 2.0 helps organizations understand and manage cybersecurity risk. CSF 2.0 organizes outcomes into six core functions: Govern, Identify, Protect, Detect, Respond, and Recover. It is intended to be adaptable across organization sizes and sectors rather than prescribing one exact technology stack.",
"NIST_CSF_QSG": "NIST CSF 2.0 Quick-Start Guides provide practical ways to begin using the Cybersecurity Framework. The guides help audiences such as small organizations, enterprise risk managers, and users of informative references translate framework outcomes into concrete planning and communication activities.",
"FASTAPI_TUTORIAL": "FastAPI is a Python web framework for building APIs using standard Python type hints. The tutorial demonstrates path operations, request parameters, request bodies, response models, dependencies, and automatic interactive API documentation. Type-driven validation is handled through Pydantic-based models.",
"FASTAPI_SECURITY": "FastAPI provides security utilities for implementing common authentication and authorization flows. Its security tutorial shows how OAuth2 password bearer schemes can be declared as dependencies and integrated into API endpoints. Security dependencies become part of the generated OpenAPI schema and interactive documentation.",
"FASTAPI_MIDDLEWARE": "FastAPI middleware runs logic for every request before it reaches a path operation and can also process the response before it is returned. Middleware can be used for cross-cutting concerns such as timing, headers, logging, tracing, or CORS-related processing.",
"FASTAPI_BACKGROUND": "FastAPI BackgroundTasks lets a path operation schedule work that runs after returning the response. This is useful for small follow-up work such as writing a log or sending a notification when the client does not need to wait for completion. Heavy distributed jobs typically need a separate task system.",
"STREAMLIT_STATE": "Streamlit Session State stores values that should persist across reruns for a user session. It can hold variables, widget state, and conversation context. Session State is useful because Streamlit reruns a script from top to bottom when users interact with widgets.",
"STREAMLIT_CACHE": "Streamlit caching avoids repeating expensive work on every rerun. st.cache_data is designed for data results that can be serialized and copied, while st.cache_resource is designed for shared resources such as models or database connections. Time-to-live settings can control cache invalidation.",
"STREAMLIT_CHAT": "Streamlit chat elements provide UI components for conversational apps. Chat messages can be rendered in separate message containers and a chat input can collect the next user message. These components are commonly combined with Session State to preserve conversation history between reruns.",
"PYTHON_JSON": "Python's json module converts between Python objects and JSON text. json.dumps serializes objects to strings, json.loads parses strings, and dump or load work with file-like objects. JSON is commonly used for configuration, API payloads, logs, and lightweight evaluation artifacts.",
"PYTHON_SQLITE": "Python's sqlite3 module provides a DB-API interface to SQLite. SQLite stores a relational database in a local file and supports SQL queries without a separate database server. Parameterized queries should be used instead of string interpolation to reduce SQL injection risk.",
"PYTHON_LOGGING": "Python logging provides a standard way to record application events with severity levels such as DEBUG, INFO, WARNING, ERROR, and CRITICAL. Handlers decide where records go, formatters control how they appear, and named loggers support module-level control in larger applications.",
"GITHUB_ACTIONS": "GitHub Actions automates software workflows from repository events. Workflow YAML files are stored under .github/workflows and define jobs, runners, and steps. A CI workflow can install dependencies and run tests automatically for pushes and pull requests.",
"GITHUB_SECURITY": "GitHub security hardening guidance for Actions recommends reducing token permissions, protecting secrets, pinning or carefully reviewing third-party actions, and treating pull request or external input as untrusted. CI systems should follow least privilege because workflows can access repository resources.",
"GITHUB_README": "A repository README explains what a project does and how to use it. Useful README content includes purpose, setup, execution steps, examples, limitations, contribution or license notes, and links to supporting evidence. A clear README turns source code into understandable portfolio evidence."
}

out_dir = ROOT / "data" / "demo_docs"
out_dir.mkdir(parents=True, exist_ok=True)
with (ROOT / "data" / "sources.csv").open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        sid = row["source_id"]
        text = SUMMARIES[sid]
        content = f"source_id: {sid}\ntitle: {row['title']}\nurl: {row['url']}\n\n{text}\n"
        (out_dir / f"{sid}.md").write_text(content, encoding="utf-8")
print(f"Wrote {len(SUMMARIES)} demo documents to {out_dir}")
