 # https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/

 # add threading for multiple requests
 # add SQL server for vulnerabilities

import socket
import os
from shutil import copyfile
import json


class TCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            ip_addr, port = addr
            print(f"A computer on IP address {ip_addr} and Port {port} is connected to the server")
            data = conn.recv(4096)
            
            response = self.handle_request(data)

            conn.sendall(response)
            # conn.close()

    def handle_request(self, data):
        # print("*" * 50)
        # print(data)
        return data


class HTTPServer(TCPServer):

    default_header = b'HTTP/1.1 200 OK\r\n\r\n' 

    def handle_request(self, data):
        response = (
            b'HTTP/1.1 200 OK\r\n', # response line
            b'\r\n', # blank line
        )

        data_split = data.decode('utf-8').split('\n')

        method = data_split[0].split()[0]
        uri = data_split[0].split()[1]

        print("uri: ", uri, method)
        if uri == '/fakesociety':
            if method == "GET":
                return self.handle_fakesociety_get()
            elif method == "POST":
                return self.handle_fakesociety_post(data)
            else:
                return self.handle_error()
        elif uri == '/':
            if method == "GET":
                return self.handle_get()
            elif method == "POST":
                return self.handle_post(data)
            else:
                return self.handle_error()
        else:
            return self.handle_error()



    def handle_error(self):
        pic_header = b'HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n'
        with open("error/error.html", "rb") as file:
            page = file.read(4096)
            page_plus_headers = pic_header + page
            return page_plus_headers

    def handle_get(self):
        with open("main/index.html", "rb") as file:
            page = file.read(4096)
            page_plus_headers =  self.default_header + page
            return page_plus_headers
    
    def handle_post(self, request):
    
        user_input = request.decode('utf-8').split('\n')[-1][6:]

        copyfile("main/post.html", "main/post_mod.html")

        with open("main/post_mod.html", "a") as addition:
            addition.write(f"<h2>{user_input}</h2>")
            addition.write("</body>\n</html>")

        with open("main/post_mod.html", "rb") as file:
            page = file.read(4096)
            page_plus_headers =  self.default_header + page
            return page_plus_headers
      
        return self.handle_error()




    def handle_fakesociety_get(self):
        with open("fakesociety/get_fakesociety.html", "rb") as file:
            page = file.read(4096)
            page_plus_headers =  self.default_header + page
            return page_plus_headers



    def handle_fakesociety_post(self, request):
        
        user_input = request.decode('utf-8').split('\n')[-1][6:]

        copyfile("fakesociety/post_fakesociety.html", "fakesociety/post_fakesociety_mod.html")

        with open("fakesociety/post_fakesociety_mod.html", "a") as addition:
            addition.write(f"<h2>{user_input}</h2>")
            addition.write("</body>\n</html>")

        with open("fakesociety/post_fakesociety_mod.html", "rb") as file:
            page = file.read(4096)
            page_plus_headers =  self.default_header + page
            return page_plus_headers
      
        return self.handle_error()







if __name__ == '__main__':
    server = HTTPServer()
    server.start()
