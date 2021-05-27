from flask import Flask

def init_app(app: Flask):
    from app.views.users_views import authentication
    app.register_blueprint(authentication)

    from app.views.casos_views import casos
    app.register_blueprint(casos)