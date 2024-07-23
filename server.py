# Jessica D

# import socket module
from socket import *

# Datetime object to get the time
from datetime import datetime

# Import threading to create multithreading capabilities.
import threading

# In order to terminate the program
import sys

# Create a list to store the threads to join later.
threads = []


# A function to craft responses so that it is easier to edit if we are using more response types.
def createResponse(responseNum=500, length=0):
    length = length

    # 200 is first as we generally expect to successfully get the file.
    if responseNum == 200:
        responseHeader = "HTTP/1.1 200 OK \r\n"
        responseBody = ""

    # 404 for file not found.
    elif responseNum == 404:
        responseHeader = "HTTP/1.1 404 Not Found\r\n"
        responseBody = ("<!DOCTYPE html>\r\n<html>\r\n<h1>404 NOT FOUND</h1>\r\n" 
                       "<p>The file you are looking for cannot be found or does not exist. Please try again.</p>\r\n</html>\r\n")
        length = len(responseBody.encode())

    # Defaulting to 500 Internal Server Error as I was initially receiving many different server errors.
    # As it is a small program, we do not yet need to prepare for a larger set of errors.
    else:
        responseHeader = "HTTP/1.1 500 Internal Server Error\r\n"
        responseBody = ("<!DOCTYPE html>\r\n<html>\r\n<h1>500 INTERNAL SERVER ERROR</h1>\r\n\r\n" 
                        "<p>There has been an unexpected problem with the server. Please try again. </p>\r\n</html>\r\n")
        length = len(responseBody.encode())

    # Retrieve the current date and time
    now = datetime.now()

    # Format all addition header fields, ensuring there is a blank line after.
    additionalHeader = (f"Content-Date: {now.strftime('%c')}\r\n"
                        f"Server: Jessica D TCP Server\r\n"
                       f"Content-Length: {length}\r\n"
                       f"Content-Type: text/html\r\n"
                       f"\r\n")

    return responseHeader + additionalHeader + responseBody


# Function to handle the client requests.
def handle_client(connectionSocket, addr):
    try:
        while True:
            message = connectionSocket.recv(1024).decode()

            # Only continue with operations if a valid message was received.
            if len(message) > 0:
                filename = message.split()[1]

                try:
                    f = open(filename[1:])
                    outputdata = f.read()
                    f.close()

                    length = len(outputdata)


                    # The original code looping through the content was replaced with single send all,
                    # as the client was not receiving the complete response.
                    connectionSocket.sendall((createResponse(200, length) + outputdata + "\r\n\r\n").encode())

                # If the file cannot be found, catch with an IOError, and send the corresponding response.
                except IOError:
                    connectionSocket.sendall(createResponse(404).encode())

    # Catch the error sent when the client closes or resets the connection
    # Print a corresponding message.
    except ConnectionResetError:
        print("Connection was reset by the client.\r\n\r\n")

    # Generic catch all for all remaining errors.
    except Exception as e:
        # Send a default 500 error response.
        connectionSocket.sendall(createResponse().encode())

        # Pass so that this does not break and stop the server.
        # In the real world it would be better to check specifically for each error.
        pass


# Function to connect and manage threads.
def run_server():
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a sever socket
    hostIP = gethostbyname(gethostname())
    serverPort = 8080

    try:
        serverSocket.bind((hostIP, serverPort))
        serverSocket.listen(1)

        while True:
            print('Ready to serve...')
            print("Listening at " + str(hostIP) + ":" + (str(serverPort)))

            # Establish the connection
            connectionSocket, addr = serverSocket.accept()

            # Creating a new thread
            thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))

            # Starting the thread
            thread.start()

            # Append to a list of current threads
            threads.append(thread)

    # Catch any errors where the server could not start.
    # Often happens when closing the server would not properly free up the port.
    except IOError:
        print("Error starting the server. Please restart.")

    # After everything above is done, we call thread.join
    # Ensures the threads are done before moving on and exiting.
    finally:
        for thread in threads:
            thread.join()
        serverSocket.close()
        sys.exit()


# Main function for running to server.
if __name__ == '__main__':
    run_server()
