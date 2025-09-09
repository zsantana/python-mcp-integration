#!/usr/bin/env python3
import sys
import json
import requests
import os

def process_request(method, params, rpc_id):
    result = None
    if method == "fetch_url":
        url = params.get("url")
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            result = response.text
        except Exception as e:
            result = f"Erro ao acessar URL {url}: {e}"

    elif method == "save_file":
        path = params.get("path")
        content = params.get("content", "")
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            result = f"Arquivo salvo: {path}"
        except Exception as e:
            result = f"Erro ao salvar arquivo {path}: {e}"

    else:
        result = f"Método {method} não suportado."

    response_json = {"jsonrpc": "2.0", "id": rpc_id, "result": result}
    print(json.dumps(response_json), flush=True)

def main():
    # Se houver argumento de linha de comando, faz fetch direto
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"=== Teste fetch_url para: {url} ===")
        process_request("fetch_url", {"url": url}, rpc_id=1)
        return

    # Caso contrário, roda no modo JSON-RPC via stdin
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            rpc_id = request.get("id")
            process_request(method, params, rpc_id)
        except Exception as e:
            error_response = {"jsonrpc": "2.0", "id": None, "error": str(e)}
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()
