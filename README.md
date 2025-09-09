# MCP Integration Project

Este projeto demonstra a integração entre **AutoGen** e **MCP (Model Context Protocol)** para criar agentes inteligentes capazes de buscar conteúdo da web, analisar diretrizes de arquitetura e gerar código automaticamente.

## 🚀 Funcionalidades

- **Busca de Conteúdo Web**: Agentes que podem fazer fetch de URLs para obter diretrizes e documentação
- **Geração de Código Java**: Criação automática de projetos Spring Boot baseados em diretrizes arquiteturais
- **Download de Projetos GitHub**: Ferramentas para baixar e analisar repositórios GitHub
- **Parser de Código Java**: Análise e processamento de código Java existente
- **Integração MCP Local**: Servidor MCP personalizado para operações locais

## 📋 Pré-requisitos

- Python 3.8+
- OpenAI API Key (configurada como variável de ambiente)
- uv (para instalação de ferramentas MCP)

## 🛠️ Instalação

### 1. Instalação Automática
Execute o script de instalação:

```bash
chmod +x install.sh
./install.sh
```

### 2. Instalação Manual

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar ferramentas MCP
uv tool install mcp-server-fetch
uv tool update-shell
```

### 3. Configuração da API Key OpenAI

```bash
export OPENAI_API_KEY="sua-api-key-aqui"
```

## 📁 Estrutura do Projeto

```
mcp-integration/
├── main.py                      # Script principal de demonstração
├── agent_v2.py                  # Agente melhorado com interface de console
├── java_code_generator.py       # Gerador de código Java com chunking
├── github_downloader.py         # Downloader de repositórios GitHub
├── github_project_downloader.py # Versão alternativa do downloader
├── simple_github_downloader.py  # Versão simplificada
├── java_parser_code.py          # Parser de código Java
├── agent_java_parse_code.py     # Agente para análise de código Java
├── mcp_local.py                 # Servidor MCP local personalizado
├── mcp_fetch_url.py             # Utilitário para fetch de URLs
├── mcp_save_file.py             # Utilitário para salvar arquivos
├── install.sh                   # Script de instalação
└── requirements.txt             # Dependências Python
```

## 🎯 Casos de Uso

### 1. Geração de Projeto Spring Boot

```bash
python main.py
```

Este script:
- Faz fetch das diretrizes de arquitetura de um site
- Usa as diretrizes para gerar um projeto Java Spring Boot
- Exibe o código gerado

### 2. Agente Interativo com Console

```bash
python agent_v2.py
```

Cria um agente interativo que pode:
- Buscar conteúdo de URLs específicas
- Gerar projetos baseados em diretrizes online
- Interagir via console

### 3. Download e Análise de Repositórios GitHub

```bash
python github_downloader.py
```

### 4. Geração Avançada de Código Java

```bash
python java_code_generator.py
```

Inclui funcionalidades de:
- Chunking de texto para grandes documentos
- Geração de código baseada em padrões de design
- Processamento em etapas

## 🔧 Componentes Principais

### MCP Local Server (`mcp_local.py`)
Servidor MCP personalizado que implementa:
- `fetch_url`: Busca conteúdo de URLs via HTTP
- Protocolo JSON-RPC para comunicação

### AutoGen Agents
Agentes inteligentes configurados com:
- Modelo GPT-4
- Ferramentas MCP integradas
- Capacidade de reflexão sobre uso de ferramentas

### Utilitários
- **Parsers Java**: Análise de código fonte Java
- **Downloaders GitHub**: Obtenção de repositórios
- **Geradores de Código**: Criação automática de projetos

## 📊 Dependências Principais

- `autogen-ext[mcp]>=0.2.2` - Framework AutoGen com suporte MCP
- `autogen-agentchat>=0.1.0` - Sistema de chat para agentes
- `openai>=1.0.0` - Cliente OpenAI
- `requests>=2.31.0` - Requisições HTTP
- `aiohttp>=3.8.0` - Cliente HTTP assíncrono

## 🔍 Exemplos de Uso

### Exemplo 1: Buscar Diretrizes e Gerar Código

```python
import asyncio
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def example():
    # Configurar MCP
    server_params = StdioServerParams(command="python", args=["mcp_local.py"])
    tools = await mcp_server_tools(server_params)
    
    # Criar agente
    agent = AssistantAgent(
        name="code_generator",
        model_client=OpenAIChatCompletionClient(model="gpt-4"),
        tools=tools
    )
    
    # Executar tarefa
    result = await agent.run(task="Fetch https://example.com and generate code")
    return result
```

### Exemplo 2: Análise de Repositório GitHub

```python
# O agente pode buscar e analisar repositórios GitHub automaticamente
task = "Download and analyze the structure of repository: https://github.com/user/repo"
```

## 🐛 Troubleshooting

### Erro: "MCP server not found"
```bash
# Verificar instalação do uv
which uv

# Reinstalar ferramentas MCP
uv tool install mcp-server-fetch
uv tool update-shell
```

### Erro: "OpenAI API Key not found"
```bash
# Configurar variável de ambiente
export OPENAI_API_KEY="sua-chave-aqui"

# Ou adicionar ao ~/.bashrc para permanência
echo 'export OPENAI_API_KEY="sua-chave-aqui"' >> ~/.bashrc
source ~/.bashrc
```

### Problemas de Timeout
Ajustar timeout nas configurações do MCP local:
```python
# Em mcp_local.py, linha ~15
r = requests.get(url, timeout=30)  # Aumentar de 5 para 30 segundos
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

- **Repositório**: [python-mcp-integration](https://github.com/zsantana/python-mcp-integration)
- **Issues**: [GitHub Issues](https://github.com/zsantana/python-mcp-integration/issues)

## 🔗 Links Úteis

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Spring Boot Guides](https://spring.io/guides/)

---

**Nota**: Este projeto é uma demonstração da integração entre AutoGen e MCP para automatização de desenvolvimento de software. Ideal para prototipagem rápida e geração automática de código baseada em diretrizes arquiteturais.
