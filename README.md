#
## Python Client Server
![Screenshot](/assets/screenshot-1.png "Server Running")
### Socket Programming Web Server
Grade: 92.26

Tools: Python, PyCharm, VS Code

### Task
For this assignment we were tasked with developing a multithreaded web server that can:
- Handle multiple requests simutaneously. 
- Utilise one main thread to listen for TCP connection requests on a fixed port.
- After receiving a new TCP connection request, set up the connection on a seperate thread.


Additionally, we were to write a HTTP client to test the server. This should: 
- Connect to the server using a TCP connection.
- Send a HTTP request to the server.
- Display the server response as an output.
- Run the client using command line arguments in this format: `client.py server_host server_port filename`

 ### Learnings & Reflections:

 #### Issues restarting the server:
A large issue when developing this assignment would be being unable to restart the server after having stopped it in PyCharm or VS Code. Since I have had previous experience working with a live server,  I knew that it was likely an issue with the port and it's process not closing properly. 

To fix this, I could either restart my device or kill the process in terminal, being the more efficient option. Using the command `netstat -anon | findstr :8080`, I can search for the processes running on the specified port (`8080`) and the corresponding Process ID (`PID`). Once found, the `taskkill` command was used to terminate the process. 

![Terminating the processe](/assets/screenshot-2.png "Terminating the processes")
