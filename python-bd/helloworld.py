import cgi
import os
import urllib


# for work with contacts of google
from google.appengine.api import users

# for work with data base of google
from google.appengine.ext import ndb

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

LIBRO_NOMBRE_DEFAULT = "Visita1"


def libro_key(libro_nombre=LIBRO_NOMBRE_DEFAULT):
    return ndb.Key('Libro',libro_nombre)


class MainPage(webapp2.RequestHandler):
    def get(self):


        libro_nombre= self.request.get('libro_nombre',LIBRO_NOMBRE_DEFAULT)

        mensajes_query = Mensaje.query(ancestor=libro_key(libro_nombre)).order(-Mensaje.fecha)

        mensajes = mensajes_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_link_text = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_link_text = 'Login'

        template_value = {
            'mensajes':mensajes,
            'libro_nombre':urllib.quote_plus(libro_nombre),
            'url':url,
            'url_link_text':url_link_text
        }


        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_value))
        # self.response.write(MAIN_PAGE_HTML)

    def post(self):
        libro_nombre = self.request.get('libro_nombre',
            LIBRO_NOMBRE_DEFAULT)
        mensaje = Mensaje(parent = libro_key(libro_nombre))

        if users.get_current_user():
            mensaje.autor = users.get_current_user()

        mensaje.contenido = self.request.get('contenido')

        mensaje.put()

        query_params = {'libro_nombre':libro_nombre}
        self.redirect('/?'+urllib.urlencode(query_params))



class Mensaje(ndb.Model):
    autor = ndb.UserProperty()
    contenido = ndb.StringProperty(indexed = False)
    fecha = ndb.DateTimeProperty(auto_now_add = True)


# class Registro(webapp2.RequestHandler):
#     def post(self):
#         ctx = {'nombre': self.request.get('content'),
#         'direccion': 'Clinica Americana'
#         }

#         template = JINJA_ENVIRONMENT.get_template('mensaje.html')
#         self.response.write(template.render(ctx))
 
# 		# self.response.write('<html><body>Tu escribiste: <pre>')
# 		# self.response.write(cgi.escape(self.request.get('content')))
# 		# self.response.write('</pre></body></html>')

 
application = webapp2.WSGIApplication(
[
    ('/',MainPage),
    ('/enviar',MainPage),],
    debug=True
)