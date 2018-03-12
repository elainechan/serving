import os
import mimetypes
import socket
import typing

HOST = "127.0.0.1"
PORT = 9000

SERVER_ROOT = os.path.abspath("www")

FILE_RESPONSE_TEMPLATE = """\
HTTP/1.1 200 OK
Content-type: {content_type}
Content-length: {content_length}
""".replace("\n", "\r\n")

RESPONSE = b"""\
HTTP/1.1 200 OK
Content-type: text/html
Content-length: 15
<h1>Hello!</h1>""".replace(b"\n", b"\r\n")

BAD_REQUEST_RESPONSE = b"""\
HTTP/1.1 400 Bad Request
Content-type: text/plain
Content-length: 11

Bad-Request""".replace(b"\n", b"\r\n")

NOT_FOUND_RESPONSE = b"""\
HTTP/1.1 404 Not Found
Content-type: text/plain
Content-length: 9

Not Found""".replace(b"\n", b"\r\n")

METHOD_NOT_ALLOWED_RESPONSE = b"""\
HTTP/1.1 405 Method Not Allowed
Content-type: text/plain
Content-length: 17

Method Not Allowed""".replace(b"\n", b"\r\n")

"""
Request Parser
"""
# socket.accept() returns (conn, address)
# This function accepts conn as argument
def iter_lines(sock: socket.socket, bufsize: int = 16_834) -> typing.Generator[bytes, None, bytes]:
	"""Given a socket, read all the individual CRLF-separated lines
    and yield each one until an empty one is found.  Returns the
    remainder after the empty line.
    """
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
Request abstraction
"""
class Request(typing.NamedTuple):
	method: str
	path: str
	headers: typing.Mapping[str, str]

	@classmethod
	def from_socket(cls, sock: socket.socket) -> "Request":
		lines = iter_lines(sock)

		try:
			request_line = next(lines).decode("ascii")
		except StopIteration:
			raise ValueError("Request line missing.")
		try:
			method, path, _ = request_line.split(" ")
		except ValueError:
			raise ValueError(f"Malformed request line '{request_line!r}'.")

		headers = {}
		for line in lines:
			try:
				name, _, value = line.decode("ascii").partition(":")
				headers[name.lower()] = value.lstrip()
			except ValueError:
				raise ValueError(f"Malformed header line '{line!r}'.")
		return cls(method=method.upper(), path=path, headers=headers) # ???? what's going on here

"""
File Server
"""
def serve_file(sock: socket.socket, path: str) -> None:
	"""Given a socket and the relative path to a file (relative to
    SERVER_SOCK), send that file to the socket if it exists.  If the
    file doesn't exist, send a "404 Not Found" response.
    """
	if path == "/":
		path = "/index.html"
	abspath = os.path.normpath(os.path.join(SERVER_ROOT, path.lstrip("/")))
	if not abspath.startswith(SERVER_ROOT):
		sock.sendall(NOT_FOUND_RESPONSE)
		return
	
	try:
		with open(abspath, "rb") as f:
			stat = os.fstat(f.fileno())
			content_type, encoding = mimetypes.guess_type(abspath)
			if content_type is None:
				content_type = "application/octet-stream"
			if encoding is not None:
				content_type += f"; charset={encoding}"
			response_headers = FILE_RESPONSE_TEMPLATE.format(
				content_type=content_type,
				content_length=stat.st_size
				).encode("ascii")
			sock.sendall(response_headers)
			sock.sendfile(f)
	except FileNotFoundError:
		sock.sendall(NOT_FOUND_RESPONSE)
		return

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
	while True:
		client_sock, client_addr = server_sock.accept()
		print(f"Received connection from {client_addr}...")
		with client_sock: # ??????? what's the difference between using and not using with statement
			try:
				request = Request.from_socket(client_sock)
				print(request)
				if request.method != "GET":
					client_sock.sendall(METHOD_NOT_ALLOWED_RESPONSE)
					continue
				serve_file(client_sock, request.path)
			except Exception as e:
				print(f"Failed to parse request: {e}")
				client_sock.sendall(BAD_REQUEST_RESPONSE)