#!/bin/bash

# Script para instalar as dependências e ferramentas MCP necessárias

echo "🔧 Instalando dependências Python..."
pip install -r requirements.txt

echo "🛠️ Instalando ferramentas MCP..."
uv tool install mcp-server-fetch

echo "🔄 Atualizando shell path..."
uv tool update-shell

echo "✅ Instalação concluída!"
echo ""
echo "📋 Para executar os programas:"
echo "   • Download simples (sem IA): python simple_github_downloader.py"
echo "   • Download básico com MCP fetch: python github_downloader.py"  
echo "   • Download com análise por IA: python github_project_downloader.py"
echo "   • Programa original: python agent_v2.py"
echo ""
echo "💡 Dica: Comece com simple_github_downloader.py se quiser apenas baixar e analisar sem IA"
