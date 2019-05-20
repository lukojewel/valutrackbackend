import falcon
from wsgiref import simple_server

from project.routes import *

if __name__ == "__main__":
	host = '127.0.0.1'
	port = 5000
	httpd = simple_server.make_server(host, port, app)
	print("Serving on %s:%s" % (host, port))
	try:
		httpd.serve_forever()
	except Exception as e:
		print("Error in API " , e)


