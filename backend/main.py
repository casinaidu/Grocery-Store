import os
from flask import Flask 
from application import workers
from application.config import LocalDevelopmentConfig, StageConfig
from application.database import db
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import *
from flask_caching import Cache

app = None
api= None
celery=None
cache=None

def create_app():
    app = Flask(__name__, template_folder="templates")
    print(os.getenv('ENV', "development"))
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    elif os.getenv('ENV', "development") == "stage":
      app.logger.info("Staring stage.")
      print("Staring  stage")
      app.config.from_object(StageConfig)
      print("pushed config")
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      print("pushed config")
    app.app_context().push()
    print("DB Init")
    db.init_app(app)
    print("DB Init complete")
    app.app_context().push()
    db.create_all()
    app.logger.info("App setup complete")
    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    api = Api(app)
    app.app_context().push()
    
    # Create celery   
    celery = workers.celery

    # Update with configuration
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )

    celery.Task = workers.ContextTask
    CORS(app, supports_credentials=True)
    CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})
    app.config['CORS_HEADERS'] = 'application/json'

    app.app_context().push()
    cache = Cache(app)
    app.app_context().push()
    print("Create app complete")
    return app, api, celery, cache

app, api, celery, cache = create_app()

from application.api import *
api.add_resource(UserAPI, "/api/getuser/<email>", "/api/adduser")
api.add_resource(CategoryAPI, "/api/categories", "/api/category/<int:id>", "/api/category")
api.add_resource(ProductAPI, "/api/products","/api/product/<int:id>","/api/product")
api.add_resource(PurchaseAPI, "/api/purchases","/api/purchase/<int:id>","/api/purchase")
# api.add_resource(ShowsAPI, "/api/getallshows")


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0')