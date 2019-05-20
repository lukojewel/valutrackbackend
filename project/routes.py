import falcon
from falcon_cors import CORS
from project.controller import *
from project.model.models import *

cors = CORS(
		allow_origins_list=[
			
		],
		allow_all_headers=True,
		allow_methods_list=['GET', 'POST', 'OPTIONS']
	)
app = falcon.API(middleware=[cors.middleware])
# app = falcon.API()

# testing the db connection
try:
	print(session.query(User).first().fname)
except:
	print("User table is empty")

# User APIs
# Themes
# app.add_route("/user/auth/sign-up", UserSignUp())



