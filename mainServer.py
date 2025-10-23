from flask import Flask, request, jsonify
# from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
# from pinecone import Pinecone
import os
import requests
from datetime import datetime
# import base64

from testbotOnlyGroq import askGroqWhichTable
# from dbHelper import connect_to_database
# import dbHelper
import dbHelper_mock
import testbotOnlyGroq

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")
# MYSQL_HOST = os.getenv("MYSQL_HOST")
# MYSQL_USER = os.getenv("MYSQL_USER")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
# MYSQL_DB = os.getenv("MYSQL_DATABASE")

app = Flask(__name__)

# pc = Pinecone(api_key=PINECONE_API_KEY)
# pcahwanamContextIndex = pc.Index("aahwanamcontext")
# print("Connected To VectorIndex")

# Init embedding model
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory chat history
messages = []
chat_history = {}  # user_id: [msg1, msg2, ...]

# def get_embedding(text):
#     return embedding_model.encode(text).tolist()

# def similaritySearchPineConeQueryHelper(pcobject, userinput):
#     vector = get_embedding(userinput)
#     result = pcobject.query(vector=vector, top_k=5, include_metadata=True)
#     return [match.metadata['text'] for match in result.matches if match.metadata and 'text' in match.metadata]

@app.route("/chat", methods=["POST"])
def chat():
    data = dict()
    data = request.get_json()
    print(f"Bot Active: {data.get("userPrompt", "")}")
    prompt = data.get("userPrompt", "")
    user_id = data.get("user_id", "default_user")
    # print(prompt)

    messages.append("User: " + prompt)
    print(f"Client Topic: {messages}")
    # if user_id not in chat_history:
    #     chat_history[user_id] = []
    # chat_history[user_id].append("User: " + prompt)

    realtimedata = []
    table = askGroqWhichTable(prompt, model='llama-3.3-70b-versatile')

    if '1' in table:
        realtimedata.append(dbHelper_mock.print_joined_service_categories())
    if '2' in table:
        realtimedata.append(dbHelper_mock.getServicePackages())
    if '3' in table:
        cityorstste = table.split('^')[-1].strip('] ')
        realtimedata.append(dbHelper_mock.getservicesbylocation(cityorstste))

    # context_chunks = similaritySearchPineConeQueryHelper(pcahwanamContextIndex, prompt)
    # context_chunks = "Unable te fetch context from the pinecone"
    context_chunks = "aahwanam provides services for different events like Birthday, marriage, family functions etc"
    context_text = "\n".join(context_chunks)

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

    use the date and time as reference in case user says any particulars about the events date, time or day.

    **RESPONSE RULES:** 
    1. Keep REPLIES CONCISE. Avoid long paragraphs.
    2. If user asks about services, list only **top 4 relevant services** in this format:
    ^Services
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
     **At the END OF THE PROMPT GIVE THREE QUICK RESPONSES that the **USER MIGHT ANSWER TO YOU BASED ON YOUR QUESTIONS** so that it can help the user to not type the prompts every time.start the QUICK RESPONSE PROMPT WITH "->" SYMBOL.**
    7. If the USER PROMPT :"{prompt}" is requesting about any of this items
    **photographer, chef, bartender, makeup, entertainment, mehendi, decor, pandit, einvitation, valet IF THE CONSERVATION IS NOT ABOUT ANY OF THIS DONT ADD ANYTHING AT THE END
    THEN GIVE ONE OF THE MOST RELEVANT ITEM ONLY FROM THE ABOVE 10 ITEMS AT THE END WITH /item IN A NEW LINE. IF NON OF THIS MATCHES DONT ADD /item AT THE END**
    8. if the user Conversation is about Complaint then as about event completed or not and ask about the event date and complaint data at the end say that your complaint received and our team will reach you out and say thank you and then ask if the user want any thing else 
    9. If irrelevant, say:
    "Sorry, I don't know about that. Please ask something related to Aahwanam."
    """

    BotResponse = testbotOnlyGroq.sendGroqRequest(prompt, SystemPromptForFinalLLMRequestprompt, model='llama-3.3-70b-versatile')
    # chat_history[user_id].append("Bot: " + BotResponse)
    print("This is the bot response: "+BotResponse)
    print("This is the User chat Context: ".join(messages))
    messages.append("ChatBot: " + BotResponse)
    return jsonify({"reply": BotResponse})

@app.route("/chatdummy", methods=["POST"])
def chatdummy():
    res = {"reply":"Hii there \n ->How \n->when \n->where \n chef"}
    return res
# @app.route("/imagen", methods=["POST"])
# def imagen():
#     try:
#         data = request.get_json()
#         prompt = data.get("prompt", "")
#         if not prompt:
#             return jsonify({"error": "No prompt provided"}), 400

#         # Call HuggingFace API
#         hf_api_url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
#         headers = {
#             "Authorization": "Bearer hf_ZGwekUXZpyaQhCydMRLGXWBNvvwZzcHBF",  # Replace with your token
#             "Content-Type": "application/json",
#         }
#         response = requests.post(hf_api_url, headers=headers, json={"inputs": prompt})

#         if response.status_code == 200:
#             image_bytes = response.content
#             # Convert image to base64 so Flutter can display it easily
#             image_base64 = base64.b64encode(image_bytes).decode("utf-8")
#             return jsonify({"image_url": f"data:image/png;base64,{image_base64}"})
#         else:
#             return jsonify({"error": "Image generation failed", "details": response.text}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
