
from gunicorn.app.wsgiapp import WSGIApplication
from flask_script import Manager, Command, Option

from flask_script import Manager
import unittest
from main import create_app
from main.views.client_views import client
from main.views.user_views import user
from main.views.address_views import address
from main.views.contract_views import contract
from main.views.sinister_views import sinister
from main.views.indemnity_views import indemnity
from main.views.instalments_views import instalment
from main.views.payments_views import payment
from main.views.dashboard_views import dashboard

class GunicornServer(Command):
 """Run the app within Gunicorn"""
 def get_options(self):
    from gunicorn.config import make_settings
    settings = make_settings()
    options = (
        Option(*klass.cli, action=klass.action)
        for setting, klass in settings.iteritems() if klass.cli
        )
    return options
 def run(self, *args, **kwargs):
    from gunicorn.app.wsgiapp import WSGIApplication
    app = WSGIApplication()
    app.app_uri = 'manage:app'
    return app.run()


app=create_app()

app.register_blueprint(dashboard)
app.register_blueprint(client)

app.register_blueprint(user)

app.register_blueprint(address)

app.register_blueprint(contract)

app.register_blueprint(sinister)

app.register_blueprint(indemnity)

app.register_blueprint(instalment)

app.register_blueprint(payment)

app.app_context().push()


manager = Manager(app)

manager.add_command("gunicorn", GunicornServer())

@manager.command
def run():
    app.run(debug=True)

@manager.command
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()