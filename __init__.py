# 这个文件可以为空，仅用来标识这是一个 Python 包 

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'SWE_Project2'  # 建议使用环境变量

    # 注册蓝图
    from .routes import login_bp, register_bp, house_bp
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(house_bp, url_prefix='/house')

    return app 