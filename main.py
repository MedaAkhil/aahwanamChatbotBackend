# from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
import mysql.connector
# import uuid
import os
import requests
import json
from datetime import datetime

from testbotOnlyGroq import askGroqWhichTable
from dbHelper import connect_to_database
import dbHelper
import dbHelper_mock
import testbotOnlyGroq

# Load env variables
load_dotenv()

# Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DATABASE")

# Init FastAPI
# app = FastAPI()

# Init Pinecone
# pc = Pinecone(api_key=PINECONE_API_KEY)#,
            #   environment=PINECONE_ENV)
# pinecone_index = pc.Index("aahwanam")  # Must be created with dim=384

# Init MySQL
# db = mysql.connector.connect(
#     host=MYSQL_HOST,
#     user=MYSQL_USER,
#     password=MYSQL_PASSWORD,
#     database=MYSQL_DB
# )

# Init local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return embedding_model.encode(text).tolist()

# def query_pinecone(user_input):
#     print("pinecone query started")
#     vector = get_embedding(user_input)
#     result = pinecone_index.query(vector=vector, top_k=5, include_metadata=True)
#     print(f"pinecone query ended{result}")
#     return [match.metadata['text'] for match in result.matches if match.metadata and 'text' in match.metadata]


# def get_services_from_mysql():
#     print("Mysql query started")
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT service_name, description FROM services")
#     print("mysql query ended")
#     return cursor.fetchall()

# def save_chat(user_id, user_msg, bot_msg):
#     cursor = db.cursor()
#     chat_id = str(uuid.uuid4())
#     cursor.execute(
#         "INSERT INTO chat_history (id, user_id, user_msg, bot_msg) VALUES (%s, %s, %s, %s)",
#         (chat_id, user_id, user_msg, bot_msg)
#     )
#     db.commit()

def send_to_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]




# @app.post("/chat")
# async def chat(request: Request):
#     data = await request.json()
#     user_input = data['message']
#     user_id = data['user_id']

#     # Step 1: Query context
#     context_chunks = query_pinecone(user_input)
#     context_text = "\n".join(context_chunks)

#     # Step 2: Get live service data
#     # service_data = get_services_from_mysql()
#     # service_text = "\n".join([
#     #     f"{svc['service_name']} – ({svc['description']})"
#     #     for svc in service_data
#     # ])
#     print(f"context_text:{context_text}")
#     # Step 3: Build final prompt
#     prompt = f"""
# You are a customer support chatbot for the Aahwanam event-planning app. 
# Use only the context and services below to answer the user's prompt.

# &context
# {context_text}

# &services
# {service_text}

# User prompt: "{user_input}"

# Respond in the following format if applicable:
# 1. Reply casually to greetings.
# 2. If no services are mentioned, say: "Aahwanam helps you book services like Décor, Photography, Catering, and more for all occasions."
# 3. If user asks for a service, respond with a service list:
# &services
# ^servicename    ₹price    includes

# 4. If user asks about event types (wedding, birthday), show:
# &services
# ...
# &eventpackages
# ^silver ₹8000/-
# ...

# 5. If user asks about packages show:
# &eventpackages
# ^silver ₹8000/-
# ...

# 6. Always end with 1-2 questions to keep conversation going.
# 7. If irrelevant, say: "Sorry, I don’t know about that. Please ask something related to Aahwanam."
# """

#     # Step 4: Call Groq
#     bot_reply = send_to_groq(prompt)

#     # Step 5: Save to DB
#     # save_chat(user_id, user_input, bot_reply)

#     return {"reply": bot_reply}







def similaritySearchPineConeQueryHelper(pcobject, userinput):
    # print("pinecone query started")
    vector = get_embedding(userinput)
    result = pcobject.query(vector=vector, top_k=5, include_metadata=True)
    # print(f"pinecone query ended {result}")
    return [match.metadata['text'] for match in result.matches if match.metadata and 'text' in match.metadata]


if __name__ == "__main__":
    # conn = connect_to_database()
    pc = Pinecone(api_key=PINECONE_API_KEY)#, 
    pcahwanamContextIndex = pc.Index("aahwanamcontext")
    print("Connected To VectorIndex")
    messages = []
    while True:
        prompt = input("You:")
        messages.append("User: "+prompt)

        realtimedata = []
        table = askGroqWhichTable(prompt, model='llama-3.3-70b-versatile')

        if '1' in table:
            # realtimedata.append(dbHelper.print_joined_service_categories(conn))
            realtimedata.append(dbHelper_mock.print_joined_service_categories())
        if '2' in table:
            # realtimedata.append(dbHelper.getServicePackages(conn))
            realtimedata.append(dbHelper_mock.getServicePackages())
        if '3' in table:
            cityorstste = table.split('^')[-1].strip('] ')
            # realtimedata.append(dbHelper.getservicesbylocation(conn, cityorstste))
            realtimedata.append(dbHelper_mock.getservicesbylocation(cityorstste))
        


        context_chunks = similaritySearchPineConeQueryHelper(pcahwanamContextIndex, prompt)
        context_text = "\n".join(context_chunks)
        # print(f"these are the content chunks:{context_text}")
        # print(f"this is the data received from the PineCone for the user prompt: {context_text}")
        # print(f"this is the Realtime data received from SQL data context: {realtimedata}")

        # SystemPromptForFinalLLMRequestprompt = 
        # f"""
        # You are a customer support chatbot for the Aahwanam event-planning app. 
        # Use only the context and services below to answer the user's prompt.

        # This is the context data for the aahwanam platform => {context_text}

        # This is the realtime data about the services (or) the budget friendly packages offered by the 
        # {realtimedata}
        # {"this is the user chat history with the bot: ".join(messages)}
        # User prompt: "{prompt}"

        # Respond in the following format if applicable:
        # 1. Reply casually to greetings.
        # 2. If no services are mentioned, say: "Aahwanam helps you book services like Décor, Photography, Catering, and more for all occasions."
        # 3. If user asks for a service, respond with a service list:
        # &services
        # ^servicename    ₹price    includes

        # 4. If user asks about event types (wedding, birthday), show:
        # &services
        # ...
        # &eventpackages
        # ^silver ₹8000/-
        # ...

        # 5. If user asks about packages show:
        # &eventpackages
        # ^silver ₹8000/-
        # ...

        # 6. Always end with 1-2 questions to keep conversation going.
        # 7. If irrelevant, say: "Sorry, I don’t know about that. Please ask something related to Aahwanam."
        # """
        # print(f"""This is the context_text:{context_text}\n\n\n\n\n\n\n\nThis is the RealTimeData:{realtimedata}\n\n\n\n\n\n\n\n\nThis is the messages:{messages}\n\n\n\n\n\n\nThis is todays date: {datetime.now()}""")
        SystemPromptForFinalLLMRequestprompt = f"""
        **You are a customer support chatbot for the Aahwanam event-planning app You main Work is to give the user a best and budget friendly service and if any question asked answer them.**
        Keep answers **short, minimal text, and mostly in list format**.

        This is the context data for the Aahwanam platform => {context_text}

        This is the realtime data about the services or budget-friendly packages offered => {realtimedata}
        Fist you need to gather the below information from the user:
        ->event Type or the event name?
        ->Date, Time and Duration Of the Event?
        ->What Services Required?

        **collect this info first by asking the user this question one by one. dont ask all the question at a time**
        User CHAT HISTORY: {" | ".join(messages)}
        User prompt: "{prompt}: Date and Time Of the user Prompt{datetime.now()} YOU SHOULD ONLY CONSIDER THIS WHILE CHECKING IF THE DATE OF THE USER EVENT AND THE DATE OF THE VENDORS IS CORRECTLY THEIR LIKE IF THE USER WANT SERVICE ON A PARTICULAR YOU SHOULD CONSODER THE AVAILABLE DATES OF THE VENDORS TO SUGGEST THE AVAILABLE VENDORS AND THEIR SERVICE"
        **AT THE STARTING OF THE RESPONSE GIVE A RESPONSE RELATED TO THE USER PREVIOUS PROMPT if IF THE PROMPT REALLY HAS SOME WANTED INFORMATION, SO THAT THE USER GET TO KNOW THAT YOU UNDERSTOOD HIM**
        use the date and time as reference in case user says any particulars about the events date, time or day.

        Response rules:
        1. Keep replies concise. Avoid long paragraphs.
        2. If user asks about services, list only **top 4 relevant services** in this format:
        ^Services
        &servicename - ₹price - includes
        &servicename - ₹price - includes
        &servicename - ₹price - includes
        &servicename - ₹price - includes

        4. If user asks only about packages, respond:
        ^EventPackages
        &packagename - ₹packagePrice - ...
        &Package - ₹packageprice - ...
        &package - ₹packageprice - ...

        5. If no services are mentioned, say:
        "Aahwanam helps you book services like Décor, Photography, Catering, and more for all occasions."

        6. Always end response with 1 short follow-up question to keep conversation going.
         **At the END OF THE PROMPT give THREE QUICK RESPONSES that the USER MIGHT ANSWER TO YOU BASED ON YOUR QUESTIONS so that it can help the user to not type the prompts every time.start the QUICK RESPONSE PROMPT WITH "->" SYMBOL.**
        7. If irrelevant, say:
        "Sorry, I don't know about that. Please ask something related to Aahwanam."
        """

        # print(f"=============================>{SystemPromptForFinalLLMRequestprompt}")
        BotResponse = ""+testbotOnlyGroq.sendGroqRequest(prompt, SystemPromptForFinalLLMRequestprompt, model='llama-3.3-70b-versatile') 
        print("Bot:"+BotResponse)

















#         SystemPromptForFinalLLMRequestprompt = f"""
# You are a customer support chatbot for the Aahwanam event-planning app. 
# Keep answers **short, minimal text, and mostly in list format**.

# This is the context data for the Aahwanam platform => {context_text}

# This is the realtime data about the services or budget-friendly packages offered => {realtimedata}

# User chat history: {" | ".join(messages)}
# User prompt: "{prompt}: Date and Time Of the user Prompt{datetime.now()}"
# use the date and time as reference in case user says any particulars about the events date, time or day.

# Response rules:
# 1. Keep replies concise. Avoid long paragraphs.
# 2. If user asks about services, list only **top 4 relevant services** in this format:
# ^Services
# &servicename – ₹price – includes
# &servicename – ₹price – includes
# &servicename – ₹price – includes
# &servicename – ₹price – includes

# 3. If user asks about event types (wedding, birthday), show services + packages like this:
# ^Services
# &Décor – ₹5000 – includes flowers
# &Photography – ₹8000 – includes candid photos
# ^EventPackages
# &Silver – ₹8000 – includes Décor + Photography
# &Gold – ₹15000 – includes Décor + Photography + Catering

# 4. If user asks only about packages, respond:
# ^EventPackages
# &Silver – ₹8000 – ...
# &Gold – ₹15000 – ...
# &Platinum – ₹25000 – ...

# 5. If no services are mentioned, say:
# "Aahwanam helps you book services like Décor, Photography, Catering, and more for all occasions."

# 6. Always end response with 1 short follow-up question to keep conversation going.
# 7. If irrelevant, say:
# "Sorry, I don’t know about that. Please ask something related to Aahwanam."
# """