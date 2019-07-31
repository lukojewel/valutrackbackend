import falcon
from falcon_cors import CORS
from project.controller import *
from project.model.models import *

cors = CORS(
		# allow_origins_list=[
			
		# ],
		allow_all_headers=True,
		allow_all_origins=True,
		allow_methods_list=['GET', 'POST', 'OPTIONS']
	)
app = falcon.API(middleware=[cors.middleware])
# app = falcon.API()


# User APIs
# Branch
app.add_route("/branch/auth/sign-up", BranchSignup())
app.add_route("/branch/auth/login", BranchLogin())
app.add_route("/branch/customer/add", AddCustomer())

# Branch
app.add_route("/head/auth/sign-up", HeadSignup())
app.add_route("/head/auth/login", HeadLogin())


