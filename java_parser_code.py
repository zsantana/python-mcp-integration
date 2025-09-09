import requests
from bs4 import BeautifulSoup

def fetch_java_code(url: str) -> list[str]:
    """
    Acessa a URL, parseia HTML e retorna uma lista de trechos de código Java.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    java_codes = []
    
    # Seletores específicos para o site spring.io e outros sites comuns
    selectors = [
        # Spring.io específico
        "pre code",
        "code",
        ".highlight pre",
        ".code-block pre",
        # Seletores genéricos
        "pre > code.language-java",
        "code.language-java", 
        "pre > code[class*='java']",
        "code[class*='java']",
        ".highlight-java code",
        ".language-java"
    ]
    
    # Adicionar debug para ver a estrutura HTML
    print(f"Procurando código Java em: {url}")
    
    for selector in selectors:
        code_blocks = soup.select(selector)
        print(f"Seletor '{selector}' encontrou {len(code_blocks)} elementos")
        
        for code_block in code_blocks:
            text = code_block.get_text().strip()
            # Filtrar apenas blocos que parecem ser Java
            if text and is_likely_java_code(text) and text not in java_codes:
                java_codes.append(text)
    
    return java_codes

def is_likely_java_code(text: str) -> bool:
    """
    Verifica se o texto provavelmente é código Java.
    """
    java_indicators = [
        'public class', 'private class', 'protected class',
        'public static void main', '@SpringBootApplication',
        'import java.', 'import org.springframework',
        'package com.', 'package org.',
        '@RestController', '@GetMapping', '@PostMapping',
        '@Autowired', '@Component', '@Service'
    ]
    
    text_lower = text.lower()
    
    # Deve ter pelo menos um indicador Java e ter estrutura de código
    has_java_indicator = any(indicator.lower() in text_lower for indicator in java_indicators)
    has_code_structure = '{' in text and '}' in text
    
    return has_java_indicator or (has_code_structure and len(text) > 50)

# ==========================
# Exemplo de uso
# ==========================
if __name__ == "__main__":
    url = "https://spring.io/guides/gs/spring-boot"
    java_snippets = fetch_java_code(url)
    
    if java_snippets:
        print(f"\nEncontrados {len(java_snippets)} trechos de código Java:")
        for i, snippet in enumerate(java_snippets, start=1):
            print(f"\n--- Trecho Java {i} ---")
            print(snippet[:200] + "..." if len(snippet) > 200 else snippet)
    else:
        print("Nenhum código Java encontrado na página.")