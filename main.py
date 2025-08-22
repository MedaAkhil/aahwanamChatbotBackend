# from fastapi import FastAPI, Request
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
import mysql.connector
# import uuid
import os
import requests
import json

from testbotOnlyGroq import askGroqWhichTable
from dbHelper import connect_to_database

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
    print("pinecone query started")
    vector = get_embedding(userinput)
    result = pcobject.query(vector=vector, top_k=5, include_metadata=True)
    print(f"pinecone query ended{result}")
    return [match.metadata['text'] for match in result.matches if match.metadata and 'text' in match.metadata]

if __name__ == "__main__":
    conn = connect_to_database()
    pc = Pinecone(api_key=PINECONE_API_KEY)#, 
    pcahwanamContextIndex = pc.Index("aahwanam")
    while True:
        prompt = input("You:")


        realtimedata = []
        table = askGroqWhichTable(prompt)

        if '1' in table:
            pass
        if '2' in table:
            pass
        if '3' in table:
            cityorstste = table.split('^')[-1].strip('] ')
        


        context_chunks = similaritySearchPineConeQueryHelper(pcahwanamContextIndex, prompt)
        context_text = "\n".join(context_chunks)
        print(f"this is the data received from the PineCone for the user prompt: {context_text}")

        prompt = f"""
        You are a customer support chatbot for the Aahwanam event-planning app. 
        Use only the context and services below to answer the user's prompt.

        This is the context data for the aahwanam platform => {context_text}

        This is the realtime data about the services (or) the budget friendly packages offered by the 
        {realtimedata}

        User prompt: "{prompt}"

        Respond in the following format if applicable:
        1. Reply casually to greetings.
        2. If no services are mentioned, say: "Aahwanam helps you book services like Décor, Photography, Catering, and more for all occasions."
        3. If user asks for a service, respond with a service list:
        &services
        ^servicename    ₹price    includes

        4. If user asks about event types (wedding, birthday), show:
        &services
        ...
        &eventpackages
        ^silver ₹8000/-
        ...

        5. If user asks about packages show:
        &eventpackages
        ^silver ₹8000/-
        ...

        6. Always end with 1-2 questions to keep conversation going.
        7. If irrelevant, say: "Sorry, I don’t know about that. Please ask something related to Aahwanam."
        """
        




