# postgres parameters of connection
host_postgres='localhost'
db_name_postgres='test8'
db_user_postgres='postgres'
db_password_postgres='postgres'

# default country
default_country_name='Tunisie'




from dotenv import load_dotenv
load_dotenv()
import os
MAIL_USERNAME = os.environ['EMAIL_USER']
MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

MAIL_DEBUG=True
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
MAIL_DEFAULT_SENDER ="sender_mail"
CORP_MAIL='welcom to 5allasli'