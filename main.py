import socket
import os
from shutil import copyfile
import json
from urllib.parse import unquote_plus

from database import initialize_database as database


class Server:

    def __init__(self, host='127.0.0.1', port=2222):
        self.host = host
        self.port = port
        self.basic_header = b'HTTP/1.1 200 OK\r\n\r\n' 
        self.max = 65536

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen()
        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            ip_addr, port = addr
            print(f"A computer on IP address {ip_addr} and Port {port} is connected to the server")
            data = conn.recv(self.max)
            response = self.handle_request(data)
            conn.sendall(response)
            conn.close()

    def handle_request(self, data):
        try:
            data_split = data.decode('utf-8').split('\n')
            method = data_split[0].split()[0]
            uri = data_split[0].split()[1]

            if uri == '/':
                base_folder = "webserver/fakesociety/"
                base_file = "index.html"
                if method == "GET":
                    return self.handle_get(base_folder, base_file)
                elif method == "POST":
                    return self.handle_post(data, base_folder, base_file)
            else:
                return self.handle_error()
        except:
            return self.handle_error()

    def handle_error(self):
        with open("webserver/error/error.html", "rb") as file:
            page = file.read(self.max)
            page_plus_headers = self.basic_header + page
            return page_plus_headers

    def handle_get(self, base_folder, base_file):
        try:
            base_path = base_folder + base_file
            mod_path = base_folder + "copy_" + base_file
            copyfile(base_path, mod_path)
            db_request = database.Modify_Database()
            res = db_request.request_posts("posts")

            with open(mod_path, "a") as addition:
                addition.write(unquote_plus(res))
                addition.write("</body>\n</html>")

            with open(mod_path, "rb") as file:
                page = file.read(self.max)
                page_plus_headers =  self.basic_header + page
                return page_plus_headers
        except:
            return self.handle_error()

    def handle_post(self, request, base_folder, base_file):
        try:
            user_input = request.decode('utf-8').split('\n')[-1]
            processed_user_input = [content.split("&") for content in user_input.split("=")]
            processed_user_input.pop(0)
            user_input_obj = {
                "username": unquote_plus(processed_user_input[0][0]),
                "password": unquote_plus(processed_user_input[1][0]),
                "title": unquote_plus(processed_user_input[2][0]),
                "post": unquote_plus(processed_user_input[3][0])
            }
            x = database.Modify_Database()
            x.create_user_add_post(user_input_obj)
            return self.handle_get(base_folder, base_file)
        except:
            return self.handle_error()


if __name__ == '__main__':
    server = Server()
    server.start()
