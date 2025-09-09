import asyncio
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

CHUNK_SIZE = 4000  # tokens aproximados

async def chunk_text(text, size=CHUNK_SIZE):
    """Divide o texto em chunks menores"""
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

async def main():
    # MCP local
    server_params = StdioServerParams(command="python", args=["mcp_local.py"])
    tools = await mcp_server_tools(server_params)

    # Agente
    agent = AssistantAgent(
        name="architect_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4.1-mini"),
        tools=tools
    )

    # ===== Passo 1: Buscar diretrizes do site =====
    fetch_task = "Fetch URL https://refactoring.guru/design-patterns/java using fetch_url tool"
    architecture_content = await agent.run(task=fetch_task)

    # ===== Passo 2: Chunking e resumo =====
    chunks = await chunk_text(architecture_content, size=4000)
    summarized_chunks = []
    for chunk in chunks:
        summary_task = f"Summarize the following architecture guidelines in concise bullet points:\n{chunk}"
        summary = await agent.run(task=summary_task)
        summarized_chunks.append(summary)

    summarized_guidelines = "\n".join(summarized_chunks)
    print("\n=== Diretrizes resumidas ===")
    print(summarized_guidelines[:1000])  # mostra 1000 caracteres

    # ===== Passo 3: Gerar projeto Spring Boot =====
    code_task = f"""
Using the following architecture guidelines, generate a complete Java Spring Boot project with:
- MVC structure
- Entities, Repositories, Services, Controllers
- Basic validation and exception handling
- README and build instructions

Architecture Guidelines:
{summarized_guidelines}
"""
    generated_code = await agent.run(task=code_task)
    print("\n=== Código gerado pelo agente (exemplo parcial) ===")
    print(generated_code[:1500])  # mostra apenas parte do código

if __name__ == "__main__":
    asyncio.run(main())
