from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

# File to store habits
HABIT_FILE = "habits.json"

# Ensure the file exists
if not os.path.exists(HABIT_FILE):
    with open(HABIT_FILE, "w") as f:
        json.dump([], f)

# Load habits from file
def load_habits():
    with open(HABIT_FILE, "r") as f:
        return json.load(f)

# Save habits to file
def save_habits(habits):
    with open(HABIT_FILE, "w") as f:
        json.dump(habits, f, indent=4)

@app.route("/")
def index():
    habits = load_habits()
    return render_template("index.html", habits=habits)

@app.route("/add", methods=["POST"])
def add_habit():
    habit_name = request.form.get("habit")
    if habit_name:
        habits = load_habits()
        habits.append({"name": habit_name, "completed": False})
        save_habits(habits)
    return redirect("/")

@app.route("/toggle/<int:habit_index>")
def toggle_habit(habit_index):
    habits = load_habits()
    if 0 <= habit_index < len(habits):
        habits[habit_index]["completed"] = not habits[habit_index]["completed"]
        save_habits(habits)
    return redirect("/")

@app.route("/delete/<int:habit_index>")
def delete_habit(habit_index):
    habits = load_habits()
    if 0 <= habit_index < len(habits):
        habits.pop(habit_index)
        save_habits(habits)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
