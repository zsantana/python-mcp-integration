#!/usr/bin/env python3
import sys, json, requests

def main():
    # Verifica se há argumentos da linha de comando
    if len(sys.argv) > 1:
        # Modo direto - executa uma única requisição
        if sys.argv[1] == "fetch_url" and len(sys.argv) > 2:
            url = sys.argv[2]
            try:
                r = requests.get(url, timeout=5)
                print(r.text)
            except Exception as e:
                print(f"Erro: {e}")
        else:
            print("Uso: python mcp_local.py fetch_url <URL>")
        return

    # Modo original - lê do stdin
    while True:
        line = sys.stdin.readline()
        if not line:
            break

        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            rpc_id = request.get("id")

            if method == "fetch_url":
                url = params.get("url")
                try:
                    r = requests.get(url, timeout=5)
                    result = r.text
                except Exception as e:
                    result = f"Erro: {e}"
            else:
                result = f"Método {method} não suportado."

            response = {"jsonrpc":"2.0","id":rpc_id,"result":result}
            print(json.dumps(response), flush=True)
        except Exception as e:
            error_response = {"jsonrpc": "2.0","id": None, "error": str(e)}
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    main()