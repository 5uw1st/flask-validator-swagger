#!usr/bin/env python3
# -*- coding:utf-8 _*-

from flask_validator_swagger import create_app
from flask_validator_swagger.apis import main_bp
from flask_validator_swagger.apis.user import user_bp
from flask_validator_swagger.config import current_config


def get_url_prefix(bp):
    return current_config.URL_PREFIX.format(api_type=bp.name, version=current_config.API_VERSION)


app = create_app()
app.register_blueprint(main_bp)
app.register_blueprint(user_bp, url_prefix=get_url_prefix(bp=user_bp))

if __name__ == '__main__':
    app.run(port=2333, use_reloader=False)
