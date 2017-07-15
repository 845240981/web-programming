
URL_PAYHROUTES=[
    ('hi/','say_hi'),
    ('hello/','say_hello')

                ]


class flameworkapp (object):


     def _pipei(self,path):
         for url , app in URL_PAYHROUTES:
             if path == url:
                 return app

     def __call__(self, env, start_response):

         path= env.get('path_info','/')
         app = self._pipei(path)
         if app:
             app = globals()[app]
             return app(env,start_response)
         else:
             start_response("404 NOT FOUND", [('Content-type', 'text/plain')])
             return ["Page dose not exists!"]


def say_hi(environ, start_response):
    start_response("200 OK",[('Content-type', 'text/html')])
    return ["hi  , you!"]

def say_hello(environ, start_response):
    start_response("200 OK",[('Content-type', 'text/html')])
    return ["hello , you!"]

app = flameworkapp()