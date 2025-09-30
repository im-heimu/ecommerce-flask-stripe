# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

# import Flask 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 

db = SQLAlchemy()

from .config import Config

# Inject Flask magic
app = Flask(__name__)

# load Configuration
app.config.from_object( Config ) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
db.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

# Создаем дефолтного администратора при первом запуске
def create_default_admin():
    with app.app_context():
        db.create_all()
        
        # Проверяем, есть ли уже пользователи
        if User.query.count() == 0:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password='admin123',
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Дефолтный администратор создан:")
            print("👤 Имя пользователя: admin")
            print("🔑 Пароль: admin123")

# Вызываем функцию создания дефолтного админа
create_default_admin()

# Import routing to render the pages
from app import views

