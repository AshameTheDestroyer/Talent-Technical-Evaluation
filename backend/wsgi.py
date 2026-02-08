from main import app
from asgiref.wsgi import WsgiToAsgi

application = WsgiToAsgi(app)
