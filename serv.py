from http.server import HTTPServer, BaseHTTPRequestHandler
from subprocess import check_output
import os
import urllib.parse
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
              
        try: 
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = open('index.html').read()
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length).decode('utf-8')

        if self.path == "/page_load":
            self.page_load(content)
        elif self.path == "/fullscreen":
            self.handle_fullscreen(content)
        
        self.send_response(302)
        self.send_header('Location', "/index.html")
        self.end_headers()
        
    
    def handle_fullscreen(self):
        pass

    def handle_page_load(self, content: str):
        link_url = content.split('=', 1)[1]
        global driver
        driver.get("http://" + urllib.parse.unquote(link_url))


driver = webdriver.Chrome()

address = ('0.0.0.0', 8080)
httpd = HTTPServer(('0.0.0.0', 8080), Serv)
print("Starting http server on %s:%d" % address)
httpd.serve_forever()
