import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# The MCP server is assumed to be deployed remotely (not spawned locally).
MCP_SERVER_URL = os.environ["MCP_SERVER_URL"]  # e.g. https://my-host.example.com/mcp
MCP_SERVER_TOKEN = os.getenv("MCP_SERVER_TOKEN")  # optional bearer token

mcp_client = MultiServerMCPClient(
    {
        "stock_weather": {
            "transport": "streamable_http",
            "url": MCP_SERVER_URL,
            **(
                {"headers": {"Authorization": f"Bearer {MCP_SERVER_TOKEN}"}}
                if MCP_SERVER_TOKEN
                else {}
            ),
        }
    }
)

model = init_chat_model(
    "anthropic:claude-sonnet-5",
    timeout=600,
    max_tokens=4096,
)


async def main():
    tools = await mcp_client.get_tools()
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a helpful assistant with access to two tools: one for looking up "
            "the last stock price for a ticker symbol, and one for looking up current "
            "weather for a city. Use them when relevant."
        ),
    )

    print("Ask about a stock price or the weather (Ctrl+C to quit).")
    while True:
        try:
            user_input = (await asyncio.to_thread(input, "\n> ")).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not user_input:
            continue

        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
