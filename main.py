 # https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/

 # add threading for multiple requests
 # add SQL server for vulnerabilities

import socket


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
        """Handles incoming data and returns a response.
        Override this in subclass.
        """

        # print("*" * 50)
        # print(data)
        return data





class HTTPServer(TCPServer):
    def handle_request(self, data):
        # return b"Request received!"
        response = (
            b'HTTP/1.1 200 OK\r\n', # response line
            b'\r\n', # blank line
            b'Request received!' # response body
        )

        print("*" * 50)
        print(data)
        data_list = data.split()
        print(data_list[0])
        if data_list[0] == b"GET":
            return self.handle_get()
        elif data_list[0] == b"POST":
            return self.handle_post()
        else:
            return b"".join(response)


    def handle_get(self):
        return b"You made a get request"
    
    def handle_post(self):
        return b"You made a post request"






if __name__ == '__main__':
    server = HTTPServer()
    server.start()
