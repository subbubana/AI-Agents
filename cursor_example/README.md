# MCP Filesystem Server Example

This project demonstrates how to create an AI assistant with full filesystem access using the Model Context Protocol (MCP). The assistant can read, create, update, and delete files and folders on demand through a conversational interface.

## Overview

The application creates an MCP server that exposes a filesystem directory to an AI agent, allowing it to:
- Read existing files and analyze their contents
- Create new files with meaningful names
- Update existing files
- Delete files and folders
- Provide assistance based on actual file contents

## Features

- **Interactive AI Assistant**: Chat-based interface for file operations
- **Safe File Operations**: Built-in safety checks for file modifications
- **MCP Integration**: Uses the Model Context Protocol for standardized AI-agent communication
- **Filesystem Access**: Full read/write access to specified directories
- **Session Management**: Persistent SQLite session storage for conversation history
- **Tracing**: OpenAI platform integration for workflow tracing

## Prerequisites

- Python 3.8+
- Node.js and npm (for npx)
- OpenAI API key

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd AI_agents/cursor_example
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure npx is available:**
   ```bash
   npm install -g npx
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Interact with the AI assistant:**
   - The assistant will start and wait for your input
   - Type your requests (e.g., "Create a new file called notes.txt")
   - The assistant will perform file operations and confirm actions
   - Type "exit" to quit

3. **Example interactions:**
   ```
   User: What files are in the sample_files directory?
   User: Create a new file called hello.txt with the content "Hello World"
   User: Read the contents of app.js
   User: exit
   ```

## Project Structure

```
cursor_example/
├── main.py              # Main application entry point
└── sample_files/       # Directory exposed to the MCP server

```

## How It Works

1. **MCP Server Setup**: Creates a filesystem MCP server using `@modelcontextprotocol/server-filesystem`
2. **Agent Initialization**: Sets up an AI agent with filesystem access capabilities
3. **Session Management**: Maintains conversation history in SQLite database
4. **Interactive Loop**: Processes user input and executes file operations through the MCP server
5. **Tracing**: Logs workflow execution for monitoring and debugging

## Configuration

- **Filesystem Directory**: The `sample_files/` directory is exposed to the MCP server
- **Port**: Uses stdio for communication (no network ports required)
- **Session Storage**: SQLite database for persistent conversation history

## Sample test case
\`

User: Create a sample todo list project.

A sample "todo list" project has been created with the following structure and features:

\*\*Files included:\*\*

\- \`README.md\`: Project overview and features

\- \`index.html\`: The main HTML page for the todo app

\- \`style.css\`: Basic styling for a clean UI

\- \`app.js\`: JavaScript to handle adding, marking, and removing todos

You can find this project in the \`sample\_files/todo-list\` directory. Let me know if you'd like to add more features or want instructions to run this todo list!

\`

## Troubleshooting

- **"npx is not installed"**: Install Node.js and npm, then run `npm install -g npx`
- **OpenAI API errors**: Verify your API key in the `.env` file
- **Permission errors**: Ensure the application/driectory has read/write access to the target directories

## Dependencies

- `agents`: OpenAI's agents framework for AI agent management
- `python-dotenv`: Environment variable management
- `asyncio`: Asynchronous programming support

## License

This project is part of the AI_agents collection and follows the same licensing terms.

## Contributing

Feel free to modify the sample files, add new features, or improve the documentation. The modular design makes it easy to extend functionality.
