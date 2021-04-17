from main.models.profile import Profile
from utilities import postgres_connetion,close_postgres_connection
# from address import Address
import uuid
from config import host_postgres,db_name_postgres,db_password_postgres,db_user_postgres,pepper
from utilities_user import hash_string

class User(Profile):
    def __init__(self,name,last_name,email,tel,id,user_name,password,user_type):

        Profile.__init__(self,name,last_name,email,tel)

        self.id=str(id)
        self.user_name=user_name
        self.password=hash_string(password)
        self.user_type=user_type
        



  

 
