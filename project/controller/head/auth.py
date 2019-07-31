import json, re
import falcon
import logging
from datetime import datetime
from sqlalchemy import between, func
from project.config import *
from passlib.hash import pbkdf2_sha256
from project.model.models import *
from base64 import b64decode, b64encode

# admin login
class HeadLogin:
    def on_get(self, req, res):
        try:
            logger.info('[Login API]')

            # Get Authorization token
            authorization_header = req.get_header('Authorization')

            # Split token by two. In other words remove Basic string from Authorization token
            split = authorization_header.split(' ')
            temp_token = b64decode(split[1])

            # Decode token text from Base64 to utf-8
            decoded_temp_token = temp_token.decode('utf8')

            # Extract data from decoded text. Normally token may have a mobile number and password
            eid, password = str(decoded_temp_token).split(':', 1)
            
            #look for admin record with eid
            db_admin = session.query(HeadOffice).filter_by(eid=eid).first()

            if db_admin:
                # Get DB password  of current admin
                signed_password = db_admin.password

                # Verify password
                valid_password = pbkdf2_sha256.verify(password, signed_password)

                if valid_password:
                    # Login success. create a token and return response.
                    access_token = db_admin.id

                    status = True
                    message = 'Login success. Access-Token generated successfully. '
                    # logger.info('[HeadOffice Login] successfully logged in. New access token generated .')
                    res.status = falcon.HTTP_201
                    res.body = json.dumps({ 'status' : status, 'access_token' : access_token, 'message' : message })
                    return
                else:
                    status = False
                    message = 'Invalid password.'
                    logger.error('[HeadOffice Login] Invalid password. ')
                    res.status = falcon.HTTP_201
                    res.body = json.dumps({ 'status' : status, 'message' : message })
                    return
            else:
                status = False
                message = 'Invalid Email.'
                logger.error('[HeadOffice Login] Invalid Email --> ' + str(eid))
                res.status = falcon.HTTP_201
                res.body = json.dumps({ 'status' : status, 'message' : message })
                return
        except Exception as e:
            status = False
            message = "[HeadOffice Login] Something went wrong : " +  str(e)
            logger.error(message)
            res.status = falcon.HTTP_200
            res.body = json.dumps({'status': status, 'message': message })

class HeadSignup:
    def on_post(self,req,res):
        try:
            try:
                # Reading data from request
                json_data =json.loads(req.bounded_stream.read().decode('utf8'))
                logger.info("[AddHeadOffice] Data {} ".format(json_data))
                name = json_data['name']
                eid = json_data['eid']
                dob = json_data['dob']
                password = json_data['password']
                security_string = json_data['security_string']
            except Exception as e:
                status = False
                message = "Required fields missing. " + str(e)
                logger.error(message)
                res.status = falcon.HTTP_201
                res.body = json.dumps({'status': status, 'message': message })
                return

            
            db_admin = session.query(HeadOffice).filter_by(eid=eid).first()
            if db_admin:
                status = False
                message = 'Account already exists.'
                logger.info('[AddHeadOffice] Account already exists ' + str(eid))
                res.status = falcon.HTTP_201
                res.body = json.dumps({ 'status' : status, 'message' : message })
                return
            else:
                signed_password = pbkdf2_sha256.hash(password)
                try:
                    new_admin = HeadOffice(
                        name=name,
                        eid=eid,
                        dob=dob,
                        password=signed_password
                    )
                    session.add(new_admin)
                    session.commit()

                    status = True
                    message = 'Signup success'
                    logger.info('[AddHeadOffice] Signup success')
                    res.status = falcon.HTTP_201
                    res.body = json.dumps({ 'status' : status, 'message' : message })
                    return

                except Exception as e:
                    status = False
                    message = "[AddHeadOffice] Error while adding admin : " +  str(e)
                    logger.error(message)
                    res.status = falcon.HTTP_200
                    res.body = json.dumps({'status': status, 'message': message })
                    return



        except Exception as e:
            status = False
            message = "[AddHeadOffice] Something went wrong : " +  str(e)
            logger.error(message)
            res.status = falcon.HTTP_200
            res.body = json.dumps({'status': status, 'message': message })

