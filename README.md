# AI Engineer 🤖

## Overview

AI Engineer is a powerful AI-powered coding assistant with multi-provider support that provides an interactive terminal interface for seamless code development. It integrates with multiple LLM providers including DeepSeek's advanced reasoning models and OpenRouter's diverse model selection to offer intelligent file operations, code analysis, and development assistance through natural conversation and function calling.

## Quick demo

![AI Engineer in action](./assets/demo.gif)

## 🚀 Multi-Provider Support

- **Multiple AI Providers**: Support for DeepSeek and OpenRouter
- **Dynamic Model Switching**: Change models during conversation
- **Provider-Specific Features**: Reasoning content for DeepSeek models
- **Unified Interface**: Same commands work across all providers
- **Enhanced Flexibility**: Choose the best model for each task

## Supported Models

### DeepSeek Models
- **deepseek-reasoner** (default) - Advanced reasoning with chain-of-thought
- **deepseek-chat** - Cost-effective general-purpose chat model and coder

### OpenRouter Models
- **google/gemini-2.5-pro-preview** - Google's latest Gemini model
- **google/gemini-2.5-flash-preview-05-20** - Google: Gemini 2.5 Flash Preview 05-20
- **anthropic/claude-sonnet-4** - Anthropic's Claude 4 Sonnet
- **anthropic/claude-3-sonnet:thinking** - Anthropic's Claude 3.7 reasoning model
- **anthropic/claude-3.7-sonnet** - Anthropic's Claude 3.7 standard model
- **openai/gpt-4.1** - OpenAI GPT-4.1
- **openai/o3-mini-high** - OpenAI GPT-o3-mini-high

## Key Features

### 🔌 **MCP Integration** ⭐
- **Model Context Protocol Support**: Extend AI capabilities with external tools and resources
- **Context7 Documentation Research**: Instant access to up-to-date library documentation
- **Hot-Reloadable MCP Servers**: Dynamic server management without restarts
- **Comprehensive MCP Commands**: Full control over MCP server lifecycle
- **Library Research Assistant**: Get current docs, examples, and best practices for any library

### 🧠 **AI Capabilities**
- **Elite Software Engineering**: Decades of experience across all programming domains
- **Multi-Provider Support**: Access to various AI models and capabilities
- **Chain of Thought Reasoning**: Visible thought process with DeepSeek models
- **Code Analysis & Discussion**: Expert-level insights and optimization suggestions
- **Intelligent Problem Solving**: Automatic file reading and context understanding

### 🔄 **NEW: Recursive Task Completion** ⭐
- **Complete Task Execution**: Never stops after the first function call
- **Automatic Issue Detection**: Built-in linter integration for Python, JavaScript, and TypeScript
- **Recursive Function Calling**: Continues executing until tasks are fully completed
- **Smart Iteration Management**: Up to 10 iterations with progress tracking
- **Multi-Language Support**: Error detection and fixes for Python, JS, and TS files

### 🌐 **Multi-Language Error Detection** 🆕
- **Python**: Automatic `flake8` linting with PEP 8 compliance checking
- **JavaScript**: `ESLint` integration for syntax and style errors
- **TypeScript**: Combined `tsc` compiler + `ESLint` for type safety and code quality
- **Automatic Setup Detection**: Works with existing project configurations
- **Extensible Architecture**: Easy to add support for more languages

### **Function Calling Tools**
The AI can automatically execute these operations when needed:

#### `read_file(file_path: str)`
- Read single file content with automatic path normalization
- Built-in error handling for missing or inaccessible files
- **Automatic**: AI can read any file you mention or reference in conversation

#### `read_multiple_files(file_paths: List[str])`
- Batch read multiple files efficiently
- Formatted output with clear file separators

#### `create_file(file_path: str, content: str)`
- Create new files or overwrite existing ones
- Automatic directory creation and safety checks

#### `create_multiple_files(files: List[Dict])`
- Create multiple files in a single operation
- Perfect for scaffolding projects or creating related files

#### `edit_file(file_path: str, original_snippet: str, new_snippet: str)`
- Precise snippet-based file editing
- Safe replacement with exact matching

### 🔧 **Model Management**
- **`/model list`** - Show all available models with providers
- **`/model current`** - Display currently selected model
- **`/model set <model_name>`** - Switch to a specific model
- **Dynamic switching** - Change models during conversation

### 🔌 **MCP Management**
- **`/mcp list`** - Show all configured MCP servers and their status
- **`/mcp enable <server>`** - Enable a specific MCP server
- **`/mcp disable <server>`** - Disable a specific MCP server
- **`/mcp reload`** - Reload MCP configuration without restart

### **File Operations**

#### **Automatic File Reading (Recommended)**
The AI can automatically read files you mention:
```
You> Can you review the main.py file and suggest improvements?
→ AI automatically calls read_file("main.py")

You> Look at src/utils.py and tests/test_utils.py
→ AI automatically calls read_multiple_files(["src/utils.py", "tests/test_utils.py"])
```

#### **Manual Context Addition (Optional)**
For when you want to preload files into conversation context:
- **`/add path/to/file`** - Include single file in conversation context
- **`/add path/to/folder`** - Include entire directory (with smart filtering)

### 🎨 **Rich Terminal Interface**
- **Color-coded feedback** (green for success, red for errors, yellow for warnings)
- **Real-time streaming** with visible reasoning process (DeepSeek models)
- **Provider indicators** showing current model in prompts
- **Structured tables** for model listings and status
- **Progress indicators** for long operations

### 🛡️ **Security & Safety**
- **Path normalization** and validation
- **Directory traversal protection**
- **File size limits** (5MB per file)
- **Binary file detection** and exclusion
- **API key validation** and error handling

## Getting Started

### Prerequisites
You need at least one API key:
1. **DeepSeek API Key**: Get from [DeepSeek Platform](https://platform.deepseek.com) (for DeepSeek models)
2. **OpenRouter API Key**: Get from [OpenRouter](https://openrouter.ai) (for OpenRouter models)
3. **Python 3.11+**: Required for optimal performance

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/FaustoS88/AI_Engineer
   cd AI_engineer
   ```

2. **Set up environment**:
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   # You only need the keys for providers you want to use
   ```

3. **Install dependencies** (choose one method):

   #### Using uv (recommended - faster)
   ```bash
   uv venv
   uv run ai-engineer.py
   ```

   #### Using pip
   ```bash
   pip install -r requirements.txt
   python3 ai-engineer.py
   ```

## Environment Setup

Add your API keys to the `.env` file:

```bash
# For DeepSeek models
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# For OpenRouter models  
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Note**: You only need the API key for the provider you want to use.

## Usage Examples

### **Model Management**
```
You> /model list

📋 Available Models:

DeepSeek Models
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Model Name       ┃ Display Name       ┃ Features  ┃ Status      ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ deepseek-reasoner│ DeepSeek Reasoner  │ Reasoning │ 🟢 Current │
└──────────────────┴────────────────────┴───────────┴─────────────┘

You> /model set anthropic/claude-3.7-sonnet
✅ Switched to Anthropic Claude 3.7 Sonnet (Openrouter)

You (Openrouter)> Hello! I'm now using Claude 3.7 Sonnet
```

### **Natural Conversation with Automatic File Operations**
```
You (DeepSeek)> Can you read the main.py file and create a test file for it?

💭 Reasoning: I need to first read the main.py file to understand its structure...

🤖 AI Engineer> I'll read the main.py file first to understand its structure.
⚡ Executing 1 function call(s)...
→ read_file
✓ Read file 'main.py'

🔄 Processing results...
Now I'll create comprehensive tests based on the code structure I found.
⚡ Executing 1 function call(s)...
→ create_file
✓ Created/updated file at 'test_main.py'

I've analyzed main.py and created comprehensive tests covering all the main functions...
```

### **🔄 Recursive Task Completion in Action**
```
You> Fix the test file

🔄 Iteration 1
🤖 AI Engineer> I'll read the test file first to understand the issues.
⚡ Executing 1 function call(s)...
→ read_file
🔍 LINTER DIAGNOSTICS:
test.py:15:5: F401 'os' imported but unused
test.py:12:1: E302 expected 2 blank lines, found 1
⚠️  ISSUES DETECTED - Please fix these errors/warnings!
✅ Function calls completed. Checking for additional actions...

🔄 Iteration 2
🔄 Continuing...
I've identified several issues. Let me fix them automatically:
⚡ Executing 1 function call(s)...
→ edit_file
✓ Fixed missing return statement
✅ Function calls completed. Checking for additional actions...

🔄 Iteration 3
🔄 Continuing...
Now I'll add proper error handling:
⚡ Executing 1 function call(s)...
→ edit_file
✓ Added try-except block for division by zero
✅ Function calls completed. Checking for additional actions...

🔄 Iteration 4
🔄 Continuing...
Removing unused imports:
⚡ Executing 1 function call(s)...
→ edit_file
✓ Cleaned up unused imports
✅ Task completed after 4 iteration(s)

Perfect! ✅ All issues have been automatically detected and fixed:
- Missing return statement ✓
- Division by zero handling ✓
- Unused imports cleanup ✓
- PEP 8 compliance ✓
```

### **🌐 Multi-Language Error Detection Examples**

#### **JavaScript Error Detection**
```
You> Fix the test_js_errors.js file

🔄 Iteration 1
🤖 AI Engineer> I'll analyze the JavaScript file for issues.
⚡ Executing 1 function call(s)...
→ read_file
🔍 LINTER DIAGNOSTICS:
test_js_errors.js:4:7: 'unusedVariable' is assigned a value but never used
test_js_errors.js:7:16: Missing semicolon
test_js_errors.js:12:1: Expected return statement in function
⚠️  ISSUES DETECTED - Please fix these errors/warnings!

🔄 Iteration 2
🔄 Continuing...
Fixing ESLint issues automatically:
⚡ Executing 1 function call(s)...
→ edit_file
✓ Fixed missing semicolons and return statements
✅ Task completed after 3 iteration(s)
```

#### **TypeScript Error Detection**
```
You> Fix the test_ts_errors.ts file

🔄 Iteration 1
🤖 AI Engineer> Analyzing TypeScript file for type and style issues.
⚡ Executing 1 function call(s)...
→ read_file
🔍 LINTER DIAGNOSTICS:
TypeScript Compiler:
test_ts_errors.ts(12,24): error TS7006: Parameter 'data' implicitly has an 'any' type
test_ts_errors.ts(18,12): error TS2322: Type 'number' is not assignable to type 'string'

ESLint:
test_ts_errors.ts:21:7: 'unusedConstant' is assigned a value but never used
⚠️  ISSUES DETECTED - Please fix these errors/warnings!

🔄 Iterations 2-5
🔄 Continuing...
Systematically fixing all TypeScript and ESLint issues:
- Added proper type annotations ✓
- Fixed type mismatches ✓
- Removed unused variables ✓
- Added null checks ✓
- Fixed interface implementations ✓
✅ Task completed after 5 iteration(s)
```

### **Cross-Provider Workflow**
```
You (DeepSeek)> /model set google/gemini-2.5-pro-preview
✅ Switched to Google Gemini 2.5 Pro Preview (Openrouter)

You (Openrouter)> Now analyze the same code with a different perspective

🤖 AI Engineer> I'll analyze the code from a different architectural perspective...
⚡ Executing 1 function call(s)...
→ read_file
```

### **🔌 MCP Integration Examples**

#### **Context7 Library Research**
```
You> Research the latest Pydantic AI documentation and show me examples

🤖 AI Engineer> I'll research the latest Pydantic AI documentation for you.
⚡ Using MCP server: Context7
→ resolve-library-id
✓ Found library: /pydantic/pydantic-ai

→ get-library-docs
✓ Retrieved latest documentation and examples

Based on the latest Pydantic AI documentation, here are the key features and examples:

## Pydantic AI Overview
Pydantic AI is a Python agent framework designed to make it less painful to build production-grade applications with generative AI...

[Detailed documentation and code examples follow]
```

#### **MCP Server Management**
```
You> /mcp list

🔌 MCP Server Status:

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Server Name               ┃ Description                              ┃ Status                                 ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ context7                  │ Context7 MCP Server for library docs    │ 🟢 Active (2 tools available)         │
└───────────────────────────┴──────────────────────────────────────────┴────────────────────────────────────────┘

You> /mcp reload
✅ MCP configuration reloaded successfully
🔄 All active servers reinitialized with new configuration
```

#### **Dynamic Library Research**
```
You> I need to understand how to use FastAPI with async database operations

🤖 AI Engineer> I'll research the latest FastAPI documentation focusing on async database operations.
⚡ Using MCP server: Context7
→ resolve-library-id
✓ Found library: /tiangolo/fastapi

→ get-library-docs
✓ Retrieved focused documentation on async database operations

Here's what I found about FastAPI async database operations:

## Async Database Operations in FastAPI
[Current documentation with examples follows...]

Would you like me to create example code based on these patterns?
```

## Technical Details

### **Multi-Provider Architecture**
- **Unified API Interface**: All providers use OpenAI-compatible APIs
- **Provider-Specific Features**: Reasoning content for DeepSeek, extra headers for OpenRouter
- **Dynamic Client Management**: Automatic client switching based on selected model
- **Graceful Fallbacks**: Clear error messages when API keys are missing

### **Model Configuration**
- **Provider Configs**: Base URLs, API keys, and special headers
- **Model Metadata**: Display names, capabilities, and feature flags
- **Runtime Switching**: Change models without restarting the application

### **Function Call Execution Flow**
1. **User Input** → Natural language request
2. **AI Reasoning** → Visible thought process (DeepSeek models only)
3. **Function Calls** → Automatic tool execution
4. **Real-time Feedback** → Operation status and results
5. **Follow-up Response** → AI processes results and responds

## Advanced Features

### **Provider-Specific Capabilities**
- **DeepSeek Models**: Chain-of-thought reasoning display
- **OpenRouter Models**: Access to latest models from multiple providers
- **Automatic Detection**: Features enabled based on current model

### **Intelligent Context Management**
- **Automatic file detection** from user messages
- **Smart conversation cleanup** to prevent token overflow
- **File content preservation** across conversation history
- **Tool message integration** for complete operation tracking

### **Batch Operations**
```
You> Create a complete Flask API with models, routes, and tests

🤖 AI Engineer> I'll create a complete Flask API structure for you.
⚡ Executing 1 function call(s)...
→ create_multiple_files
✓ Created 4 files: app.py, models.py, routes.py, test_api.py
```

## 🔌 MCP (Model Context Protocol) Integration

AI Engineer includes powerful MCP integration that extends the AI's capabilities with external tools and resources. This enables real-time access to up-to-date documentation, APIs, and specialized tools.

### **Available MCP Servers**

#### **Context7 Documentation Research**
- **Server**: `context7`
- **Purpose**: Retrieve up-to-date documentation and examples for any library
- **Tools**:
  - `resolve-library-id`: Find the correct library identifier
  - `get-library-docs`: Fetch focused documentation and examples
- **Usage**: Automatically used when you ask about libraries, frameworks, or need current documentation

### **MCP Configuration**

MCP servers are configured in `mcp.config.json`:
```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "description": "Context7 MCP Server for library docs",
      "enabled": true
    }
  }
}
```
-for the Brave Search MCP, remember to add the brave api key in the mcp.config.json file

```json
{
  "servers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      },
      "description": "Brave Search MCP Server for web search",
      "enabled": true
    }
  }
}
```

### **MCP Features**
- **Hot-Reloadable**: Changes to MCP configuration take effect without restart
- **Lazy Initialization**: Servers start only when needed to improve performance
- **Error Handling**: Graceful fallbacks when MCP servers are unavailable
- **Status Monitoring**: Real-time status of all configured servers
- **Dynamic Management**: Enable/disable servers during runtime

### **How MCP Enhances AI Engineer**
1. **Current Documentation**: Always get the latest docs, not outdated training data
2. **Library Research**: Instant access to documentation for any library or framework
3. **Code Examples**: Get working examples and best practices
4. **API References**: Access to current API documentation and usage patterns
5. **Extensibility**: Easy to add new MCP servers for specialized capabilities

## Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/model list` | Show all available models | `/model list` |
| `/model current` | Show current model | `/model current` |
| `/model set <name>` | Switch to model | `/model set anthropic/claude-3.5-sonnet` |
| `/mcp list` | Show MCP server status | `/mcp list` |
| `/mcp enable <server>` | Enable MCP server | `/mcp enable context7` |
| `/mcp disable <server>` | Disable MCP server | `/mcp disable context7` |
| `/mcp reload` | Reload MCP configuration | `/mcp reload` |
| `/add <path>` | Add file/folder to context | `/add src/utils.py` |
| `exit` or `quit` | End session | `exit` |

## Getting Started

### Prerequisites
You need at least one API key:
1. **DeepSeek API Key**: Get from [DeepSeek Platform](https://platform.deepseek.com) (for DeepSeek models)
2. **OpenRouter API Key**: Get from [OpenRouter](https://openrouter.ai) (for OpenRouter models)
3. **Python 3.11+**: Required for optimal performance

### Multi-Language Error Detection Setup
For automatic error detection and fixing in JavaScript and TypeScript:
4. **Node.js & npm**: Required for ESLint and TypeScript compiler
5. **ESLint**: `npm install -g eslint` (for JavaScript/TypeScript linting)
6. **TypeScript**: `npm install -g typescript` (for TypeScript type checking)

📖 **See [MULTI_LANGUAGE_SETUP.md](MULTI_LANGUAGE_SETUP.md) for detailed setup instructions**

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/FaustoS88/AI_Engineer
   cd AI_engineer
   ```

2. **Set up environment**:
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env and add your API keys
   # You only need the keys for providers you want to use
   ```

3. **Install dependencies** (choose one method):

   #### Using uv (recommended - faster)
   ```bash
   uv venv
   uv run ai-engineer.py
   ```

   #### Using pip
   ```bash
   pip install -r requirements.txt
   python3 ai-engineer.py
   ```

## Environment Setup

Add your API keys to the `.env` file:

```bash
# For DeepSeek models
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# For OpenRouter models  
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Note**: You only need the API key for the provider you want to use.

## Troubleshooting

### **Common Issues**

**API Key Not Found**
```bash
# Make sure .env file exists with your API keys
cp .env.example .env
# Edit .env and add your keys
```

**Model Not Available**
```bash
# Check available models
/model list

# Ensure you have the correct API key for the provider
```

**Import Errors**
```bash
# Install dependencies
uv sync  # or pip install -r requirements.txt
```

## Contributing

This project showcases multi-provider AI integration with function calling. Contributions are welcome!

### **Development Setup**
```bash
git clone <repository-url>
cd AI_engineer
uv venv
uv sync
```

### **Run**
```bash
# Run the application (preferred)
uv run ai-engineer.py
```
or
```bash
python3 ai-engineer.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> **Note**: AI Engineer provides a unified interface to multiple AI providers, allowing you to choose the best model for each task. Use responsibly and enjoy the enhanced AI pair programming experience! 🚀