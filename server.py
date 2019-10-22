from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random
from model import Model

class S(BaseHTTPRequestHandler):
    def initialize_model(self):
        self.model = Model()
        
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("Hello".encode('utf-8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        #self._set_headers()
        
        #self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        #self.data = json.loads(self.data_string)
        
        if(self.path.startswith('/new-folder')):
            self.send_response(200)
            self.end_headers()
            params = self.path.split('/')
            try:
                userID = params[2]
                folder_name = params[3]
                self.wfile.write(json.dumps(self.model.new_folder(userID, folder_name)).encode('utf-8'))
            except Exception as err:
                self.wfile.write(str(err).encode("utf-8"))
                
        if(self.path.startswith('/new-subfolder')):
            self.send_response(200)
            self.end_headers()
            params = self.path.split('/')
            try:
                userID = params[2]
                folder_name = params[3]
                subfolder_name = params[4]
                if self.model.new_subfolder(userID, folder_name, subfolder_name)["status"] == "success":
                    self.wfile.write("OK".encode('utf-8'))
                else:
                    self.wfile.write("User and folder not exist".encode('utf-8'))
            except Exception as err:
                self.wfile.write(str(err).encode("utf-8"))
                
        if(self.path.startswith('/userid-content')):
            self.send_response(200)
            self.end_headers()
            params = self.path.split('/')
            try:
                userID = params[2]
                root_folder_limit = int(params[3]) if params[3].isdigit() else params[3]
                sub_folder_limit = int(params[4]) if params[4].isdigit() else params[4]
                self.wfile.write(json.dumps(self.model.get_folder_content(userID, root_folder_limit, sub_folder_limit)).encode('utf-8'))
            except Exception as err:
                self.wfile.write(str(err).encode("utf-8"))
                
        if(self.path.startswith('/item-count')):
            self.send_response(200)
            self.end_headers()
            params = self.path.split('/')
            try:
                userID = params[2]
                self.wfile.write(json.dumps({"total":self.model.get_folder_count(userID)}).encode('utf-8'))
            except Exception as err:
                self.wfile.write(str(err).encode("utf-8"))
                
        if(self.path.startswith('/folder-content')):
            self.send_response(200)
            self.end_headers()
            params = self.path.split('/')
            params = self.path.split('/')
            try:
                userID = params[2]
                root_folder = params[3]
                sub_folder_limit = int(params[4]) if params[4].isdigit() else params[4]
                self.wfile.write(json.dumps(self.model.get_folder_sorted(userID, root_folder, sub_folder_limit), indent=4, sort_keys=True).encode('utf-8'))
            except Exception as err:
                self.wfile.write(str(err).encode("utf-8"))
        if(self.path.startswith('/newest-folder')):
            self.send_response(200)
            self.end_headers()
            try:
                self.wfile.write(self.model.get_newest().encode('utf-8'))
            except Exception as err:
                self.wfile.write(str(err).encode("utf-8"))

        return


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    handler_class.initialize_model(handler_class)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()