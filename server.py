import mimetypes #imported this to find the file's content type
import socket
import os

#these are all our server settings
HOST = '127.0.0.1'
PORT = 8080
TIMEOUT = 10 #how long in seconds before the server will timeout
STATIC_DIR = './static' #what directory will we serve files from

#the function to handle client requests
def handle_request(client_socket):
    try:
        #set the timeout for the client socket here
        client_socket.settimeout(TIMEOUT)
        #receive and decode the request
        request = client_socket.recv(1024).decode('utf-8')
        #split the headers so we can work with them
        headers = request.splitlines()
        #log the request method and url which are both in headers[0]
        if len(headers) > 0:
            print(f"Request: {headers[0]}")
        #parse the headers[0] to get this info and we'll use status_code and content_type later
        method, url, _ = headers[0].split()
        status_code = ''
        content_type = ''

        if method == 'GET':
            #determine what file to serve. if /, then index.html
            file_path = STATIC_DIR + (url if url != '/' else '/index.html')
            #if the file exists, guess its type and then update content_type
            if os.path.exists(file_path):
                content_type, _ = mimetypes.guess_type(file_path)
                content_type = content_type or 'text/html'
                #open the file and read it, status should be OK
                with open(file_path, 'rb') as file:
                    response_body = file.read()
                    response_headers = (
                        'HTTP/1.1 200 OK\r\n'
                        f'Content-Length: {len(response_body)}\r\n'
                        f'Content-Type: {content_type}\r\n\r\n'
                    )
                    status_code = '200 OK'
            else:
                #we couldn't find a file for it so serve 404 (or we intentionally went to 404.html)
                error_404_page = STATIC_DIR + '/404.html'
                if os.path.exists(error_404_page):
                    with open(error_404_page, 'rb') as file:
                        response_body = file.read()
                        content_type = 'text/html'
                else:
                    #fallback for if the 404 file itself isn't found, we'll directly display this in the body
                    response_body = b'<html><body><h1>404 Not Found</h1></body></html>'
                    content_type = 'text/html'

                response_headers = (
                    'HTTP/1.1 404 Not Found\r\n'
                    f'Content-Type: {content_type}\r\n\r\n'
                )
                status_code = '404 Not Found'
            #send the response back
            client_socket.send(response_headers.encode('utf-8') + response_body)

        else:
            #if we get a request other then GET
            response_body = b'<html><body><h1>405 Method Not Allowed</h1></body></html>'
            response_headers = (
                'HTTP/1.1 405 Method Not Allowed\r\n'
                f'Content-Type: text/html\r\n\r\n'
            )
            status_code = '405 Method Not Allowed'
            #send the response back
            client_socket.send(response_headers.encode('utf-8') + response_body)
        #print all the necessary info
        print(f"Method: {method}, URL: {url}, Status: {status_code}, Content-Type: {content_type}")
    #remember to check for exceptions: in this case, it's a timeout
    except socket.timeout:
        print(f"Connection timed out for client {client_socket.getpeername()}")
        client_socket.send(b'HTTP/1.1 408 Request Timeout\r\n\r\n')
    #print the other errors if it's not a socket.timeout error
    except Exception as e:
        print(f"Error: {e}")
    #close the socket
    finally:
        client_socket.close()

#the function that has start server logic
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

#server will auto-start because of this
if __name__ == "__main__":
    start_server()
