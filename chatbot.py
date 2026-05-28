from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# ==========================================
# FITNESS CHATBOT RESPONSES
# ==========================================

responses = {

    "hi": "👋 Hey Fitness Warrior! Welcome to FitBot. Ask me anything about workouts, diet, gym, fitness or weight loss!",

    "hello": "🔥 Ready to transform yourself? Let's go!",

    "weight loss": """
🔥 Weight Loss Tips:
• Drink more water
• Avoid sugar & junk food
• Walk daily
• Increase protein intake
• Sleep properly
""",

    "weight gain": """
🍗 Weight Gain Tips:
• Eat more calories
• Strength training
• Protein-rich foods
• Healthy smoothies
""",

    "diet": """
🥗 Diet Plan:
Breakfast → Oats & Fruits
Lunch → Rice + Protein
Snacks → Nuts & Juice
Dinner → Light Protein Meal
""",

    "abs": """
🏋️ Abs Workout:
• Crunches
• Leg Raises
• Plank
• Mountain Climbers
""",

    "chest": """
💪 Chest Workout:
• Pushups
• Bench Press
• Dumbbell Fly
• Incline Press
""",

    "biceps": """
💪 Biceps Workout:
• Dumbbell Curls
• Hammer Curls
• Barbell Curls
""",

    "legs": """
🦵 Leg Workout:
• Squats
• Lunges
• Leg Press
• Calf Raises
""",

    "cardio": """
🏃 Best Cardio:
• Running
• Cycling
• Jump Rope
• Burpees
""",

    "protein": """
🥚 Protein Foods:
• Eggs
• Chicken
• Paneer
• Fish
• Nuts
""",

    "gym": """
🏋️ Weekly Gym Routine:
Day 1 → Chest
Day 2 → Back
Day 3 → Legs
Day 4 → Shoulders
Day 5 → Arms
""",

    "motivation": random.choice([
        "🔥 Discipline beats motivation.",
        "🏆 Train insane or remain the same.",
        "💪 Every workout counts.",
        "🚀 Small progress is still progress."
    ]),

    "shoulder": """
🏋️ Shoulder Workout:
• Shoulder Press
• Lateral Raises
• Front Raises
• Arnold Press
""",

    "back": """
💥 Back Workout:
• Pull Ups
• Deadlifts
• Lat Pulldown
• Seated Row
""",

    "triceps": """
💪 Triceps Workout:
• Tricep Pushdown
• Dips
• Skull Crushers
• Close Grip Pushups
""",

    "beginner": """
🌟 Beginner Fitness Tips:
• Start with light workouts
• Focus on consistency
• Eat healthy
• Stay hydrated
• Warm up properly
""",

    "home workout": """
🏠 Home Workout Plan:
• Pushups
• Squats
• Plank
• Jumping Jacks
• Lunges
""",

    "calories": """
🔥 Calories Guide:
• Weight loss → Calorie deficit
• Weight gain → Calorie surplus
• Protein is important for muscle growth
""",

    "supplements": """
💊 Popular Supplements:
• Whey Protein
• Creatine
• Multivitamins
• Fish Oil
""",

    "stretching": """
🤸 Stretching Benefits:
• Improves flexibility
• Reduces injury risk
• Improves blood flow
• Relaxes muscles
""",

    "warm up": """
🔥 Warm Up Exercises:
• Jumping Jacks
• Arm Circles
• High Knees
• Light Jogging
""",

    "cool down": """
❄️ Cool Down Tips:
• Deep breathing
• Light stretching
• Walk slowly
• Drink water
""",

    "water": """
💧 Water Intake:
• Drink 3-4 litres daily
• More during workouts
• Stay hydrated throughout the day
""",

    "sleep": """
😴 Sleep Tips:
• Sleep 7-8 hours daily
• Avoid screens before bed
• Sleep at consistent times
""",

    "running": """
🏃 Running Benefits:
• Burns calories
• Improves stamina
• Good for heart health
• Reduces stress
""",

    "yoga": """
🧘 Yoga Benefits:
• Better flexibility
• Stress relief
• Improved balance
• Better breathing
""",

    "fitness": """
💪 Fitness Basics:
• Exercise regularly
• Eat healthy food
• Stay consistent
• Sleep properly
• Stay motivated
"""
}

# ==========================================
# MODERN HTML UI
# ==========================================

html = '''
<!DOCTYPE html>
<html>
<head>

<title>FitBot</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:Arial;
    background:linear-gradient(135deg,#0f172a,#1e293b,#111827);
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    overflow:hidden;
}

.container{
    width:80%;
    max-width:900px;
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(10px);
    border-radius:25px;
    padding:25px;
    box-shadow:0px 0px 30px rgba(0,0,0,0.6);
}

.header{
    text-align:center;
    margin-bottom:20px;
}

.header h1{
    color:#38bdf8;
    font-size:42px;
}

.header p{
    color:white;
    margin-top:10px;
}

.chatbox{
    background:#020617;
    height:450px;
    overflow-y:auto;
    border-radius:20px;
    padding:20px;
    border:2px solid #38bdf8;
}

.user-msg{
    background:#38bdf8;
    color:black;
    padding:12px 18px;
    border-radius:20px;
    margin:15px 0;
    width:fit-content;
    margin-left:auto;
    font-weight:bold;
}

.bot-msg{
    background:#1e293b;
    color:white;
    padding:15px;
    border-radius:20px;
    margin:15px 0;
    width:fit-content;
    max-width:80%;
    white-space:pre-line;
}

form{
    display:flex;
    margin-top:20px;
    gap:10px;
}

input{
    flex:1;
    padding:15px;
    border:none;
    border-radius:15px;
    font-size:16px;
    outline:none;
    background:#e2e8f0;
}

button{
    padding:15px 25px;
    border:none;
    border-radius:15px;
    background:#38bdf8;
    color:black;
    font-weight:bold;
    cursor:pointer;
    transition:0.3s;
}

button:hover{
    background:#0ea5e9;
    transform:scale(1.05);
}

.suggestions{
    margin-top:15px;
    color:#cbd5e1;
    text-align:center;
}

</style>

</head>

<body>

<div class="container">

<div class="header">
    <h1>💪 FitBot</h1>
    <p>Your Personal Fitness Assistant</p>
</div>

<div class="chatbox">

{% for chat in chats %}

<div class="user-msg">
{{ chat.user }}
</div>

<div class="bot-msg">
{{ chat.bot }}
</div>

{% endfor %}

</div>

<form method="POST">

<input type="text" name="message" placeholder="Ask about workouts, diet, gym..." required>

<button type="submit">Send</button>

</form>

<div class="suggestions">
Try: hi, chest workout, abs, cardio, diet, protein, motivation
</div>

</div>

</body>
</html>
'''

# ==========================================
# CHAT STORAGE
# ==========================================

chat_history = [
    {
        "user": "Hello",
        "bot": "👋 Welcome to FitBot! Ask me anything about workouts, fitness, gym or diet plans."
    }
]

# ==========================================
# MAIN ROUTE
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        user_message = request.form['message'].lower()

        bot_reply = "❌ Sorry, I don't understand. Try asking about workouts, diet, abs, chest, gym or cardio."

        for key in responses:

            if key in user_message:

                bot_reply = responses[key]
                break

        chat_history.append({
            'user': user_message,
            'bot': bot_reply
        })

    return render_template_string(html, chats=chat_history)

# ==========================================
# RUN APP
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)
