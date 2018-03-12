# File Server From Scratch

- `socket` version
- `http.server` version

## Inspiration
- [AOSA: A Simple Server](http://aosabook.org/en/500L/a-simple-web-server.html)
- [WEB APPLICATION FROM SCRATCH, PART I](https://defn.io/2018/02/25/web-app-from-scratch-01/)
- [Repo: A web app from scratch](https://github.com/Bogdanp/web-app-from-scratch/tree/part-01)
- [Python Network Programming](https://www.tutorialspoint.com/python/python_networking.htm)

## References
- [Node: Anatomy of an HTTP Transaction](https://nodejs.org/en/docs/guides/anatomy-of-an-http-transaction/)
- [Python Socket Programming HOWTO](https://docs.python.org/3.6/howto/sockets.html)
- [Python `socketserver` module](https://docs.python.org/3/library/socketserver.html#module-socketserver)
- [Python `http.server` module](https://docs.python.org/3.6/library/http.server.html#module-http.server)
- [Python `ssl` (Secure Sockets Layer) module](https://docs.python.org/3/library/ssl.html#module-ssl)
- [Unix socket tutorial](https://www.tutorialspoint.com/unix_sockets/index.htm)
- [unix domain socket - AF_INET vs AF_UNIX](https://stackoverflow.com/questions/21032562/example-to-explain-unix-domain-socket-af-inet-vs-af-unix)
- [Buffer definition](http://www.linfo.org/buffer.html)
- [Python Buffer Protocol](https://docs.python.org/3/c-api/buffer.html#bufferobjects)

### Notes
- `memoryview`: show memory location
```python
>>> v = memoryview(b'abcd')
>>> v
<memory at 0x1029efa08>
>>>
```
- **Socket**
	- Allows communication between two different processes on the same or different machines. It's a way to talk to other computers using standard Unix file descriptors.
- **File descriptor**
	- An integer associated with an open file; it can be a network connection, a text file, a terminal, or something else.
- **`SOL_SOCKET`**
	- "Socket option level = socket." 
	- When this is chosen, the socket itself will be searched. Use this constant as the level argument to `getsockopt` or `setsockopt` to manipulate the socket-level options.
	- [GNU C Library docs](http://www.delorie.com/gnu/docs/glibc/libc_352.html)
	- [Stackoverflow](https://stackoverflow.com/questions/21515946/sol-socket-in-getsockopt)
- **`SO_REUSEADDR`**
	- Indicates that the rules used in validating addresses supplied in a `bind` call should allow reuse of local addresses. For `AF_INET` sockets this means that a socket may bind, except when there is an active listening socket bound to the address.
	- [Linux man pages](http://man7.org/linux/man-pages/man7/socket.7.html)
	- [The Single UNIX Specification](http://pubs.opengroup.org/onlinepubs/7908799/xns/getsockopt.html)
	- [What exactly does SO_REUSEADDR do?](http://www.unixguide.net/network/socketfaq/4.5.shtml)
- [**`with` statement**](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
	- The with statement is used to wrap the execution of a block with methods defined by a context manager.
	- Used when working with unmanaged resources (like file streams).
	- It allows you to ensure that a resource is "cleaned up" when the code that uses it finishes running, even if exceptions are thrown.
	- [Stackoverflow](https://stackoverflow.com/questions/1369526/what-is-the-python-keyword-with-used-for)
- [**`typing` library**](https://docs.python.org/3/library/typing.html)
- [**Generators**](https://wiki.python.org/moin/Generators)
	- [*class* `typing.Generator(Iterator[T_co], Generic[T_co, T_contra, V_co])`](https://docs.python.org/3/library/typing.html#typing.Generator)
	- A generator can be annotated by the generic type `Generator[YieldType, SendType, ReturnType]`. 
	- [Jeff Knupp - Improve Your Python: 'yield' and Generators Explained](https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/)
	- [freeCodeCamp: How — and why — you should use Python Generators](https://medium.freecodecamp.org/how-and-why-you-should-use-python-generators-f6fb56650888)
	- [Stack Abuse: Python Generators](http://stackabuse.com/python-generators/)
- [**Function annotations**](https://docs.python.org/3/tutorial/controlflow.html#function-annotations)
	- [Stackoverflow](https://stackoverflow.com/questions/14379753/what-does-mean-in-python-function-definitions)
	- [PEP 3107 specification](https://www.python.org/dev/peps/pep-3107/)
	- Completely optional metadata information about the types used by user-defined functions.
	- Annotations are stored in the `__annotations__` attribute of the function as a dictionary and have no effect on any other part of the function.
	- `def iter_lines(sock: socket.socket, bufsize: int = 16_834) -> typing.Generator[bytes, None, bytes]:`
	- Parameter annotations are defined by a colon after the parameter name, followed by an expression evaluating to the value of the annotation: `def iter_lines(sock: socket.socket, bufsize: int = 16_834)`
	- Return annotations are defined by a literal `->`, followed by an expression, between the parameter list and the colon denoting the end of the def statement: `-> typing.Generator[bytes, None, bytes]:`
- **`bytes.index()`**
	- Search in byte string
	- [Stackoverflow](https://stackoverflow.com/questions/10923602/python-3-bytes-index-better-way)
- [**`collections.namedtuple()`**](https://docs.python.org/3/library/collections.html#collections.namedtuple)
	- factory function for creating tuple subclasses with named fields
	- Returns a new tuple subclass named typename. The new subclass is used to create tuple-like objects that have fields accessible by attribute lookup as well as being indexable and iterable.
- [**`typing.NamedTuple()`**](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
	- typed version of `namedtuple`
- [**`typing.Mapping()`**](https://docs.python.org/3/glossary.html#term-mapping)
	- A generic version of `collections.abc.Mapping`, supporting arbitrary key lookups.
- [**`@classmethod`**](https://docs.python.org/3/library/functions.html#classmethod)
	- [Stack Abuse](http://stackabuse.com/pythons-classmethod-and-staticmethod-explained/)
	- [Stackoverflow](https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner)
	- a decorator that transforms a method into a class method
	- [decorator](https://docs.python.org/3/glossary.html#term-decorator) = a function returning another function, usually applied as a function transformation using the `@wrapper` syntax.
- [**`next()`**](https://docs.python.org/3/library/functions.html#next)
- **`f"Malformed request line '{request_line!r}'."`**
	- `!r` computes the “official” string representation of an object.
	- [Stackoverflow](https://stackoverflow.com/questions/38418070/what-does-r-do-in-str-and-repr)
	- [`repr()`](https://docs.python.org/3/library/functions.html#repr)
	- [`object.__repr__(self)`](https://docs.python.org/3/reference/datamodel.html#object.__repr__)
- [**`str.partition(sep)`**](https://docs.python.org/3/library/stdtypes.html#str.partition)
	- Split the string at the first occurrence of _sep_, and return a 3-tuple containing the part before the separator, the separator itself, and the part after the separator. If the separator is not found, return a 3-tuple containing the string itself, followed by two empty strings.
- [**`str.lstrip([chars])`**](https://docs.python.org/3/library/stdtypes.html#str.lstrip)
	- Return a copy of the string with leading characters removed. The chars argument is a string specifying the set of characters to be removed. If omitted or None, the chars argument defaults to removing whitespace. The chars argument is not a prefix; rather, all combinations of its values are stripped.
- [**`fileno()`**](https://docs.python.org/3.6/library/io.html#io.IOBase.fileno)
	- Return the underlying file descriptor (an integer) of the stream if it exists.
	- An OSError is raised if the IO object does not use a file descriptor.
- [**`mimetypes.guess_type(url, strict=True)`**](https://docs.python.org/3.6/library/mimetypes.html#mimetypes.guess_type)	- Guess the type of a file based on its filename or URL, given by url.
- [**`os.fstat()`**](https://docs.python.org/3/library/os.html#os.fstat)
	- Get the status of the file descriptor fd. Return a `stat_result` object.

