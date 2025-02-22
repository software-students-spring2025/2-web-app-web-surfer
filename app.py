from flask import Flask
from flask_cors import CORS
from config import init_db
from routes import setup_routes
import secrets

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # 设置 secret key
    app.secret_key = secrets.token_hex(16)
    
    # 初始化数据库
    mongo = init_db(app)
    
    # 设置路由
    setup_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5001)