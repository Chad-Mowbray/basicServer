 # https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/

 # add threading for multiple requests
 # add SQL server for vulnerabilities

import socket
import os
from shutil import copyfile


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
            print("Connected to by", addr)
            data = conn.recv(1024)

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

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
            b'Request received!' # response body
        )

        data_list = data.split()
        if data_list[0] == b"GET":
            return self.handle_get()
        elif data_list[0] == b"POST":
            return self.handle_post(data)
        else:
            return b"".join(response)


    def handle_get(self):
        with open("index.html", "rb") as file:
            page = file.read(4096)
            page_plus_headers =  self.default_header + page
            return page_plus_headers
    
    def handle_post(self, request):
    
        user_input = request.decode('utf-8').split('\n')[-1][6:]

        copyfile("post.html", "post_mod.html")

        with open("post_mod.html", "a") as addition:
            addition.write(f"<h2>{user_input}</h2>")
            addition.write("</body>\n</html>")

        with open("post_mod.html", "rb") as file:
            page = file.read(4096)
            page_plus_headers =  self.default_header + page
            return page_plus_headers
      
        return b'Some kind of error'






if __name__ == '__main__':
    server = HTTPServer()
    server.start()
