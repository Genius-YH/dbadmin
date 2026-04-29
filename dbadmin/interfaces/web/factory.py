from flask import Flask
from config import Config
from dbadmin.infrastructure.db import SqlAlchemyGateway
from dbadmin.application.services import AdminService


def build_container():
    app = Flask(__name__)
    app.config.from_object(Config)

    dbs = {"default": app.config["DATABASE_URL"]}
    dbs.update(app.config.get("DATABASES", {}))

    gateways = {name: SqlAlchemyGateway(url) for name, url in dbs.items()}
    services = {name: AdminService(gw) for name, gw in gateways.items()}
    return app, gateways, services
