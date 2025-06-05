import os
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Timer
import subprocess
import socket

# Classe personalizada do manipulador HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        SimpleHTTPRequestHandler.end_headers(self)

def find_available_port(start_port=8000, max_tries=10):
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                continue
    raise OSError("Nenhuma porta disponível encontrada.")

def open_browser(port):
    webbrowser.open(f'http://localhost:{port}/index.html')

# Função principal
def main():
    print("Iniciando Apresentação da Reforma Tributária...")

    # Combinar os slides
    print("Combinando slides...")
    try:
        subprocess.run(["python", "combine_slides.py"], check=True)
    except subprocess.CalledProcessError:
        print("Erro ao combinar slides. Tentando método alternativo...")
        try:
            from combine_slides import combine_slides
            combine_slides()
        except Exception as e:
            print(f"Erro no método alternativo de combinação: {e}")
            return

    try:
        port = find_available_port()
        print(f"Iniciando servidor web na porta {port}...")
        server = HTTPServer(('localhost', port), MyHandler)
        Timer(1, open_browser, args=(port,)).start()
        print(f"Servidor rodando em http://localhost:{port}/index.html")
        print("Pressione Ctrl+C para encerrar o servidor")
        server.serve_forever()
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
    finally:
        try:
            server.shutdown()
        except:
            pass

if __name__ == "__main__":
    main()
