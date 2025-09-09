import asyncio
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    # MCP local
    server_params = StdioServerParams(command="python", args=["mcp_local.py"])
    tools = await mcp_server_tools(server_params)

    # Agente
    agent = AssistantAgent(
        name="architect_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4o"),
        tools=tools
    )

    # Passo 1: buscar diretrizes do site
    fetch_task = "Fetch URL https://example.com/arquitetura using fetch_url tool"
    architecture_content = await agent.run(task=fetch_task)

    print("\n=== Diretrizes de Arquitetura Obtidas ===")
    print(architecture_content[:500])  # mostra apenas os primeiros 500 caracteres

    # Passo 2: gerar código baseado nas diretrizes
    code_task = f"Use the following architecture guidelines to generate a Java Spring Boot project:\n{architecture_content}"
    generated_code = await agent.run(task=code_task)

    print("\n=== Código Gerado pelo Agente ===")
    print(generated_code[:1000])  # mostra parte do código

if __name__ == "__main__":
    asyncio.run(main())
