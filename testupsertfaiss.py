# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
# import os
# from dotenv import load_dotenv
# import shutil
# shutil.rmtree("my_vector_db")
# exit()
# print("hello")
# # Load environment variables (if needed)
# load_dotenv()
# raw_text = """
#         You are a customer support chatbot for the “Aahwanam” event-planning app. The user interface includes the following screens and flows:
        
#         • **Home / Services screen** – Shows service categories like Décor, Pandit, Photography, Mehndi, Bartender, Chef, Entertainment; users can browse by category, see trending providers and packages, view minimum pricing (e.g. ₹5,000 onwards).
        
#         • **Category browsing** – Horizontal category list, then vendor cards grouped by “Decorators in your city,” “Mehndi artists for you,” “Trending,” and “Packages for all events.” Each card shows ratings, price, and vendor name.
        
#         • **Package selection flow** – User picks a service (e.g., Photography → Pre‑wedding), then chooses one of several packages (Silver ₹8,000; Gold ₹12,000; Diamond ₹20,000) with included features and ratings.
        
#         • **Booking form** – After selecting a package, the user picks an event date & time (calendar/time picker), enters event address, then can “Add to cart” or “Book Service”.
        
#         • **Vendor interface confirmation** – When vendor logs in or builds profile, there’s a message: “Your profile built successfully, wait for admin approval. After verification you will get leads.”
        
#         • **Vendor themes/edit interface** – Vendors can configure service details, set themes and pricing (e.g., kids‑birthday decoration ₹2,800 / ₹4,000 etc.), add gallery items, choose “Edit” or “Add New Item”.
        
#         • **Settings page** – Vendors can toggle notifications, change password, enter a WhatsApp mobile number for auto‑sharing booking details, enable/disable auto‑share, and log out.
        
#         **Service Details:**
        
#         1. **Décor**:
#         The Décor service offers decorations for events like weddings and parties. It includes flower arrangements, lighting, and stage setups. Pricing starts from ₹5,000. Setup time is typically 3 to 6 hours.
        
#         2. **Pandit**:
#         The Pandit service provides experienced pandits for religious rituals. The service starts at ₹2,000, with rituals lasting between 1 to 3 hours. Book via the 'Pandit' section in the app.
        
#         3. **Photography**:
#         Photography packages include pre-wedding, wedding, and event coverage. Prices range from ₹8,000 to ₹20,000, depending on the package. Service duration varies from 4 to 8 hours.
        
#         4. **Mehndi**:
#         Mehndi services for bridal and guest designs. Prices start from ₹1,500 for basic designs. Bridal mehndi may take 3-4 hours, while guest designs take about 1-2 hours.
        
#         5. **Chef**:
#         Catering services offering different cuisines for events. Prices start from ₹5,000 for 50 guests. Service duration is typically 3 to 5 hours depending on the event scale.
        
#         6. **Bartender**:
#         Bartenders for events, with pricing starting at ₹4,000 for 4-hour shifts. The service typically lasts 3 to 6 hours.
        
#         7. **Entertainment**:
#         DJ, live bands, and other entertainers for events. Prices range from ₹10,000 to ₹40,000 based on the type of entertainment and duration (typically 2-6 hours).
        
#         **Additional Service Information:**
        
#         8. **Valet Parking**:
#         - **Royal Valet Service**: ₹8,000 onwards (for luxury events with professional valet service).
#         - **Standard Valet**: ₹6,000 onwards.
        
#         9. **Event Type Information**:
#         - **Event Types**: Birthday, Wedding, Anniversary, Kids Party, Pre-Wedding, Corporate Event, Baby Shower, Engagement.
        
#         **Event Package Information:**
        
#         - **Silver Package**: ₹8,000 onwards, basic services like photography, makeup, and valet.
#         - **Gold Package**: ₹12,000 onwards, upgraded services with premium photography and makeup.
#         - **Diamond Package**: ₹18,000 onwards, premium services including photography, videography, valet, and entertainment.
        
#         **Event Add-Ons**:
#         - **Balloon Decoration**: Kids Special, Floral, Love Theme
#         - **Photography**: Pre-Wedding, Wedding, Baby Photoshoot.
#         - **Entertainment**: DJ, Choreography, Live Band.
        
#         **User Instructions**: 
#         - Provide pricing, services, and details related to **Aahwanam's event services**.
#         - Always respond in the context of the app's offerings. If the question is not related to the services or app flow, reply with: 
#         “Sorry, I don’t know about that. Please ask something related to 'Aahwanam’.”
#     """
# # Split text into chunks
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
# documents = splitter.create_documents([raw_text])

# # Use updated HuggingFace Embeddings class
# embedding_model = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )

# # Create and save FAISS vector store
# vector_db = FAISS.from_documents(documents, embedding_model)
# vector_db.save_local("my_vector_db")











# # Load the vector DB
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# vector_db = FAISS.load_local("my_vector_db", embedding_model, allow_dangerous_deserialization=True)

# # Get internal FAISS index and document store
# faiss_index = vector_db.index
# stored_texts = vector_db.docstore._dict  # This is a dict: {document_id: Document}

# # Print embedding vectors
# import numpy as np

# # 1. FAISS index contains raw numpy array of embeddings
# embedding_vectors = faiss_index.reconstruct_n(0, faiss_index.ntotal)

# # 2. Loop through each document and its embedding
# for i, (doc_id, doc_obj) in enumerate(stored_texts.items()):
#     print(f"\n📄 Document {i+1}:")
#     print("Text:", doc_obj.page_content)
#     print("Embedding:", embedding_vectors[i])
#     print("-" * 50)











import numpy as np

# Load the vector DB
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.load_local("my_vector_db", embedding_model, allow_dangerous_deserialization=True)

# Get internal index and documents
faiss_index = vector_db.index
stored_texts = vector_db.docstore._dict  # Dictionary: {doc_id: Document}

# Total number of vectors (i.e., chunks)
num_vectors = faiss_index.ntotal
num_documents = len(stored_texts)

print(f"🔢 Total Embedding Vectors in FAISS Index: {num_vectors}")
print(f"📚 Total Documents Stored: {num_documents}")
print("=" * 60)

# Reconstruct all embeddings
embedding_vectors = faiss_index.reconstruct_n(0, num_vectors)

# Loop through and display info
for i, (doc_id, doc_obj) in enumerate(stored_texts.items()):
    doc_text = doc_obj.page_content
    vector = embedding_vectors[i]
    num_tokens = len(doc_text.split())

    print(f"\n📄 Document {i+1}")
    print(f"🔠 Tokens (words): {num_tokens}")
    print(f"📝 Text: {doc_text}")
    print(f"📈 Embedding (first 10 dims): {vector[:10]} ...")
    print("-" * 60)






















raw_text = """
        The user interface includes the following screens and flows:
        
        • **Home / Services screen** – Shows service categories like Décor, Pandit, Photography, Mehndi, Bartender, Chef, Entertainment; users can browse by category, see trending providers and packages, view minimum pricing (e.g. ₹5,000 onwards).
        
        • **Category browsing** – Horizontal category list, then vendor cards grouped by “Decorators in your city,” “Mehndi artists for you,” “Trending,” and “Packages for all events.” Each card shows ratings, price, and vendor name.
        
        • **Package selection flow** – User picks a service (e.g., Photography → Pre‑wedding), then chooses one of several packages (Silver ₹8,000; Gold ₹12,000; Diamond ₹20,000) with included features and ratings.
        
        • **Booking form** – After selecting a package, the user picks an event date & time (calendar/time picker), enters event address, then can “Add to cart” or “Book Service”.
        
        • **Vendor interface confirmation** – When vendor logs in or builds profile, there’s a message: “Your profile built successfully, wait for admin approval. After verification you will get leads.”
        
        • **Vendor themes/edit interface** – Vendors can configure service details, set themes and pricing (e.g., kids‑birthday decoration ₹2,800 / ₹4,000 etc.), add gallery items, choose “Edit” or “Add New Item”.
        
        • **Settings page** – Vendors can toggle notifications, change password, enter a WhatsApp mobile number for auto‑sharing booking details, enable/disable auto‑share, and log out.
        
        **Service Details:**
        
        1. **Décor**:
        The Décor service offers decorations for events like weddings and parties. It includes flower arrangements, lighting, and stage setups. Pricing starts from ₹5,000. Setup time is typically 3 to 6 hours.
        
        2. **Pandit**:
        The Pandit service provides experienced pandits for religious rituals. The service starts at ₹2,000, with rituals lasting between 1 to 3 hours. Book via the 'Pandit' section in the app.
        
        3. **Photography**:
        Photography packages include pre-wedding, wedding, and event coverage. Prices range from ₹8,000 to ₹20,000, depending on the package. Service duration varies from 4 to 8 hours.
        
        4. **Mehndi**:
        Mehndi services for bridal and guest designs. Prices start from ₹1,500 for basic designs. Bridal mehndi may take 3-4 hours, while guest designs take about 1-2 hours.
        
        5. **Chef**:
        Catering services offering different cuisines for events. Prices start from ₹5,000 for 50 guests. Service duration is typically 3 to 5 hours depending on the event scale.
        
        6. **Bartender**:
        Bartenders for events, with pricing starting at ₹4,000 for 4-hour shifts. The service typically lasts 3 to 6 hours.
        
        7. **Entertainment**:
        DJ, live bands, and other entertainers for events. Prices range from ₹10,000 to ₹40,000 based on the type of entertainment and duration (typically 2-6 hours).
        
        **Additional Service Information:**
        
        8. **Valet Parking**:
        - **Royal Valet Service**: ₹8,000 onwards (for luxury events with professional valet service).
        - **Standard Valet**: ₹6,000 onwards.
        
        9. **Event Type Information**:
        - **Event Types**: Birthday, Wedding, Anniversary, Kids Party, Pre-Wedding, Corporate Event, Baby Shower, Engagement.
        
        **Event Package Information:**
        
        - **Silver Package**: ₹8,000 onwards, basic services like photography, makeup, and valet.
        - **Gold Package**: ₹12,000 onwards, upgraded services with premium photography and makeup.
        - **Diamond Package**: ₹18,000 onwards, premium services including photography, videography, valet, and entertainment.
        
        **Event Add-Ons**:
        - **Balloon Decoration**: Kids Special, Floral, Love Theme
        - **Photography**: Pre-Wedding, Wedding, Baby Photoshoot.
        - **Entertainment**: DJ, Choreography, Live Band.
    """