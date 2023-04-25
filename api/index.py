from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

#import audioldm
 
class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        q = query_params.get("q", [""])[0]
        self.wfile.write(q.encode('utf-8'))
        return