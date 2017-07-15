import socket
import sys
from io import StringIO


class WGGIserver(object):

    address_family =socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size =1

    def __init__(self,server_address):
        self.listen_socket =listen_socket =socket.socket(self.address_family , self.socket_type)
        listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        listen_socket.bind(server_address)
        listen_socket.listen(self.request_queue_size)
        host,port =listen_socket.getsockname()
        self.server_ip =socket.getfqdn(host)
        self.server_port =port
        self.headers_set=[]
    def set_app(self,application):
        self.application = application

    def serve_forever(self):
        listen_socket=self.listen_socket
        while True:
            self.client_connection,client_address=listen_socket.accept()
            self.hand_one_request()

    def hand_one_request(self):
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data.decode('utf-8')
        for line in request_data.split():
            print(''.join('< {line}\n').format(line=line))
        self.parse_request(request_data)
        env = self.get_environ()

        result = self.application(env,self.start_response)

        self.finish_reponse(result)

    def parse_request(self,text):
        request_line = text.split()
        self.request_method,  self.path,   self.request_version = request_line


    def get_environ(self):
        env={}
        env['wsgi.version'] = (1.0)
        env['wsgi.url_scheme']='http'
        env['wsgi.input']=StringIO(self.request_data)
        env['wsgi.errors']=sys.stderr
        env['wsgi.multithread']=False
        env['wsgi.multiprocess']=False

        env['request_method']=self.request_method
        env['path_info']=self.path
        env['server_name']=self.server_ip
        env['SERVER_PORT']=str(self.server_port)
        return env
    def start_response(status,response_headers,exc_info=False):
        server_headers = [
            ('Date','Tue, 31 Mar 2017 12.32 GMT'),
            ('Server','WSGIServer 0.2'),

            ]
        self.headers_set = [status,response_headers+server_headers]


    def finish_result(self,result):
        try:
            status,resonse_headers =self.headers_set
            response ='HTTP/1.1{status}\r\n'.format(status=status)
            for header in resonse_headers:
                response = response + '{0}:{1}\r\n'.format(header)
            response=response+'\r\n'
            for data in result:
                response=response+data
            for line in response.splitlines():
                print(line+'\n')
            self.client_connection.sendall(response)

        finally:
            self.client_connection.close()

SERVER_ADDRESS =(HOST, PORT) = '',8888

def make_server(server_address,application):
    sever =WGGIserver(server_address)
    sever.set_app(application)
    return sever

if __name__ =='__main__':
    if len(sys.argv)<2:
        sys.exit("please give me a application")
    app_path = sys.argv[1]
    module,application =app_path.split(':')
    module = __import__(module)
    application = getattr(module,application)
    httpd =make_server(SERVER_ADDRESS,application)
    print("WSGIserver:Serving HTTP on port {port}....\n".format(port=PORT))

