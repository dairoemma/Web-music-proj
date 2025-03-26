from .routes_user import user_bp
from .routes_admin import admin_bp
from .routes_musician import musician_bp


blueprints = [
    (user_bp,"/user"), 
    (admin_bp,"/admin"), 
    (musician_bp,"/musician"),
    ]

