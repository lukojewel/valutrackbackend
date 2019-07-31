import json, re
import falcon
import logging
from datetime import datetime
from sqlalchemy import between, func
from project.config import *
from passlib.hash import pbkdf2_sha256
from project.model.models import *
from base64 import b64decode, b64encode

class AddCustomer:
    def on_post(self,req,res):
        try:
            try:
                # Reading data from request
                json_data =json.loads(req.bounded_stream.read().decode('utf8'))
                logger.info("[AddCustomer] Data {} ".format(json_data))
                name = json_data['name']
                email = json_data['email']
                branch = json_data['branch']
                contact = json_data['contact']
                dob = json_data['dob']
                try:
                	due = json_data['due']
                except:
                	due = 0
            except Exception as e:
                status = False
                message = "Required fields missing. " + str(e)
                logger.error(message)
                res.status = falcon.HTTP_201
                res.body = json.dumps({'status': status, 'message': message })
                return

            
            db_admin = session.query(Customer).filter_by(email=email).first() or session.query(Customer).filter_by(contact=contact).first()
            if db_admin:
                status = False
                message = 'Account already exists.'
                logger.info('[AddCustomer] Account already exists ' + str(email))
                res.status = falcon.HTTP_201
                res.body = json.dumps({ 'status' : status, 'message' : message })
                return
            else:
                try:
                    new_admin = Customer(
                        name=name,
                        email=email,
                        branch=branch,
                        contact=contact,
                        dob=dob
                    )
                    session.add(new_admin)
                    session.commit()

                    status = True
                    message = 'success'
                    logger.info('[AddCustomer] success')
                    res.status = falcon.HTTP_201
                    res.body = json.dumps({ 'status' : status, 'message' : message })
                    return

                except Exception as e:
                    status = False
                    message = "[AddCustomer] Error while adding admin : " +  str(e)
                    logger.error(message)
                    res.status = falcon.HTTP_200
                    res.body = json.dumps({'status': status, 'message': message })
                    return



        except Exception as e:
            status = False
            message = "[AddCustomer] Something went wrong : " +  str(e)
            logger.error(message)
            res.status = falcon.HTTP_200
            res.body = json.dumps({'status': status, 'message': message })

