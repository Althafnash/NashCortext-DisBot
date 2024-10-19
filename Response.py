import random 
from Knowledge_base import knowledge_base

def get_response(user_message: str) -> str:
    user_message = user_message.lower()

    # Simple keyword-based responses
    if "/hello" in user_message:
        Hello = [
            "Hey!😊",
            "Hi!👋",
            "Sup!🙌"
        ]
        return random.choice(Hello)
    elif "/bye" in user_message:
        good = [
            "Goodbye 👋",
            "bye 👋"
        ]
        return random.choice(good)
    elif "/joke" in user_message:
        Jokes = [
            "Why don't scientists trust atoms? Because they make up everything! 😄",
            "Why did the chicken join a band? Because it had the drumsticks!  🐔🥁",
            "What do you call fake spaghetti? An impasta! 🍝"
        ]
        return random.choice(Jokes)
    elif "/quotes" in user_message:
        Quotes = [
            "The best time to plant a tree was 20 years ago. The second best time is now. 🌳",
            "Do not watch the clock. Do what it does. Keep going. ⏳",
            "The only way to do great work is to love what you do. 💼"
        ]
        return random.choice(Quotes)
    
    elif "/access knowledge base" in user_message:
        response = "Here is what I found:\n"
        for key, value in knowledge_base.items():
            if key in user_message:
                response += f"{key}: {value}\n"
        if response == "Here is what I found:\n":
            response = "No matching knowledge found."
        return response

    
    else:
        return "Sorry, I don't understand that. Can you try asking something else? 🤔"