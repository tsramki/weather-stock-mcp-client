# Weather & Stock MCP Client

A LangChain agent that connects to a remote MCP server over streamable HTTP and uses its tools to answer questions about stock prices and weather.

- `get_stock_price(ticker)`: last traded price (via yfinance)
- `get_weather(city)`: current weather (via OpenWeather)

The client uses `MultiServerMCPClient` from `langchain-mcp-adapters` and the model is `anthropic:claude-sonnet-5`.

## Prerequisites

- Python 3.13 and [uv](https://docs.astral.sh/uv/)
- An Anthropic API key
- The MCP server (`../weather-stock-mcp-server`) running and reachable over HTTP

## Setup

```bash
uv venv
uv pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

| Variable | Required | Description |
|---|---|---|
| `MCP_SERVER_URL` | yes | Full URL of the MCP endpoint, **including the `/mcp` path**, e.g. `http://127.0.0.1:8000/mcp` |
| `ANTHROPIC_API_KEY` | yes | Anthropic API key used for the model |
| `MCP_SERVER_TOKEN` | yes | Bearer token sent as `Authorization` header. |

## Run

1. Start the MCP server :

   ```bash
   cd ../weather-stock-mcp-server
   python server.py   # serves streamable HTTP on port 8000
   ```

2. Start the client:

   ```bash
   uv run agent.py
   ```

3. Ask questions at the prompt, e.g. `What is the price of AAPL?` or `What's the weather in Paris?`. Press Ctrl+C to quit.

## Troubleshooting

- **`McpError: Session terminated`**: the URL is wrong, usually a missing `/mcp` path, or the server isn't running.
- **`Anthropic authentication failed: no API key...`**: set `ANTHROPIC_API_KEY` in `.env`. You can ignore the LangSmith gateway variables mentioned in that message.
- **`KeyError: 'MCP_SERVER_URL'`**: `.env` is missing or the variable isn't set.
- **`Client error: '401 Unauthorized'`**: `.env` is missing MCP_SERVER_TOKEN or the variable isn't set.
