#include <iostream>
#include <string>
#include <thread>
#include <vector>
#include <algorithm>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

void handle_client(int client_socket, const sockaddr_in& client_address) {
    try {
        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &client_address.sin_addr, client_ip, INET_ADDRSTRLEN);
        int client_port = ntohs(client_address.sin_port);
        std::cout << "Connection from: " << client_ip << ":" << client_port << std::endl;

        char buffer[1024];
        ssize_t bytes_received = recv(client_socket, buffer, sizeof(buffer), 0);
        if (bytes_received > 0) {
            std::string data(buffer, bytes_received);
            std::cout << "Received data: " << data << std::endl;

            ssize_t bytes_sent = send(client_socket, buffer, bytes_received, 0);
            if (bytes_sent != bytes_received) {
                std::cerr << "Error: Failed to send data back to client" << std::endl;
            }
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    close(client_socket);
}

void networked_data_relay() {
    int server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        std::cerr << "Error: Failed to create socket" << std::endl;
        return;
    }

    sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(12345);  // Use a non-privileged port

    if (bind(server_socket, (sockaddr*)&server_address, sizeof(server_address)) == -1) {
        std::cerr << "Error: Failed to bind socket" << std::endl;
        close(server_socket);
        return;
    }

    if (listen(server_socket, 5) == -1) {
        std::cerr << "Error: Failed to listen for incoming connections" << std::endl;
        close(server_socket);
        return;
    }

    std::cout << "Server is listening on TCP port " << ntohs(server_address.sin_port) << "..." << std::endl;

    while (true) {
        sockaddr_in client_address;
        socklen_t client_address_len = sizeof(client_address);
        int client_socket = accept(server_socket, (sockaddr*)&client_address, &client_address_len);
        if (client_socket == -1) {
            std::cerr << "Error: Failed to accept client connection" << std::endl;
            continue;
        }

        std::thread client_thread(handle_client, client_socket, client_address);
        client_thread.detach();
    }

    close(server_socket);
}