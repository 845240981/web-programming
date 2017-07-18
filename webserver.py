import socket

host,port ='',7000

listen_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listen_socket.bind((host, port))
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

listen_socket.listen(1)
print("Serving HTTP on port %s " % port)
while True:
    clien_connection ,client_address= listen_socket.accept()
    print(clien_connection)
    request = clien_connection.recv(1024)
    print(request.decode('utf-8'))
    http_response = b"""\
        HTTP/1.1 200 OK

        Hello, World!
        """

    clien_connection.sendall(http_response)


    clien_connection.close()
