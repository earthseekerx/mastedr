from flask import Flask, request
import socket
import threading
import tkinter as tk
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

app = Flask(__name__)

def handle_client(client_socket, client_address):
    try:
        print("Connection from:", client_address)

        # Generate a new symmetric key for each data packet
        symmetric_key = get_random_bytes(16)  # 16 bytes for AES-128

        # Load user's public key (replace with actual public key loading)
        user_public_key = RSA.import_key(open('user_public.pem').read())

        # Encrypt the symmetric key with the user's public key
        cipher_rsa = PKCS1_OAEP.new(user_public_key)
        encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)

        # Send the encrypted symmetric key and data packet to the user
        client_socket.sendall(encrypted_symmetric_key)

        # Receive data from the client
        data = client_socket.recv(1024)
        print("Received data:", data.decode())

        # Decrypt the symmetric key using the user's private key
        # Load user's private key (replace with actual private key loading)
        user_private_key = RSA.import_key(open('user_private.pem').read())
        cipher_rsa = PKCS1_OAEP.new(user_private_key)
        decrypted_symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)

        # Use the symmetric key to encrypt and decrypt the data packet
        cipher_aes = AES.new(decrypted_symmetric_key, AES.MODE_EAX)
        encrypted_data = cipher_aes.encrypt(data)
        decrypted_data = cipher_aes.decrypt(encrypted_data)

        print("Decrypted data:", decrypted_data.decode())

        # Send the encrypted data back to the client
        client_socket.sendall(encrypted_data)

    finally:
        # Close the connection
        client_socket.close()

def connect():
    # Connect to the server
    server_address = ('localhost', 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # Handle the client connection
    handle_client(client_socket, server_address)

def stop_connection():
    print("Stopping connection...")

def reload_connection():
    print("Reloading connection...")

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    print("Generated key pair")

def close_application():
    print("Closing application...")
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Simple Frontend")

# Create buttons for actions
connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.pack()

stop_button = tk.Button(root, text="Stop Connection", command=stop_connection)
stop_button.pack()

reload_button = tk.Button(root, text="Reload Connection", command=reload_connection)
reload_button.pack()

generate_key_button = tk.Button(root, text="Generate Key Pair", command=generate_key_pair)
generate_key_button.pack()

close_button = tk.Button(root, text="Close Application", command=close_application)
close_button.pack()

# Start the main event loop
root.mainloop()
def networked_data_relay():
    # Create a TCP socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the port number for the "http" service
    port = socket.getservbyname("http")

    # Define the server address and TCP port
    server_address = ('localhost', port)

    # Bind the socket to the address
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)

    print("Server is listening on TCP port", port, "...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()

        # Handle the client connection in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Call the function to start the server
networked_data_relay()

# Call the function to start the server
networked_data_relay()
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
