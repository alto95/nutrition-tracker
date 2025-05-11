from app import db
from datetime import datetime

class Food(db.Model):
    __tablename__ = 'foods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    calories = db.Column(db.Float, nullable=False, default=0)
    carbohydrates = db.Column(db.Float, nullable=False, default=0)
    proteins = db.Column(db.Float, nullable=False, default=0)
    fats = db.Column(db.Float, nullable=False, default=0)
    serving_size = db.Column(db.Float, nullable=False, default=100)
    serving_unit = db.Column(db.String(20), nullable=False, default='g')
    is_recipe = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # For recipes
    recipe_instructions = db.Column(db.Text, nullable=True)
    
    # Relationships
    meal_items = db.relationship('MealItem', backref='food', lazy=True)
    
    def __repr__(self):
        return f'<Food {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'calories': self.calories,
            'carbohydrates': self.carbohydrates,
            'proteins': self.proteins,
            'fats': self.fats,
            'serving_size': self.serving_size,
            'serving_unit': self.serving_unit,
            'is_recipe': self.is_recipe,
            'created_at': self.created_at.isoformat(),
            'recipe_instructions': self.recipe_instructions if self.is_recipe else None
        }
