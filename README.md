# AI Engineer

> Archived in November 2026. A learning project from June 2025, kept for reference and no longer maintained.

AI Engineer is a terminal coding assistant. On top of its base (credited at the end) I added a provider and model registry with runtime switching between DeepSeek and OpenRouter models, a loop of up to ten tool-calling rounds that feeds flake8, ESLint and tsc output back to the model, and MCP servers attached to a Pydantic AI agent, with `/mcp` commands and config reload.

[Demo recording](assets/demo.gif) (27 MB GIF, June 2025, recorded before the MCP work).

## Running it

It was written against Pydantic AI 0.2 and mid-2025 model names, several of them since retired by their providers. The locked versions still start the app; a plain `pip install -r requirements.txt` now pulls Pydantic AI 2 and fails at import.

    git clone https://github.com/FaustoS88/AI-Engineer && cd AI-Engineer
    export DEEPSEEK_API_KEY=...
    uv run --frozen ai-engineer.py

## Known limits

`edit_file` works only on files first loaded with `/add`. File tools run without confirmation and are not confined to the working directory.

## Credits

Built on [deepseek-engineer](https://github.com/Doriandarko/deepseek-engineer) by Doriandarko (MIT), which provides the file tools, the system prompt and the conversation handling. MIT, see [LICENSE](LICENSE).
