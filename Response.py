import random 
from Knowledge_base import knowledge_base
from datetime import datetime

def log_message(username : str , user_message : str):
    with open("user_messages.log","a") as log_file:
        log_file.write(f"{username} : {user_message} \n")

def get_time() -> str :
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"the current time is {current_time}"

def Calculator(operation: str , firstnumber:int , secondnumber:int):
    if operation == "add":
        return firstnumber + secondnumber
    elif operation == "sub":
        return firstnumber - secondnumber
    elif operation == "multiply":
        return firstnumber * secondnumber
    elif operation == "divide":
        return firstnumber / secondnumber
    else:
        return "Not a valid operation"

def get_response(user_message: str,username: str) -> str:
    user_message = user_message.lower()
    log_message(username, user_message)

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
    
    elif "/time" in user_message:
        return get_time()
    
    elif "/calculator" in user_message:
        parts = user_message.split()
        
        if len(parts) != 4:  # Ensure the user provided the correct number of arguments
            return "Usage: /calculator [operation] [number1] [number2]"

        operation = parts[1]
        try:
            firstnumber = int(parts[2])
            secondnumber = int(parts[3])
            result = Calculator(operation=operation, firstnumber=firstnumber, secondnumber=secondnumber)
            return str(result)  
        except ValueError:
            return "Please provide valid numbers."

    else:
        return "Sorry, I don't understand that. Can you try asking something else? 🤔"