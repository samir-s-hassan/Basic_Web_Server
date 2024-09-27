import mimetypes #This is to find the content type of the file
import socket
import os

# Server settings: localhost and port 8080
HOST = '127.0.0.1'
PORT = 8080

# Directory to serve files from
STATIC_DIR = './static'

# Handles the client requests
def handle_request(client_socket):
    try:
        # Receive and decode the request
        request = client_socket.recv(1024).decode('utf-8')
        headers = request.splitlines()

        # Log the request method and URL which are present in headers[0]
        if len(headers) > 0:
            print(f"Request: {headers[0]}")

        # Parse the request line
        method, url, _ = headers[0].split() #Headers[0] here
        status_code = ''
        content_type = ''

        if method == 'GET':
            # Determine the file to serve (index.html for root)
            file_path = STATIC_DIR + (url if url != '/' else '/index.html')
            
            # Serve the file if it exists, otherwise return 404
            if os.path.exists(file_path):
                # Get the MIME type based on the file extension
                content_type, _ = mimetypes.guess_type(file_path)
                
                # Default to text/html if no MIME type is found
                if content_type is None:
                    content_type = 'text/html'
                
                with open(file_path, 'rb') as file:
                    response_body = file.read()
                    response_headers = 'HTTP/1.1 200 OK\r\n'
                    response_headers += f'Content-Length: {len(response_body)}\r\n'
                    response_headers += f'Content-Type: {content_type}\r\n\r\n'
                    status_code = '200 OK'
            else:
                # Set content type explicitly for 404 response
                response_body = b'<html><body><h1>404 Not Found</h1></body></html>'
                response_headers = 'HTTP/1.1 404 Not Found\r\n'
                # Explicitly set content type for 404 page because if the file path doesn't exist, we never looked for it 
                content_type = 'text/html'  
                response_headers += f'Content-Type: {content_type}\r\n\r\n'
                status_code = '404 Not Found'
            
            # Send the response
            client_socket.send(response_headers.encode('utf-8') + response_body)
        
        else:
            # Handle unsupported methods (e.g., POST)
            response_body = b'<html><body><h1>405 Method Not Allowed</h1></body></html>'
            response_headers = 'HTTP/1.1 405 Method Not Allowed\r\n'
            content_type = 'text/html'
            response_headers += f'Content-Type: {content_type}\r\n\r\n'
            status_code = '405 Method Not Allowed'
            client_socket.send(response_headers.encode('utf-8') + response_body)
    
        # Log the request method, URL, response status, and content type
        print(f"Method: {method}, URL: {url}, Status: {status_code}, Content-Type: {content_type}")
    
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
            print(f"---------------------------------------------------------")
            print(f"Connection from {addr}")
            handle_request(client_socket)

# Run the server
if __name__ == "__main__":
    start_server()
