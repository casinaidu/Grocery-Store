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
    app.app_context().push()
    cache = Cache(app)
    app.app_context().push()
    print("Create app complete")
    return app, api, celery, cache

app, api, celery, cache = create_app()

# Import all the controllers so they are loaded
# from application.api import UserLoginAPI,VenueAdminAPI,ShowAdminAPI,BookingAPI,ShowsAPI
# api.add_resource(UserLoginAPI, "/api/getuser/<email>","/api/adduser")
# api.add_resource(VenueAdminAPI, "/api/getvenue","/api/addvenue","/api/editvenue/<venue_id>","/api/deletevenue/<venue_id>")
# api.add_resource(ShowAdminAPI, "/api/getshow/<venue_id>","/api/addshow/<venue_id>","/api/editshow/<show_id>","/api/deleteshow/<show_id>")
# api.add_resource(BookingAPI, "/api/addbooking/<user_id>/<venue_id>/<show_id>")
# api.add_resource(ShowsAPI, "/api/getallshows")


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)