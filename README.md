**##Fitness Freak Chatbot Documentation**

The "Fitness Freak" chatbot has been developed to assist users in their fitness journey by offering personalized:
**-workout routines
-nutrition advice
-progress tracking and 
-motivational support.** 
This chatbot relies on the advanced capabilities of the OpenAI GPT-3.5 Turbo model to generate responses based on user inputs and **personal information**.

**##Outlined below is an in-depth explanation of the chatbot's code and its functionalities:**

**System Prompt and User Questions:**
The chatbot commences by displaying a system prompt using the SYSTEM_PROMPT variable. 
This prompt serves to introduce the chatbot and educate the users with its capabilities.

**A list of user questions (QUESTIONS) is provided, covering various aspects of the user's personal information required for customization.**

**Chatbot Function:**
The core functionality of the chatbot is implemented through the on_message function, which takes two arguments: message_history (a list of previous messages in the conversation) and state (a dictionary to store conversation state).

**Conversation State:**
To keep track of user responses and progress throughout the questionnaire, the chatbot maintains a conversation state. 
This state is stored in the state dictionary and includes information such as the current question counter and the user's personal details.

**Handling User Responses:**
Utilizing the state, the chatbot identifies the current question and retrieves the subsequent question from the QUESTIONS list.

After presenting the user with the next question, the chatbot awaits their response.

**Processing User Inputs:**
Following each user response, the chatbot updates the state with the user's answer corresponding to the current question.
The chatbot then increments the counter in the state to progress to the subsequent question.

**Functionalities and Personalized Responses:**
Once all the necessary personal information is collected, the chatbot examines the user's query to determine if they are seeking a specific functionality 
(workout routine, nutrition advice, progress tracking, or motivational support).

**Function Calls for Specific Functionalities:**
When the user requests a specific functionality, the chatbot invokes the relevant function (personalized_workout_plan, nutrition_advice, progress_tracking_info, motivational_support). 
These functions provide personalized responses based on the user's information as it incorporates the user's personal information as the system prompt to ensure **personalized recommendations.**

The generated responses are then returned to the user as the chatbot's reply.



# Fitness Freak Chatbot using Textbase

✨ Textbase is a framework for building chatbots using NLP and ML. ✨

## Installation
Run the following command:
```bash
git clone https://github.com/cofactoryai/textbase
cd textbase
poetry install
```

## Start development server
Run the following command:

```bash
poetry run python textbase/textbase_cli.py test main.py
```

Now go to [http://localhost:4000](http://localhost:4000) and start chatting with our bot!

