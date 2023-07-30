import textbase
from textbase.message import Message
from textbase import models
import os
import json
from typing import List



api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OpenAI API key not found in the environment.")

models.OpenAI.api_key = api_key

SYSTEM_PROMPT = """Welcome to the Fitness Freak chatbot! 
I am here to help you achieve your fitness goals and lead a healthy lifestyle.
Whether you need personalized: 
- workout routines
- nutrition advice
- progress tracking
- motivational support
I've got you covered. 
Let's get started on your fitness journey..
I will take some of your personal information to make everything as personalized as possible. 
Please provide me with the following details:
1. Your current fitness level (beginner, intermediate, advanced).
2. Your fitness goals (e.g., weight loss, muscle gain, endurance improvement).
3. Any medical conditions or physical limitations I should consider.
4. How much time you can dedicate to working out each week.
5. Your preferred workout environment (gym, home, outdoors).
6. Any specific types of exercises you enjoy or would like to include.
7. Equipment availability (dumbbells, resistance bands, etc.).
8. How many rest days you prefer per week. 
9. Feel free to share as much detail as you can"""



QUESTIONS = [
    "1.Welcome to the Fitness Freak chatbot! "\
    "I am here to help you achieve your fitness goals and lead a healthy lifestyle."\
    "Whether you need personalized: "\
    "- workout routines"\
    "- nutrition advice"\
    "- progress tracking"\
    "- motivational support"\
    "I've got you covered. "\
    "Let's get started on your fitness journey.."\
    "I will take some of your personal information to make everything as personalized as possible.What is your current fitness level? (beginner, intermediate, advanced)",
    "2. What are your fitness goals? (e.g., weight loss, muscle gain, endurance improvement)",
    "3. Do you have any medical conditions or physical limitations that we should consider? If yes, please provide details.",
    "4. How much time can you dedicate to working out each week?",
    "5. What is your preferred workout environment? (gym, home, outdoors)",
    "6. Are there any specific types of exercises you enjoy or would like to include? If yes, please provide details.",
    "7. What equipment do you have available? (e.g., dumbbells, resistance bands, etc.)",
    "8. How many rest days do you prefer per week?",
    "9. How would you describe your current eating habits? (e.g., balanced, vegetarian, vegan, etc.)",
    "10. Do you have any dietary restrictions or food allergies? If yes, please specify.",
    "11. What are your favorite healthy foods or meals?",
    "12. Are there any foods you would like to include or avoid in your nutrition plan? If yes, please provide details.",
    "13. How many meals and snacks do you typically have in a day?",
    "14. Do you drink enough water throughout the day? If not, how much water do you consume on average?",
    "15. What are the specific metrics you want to track for your fitness progress? (e.g., weight, body measurements, strength levels, etc.)",
    "16. How often would you like to receive updates on your progress? (e.g., weekly, bi-weekly, monthly)",
    "17. Are you open to periodic fitness assessments to evaluate your progress?",
    "18. What inspires and motivates you to stay committed to your fitness goals?",
    "19. Have you achieved any significant fitness milestones in the past? If yes, tell us about them.",
    "20. What challenges or obstacles do you anticipate on your fitness journey, and how can we support you in overcoming them?",
    "21. How do you prefer to receive motivational support? (e.g., positive affirmations, goal reminders, inspirational quotes)"
]




@textbase.chatbot("fitness-freak-bot")
def on_message(message_history: List[Message], state: dict = None):
    print("system prompt", SYSTEM_PROMPT)
   
    if state is None or "counter" not in state:
        state = {"counter": 0, "user_info": {}}

    if state["counter"] == 0:
        user_greeting = message_history[-1].content
        state["user_info"]["Greeting"] = user_greeting

        question = QUESTIONS[state["counter"]]
        bot_response = question

        state["counter"] += 1
    elif state["counter"] < len(QUESTIONS):
        if len(message_history) > 0:
            user_answer = message_history[-1].content
            user_info_key = QUESTIONS[state["counter"] - 1]
            state["user_info"][user_info_key] = user_answer

        question = QUESTIONS[state["counter"]]
        bot_response = question

        state["counter"] += 1
    else:
        # Check if the user is asking for a specific functionality
        user_query = message_history[-1].content.lower()
        if "workout routine" in user_query:
            # Call the generate_personalized_workout_plan function
            workout_plan = personalized_workout_plan(state["user_info"], message_history)
            bot_response = workout_plan
        elif "nutrition advice" in user_query:
            # Call the nutrition_advice function
            nutrition = nutrition_advice(state["user_info"], message_history)
            bot_response = nutrition
        elif "progress tracking" in user_query:
            # Call the progress_tracking_info function
            progress = progress_tracking_info(state["user_info"], message_history)
            bot_response = progress
        elif "motivational support" in user_query:
            # Call the motivational_support function
            motivational = motivational_support(state["user_info"], message_history)
            bot_response = motivational
        else:
            # Provide the list of functionalities
            functionalities_list = "- workout routines\n- nutrition advice\n- progress tracking\n- motivational support"
            bot_response = f"Here are the functionalities I can help you with:\n{functionalities_list}"

    return bot_response, state


def personalized_workout_plan(user_info: dict,message_history) -> str:
    user_info_str = json.dumps(user_info, indent=2)
    workout_plan = "Here is the personal information of the user:{user_info_str}"\
              "You have to design a personalised workout plan for the user in such a way that is suitable for him taking in account all the personal information provided "\
              "below is an example of the structure of the workout plan in which way its expected from you"\
              "example-response:"\
                "Here's your personalized workout plan:\n\n" \
                   "- Monday: Cardio workout (30 mins)\n" \
                   "- Tuesday: Upper body strength training (45 mins)\n" \
                   "- Wednesday: Rest day\n" \
                   "- Thursday: Lower body strength training (45 mins)\n" \
                   "- Friday: Yoga and stretching (30 mins)\n" \
                   "- Saturday: Outdoor activities (e.g., hiking, cycling) (60 mins)\n" \
                   "- Sunday: Rest day\n" \
                   "\nRemember to warm up before each workout and cool down afterward. " \
                   "Stay hydrated and listen to your body. Have a great workout!"\
                   "things to remember, there's no need for any additional text like an apology or explanation. Just provide the plan as per the structure above."
    
    bot_response = models.OpenAI.generate(
        system_prompt=workout_plan,
        message_history=message_history,
        model="gpt-3.5-turbo",
        temperature=0.9
    )

    return bot_response    

def nutrition_advice(user_info: dict, message_history) -> str:
    user_info_str = json.dumps(user_info, indent=2)
    nutrition_advice = "Here is the personal information of the user:" + user_info_str + \
                       "You have to provide personalized nutrition advice based on the user's fitness level, goals, dietary preferences, and any medical conditions or limitations they may have." \
                       "Provide a well-balanced nutrition plan that aligns with the user's fitness goals and helps them achieve the desired results." \
                       "Remember to take into account any specific dietary requirements or preferences shared by the user." \
                       "things to remember, there's no need for any additional text like an apology or explanation. Just provide the advice as per the user's information."
    
    bot_response = models.OpenAI.generate(
        system_prompt=nutrition_advice,
        message_history=message_history,
        model="gpt-3.5-turbo",
        temperature=0.9
    )

    return bot_response

def progress_tracking_info(user_info: dict, message_history) -> str:
    user_info_str = json.dumps(user_info, indent=2)
    progress_info = "Here is the personal information of the user:" + user_info_str + \
                    "To effectively track progress, recommend the user to set clear and achievable fitness goals." \
                    "Guide them on how to measure and record their progress regularly." \
                    "Suggest using tools like fitness apps or journals to track workouts, weight, body measurements, and other relevant metrics." \
                    "Encourage the user to celebrate their achievements and stay consistent on their fitness journey." \
                    "things to remember, there's no need for any additional text like an apology or explanation. Just provide the guidance as per the user's information."
    
    bot_response = models.OpenAI.generate(
        system_prompt=progress_info,
        message_history=message_history,
        model="gpt-3.5-turbo",
        temperature=0.9
    )

    return bot_response

def motivational_support(user_info: dict, message_history) -> str:
    user_info_str = json.dumps(user_info, indent=2)
    motivational_support = "Here is the personal information of the user:" + user_info_str + \
                           "To provide motivational support, offer inspiring messages and positive reinforcement." \
                           "Remind the user of their fitness goals and the progress they have made so far." \
                           "Encourage them to stay consistent and remind them that small steps forward are still progress." \
                           "Use motivating language to boost their confidence and determination." \
                           "things to remember, there's no need for any additional text like an apology or explanation. Just provide the support as per the user's information."
    
    bot_response = models.OpenAI.generate(
        system_prompt=motivational_support,
        message_history=message_history,
        model="gpt-3.5-turbo",
        temperature=0.9
    )

    return bot_response

