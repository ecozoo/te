import http.server
import socketserver
import os
# import sys

#import importlib
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置响应头，指定编码为utf-8
        # self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-type', 'text/html; charset=en_US.UTF-8')
        # self.send_header('Content-type', 'text/html; charset=iso-8859-1')
        self.end_headers()

""" 直接在html中meta中指定是uft-8可以解决某些utf-8字符被ascii显示的乱码, 但每个html文件都得改. 下面的Handler统一解决
<head>
  <meta charset="UTF-8">
  <title>My HTML Page</title>
</head>
"""
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        """Overrides SimpleHTTPRequestHandler method"""
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return self.send_error(403, "Directory access is forbidden.")
        ctype = self.guess_type(path)
        try:
            # Use UTF-8 instead of ASCII
            self.send_response(200)
            self.send_header("Content-type", ctype + "; charset=utf-8")
            self.send_header("Content-Length", os.stat(path).st_size)
            self.send_header("Last-Modified", self.date_time_string(os.stat(path).st_mtime))
            self.end_headers()
            return open(path, "rb")
        except Exception:
            self.send_error(404, "File not found")

PORT = 18080  # 更改端口以匹配您希望服务器侦听的端口
# Handler = http.server.SimpleHTTPRequestHandler
Handler = CustomHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
