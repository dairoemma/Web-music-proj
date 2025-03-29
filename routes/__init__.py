from .routes_user import user_bp
from .routes_admin import admin_bp
from .routes_musician import musician_bp

# imported the blueprint for all routes and stored them in the blueprints list and gave the routes names
blueprints = [
    (user_bp,"/user"), 
    (admin_bp,"/admin"), 
    (musician_bp,"/musician"),
    ]

