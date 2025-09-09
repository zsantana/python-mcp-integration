import sys, json, requests

def main():
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
                    result = r.text  # retorna o conteúdo completo
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
