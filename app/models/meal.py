from app import db
from datetime import datetime

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    meal_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('MealItem', backref='meal', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Meal {self.name} at {self.meal_time}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'meal_time': self.meal_time.isoformat(),
            'user_id': self.user_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }
    
    @property
    def total_calories(self):
        return sum(item.calories for item in self.items)
    
    @property
    def total_carbs(self):
        return sum(item.carbohydrates for item in self.items)
    
    @property
    def total_proteins(self):
        return sum(item.proteins for item in self.items)
    
    @property
    def total_fats(self):
        return sum(item.fats for item in self.items)

class MealItem(db.Model):
    __tablename__ = 'meal_items'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<MealItem {self.food_id} in meal {self.meal_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'meal_id': self.meal_id,
            'food_id': self.food_id,
            'food_name': self.food.name if self.food else None,
            'amount': self.amount,
            'calories': self.calories,
            'carbohydrates': self.carbohydrates,
            'proteins': self.proteins,
            'fats': self.fats
        }
    
    @property
    def calories(self):
        return (self.food.calories / self.food.serving_size) * self.amount if self.food else 0
    
    @property
    def carbohydrates(self):
        return (self.food.carbohydrates / self.food.serving_size) * self.amount if self.food else 0
    
    @property
    def proteins(self):
        return (self.food.proteins / self.food.serving_size) * self.amount if self.food else 0
    
    @property
    def fats(self):
        return (self.food.fats / self.food.serving_size) * self.amount if self.food else 0
