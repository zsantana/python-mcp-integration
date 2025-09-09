# pip install -U autogen-ext[mcp] json-schema-to-pydantic>=0.2.2
# uv tool install mcp-server-fetch
# verify it in path by running uv tool update-shell
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_core import CancellationToken
from autogen_agentchat.ui import Console

async def main() -> None:
    # Setup server params for local filesystem access
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    tools = await mcp_server_tools(fetch_mcp_server)

    # Create an agent that can use the fetch tool.
    model_client = OpenAIChatCompletionClient(model="gpt-4.1-mini")
    agent = AssistantAgent(
        name="github_downloader", 
        model_client=model_client, 
        tools=tools, 
        reflect_on_tool_use=True,
    )

    termination = MaxMessageTermination(
        max_messages=10) | TextMentionTermination("TERMINATE")

    team = RoundRobinGroupChat([agent], termination_condition=termination)

    # Task to download the specific GitHub project
    task = """
    Baixe o projeto do GitHub: https://github.com/zsantana/spring-boot-mcp-server
    
    Por favor:
    1. Acesse a página do repositório GitHub
    3. Baixe os arquivos principais do projeto
    4. Forneça um resumo do que foi baixado e da estrutura do projeto
    5. Identifique as tecnologias e dependências utilizadas
    
    """
 
    await Console(team.run_stream(task=task, cancellation_token=CancellationToken()))
    
if __name__ == "__main__":
    asyncio.run(main())
