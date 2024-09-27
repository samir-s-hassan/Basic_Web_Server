import socket
import os

# Server settings: localhost and port 8080
HOST = '127.0.0.1'
PORT = 8080

# Directory to serve files from
STATIC_DIR = './static'

# Handles client requests
def handle_request(client_socket):
    try:
        # Receive and decode the request
        request = client_socket.recv(1024).decode('utf-8')
        headers = request.splitlines()

        # Log the request method and URL
        if len(headers) > 0:
            print(f"Request: {headers[0]}")

        # Parse the request line
        method, url, _ = headers[0].split()
        
        if method == 'GET':
            # Determine the file to serve (index.html for root)
            file_path = STATIC_DIR + (url if url != '/' else '/index.html')
            
            # Serve the file if it exists, otherwise return 404
            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    response_body = file.read()
                    response_headers = 'HTTP/1.1 200 OK\r\n'
                    response_headers += f'Content-Length: {len(response_body)}\r\n'
                    response_headers += 'Content-Type: text/html\r\n\r\n'
            else:
                response_body = b'<html><body><h1>404 Not Found</h1></body></html>'
                response_headers = 'HTTP/1.1 404 Not Found\r\n'
                response_headers += 'Content-Type: text/html\r\n\r\n'
            
            # Send the response
            client_socket.send(response_headers.encode('utf-8') + response_body)
        
        else:
            # Handle unsupported methods (e.g., POST)
            response_body = b'<html><body><h1>405 Method Not Allowed</h1></body></html>'
            response_headers = 'HTTP/1.1 405 Method Not Allowed\r\n'
            response_headers += 'Content-Type: text/html\r\n\r\n'
            client_socket.send(response_headers.encode('utf-8') + response_body)
    
    except Exception as e:
        # Print any errors that occur
        print(f"Error: {e}")
    
    finally:
        # Close the connection
        client_socket.close()

# Starts the server and listens for connections
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind to the host and port, and start listening
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Serving on port {PORT}...")

        # Main loop to accept and handle client connections
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_request(client_socket)

# Run the server
if __name__ == "__main__":
    start_server()
