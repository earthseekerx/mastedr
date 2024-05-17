from Flask import Flask, request
import socket

app = Flask(__name__)

def networked_data_relay():
    # Create a TCP socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and TCP port (443 requires special permissions)
    server_address = ('localhost', 443)

    # Bind the socket to the address
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)

    print("Server is listening on TCP port 443...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()

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

@app.route('/relay', methods=['POST'])
def relay_data():
    data = request.get_data()
    # Here you can add your logic to relay the data to other nodes in the cluster
    # For demonstration purposes, we will just print the data
    print("Received data:", data)
    
    # Relay the data using the networked data relay function
    networked_data_relay()
    
    return "Data relayed successfully!"

if __name__ == '__main__':
    # Note: Running on port 443 may require special permissions
    app.run(host='0.0.0.0', port=443)