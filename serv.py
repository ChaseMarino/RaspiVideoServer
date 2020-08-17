from http.server import HTTPServer, BaseHTTPRequestHandler
from subprocess import check_output

import urllib.parse
import webbrowser
import os


def get_pid(name):
    return check_output(["pidof",name])

class Serv(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == '/':
            self.path = '/index.html'
        
        if not(os.path.isfile(self.path[1:])):
            link = self.path[14::]
            link = urllib.parse.unquote(link)
            os.kill(pid, get_pid("chromium-browser"))
            webbrowser.open(link)
            self.path = 'index.html'
            
        try: 
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = open('index.html').read()
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))


httpd = HTTPServer(('0.0.0.0', 8080), Serv)
httpd.serve_forever()
