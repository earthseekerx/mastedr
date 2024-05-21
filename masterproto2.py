import socket
import threading

def handle_client(client_socket, client_address):
    try:
        print("Connection from:", client_address)

        # Receive data from the client
        data = client_socket.recv(1024)
        print("Received data:", data.decode())

        # Relay the data back to the client
        client_socket.sendall(data)

    finally:
        # Close the connection
        client_socket.close()

def networked_data_relay():
    # Create a TCP socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and TCP port
    server_address = ('localhost', 12345)  # Use a non-privileged port

    # Bind the socket to the address
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)

    print("Server is listening on TCP port", server_address[1], "...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()

        # Handle the client connection in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Call the function to start the server
networked_data_relay()
