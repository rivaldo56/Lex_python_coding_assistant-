Lex – AI Coding Agent

Lex is a lightweight AI coding assistant built on top of Google’s Gemini API.
It can:

Read and write files safely inside the working directory

Run Python scripts with arguments

Inspect project directories and file metadata

Debug and auto-fix code using natural language prompts

✨ Features

File Management – get_file_info, get_files_info, get_file_content, write_file

Execution – run Python files with optional CLI args

Security – sandboxed to a working directory, prevents escaping to parent paths

Agentic Loop – interprets user prompts and automatically calls tools until a task is complete

⚙️ Installation

Clone the repo:

git clone https://github.com/yourusername/Lex.git
cd Lex


Create and activate a virtual environment (using uv or venv):

uv venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows


Install dependencies:

uv pip install -r requirements.txt

🔑 Environment Setup

Create a .env file in the root directory and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

🚀 Usage

Run the agent with a natural language prompt:

uv run main.py "write 'hello' to main.txt"


Verbose mode (debugging):

uv run main.py "can you fix calculator/main.py" --verbose

📂 Project Structure
Lex/
│── main.py               # Entry point, agent loop
│── call_function.py      # Function call dispatcher
│── functions/            # Tool implementations
│   |
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
│── tests/                # Unit tests (if any)
│── .env                  # API key (not tracked)
│── requirements.txt
│── README.md

🛠️ Example
uv run main.py "create a file hello.py that prints 'Hello, World!'"


Output:

- Calling function: write_file
Successfully wrote to "hello.py"

uv run main.py "run hello.py"
Hello, World!

🧑‍💻 Roadmap

Add support for multi-file edits in one request

Integrate with Git for automatic commits

Expand beyond Python to other languages

🤝 Contributing

Pull requests are welcome! Please fork the repo and submit changes via PR.

📜 License

MIT License – feel free to use, modify, and distribute.
