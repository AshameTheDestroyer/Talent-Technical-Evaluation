from main import app
from asgiref.wsgi import AsgiToWsgi

application = AsgiToWsgi(app)
