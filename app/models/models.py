from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    height = db.Column(db.Float, nullable=True)  # in cm
    weight = db.Column(db.Float, nullable=True)  # in kg
    goal_calories = db.Column(db.Integer, nullable=True)
    goal_carbs = db.Column(db.Float, nullable=True)  # in grams
    goal_proteins = db.Column(db.Float, nullable=True)  # in grams
    goal_fats = db.Column(db.Float, nullable=True)  # in grams
    avatar_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    meals = db.relationship('Meal', backref='user', lazy=True, cascade='all, delete-orphan')
    glucose_readings = db.relationship('GlucoseReading', backref='user', lazy=True, cascade='all, delete-orphan')
    recipes = db.relationship('Recipe', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'goal_calories': self.goal_calories,
            'goal_carbs': self.goal_carbs,
            'goal_proteins': self.goal_proteins,
            'goal_fats': self.goal_fats,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Food/Recipe Model
class Recipe(db.Model):
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    serving_size = db.Column(db.Float, nullable=False)  # in grams
    serving_unit = db.Column(db.String(20), nullable=False, default='g')
    calories = db.Column(db.Integer, nullable=False)  # per serving
    carbs = db.Column(db.Float, nullable=False)  # in grams
    proteins = db.Column(db.Float, nullable=False)  # in grams
    fats = db.Column(db.Float, nullable=False)  # in grams
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    meal_items = db.relationship('MealItem', backref='recipe', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'serving_size': self.serving_size,
            'serving_unit': self.serving_unit,
            'calories': self.calories,
            'carbs': self.carbs,
            'proteins': self.proteins,
            'fats': self.fats,
            'is_public': self.is_public,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Meal Model
class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    meal_items = db.relationship('MealItem', backref='meal', lazy=True, cascade='all, delete-orphan')
    
    def total_calories(self):
        return sum(item.calories_total() for item in self.meal_items)
    
    def total_carbs(self):
        return sum(item.carbs_total() for item in self.meal_items)
    
    def total_proteins(self):
        return sum(item.proteins_total() for item in self.meal_items)
    
    def total_fats(self):
        return sum(item.fats_total() for item in self.meal_items)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'timestamp': self.timestamp.isoformat(),
            'notes': self.notes,
            'total_calories': self.total_calories(),
            'total_carbs': self.total_carbs(),
            'total_proteins': self.total_proteins(),
            'total_fats': self.total_fats(),
            'meal_items': [item.to_dict() for item in self.meal_items],
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Meal Item (junction between Meal and Food/Recipe)
class MealItem(db.Model):
    __tablename__ = 'meal_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False, default=1.0)  # number of servings
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    
    def calories_total(self):
        return self.recipe.calories * self.quantity
    
    def carbs_total(self):
        return self.recipe.carbs * self.quantity
    
    def proteins_total(self):
        return self.recipe.proteins * self.quantity
    
    def fats_total(self):
        return self.recipe.fats * self.quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'recipe': self.recipe.to_dict() if self.recipe else None,
            'calories_total': self.calories_total(),
            'carbs_total': self.carbs_total(),
            'proteins_total': self.proteins_total(),
            'fats_total': self.fats_total(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Glucose Reading Model
class GlucoseReading(db.Model):
    __tablename__ = 'glucose_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)  # in mg/dL
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=True)  # Optional relation to a meal
    
    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'timestamp': self.timestamp.isoformat(),
            'notes': self.notes,
            'user_id': self.user_id,
            'meal_id': self.meal_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
