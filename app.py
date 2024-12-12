from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Conversation state to track progress for each user
conversation_state = {}

def coffee_bot(user_id, message):
    state = conversation_state.get(user_id, {})

    # Step 1: Ask for the user's name
    if 'name' not in state:
        if not state.get('asked_name', False):
            state['asked_name'] = True
            conversation_state[user_id] = state
            return "Hi! What's your name?"
        else:
            state['name'] = message.strip()
            conversation_state[user_id] = state
            return f"Welcome to the Cafe, {state['name']}! I will help you order your drink.\nWhat size drink can I get for you? \n[a] Small \n[b] Medium \n[c] Large"

    # Step 2: Ask for drink size
    if 'size' not in state:
        size_map = {'a': 'small', 'b': 'medium', 'c': 'large'}
        size = size_map.get(message.lower())
        if size:
            state['size'] = size
            conversation_state[user_id] = state
            return f"Got it. A {size} drink.\nWhat type of drink would you like? \n[a] Brewed Coffee \n[b] Mocha \n[c] Latte"
        else:
            return "Please choose a valid option: \n[a] Small \n[b] Medium \n[c] Large"

    # Step 3: Ask for drink type
    if 'drink_type' not in state:
        drink_map = {'a': 'Brewed Coffee', 'b': 'Mocha', 'c': 'Latte'}
        drink = drink_map.get(message.lower())
        if drink:
            state['drink_type'] = drink
            conversation_state[user_id] = state
            if drink == 'Latte':
                return "And what kind of milk for your latte? \n[a] 2% milk \n[b] Non-fat milk \n[c] Soy milk"
            return f"Great choice. {drink}.\nWould you like a plastic cup or your own reusable cup? \n[a] Plastic cup \n[b] Reusable cup"
        else:
            return "Please choose a valid option: \n[a] Brewed Coffee \n[b] Mocha \n[c] Latte"

    # Step 4: Ask for milk type if Latte was chosen
    if state.get('drink_type') == 'Latte' and 'milk' not in state:
        milk_map = {'a': '2% milk', 'b': 'Non-fat milk', 'c': 'Soy milk'}
        milk = milk_map.get(message.lower())
        if milk:
            state['milk'] = milk
            conversation_state[user_id] = state
            return f"Got it. A latte with {milk}.\nWould you like a plastic cup or your own reusable cup? \n[a] Plastic cup \n[b] Reusable cup"
        else:
            return "Please choose a valid option: \n[a] 2% milk \n[b] Non-fat milk \n[c] Soy milk"

    # Step 5: Ask for cup type
    if 'cup_type' not in state:
        cup_map = {'a': 'plastic cup', 'b': 'reusable cup'}
        cup = cup_map.get(message.lower())
        if cup:
            state['cup_type'] = cup
            conversation_state[user_id] = state
            return f"Got it. Using a {cup}.\nWould you like your drink hot or iced? \n[a] Hot \n[b] Iced"
        else:
            return "Please choose a valid option: \n[a] Plastic cup \n[b] Reusable cup"

    # Step 6: Ask for hot or iced
    if 'temperature' not in state:
        temp_map = {'a': 'hot', 'b': 'iced'}
        temp = temp_map.get(message.lower())
        if temp:
            state['temperature'] = temp
            conversation_state[user_id] = state
            size = state['size']
            drink_type = state['drink_type']
            milk = state.get('milk', '')
            cup_type = state['cup_type']
            temperature = state['temperature']
            milk_text = f" with {milk}" if milk else ""
            return (f"Alright, {state['name']}, here's your order: A {size} {temperature} {drink_type}{milk_text} "
                f"in a {cup_type}. Thank you! Order coming right up!")
        else:
            return "Please choose a valid option: \n[a] Hot \n[b] Iced"

    return "I'm sorry, I did not understand your selection. Please follow the instructions."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    user_id = request.json.get('user_id', 'default_user')

    # Call the coffee_bot function for conversation flow
    bot_response = coffee_bot(user_id, user_message)

    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)