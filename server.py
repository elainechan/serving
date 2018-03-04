import socket
import typing

HOST = "127.0.0.1"
PORT = 9000

RESPONSE = b"""\
HTTP/1.1 200 OK
Content-type: text/html
Content-length: 15
<h1>Hello!</h1>""".replace(b"\n", b"\r\n")

"""
Request Parser
"""
# socket.accept() returns (conn, address)
# This function accepts conn as argument
def iter_lines(sock: socket.socket, bufsize: int = 16_834) -> typing.Generator[bytes, None, bytes]:
	# ?????? what's up with the argument
	buff = b""
	while True:
		data = sock.recv(bufsize)
		if not data:
			return b"" # Return empty byte if no data is received from socket
		buff += data
		while True:
			try:
				i = buff.index(b"\r\n") # Search locations of carriage returns and line feeds
				line, buff = buff[:i], buff[i + 2:] # Determine current line and buffer data content
				if not line:
					return buff # Return buffer data if line is empty
				yield line
			except IndexError:
				break

"""
Simple Server
The `socket` module provides access to the BSD socket interface. 
The `socket()` function returns a socket object whose methods implement the various socket system calls. 
"""
# Create TCP socket
with socket.socket() as server_sock:
	# Sets the socket option to reuse the address to 1 even if port is busy (in TIME_WAIT state).
	# Passes SOL_SOCKET ("Socket option level = socket") and the value we want it set to.
	server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Tells the socket what address to bind to.
	server_sock.bind((HOST, PORT))
	# 0 is the number of pending connections the socket may have before new connections are refused.
	# Since this server is going to process one connection at a time,
	# we want to refuse any additional connections.
	server_sock.listen(0)
	print(f"Listening on {HOST}:{PORT}...")
	# If you try to run this code now, it’ll print to standard out that it’s listening on 127.0.0.1:9000 and then exit. 
	# In order to actually process incoming connections, we need to call the accept method on our socket. 
	# Doing so will block the process until a client connects to our server.
	client_sock, client_addr = server_sock.accept()
	print(f"New connection from {client_addr}.")
	with client_sock: # ??????? what's the difference between using and not using with statement
		for line in iter_lines(client_sock):
			print(line) # Print out requests line by line
		client_sock.sendall(RESPONSE)