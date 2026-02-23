# AI Engineer

An interactive terminal coding assistant that talks to multiple LLM providers. Supports DeepSeek (with chain-of-thought display), OpenRouter, and any OpenAI-compatible endpoint. File operations are handled through function calling — the AI reads, creates, and edits files automatically as part of the conversation.

## Demo

![AI Engineer in action](./assets/demo.gif)

## Providers and Models

### DeepSeek
- `deepseek-reasoner` (default) — reasoning model with visible chain-of-thought
- `deepseek-chat` — faster, cheaper general-purpose model

### OpenRouter
- `google/gemini-2.5-pro-preview`
- `anthropic/claude-sonnet-4`
- `anthropic/claude-3.7-sonnet`
- `openai/gpt-4.1`
- `openai/o3-mini-high`
- ...and any other model available on OpenRouter

## Features

- **Multi-provider support** with runtime model switching (`/model set <name>`)
- **Automatic file operations** — mention a file in conversation and the AI reads it
- **Recursive task completion** — keeps iterating (up to 10 rounds) until the task is done, with linter feedback between iterations
- **Multi-language linting** — Python (flake8), JavaScript (ESLint), TypeScript (tsc + ESLint)
- **MCP integration** — connects to Model Context Protocol servers like Context7 for live documentation lookup
- **Rich terminal UI** — streaming output, color-coded feedback, model/provider indicator in the prompt

## Installation

```bash
git clone https://github.com/FaustoS88/AI_Engineer
cd AI_engineer
cp .env.example .env
# add your API keys to .env
```

Install dependencies (pick one):
```bash
# uv (faster)
uv venv && uv run ai-engineer.py

# pip
pip install -r requirements.txt && python3 ai-engineer.py
```

For JavaScript/TypeScript linting support:
```bash
npm install -g eslint typescript
```

## Environment

```bash
# .env
DEEPSEEK_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

You only need the key for the provider(s) you actually use.

## Commands

| Command | Description |
|---------|-------------|
| `/model list` | Show all available models |
| `/model current` | Show current model |
| `/model set <name>` | Switch model |
| `/mcp list` | Show MCP server status |
| `/mcp enable <server>` | Enable an MCP server |
| `/mcp disable <server>` | Disable an MCP server |
| `/mcp reload` | Reload MCP config without restart |
| `/add <path>` | Preload a file or folder into context |
| `exit` / `quit` | End session |

## MCP Integration

MCP servers are configured in `mcp.config.json`. Example with Context7 (library docs) and Brave Search:

```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "description": "Up-to-date library documentation",
      "enabled": true
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": { "BRAVE_API_KEY": "${BRAVE_API_KEY}" },
      "description": "Brave Search for web queries",
      "enabled": true
    }
  }
}
```

Servers are lazy-initialized and hot-reloadable via `/mcp reload`.

## Function Calling Tools

The AI can call these automatically during conversation:

- `read_file(file_path)` — read a single file
- `read_multiple_files(file_paths)` — batch read
- `create_file(file_path, content)` — create or overwrite
- `create_multiple_files(files)` — scaffold multiple files at once
- `edit_file(file_path, original_snippet, new_snippet)` — precise snippet replacement

## Troubleshooting

**API key not found** — check that `.env` exists and has the right key name.

**Model not available** — run `/model list` to see what's configured, and confirm you have the API key for that provider.

**Import errors** — run `uv sync` or `pip install -r requirements.txt`.

**JS/TS linting not working** — make sure `eslint` and `typescript` are installed globally (`npm install -g eslint typescript`). See [MULTI_LANGUAGE_SETUP.md](MULTI_LANGUAGE_SETUP.md) for details.

## License

MIT — see [LICENSE](LICENSE).
