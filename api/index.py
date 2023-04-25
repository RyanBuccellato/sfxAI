from http.server import BaseHTTPRequestHandler
import urlparse

import audioldm
 
class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        o = urlparse.urlparse(self.path)
        q = urlparse.parse_qs(o.query)
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(f'{q.get("q")}}'.encode('utf-8'))
        return