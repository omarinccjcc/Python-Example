import cgi
import os
from google.appengine.api import users
import webapp2
import jinja2

# MAIN_PAGE_HTML = """\
# <html>
# <body>
# <form action="/sign" method="post">
# <div><textarea name='content' rows="3" cols="60"></textarea></div>
# <div><input type="submit" value="Enviar"></div>
# </form>
# </body>
# </html>
# """
 
JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname (__file__) ),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
        # self.response.write(MAIN_PAGE_HTML)
 
class Registro(webapp2.RequestHandler):
    def post(self):
        ctx = {'nombre': self.request.get('content'),
        'direccion': 'Clinica Americana'
        }

        template = JINJA_ENVIRONMENT.get_template('mensaje.html')
        self.response.write(template.render(ctx))
 
		# self.response.write('<html><body>Tu escribiste: <pre>')
		# self.response.write(cgi.escape(self.request.get('content')))
		# self.response.write('</pre></body></html>')

 
application = webapp2.WSGIApplication(
[
    ('/',MainPage),
    ('/sign',Registro),],
    debug=True
)