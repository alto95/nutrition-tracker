from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User, Food, Meal, GlucoseReading, Recipe
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost/nutrition_tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret')  # Change this in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app)
jwt = JWTManager(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "User already exists"}), 400
        
    new_user = User(
        email=data['email'],
        name=data.get('name', ''),
        height=data.get('height'),
        weight=data.get('weight'),
        age=data.get('age'),
        gender=data.get('gender')
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    
    access_token = create_access_token(identity=new_user.id)
    return jsonify(access_token=access_token, user=new_user.to_dict()), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"msg": "Bad credentials"}), 401
        
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token, user=user.to_dict())

@app.route('/api/google-auth', methods=['POST'])
def google_auth():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Create new user
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token, user=user.to_dict())

# User routes
@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    return jsonify(user.to_dict())

@app.route('/api/user', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'height' in data:
        user.height = data['height']
    if 'weight' in data:
        user.weight = data['weight']
    if 'age' in data:
        user.age = data['age']
    if 'gender' in data:
        user.gender = data['gender']
    if 'password' in data:
        user.set_password(data['password'])
        
    db.session.commit()
    return jsonify(user.to_dict())

# Food routes
@app.route('/api/foods', methods=['GET'])
@jwt_required()
def get_foods():
    user_id = get_jwt_identity()
    foods = Food.query.filter_by(user_id=user_id).all()
    return jsonify([food.to_dict() for food in foods])

@app.route('/api/foods', methods=['POST'])
@jwt_required()
def create_food():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_food = Food(
        name=data['name'],
        calories=data['calories'],
        carbs=data['carbs'],
        protein=data['protein'],
        fat=data.get('fat', 0),
        user_id=user_id
    )
    
    db.session.add(new_food)
    db.session.commit()
    
    return jsonify(new_food.to_dict()), 201

@app.route('/api/foods/<int:food_id>', methods=['PUT'])
@jwt_required()
def update_food(food_id):
    user_id = get_jwt_identity()
    food = Food.query.filter_by(id=food_id, user_id=user_id).first()
    
    if not food:
        return jsonify({"msg": "Food not found or unauthorized"}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        food.name = data['name']
    if 'calories' in data:
        food.calories = data['calories']
    if 'carbs' in data:
        food.carbs = data['carbs']
    if 'protein' in data:
        food.protein = data['protein']
    if 'fat' in data:
        food.fat = data['fat']
        
    db.session.commit()
    return jsonify(food.to_dict())

@app.route('/api/foods/<int:food_id>', methods=['DELETE'])
@jwt_required()
def delete_food(food_id):
    user_id = get_jwt_identity()
    food = Food.query.filter_by(id=food_id, user_id=user_id).first()
    
    if not food:
        return jsonify({"msg": "Food not found or unauthorized"}), 404
    
    db.session.delete(food)
    db.session.commit()
    return jsonify({"msg": "Food deleted"})

# Recipe routes
@app.route('/api/recipes', methods=['GET'])
@jwt_required()
def get_recipes():
    user_id = get_jwt_identity()
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return jsonify([recipe.to_dict() for recipe in recipes])

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required()
def get_recipe(recipe_id):
    user_id = get_jwt_identity()
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=user_id).first()
    
    if not recipe:
        return jsonify({"msg": "Recipe not found or unauthorized"}), 404
        
    return jsonify(recipe.to_dict())

@app.route('/api/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_recipe = Recipe(
        name=data['name'],
        ingredients=data['ingredients'],
        instructions=data.get('instructions', ''),
        calories=data['calories'],
        carbs=data['carbs'],
        protein=data['protein'],
        fat=data.get('fat', 0),
        user_id=user_id
    )
    
    db.session.add(new_recipe)
    db.session.commit()
    
    return jsonify(new_recipe.to_dict()), 201

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    user_id = get_jwt_identity()
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=user_id).first()
    
    if not recipe:
        return jsonify({"msg": "Recipe not found or unauthorized"}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        recipe.name = data['name']
    if 'ingredients' in data:
        recipe.ingredients = data['ingredients']
    if 'instructions' in data:
        recipe.instructions = data['instructions']
    if 'calories' in data:
        recipe.calories = data['calories']
    if 'carbs' in data:
        recipe.carbs = data['carbs']
    if 'protein' in data:
        recipe.protein = data['protein']
    if 'fat' in data:
        recipe.fat = data['fat']
        
    db.session.commit()
    return jsonify(recipe.to_dict())

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    user_id = get_jwt_identity()
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=user_id).first()
    
    if not recipe:
        return jsonify({"msg": "Recipe not found or unauthorized"}), 404
    
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"msg": "Recipe deleted"})

# Meal routes
@app.route('/api/meals', methods=['GET'])
@jwt_required()
def get_meals():
    user_id = get_jwt_identity()
    
    # Get query parameters for filtering
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Meal.query.filter_by(user_id=user_id)
    
    if start_date:
        query = query.filter(Meal.timestamp >= start_date)
    if end_date:
        query = query.filter(Meal.timestamp <= end_date)
        
    meals = query.order_by(Meal.timestamp.desc()).all()
    return jsonify([meal.to_dict() for meal in meals])

@app.route('/api/meals', methods=['POST'])
@jwt_required()
def create_meal():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_meal = Meal(
        name=data['name'],
        calories=data['calories'],
        carbs=data['carbs'],
        protein=data['protein'],
        fat=data.get('fat', 0),
        timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
        user_id=user_id
    )
    
    db.session.add(new_meal)
    db.session.commit()
    
    return jsonify(new_meal.to_dict()), 201

@app.route('/api/meals/<int:meal_id>', methods=['PUT'])
@jwt_required()
def update_meal(meal_id):
    user_id = get_jwt_identity()
    meal = Meal.query.filter_by(id=meal_id, user_id=user_id).first()
    
    if not meal:
        return jsonify({"msg": "Meal not found or unauthorized"}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        meal.name = data['name']
    if 'calories' in data:
        meal.calories = data['calories']
    if 'carbs' in data:
        meal.carbs = data['carbs']
    if 'protein' in data:
        meal.protein = data['protein']
    if 'fat' in data:
        meal.fat = data['fat']
    if 'timestamp' in data:
        meal.timestamp = datetime.fromisoformat(data['timestamp'])
        
    db.session.commit()
    return jsonify(meal.to_dict())

@app.route('/api/meals/<int:meal_id>', methods=['DELETE'])
@jwt_required()
def delete_meal(meal_id):
    user_id = get_jwt_identity()
    meal = Meal.query.filter_by(id=meal_id, user_id=user_id).first()
    
    if not meal:
        return jsonify({"msg": "Meal not found or unauthorized"}), 404
    
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"msg": "Meal deleted"})

# Add a meal from a recipe
@app.route('/api/meals/from-recipe/<int:recipe_id>', methods=['POST'])
@jwt_required()
def create_meal_from_recipe(recipe_id):
    user_id = get_jwt_identity()
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=user_id).first()
    
    if not recipe:
        return jsonify({"msg": "Recipe not found or unauthorized"}), 404
    
    # Get timestamp from request or use current time
    data = request.get_json() or {}
    timestamp = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
    
    new_meal = Meal(
        name=recipe.name,
        calories=recipe.calories,
        carbs=recipe.carbs,
        protein=recipe.protein,
        fat=recipe.fat,
        timestamp=timestamp,
        user_id=user_id,
        recipe_id=recipe.id
    )
    
    db.session.add(new_meal)
    db.session.commit()
    
    return jsonify(new_meal.to_dict()), 201

# Glucose reading routes
@app.route('/api/glucose', methods=['GET'])
@jwt_required()
def get_glucose_readings():
    user_id = get_jwt_identity()
    
    # Get query parameters for filtering
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = GlucoseReading.query.filter_by(user_id=user_id)
    
    if start_date:
        query = query.filter(GlucoseReading.timestamp >= start_date)
    if end_date:
        query = query.filter(GlucoseReading.timestamp <= end_date)
        
    readings = query.order_by(GlucoseReading.timestamp.desc()).all()
    return jsonify([reading.to_dict() for reading in readings])

@app.route('/api/glucose', methods=['POST'])
@jwt_required()
def create_glucose_reading():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_reading = GlucoseReading(
        value=data['value'],
        timestamp=datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat())),
        notes=data.get('notes', ''),
        user_id=user_id
    )
    
    db.session.add(new_reading)
    db.session.commit()
    
    return jsonify(new_reading.to_dict()), 201

@app.route('/api/glucose/<int:reading_id>', methods=['PUT'])
@jwt_required()
def update_glucose_reading(reading_id):
    user_id = get_jwt_identity()
    reading = GlucoseReading.query.filter_by(id=reading_id, user_id=user_id).first()
    
    if not reading:
        return jsonify({"msg": "Reading not found or unauthorized"}), 404
    
    data = request.get_json()
    
    if 'value' in data:
        reading.value = data['value']
    if 'timestamp' in data:
        reading.timestamp = datetime.fromisoformat(data['timestamp'])
    if 'notes' in data:
        reading.notes = data['notes']
        
    db.session.commit()
    return jsonify(reading.to_dict())

@app.route('/api/glucose/<int:reading_id>', methods=['DELETE'])
@jwt_required()
def delete_glucose_reading(reading_id):
    user_id = get_jwt_identity()
    reading = GlucoseReading.query.filter_by(id=reading_id, user_id=user_id).first()
    
    if not reading:
        return jsonify({"msg": "Reading not found or unauthorized"}), 404
    
    db.session.delete(reading)
    db.session.commit()
    return jsonify({"msg": "Reading deleted"})

# Analytics routes
@app.route('/api/analytics/daily', methods=['GET'])
@jwt_required()
def get_daily_analytics():
    user_id = get_jwt_identity()
    date = request.args.get('date', datetime.now().date().isoformat())
    
    # Get all meals for the specified date
    start_date = f"{date}T00:00:00"
    end_date = f"{date}T23:59:59"
    
    meals = Meal.query.filter_by(user_id=user_id).filter(
        Meal.timestamp >= start_date,
        Meal.timestamp <= end_date
    ).all()
    
    # Get all glucose readings for the specified date
    readings = GlucoseReading.query.filter_by(user_id=user_id).filter(
        GlucoseReading.timestamp >= start_date,
        GlucoseReading.timestamp <= end_date
    ).all()
    
    # Calculate totals
    total_calories = sum(meal.calories for meal in meals)
    total_carbs = sum(meal.carbs for meal in meals)
    total_protein = sum(meal.protein for meal in meals)
    total_fat = sum(meal.fat for meal in meals)
    
    # Calculate glucose stats
    glucose_values = [reading.value for reading in readings]
    glucose_avg = sum(glucose_values) / len(glucose_values) if glucose_values else 0
    glucose_min = min(glucose_values) if glucose_values else 0
    glucose_max = max(glucose_values) if glucose_values else 0
    
    return jsonify({
        "date": date,
        "nutrition": {
            "calories": total_calories,
            "carbs": total_carbs,
            "protein": total_protein,
            "fat": total_fat
        },
        "glucose": {
            "average": glucose_avg,
            "min": glucose_min,
            "max": glucose_max,
            "readings_count": len(glucose_values)
        },
        "meals_count": len(meals)
    })

@app.route('/api/analytics/weekly', methods=['GET'])
@jwt_required()
def get_weekly_analytics():
    user_id = get_jwt_identity()
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)  # Get last 7 days
    
    # Format dates for database query
    start_date_str = f"{start_date.isoformat()}T00:00:00"
    end_date_str = f"{end_date.isoformat()}T23:59:59"
    
    # Get all meals for the date range
    meals = Meal.query.filter_by(user_id=user_id).filter(
        Meal.timestamp >= start_date_str,
        Meal.timestamp <= end_date_str
    ).all()
    
    # Get all glucose readings for the date range
    readings = GlucoseReading.query.filter_by(user_id=user_id).filter(
        GlucoseReading.timestamp >= start_date_str,
        GlucoseReading.timestamp <= end_date_str
    ).all()
    
    # Organize data by day
    daily_data = {}
    
    # Initialize all days
    for i in range(7):
        day = (start_date + timedelta(days=i)).isoformat()
        daily_data[day] = {
            "nutrition": {"calories": 0, "carbs": 0, "protein": 0, "fat": 0},
            "glucose": {"values": [], "count": 0},
            "meals_count": 0
        }
    
    # Add meal data
    for meal in meals:
        day = meal.timestamp.date().isoformat()
        daily_data[day]["nutrition"]["calories"] += meal.calories
        daily_data[day]["nutrition"]["carbs"] += meal.carbs
        daily_data[day]["nutrition"]["protein"] += meal.protein
        daily_data[day]["nutrition"]["fat"] += meal.fat
        daily_data[day]["meals_count"] += 1
    
    # Add glucose data
    for reading in readings:
        day = reading.timestamp.date().isoformat()
        daily_data[day]["glucose"]["values"].append(reading.value)
        daily_data[day]["glucose"]["count"] += 1
    
    # Calculate glucose averages
    for day, data in daily_data.items():
        values = data["glucose"]["values"]
        data["glucose"]["average"] = sum(values) / len(values) if values else 0
        data["glucose"]["min"] = min(values) if values else 0
        data["glucose"]["max"] = max(values) if values else 0
        del data["glucose"]["values"]  # Remove raw values
    
    return jsonify({
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily_data": daily_data
    })

@app.route('/api/analytics/monthly', methods=['GET'])
@jwt_required()
def get_monthly_analytics():
    user_id = get_jwt_identity()
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))
    
    # Create start and end dates for the month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Format dates for database query
    start_date_str = f"{start_date.date().isoformat()}T00:00:00"
    end_date_str = f"{end_date.date().isoformat()}T23:59:59"
    
    # Get all meals for the month
    meals = Meal.query.filter_by(user_id=user_id).filter(
        Meal.timestamp >= start_date_str,
        Meal.timestamp <= end_date_str
    ).all()
    
    # Get all glucose readings for the month
    readings = GlucoseReading.query.filter_by(user_id=user_id).filter(
        GlucoseReading.timestamp >= start_date_str,
        GlucoseReading.timestamp <= end_date_str
    ).all()
    
    # Calculate total nutrition for the month
    total_calories = sum(meal.calories for meal in meals)
    total_carbs = sum(meal.carbs for meal in meals)
    total_protein = sum(meal.protein for meal in meals)
    total_fat = sum(meal.fat for meal in meals)
    
    # Calculate average glucose for the month
    glucose_values = [reading.value for reading in readings]
    glucose_avg = sum(glucose_values) / len(glucose_values) if glucose_values else 0
    glucose_min = min(glucose_values) if glucose_values else 0
    glucose_max = max(glucose_values) if glucose_values else 0
    
    return jsonify({
        "year": year,
        "month": month,
        "nutrition": {
            "calories": total_calories,
            "carbs": total_carbs,
            "protein": total_protein,
            "fat": total_fat
        },
        "glucose": {
            "average": glucose_avg,
            "min": glucose_min,
            "max": glucose_max,
            "readings_count": len(glucose_values)
        },
        "meals_count": len(meals)
    })

# Search route
@app.route('/api/search', methods=['GET'])
@jwt_required()
def search():
    user_id = get_jwt_identity()
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"msg": "Query parameter 'q' is required"}), 400
    
    # Search foods
    foods = Food.query.filter_by(user_id=user_id).filter(
        Food.name.ilike(f'%{query}%')
    ).all()
    
    # Search recipes
    recipes = Recipe.query.filter_by(user_id=user_id).filter(
        Recipe.name.ilike(f'%{query}%')
    ).all()
    
    # Search meals
    meals = Meal.query.filter_by(user_id=user_id).filter(
        Meal.name.ilike(f'%{query}%')
    ).all()
    
    return jsonify({
        "foods": [food.to_dict() for food in foods],
        "recipes": [recipe.to_dict() for recipe in recipes],
        "meals": [meal.to_dict() for meal in meals]
    })

if __name__ == '__main__':
    app.run(debug=True)
