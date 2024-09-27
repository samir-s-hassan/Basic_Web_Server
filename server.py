import mimetypes
import socket
import os

HOST = '127.0.0.1'
PORT = 8080
TIMEOUT = 10
STATIC_DIR = './static'

def handle_request(client_socket):
    try:
        client_socket.settimeout(TIMEOUT)
        request = client_socket.recv(1024).decode('utf-8')
        headers = request.splitlines()

        if len(headers) > 0:
            print(f"Request: {headers[0]}")

        method, url, _ = headers[0].split()
        status_code = ''
        content_type = ''

        if method == 'GET':
            file_path = STATIC_DIR + (url if url != '/' else '/index.html')

            if os.path.exists(file_path):
                content_type, _ = mimetypes.guess_type(file_path)
                content_type = content_type or 'text/html'

                with open(file_path, 'rb') as file:
                    response_body = file.read()
                    response_headers = (
                        'HTTP/1.1 200 OK\r\n'
                        f'Content-Length: {len(response_body)}\r\n'
                        f'Content-Type: {content_type}\r\n\r\n'
                    )
                    status_code = '200 OK'
            else:
                error_404_page = STATIC_DIR + '/404.html'
                if os.path.exists(error_404_page):
                    with open(error_404_page, 'rb') as file:
                        response_body = file.read()
                        content_type = 'text/html'
                else:
                    response_body = b'<html><body><h1>404 Not Found</h1></body></html>'
                    content_type = 'text/html'

                response_headers = (
                    'HTTP/1.1 404 Not Found\r\n'
                    f'Content-Type: {content_type}\r\n\r\n'
                )
                status_code = '404 Not Found'

            client_socket.send(response_headers.encode('utf-8') + response_body)

        else:
            response_body = b'<html><body><h1>405 Method Not Allowed</h1></body></html>'
            response_headers = (
                'HTTP/1.1 405 Method Not Allowed\r\n'
                f'Content-Type: text/html\r\n\r\n'
            )
            status_code = '405 Method Not Allowed'
            client_socket.send(response_headers.encode('utf-8') + response_body)

        print(f"Method: {method}, URL: {url}, Status: {status_code}, Content-Type: {content_type}")

    except socket.timeout:
        print(f"Connection timed out for client {client_socket.getpeername()}")
        client_socket.send(b'HTTP/1.1 408 Request Timeout\r\n\r\n')
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Serving on port {PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"---------------------------------------------------------")
            print(f"Connection from {addr}")
            handle_request(client_socket)

if __name__ == "__main__":
    start_server()
