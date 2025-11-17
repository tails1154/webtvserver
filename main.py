import socket
import threading

# Server configuration
# NOTE: 192.168.0.124 is my local ip
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 1615       # Port to listen on

def handle_client(client_socket, client_address):
    """
    Handles communication with a connected client.
    """
    print(f"[*] Accepted connection from: {client_address[0]}:{client_address[1]}")
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                print(f"[*] Client {client_address[0]}:{client_address[1]} disconnected.")
                break

            print("Got data:")

            decoded_data = data.decode('utf-8')
            print(decoded_data)
            if decoded_data.startswith("GET wtv-1800:/preregister"):
               print(f"[*] Client {client_address[0]}:{client_address[1]} sent a request to wtv-1800:/preregister")
               print("[*] Sending back html file")
               with open("services/wtv-1800/preregister.html") as f:
                   data=f.read()
               response = "200 OK\r\nConnection: close\r\n" + data
               client_socket.sendall(response.encode('utf-8'))
               print("[*] Sent request")

    except Exception as e:
        print(f"[-] Error handling client {client_address[0]}:{client_address[1]}: {e}")
    finally:
        client_socket.close()

def start_server():
    """
    Starts the TCP server and listens for incoming connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow reusing the address
    server_socket.bind((HOST, PORT))
    server_socket.listen(5) # Max backlog of 5 pending connections

    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
