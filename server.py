import http.server
import socketserver

PORT = 18080  # 更改端口以匹配您希望服务器侦听的端口
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
