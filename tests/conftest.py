import pytest
from flask import template_rendered
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


flask_app=create_app()
flask_app.register_blueprint(dashboard)
flask_app.register_blueprint(client)

flask_app.register_blueprint(user)

flask_app.register_blueprint(address)

flask_app.register_blueprint(contract)

flask_app.register_blueprint(sinister)

flask_app.register_blueprint(indemnity)

flask_app.register_blueprint(instalment)

flask_app.register_blueprint(payment)
flask_app.app_context().push()

@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)