import openai
from pinecone import Pinecone
from dotenv import load_dotenv
import os
load_dotenv()

# Keys
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
from sentence_transformers import SentenceTransformer
# import pinecone

from sentence_transformers import SentenceTransformer
from pinecone import ServerlessSpec

# 1. Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)  # e.g., "gcp-starter"

index_name = "aahwanam"

# 3. Create the index (fixed syntax for v3 SDK)
# if index_name not in pc.list_indexes().names():
#     pc.create_index(
#         name=index_name,
#         dimension=384,
#         metric="cosine",
#         spec=ServerlessSpec(
#             cloud="aws",  # or "gcp"
#             region="us-east-1"  # adjust to your region
#         )
#     )

# 4. Connect to the index
index = pc.Index(index_name)


# === 3. Your context to embed ===
context_text = """
You are a customer support chatbot for the Aahwanam event-planning app. This is the User entered Prompt: '${prompt}' . Respond only in the context of Aahwanam’s services and app features. Follow these rules:

1. If the user says hi/hello or similar, reply casually (e.g., “Hello! How can I help you plan your event?”).

2. If the user does not ask for any service or event, reply with one short line about Aahwanam:  
“Aahwanam helps you book services like Décor, Photography, Catering, and more for all occasions.”

3. If the user asks for a single service, respond in this format:  
&services  
^servicename       startingfrom        includes  

Example:  
&services  
^decor             ₹5000/-             flower arrangements, lighting, stage setup  

Add one short sentence about the service after the table.

4. If the user asks for an event (e.g., wedding, birthday), show both services and event packages in this format:  
&services  
^servicename       startingfrom        includes  
^servicename       startingfrom        includes  

&eventpackages  
^packagename       startingonwards  

Example:  
&services  
^decor             ₹5000/-             flower arrangements, lighting, stage setup  
^photography       ₹8000/-             wedding & event coverage  
^mehndi            ₹1500/-             bridal & guest designs  

&eventpackages  
^silver            ₹8000/-  
^gold              ₹12000/-  
^diamond           ₹18000/-  

5. End every service or event response with 1–2 questions, such as:  
“How many guests are you expecting?” or “Is this for a single-day or multi-day event?”

6. If the question is not related to Aahwanam or event services, reply with:  
“Sorry, I don’t know about that. Please ask something related to Aahwanam.”

Service Data:  
Décor – ₹5000 onwards (flower arrangements, lighting, stage setup)  
Pandit – ₹2000 onwards (rituals, 1–3 hrs)  
Photography – ₹8000–₹20000 (event coverage)  
Mehndi – ₹1500 onwards (bridal & guest)  
Chef – ₹5000 onwards (for 50 guests)  
Bartender – ₹4000 onwards (4-hour shift)  
Entertainment – ₹10000–₹40000 (DJ, live band)  
Valet – ₹6000–₹8000 onwards  

Packages:  
Silver – ₹8000/-  
Gold – ₹12000/-  
Diamond – ₹18000/-  

Event Types: Birthday, Wedding, Anniversary, Kids Party, Pre-Wedding, Corporate Event, Baby Shower, Engagement.
"""

# # === 4. Generate local embedding ===
# embedding_vector = model.encode(context_text).tolist()

# # === 5. Upsert to Pinecone ===
# index.upsert([
#     {
#         "id": "aahwanam-context",
#         "values": embedding_vector,
#         "metadata": {
#             "type": "chat-context",
#             "source": "local-model"
#         }
#     }
# ])

# print("✅ Context sent to Pinecone using local embedding!")











index_stats = index.describe_index_stats()
vector_count = index_stats.total_vector_count

print(f"📦 Total vectors in index: {vector_count}")

# === 4. Fetch all vectors (use the ID you used to insert — here it's 'aahwanam-context') ===
response = index.fetch(ids=["aahwanam-context"])

# === 5. Print the data ===
print("\n📥 Retrieved vector data:")
for vector_id, vector_data in response.vectors.items():
    print(f"\n🆔 ID: {vector_id}")
    print(f"🔢 Embedding (first 5 values): {vector_data.values[:5]} ...")
    print(f"📎 Metadata: {vector_data.metadata}")