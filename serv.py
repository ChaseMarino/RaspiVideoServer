from http.server import HTTPServer, BaseHTTPRequestHandler
from subprocess import check_output
import os
import urllib.parse
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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
            self.handle_page_load(content)
        elif self.path == "/fullscreen":
            self.handle_fullscreen(content)
        elif self.path == "/volumeUp":
            self.handle_volumeUp(content)
        elif self.path == "/volumeDown":
            self.handle_volumeDown(content)
        elif self.path == "/pause":
            self.handle_pause(content)



        self.send_response(302)
        self.send_header('Location', "/index.html")
        self.end_headers()
        
    def handle_pause(self, content: str):
        driver.find_element_by_tag_name("html").send_keys("SPACE")

    def handle_fullscreen(self, content: str):
        driver.find_element_by_tag_name("html").send_keys("f")
        
    def handle_volumeUp(self, content: str):
        driver.find_element_by_tag_name("html").send_keys("ARROW_UP")

    def handle_volumeDown(self, content: str):
        driver.find_element_by_tag_name("html").send_keys("ARROW_DOWN")

    def handle_page_load(self, content: str):
        link_url = content.split('=', 1)[1]
        global driver
        driver.get("http://" + urllib.parse.unquote(link_url))


driver = webdriver.Chrome()

address = ('0.0.0.0', 8080)
httpd = HTTPServer(('0.0.0.0', 8080), Serv)
print("Starting http server on %s:%d" % address)
httpd.serve_forever()
