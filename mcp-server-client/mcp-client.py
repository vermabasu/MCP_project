import asyncio

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from mcp_use import MCPAgent, MCPClient
import os

async def main():
    """Run chat using MCPAgent built in memory."""

    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    config_file = "mcp-server-client/mcp-server.json"

    print("Initializing MCPClient...")

    client = MCPClient(config_file)
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"),verbose=False)
    print("MCPClient initialized successfully.")

    agent = MCPAgent(client=client, llm=llm,max_steps=10,memory_enabled=True)

    try:
        print("Starting chat...")
        while True:
            input_text = input("Enter your message: ")
            if input_text.lower() in ["exit", "quit", "bye"]:
                print("Exiting...")
                return
            if input_text.lower() == "clear":
                print("Clearing memory...")
                agent.clear_conversation_history()
                print("Memory cleared successfully.")
                return
            print("Assistant: ", end="",flush=True)

            response = await agent.run(input_text)
            print(response)
    except Exception as e:
            print(f"Error: {e}")
    finally:
        if client and client.sessions:
            print("Closing MCPClient...")
            await client.close_all_sessions()
            print("MCPClient closed successfully.")
        print("Exiting...")

if __name__ == "__main__":
    asyncio.run(main())
