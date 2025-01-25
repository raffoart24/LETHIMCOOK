import random
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Funzione per ottenere le ricette dal database
def get_recipes(diet_type):
    conn = sqlite3.connect('planner.db')
    cursor = conn.cursor()
    query = """
    SELECT nome 
    FROM ricette 
    WHERE categoria = ?"""
    cursor.execute(query, (diet_type,))
    recipes = cursor.fetchall()
    conn.close()
    return [recipe[0] for recipe in recipes]

# Funzione per creare un piano settimanale
def generate_weekly_plan(recipes):
    random.shuffle(recipes)
    selected_recipes = recipes[:14]
    if len(selected_recipes) < 14:
        raise ValueError("Non ci sono abbastanza ricette per il piano settimanale.")

    weekly_plan = {}
    days = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    for i, day in enumerate(days):
        weekly_plan[day] = {
            "Pranzo": selected_recipes[i * 2],
            "Cena": selected_recipes[i * 2 + 1]
        }
    return weekly_plan

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcola_dieta', methods=['POST'])
def calcola_dieta():
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    height = int(request.form['height'])
    weight = int(request.form['weight'])
    diet_type = request.form['diet-type']
    diet_goal = request.form['diet-goal']

    # Calcolo del Metabolismo Basale (BMR)
    if gender == 'maschio':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Moltiplicatore di attività
    activity_multiplier = 1.2
    if diet_goal == 'dimagrimento':
        activity_multiplier = 1.1
    elif diet_goal == 'massa':
        activity_multiplier = 1.3

    daily_calories = bmr * activity_multiplier
    rounded_daily_calories = round(daily_calories)

    if diet_goal == 'dimagrimento':
        calorie_goal = rounded_daily_calories - 500
    elif diet_goal == 'massa':
        calorie_goal = rounded_daily_calories + 500
    else:
        calorie_goal = rounded_daily_calories

    recipes = get_recipes(diet_type)
    weekly_plan = generate_weekly_plan(recipes)

    return render_template(
        'index.html',
        name=name,
        diet_goal=diet_goal,
        calorie_goal=calorie_goal,
        diet_type=diet_type,
        weekly_plan=weekly_plan
    )

if __name__ == '__main__':
    app.run(debug=True)
