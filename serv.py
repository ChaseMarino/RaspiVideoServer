from http.server import HTTPServer, BaseHTTPRequestHandler
from subprocess import check_output
import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):


        driver = webdriver.Chrome(executable_path='/home/chase/.local/bin/chromedriver')

        if self.path == '/':
            self.path = '/index.html'
        
        if  (self.path.find("index") == -1 and self.path.find("style") == -1):
            link = self.path[14::]
            link = urllib.parse.unquote(link)
            driver.get(link)
            self.path = 'index.html'
              
        try: 
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = open('index.html').read()
            self.send_response(404)

        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))

        print ("\n \n \n \n ")
        print (self.path)
        print ("\n \n \n \n ")

httpd = HTTPServer(('0.0.0.0', 8080), Serv)
httpd.serve_forever()
