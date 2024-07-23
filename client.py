# Jessica D

# import socket module
from socket import *

# import argparse module for command line processing
import argparse

def main():
    # Parser for command line argument
    parser = argparse.ArgumentParser("Client")
    parser.add_argument("server_host")
    # Set input type to int to ensure proper processing
    parser.add_argument("server_port", type=int)
    parser.add_argument("filename")
    args = parser.parse_args()

    # TCP server destination IP
    serverIP = args.server_host

    # TCP server destination port
    serverPort = args.server_port

    # Filename
    filename = args.filename

    # Keep the client running until the user chooses to close it.
    while True:

        # Create a new socket each time we re-loop
        # Otherwise it throws an error
        clientSocket = socket(AF_INET, SOCK_STREAM)

        # Set option to
        clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        clientSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)

        clientSocket.connect((serverIP, serverPort))

        # Keep the request loop open until the user chooses to exit.
        while True:
            # Formatting the GET request.
            request = f"GET /{filename} HTTP/1.1\r\nHost: {serverIP}:{serverPort}\r\n\r\n"

            # Send the request to the server
            clientSocket.send(request.encode())

            # Retrieving the response from the server
            message = clientSocket.recv(1024).decode()

            # Print out the response for the command line
            print(message)

            # Input for the user to request another file.
            close_option = input("Do want to request another file? y / n: ")
            if close_option.lower() == "n":
                # Break out of this loop, which will also automatically close the connection below.
                break

            else:
                filename = input("Please enter another file name: ")

        # Response to let the user know it is closing.
        print("Closing connection... \r\n")
        clientSocket.close()
        break

    clientSocket.close()


if __name__ == "__main__":
    main()