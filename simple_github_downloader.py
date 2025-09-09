# pip install requests
import os
import requests
import zipfile
import tempfile
from pathlib import Path

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
    
    # Try different branch names
    branches = ['main', 'master']
    
    for branch in branches:
        # GitHub ZIP download URL
        zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/{branch}.zip"
        
        # Create download directory
        os.makedirs(download_path, exist_ok=True)
        
        print(f"Tentando baixar {repo_name} da branch '{branch}' de {zip_url}...")
        
        try:
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
            
            # Find the extracted folder
            extracted_folder = os.path.join(download_path, f"{repo_name}-{branch}")
            if os.path.exists(extracted_folder):
                print(f"✅ Repository downloaded and extracted to: {extracted_folder}")
                return extracted_folder
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ Branch '{branch}' não encontrada, tentando próxima...")
                continue
            else:
                raise e
    
    raise Exception(f"Não foi possível baixar o repositório de nenhuma branch testada: {branches}")

def read_file_safely(file_path: str, max_chars: int = 2000) -> str:
    """Read a file safely with encoding handling."""
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read(max_chars)
                if len(content) == max_chars:
                    content += "\n... (arquivo truncado)"
                return content
        except UnicodeDecodeError:
            continue
    
    return f"❌ Não foi possível ler o arquivo {file_path}"

def analyze_project_comprehensive(project_path: str) -> None:
    """
    Comprehensive analysis of the downloaded project.
    """
    print(f"\n🔍 ANÁLISE DETALHADA DO PROJETO")
    print("=" * 50)
    
    project_name = os.path.basename(project_path)
    print(f"📁 Projeto: {project_name}")
    print(f"📍 Localização: {project_path}")
    
    # Key files to analyze in detail
    key_files = {
        'README.md': '📖 Documentação',
        'README.rst': '📖 Documentação', 
        'pom.xml': '☕ Maven (Java)',
        'build.gradle': '🐘 Gradle (Java/Kotlin)',
        'package.json': '📦 Node.js',
        'requirements.txt': '🐍 Python',
        'Dockerfile': '🐳 Docker',
        'docker-compose.yml': '🐳 Docker Compose',
        '.env.example': '⚙️ Configuração',
        'application.properties': '⚙️ Spring Boot Config',
        'application.yml': '⚙️ Spring Boot Config'
    }
    
    print(f"\n🔍 ARQUIVOS CHAVE ENCONTRADOS:")
    print("-" * 30)
    
    found_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file in key_files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                found_files.append((relative_path, file, file_path))
                
                icon_desc = key_files.get(file, '📄')
                print(f"  {icon_desc} {relative_path}")
    
    # Read and display content of key files
    print(f"\n📄 CONTEÚDO DOS ARQUIVOS PRINCIPAIS:")
    print("-" * 40)
    
    for relative_path, filename, full_path in found_files:
        print(f"\n📄 {relative_path}:")
        print("─" * (len(relative_path) + 4))
        content = read_file_safely(full_path)
        print(content)
        print()
    
    # Analyze source code structure
    print(f"\n🏗️ ESTRUTURA DO CÓDIGO FONTE:")
    print("-" * 30)
    
    source_dirs = ['src', 'lib', 'app', 'backend', 'frontend']
    for source_dir in source_dirs:
        source_path = os.path.join(project_path, source_dir)
        if os.path.exists(source_path):
            print(f"\n📂 {source_dir}/")
            for root, dirs, files in os.walk(source_path):
                level = root.replace(source_path, '').count(os.sep)
                if level > 3:  # Limit depth
                    continue
                indent = '  ' * level
                folder_name = os.path.basename(root)
                if folder_name:
                    print(f"{indent}📁 {folder_name}/")
                
                # Show relevant source files
                sub_indent = '  ' * (level + 1)
                relevant_extensions = ['.java', '.py', '.js', '.ts', '.kt', '.scala', '.go', '.rs']
                source_files = [f for f in files if any(f.endswith(ext) for ext in relevant_extensions)]
                
                for file in source_files[:5]:  # Show max 5 files per directory
                    print(f"{sub_indent}📄 {file}")
                if len(source_files) > 5:
                    print(f"{sub_indent}... e mais {len(source_files) - 5} arquivos")
    
    # Technology detection
    print(f"\n🛠️ TECNOLOGIAS DETECTADAS:")
    print("-" * 25)
    
    technologies = []
    
    # Check for Java/Spring Boot
    if any('pom.xml' in f[1] or 'build.gradle' in f[1] for f in found_files):
        technologies.append("☕ Java")
        if os.path.exists(os.path.join(project_path, 'src', 'main', 'java')):
            technologies.append("🍃 Spring Boot (provável)")
    
    # Check for Python
    if any('requirements.txt' in f[1] or 'setup.py' in f[1] for f in found_files):
        technologies.append("🐍 Python")
    
    # Check for Node.js
    if any('package.json' in f[1] for f in found_files):
        technologies.append("📦 Node.js")
    
    # Check for Docker
    if any('Dockerfile' in f[1] or 'docker-compose.yml' in f[1] for f in found_files):
        technologies.append("🐳 Docker")
    
    for tech in technologies:
        print(f"  {tech}")
    
    # Provide execution suggestions
    print(f"\n🚀 SUGESTÕES DE EXECUÇÃO:")
    print("-" * 25)
    
    if any('pom.xml' in f[1] for f in found_files):
        print("☕ Para projetos Maven (Java):")
        print("   mvn clean install")
        print("   mvn spring-boot:run")
    
    if any('build.gradle' in f[1] for f in found_files):
        print("🐘 Para projetos Gradle:")
        print("   ./gradlew build")
        print("   ./gradlew bootRun")
    
    if any('package.json' in f[1] for f in found_files):
        print("📦 Para projetos Node.js:")
        print("   npm install")
        print("   npm start")
    
    if any('requirements.txt' in f[1] for f in found_files):
        print("🐍 Para projetos Python:")
        print("   pip install -r requirements.txt")
        print("   python main.py")
    
    if any('Dockerfile' in f[1] for f in found_files):
        print("🐳 Para Docker:")
        print("   docker build -t app .")
        print("   docker run -p 8080:8080 app")

def main():
    """Main function to download and analyze the GitHub repository."""
    repo_url = "https://github.com/zsantana/spring-boot-mcp-server"
    
    print("🌟 GITHUB PROJECT DOWNLOADER & ANALYZER")
    print("=" * 50)
    print(f"🎯 Repositório: {repo_url}")
    
    try:
        extracted_path = download_github_repo(repo_url)
        analyze_project_comprehensive(extracted_path)
        
        print(f"\n✅ ANÁLISE CONCLUÍDA!")
        print(f"📁 Projeto baixado em: {extracted_path}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
