from flask_smorest import Blueprint
from flask.views import MethodView

# Keeping the original tag name "Healt Check" to preserve existing docs/tests
blp = Blueprint("Healt Check", "health check", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    def get(self):
        return {"message": "Healthy"}
