from wsgiref.simple_server import make_server
from pyramid.config import Configurator

if __name__ =='__main__':
  with Configurator() as config:
    config.include('pyramid_jinja2')
    config.add_static_view(name = 'static', path='static')
    config.add_route('home','/')
    config.add_route('output', '/output/{filename}')
    config.add_route('error', '/error/{error_type}')
    config.scan('views')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()