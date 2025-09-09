import asyncio
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import requests
from bs4 import BeautifulSoup
import sys

CHUNK_SIZE = 4000  # tokens aproximados

async def fetch_java_code(url: str) -> list[str]:
    """
    Acessa a URL, parseia HTML e retorna uma lista de trechos de código Java.
    """
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    java_codes = []
    for code_block in soup.select("pre > code.language-java"):
        java_codes.append(code_block.get_text())
    
    return java_codes

async def chunk_text(text, size=CHUNK_SIZE):
    """Divide o texto em chunks menores"""
    chunks = []
    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])
    return chunks

async def main():
    # MCP local
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    tools = await mcp_server_tools(fetch_mcp_server)

    # Agente
    agent = AssistantAgent(
        name="architect_agent",
        model_client=OpenAIChatCompletionClient(model="gpt-4.1-mini"),
        tools=tools
    )

    # ===== Passo 1: Fetch URL e extrair código Java =====
    url = "https://spring.io/guides/gs/spring-boot"
    java_snippets = await fetch_java_code(url)

    # ===== Passo 2: Chunking e resumo =====
    summarized_chunks = []
    for snippet in java_snippets:
        summary_task = f"Summarize the following Java code snippet:\n{snippet}"
        summary = await agent.run(task=summary_task)
        summarized_chunks.append(summary)

    summarized_code = "\n".join(summarized_chunks)
    print("\n=== Código Java resumido ===")
    print(summarized_code[:1000])  # mostra 1000 caracteres

    # ===== Passo 3: Gerar arquivos do projeto =====
    file_tasks = [
        {"path": "project/src/main/java/com/example/MainApplication.java",
         "prompt": f"Generate a Spring Boot MainApplication.java class using the following code:\n{summarized_code}"},
        {"path": "project/src/main/java/com/example/controller/HelloController.java",
         "prompt": f"Generate a REST controller HelloController.java using the following code:\n{summarized_code}"},
        {"path": "project/pom.xml",
         "prompt": f"Generate a Maven pom.xml file for a Spring Boot project using the following code:\n{summarized_code}"},
        {"path": "project/README.md",
         "prompt": f"Generate a README.md explaining how to build and run the project:\n{summarized_code}"}
    ]

    for task in file_tasks:
        code = await agent.run(task=task["prompt"])
        save_task = {
            "method": "save_file",
            "params": {"path": task["path"], "content": code},
            "id": "1"
        }
        tools[0].send(save_task)  # tools[0] é o StdioServerParams tool client
        print(f"Arquivo solicitado para geração: {task['path']}")

    print("\n=== Todos os arquivos do projeto foram gerados! ===")

if __name__ == "__main__":
    asyncio.run(main())
