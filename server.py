from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os

PORT = 8000

class Handler(SimpleHTTPRequestHandler):
    pass

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    server = HTTPServer(("0.0.0.0", PORT), Handler)

    print("=" * 50)
    print(f"Lionex Landing Page Running")
    print(f"http://localhost:{PORT}")
    print("=" * 50)

    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except:
        pass

    server.serve_forever()
