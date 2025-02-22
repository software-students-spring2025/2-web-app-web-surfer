import os
from flask_pymongo import PyMongo
from mongoengine import connect, disconnect

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SWE_Project2'
    # 添加其他配置项
    DEBUG = True
    # 数据库配置等

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# MongoDB配置 - 使用原有的数据库名称
MONGO_URI = "mongodb://localhost:27017/SWE_Project2_Rental_Software"

def init_db(app):
    # 先断开所有现有连接
    disconnect()
    
    # 设置Flask-PyMongo
    app.config["MONGO_URI"] = MONGO_URI
    mongo = PyMongo(app)
    
    # 设置MongoEngine连接
    connect(db='SWE_Project2_Rental_Software', host=MONGO_URI)
    
    print("MongoDB连接成功")
    return mongo 