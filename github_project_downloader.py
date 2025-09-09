# pip install -U autogen-ext[mcp] json-schema-to-pydantic>=0.2.2 requests
# uv tool install mcp-server-fetch
import asyncio
import os
import requests
import zipfile
import tempfile
from pathlib import Path
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_core import CancellationToken
from autogen_agentchat.ui import Console

def analyze_project_structure(project_path: str) -> str:
    """
    Analyze the structure and key files of a downloaded project.
    
    Args:
        project_path: Path to the extracted project
        
    Returns:
        Analysis summary of the project
    """
    analysis = []
    analysis.append(f"📁 Projeto: {os.path.basename(project_path)}")
    analysis.append(f"📍 Localização: {project_path}\n")
    
    # Key files to look for
    key_files = ['README.md', 'pom.xml', 'build.gradle', 'package.json', 'requirements.txt', 'Dockerfile']
    found_files = []
    
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file in key_files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                found_files.append(relative_path)
                
                # Read and analyze key files
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()[:1000]  # First 1000 chars
                        analysis.append(f"\n📄 {relative_path}:")
                        analysis.append(f"   Primeiras linhas: {content[:200]}...")
                except Exception as e:
                    analysis.append(f"\n📄 {relative_path}: (erro ao ler - {e})")
    
    if found_files:
        analysis.append(f"\n🔍 Arquivos chave encontrados: {', '.join(found_files)}")
    
    # Analyze directory structure
    analysis.append(f"\n🏗️ Estrutura do projeto:")
    for root, dirs, files in os.walk(project_path):
        level = root.replace(project_path, '').count(os.sep)
        if level > 2:  # Limit depth to avoid too much output
            continue
        indent = '  ' * level
        analysis.append(f"{indent}{os.path.basename(root)}/")
        if level < 2:  # Show files only for top 2 levels
            sub_indent = '  ' * (level + 1)
            for file in files[:5]:  # Show max 5 files per directory
                analysis.append(f"{sub_indent}{file}")
            if len(files) > 5:
                analysis.append(f"{sub_indent}... and {len(files) - 5} more files")
    
    return '\n'.join(analysis)

def download_github_repo(repo_url: str, download_path: str = "./downloaded_repos") -> str:
    """
    Download a GitHub repository as ZIP and extract it.
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/zsantana/spring-boot-mcp-server)
        download_path: Local path to extract the repository
        
    Returns:
        Path to the extracted repository
    """
    # Extract owner and repo name from URL
    parts = repo_url.rstrip('/').split('/')
    owner = parts[-2]
    repo_name = parts[-1]
    
    # GitHub ZIP download URL
    zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
    
    # Create download directory
    os.makedirs(download_path, exist_ok=True)
    
    print(f"Downloading {repo_name} from {zip_url}...")
    
    # Download the ZIP file
    response = requests.get(zip_url)
    response.raise_for_status()
    
    # Save and extract ZIP file
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
        temp_file.write(response.content)
        temp_zip_path = temp_file.name
    
    # Extract ZIP
    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(download_path)
    
    # Clean up temp file
    os.unlink(temp_zip_path)
    
    # Find the extracted folder (usually repo_name-main)
    extracted_folder = os.path.join(download_path, f"{repo_name}-main")
    if not os.path.exists(extracted_folder):
        # Try without -main suffix
        extracted_folder = os.path.join(download_path, repo_name)
    
    print(f"Repository downloaded and extracted to: {extracted_folder}")
    return extracted_folder

async def main() -> None:
    # First, download the GitHub repository directly
    repo_url = "https://github.com/zsantana/spring-boot-mcp-server"
    try:
        extracted_path = download_github_repo(repo_url)
        print(f"✅ Repositório baixado com sucesso em: {extracted_path}")
        
        # Analyze the project structure locally
        analysis = analyze_project_structure(extracted_path)
        print(f"\n{analysis}")
        
    except Exception as e:
        print(f"❌ Erro ao baixar o repositório: {e}")
        return
    
    # Setup MCP server with fetch capabilities for additional analysis
    fetch_mcp_server = StdioServerParams(command="uvx", args=["mcp-server-fetch"])
    tools = await mcp_server_tools(fetch_mcp_server)

    # Create an agent that can use fetch tools for additional research
    model_client = OpenAIChatCompletionClient(model="gpt-4.1-mini")
    agent = AssistantAgent(
        name="project_analyzer", 
        model_client=model_client, 
        tools=tools, 
        reflect_on_tool_use=True
    )

    termination = MaxMessageTermination(
        max_messages=6) | TextMentionTermination("TERMINATE")

    team = RoundRobinGroupChat([agent], termination_condition=termination)

    # Task to provide additional analysis using web research
    task = f"""
    Baseado na análise inicial do projeto Spring Boot MCP Server baixado do GitHub (https://github.com/zsantana/spring-boot-mcp-server), forneça uma análise mais detalhada:

    Análise inicial já realizada:
    {analysis}

    Por favor:
    1. Pesquise informações sobre Spring Boot MCP Server na web se necessário
    2. Explique o que é um MCP Server e como funciona
    3. Analise as tecnologias identificadas no projeto
    4. Forneça instruções detalhadas de como executar o projeto
    5. Explique os casos de uso e benefícios deste tipo de servidor
    6. Sugira melhorias ou próximos passos para desenvolvimento

    TERMINATE quando a análise detalhada estiver completa.
    """
 
    await Console(team.run_stream(task=task, cancellation_token=CancellationToken()))
    
if __name__ == "__main__":
    asyncio.run(main())
