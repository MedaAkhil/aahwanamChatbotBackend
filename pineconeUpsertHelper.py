from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
documents = [
    {
        "id": "aahwanam-overview",
        "text": """
You are a customer support chatbot for the “Aahwanam” event-planning app. The user interface includes the following screens and flows:

• Home / Services screen – Shows service categories like Décor, Pandit, Photography, Mehndi, Bartender, Chef, Entertainment; users can browse by category, see trending providers and packages.

• Category browsing – Horizontal category list, then vendor cards grouped by “Decorators in your city,” “Mehndi artists for you,” “Trending,” and “Packages for all events.” Each card shows ratings and vendor name.

• Package selection flow – User picks a service (e.g., Photography → Pre‑wedding), then chooses one of several packages (Silver, Gold, Diamond) with included features and ratings.

• Booking form – After selecting a package, the user picks an event date & time (calendar/time picker), enters event address, then can “Add to cart” or “Book Service”.

• Vendor interface confirmation – When vendor logs in or builds profile, there’s a message: “Your profile built successfully, wait for admin approval. After verification you will get leads.”

• Vendor themes/edit interface – Vendors can configure service details, set themes, add gallery items, choose “Edit” or “Add New Item”.

• Settings page – Vendors can toggle notifications, change password, enter a WhatsApp mobile number for auto‑sharing booking details, enable/disable auto‑share, and log out.
        """,
        "metadata": {
            "source": "aahwanam-docs",
            "type": "ui-flows"
        }
    },
    {
        "id": "decor-service",
        "text": "Décor service offers decorations for events like weddings and parties. It includes flower arrangements, lighting, and stage setups.",
        "metadata": {"category": "service", "name": "Décor"}
    },
    {
        "id": "pandit-service",
        "text": "Pandit service provides experienced pandits for religious rituals. Book via the 'Pandit' section in the app.",
        "metadata": {"category": "service", "name": "Pandit"}
    },
    {
        "id": "photography-service",
        "text": "Photography packages include pre-wedding, wedding, and event coverage.",
        "metadata": {"category": "service", "name": "Photography"}
    },
    {
        "id": "mehndi-service",
        "text": "Mehndi services for bridal and guest designs.",
        "metadata": {"category": "service", "name": "Mehndi"}
    },
    {
        "id": "chef-service",
        "text": "Chef service provides catering with various cuisines for events.",
        "metadata": {"category": "service", "name": "Chef"}
    },
    {
        "id": "bartender-service",
        "text": "Bartenders for events.",
        "metadata": {"category": "service", "name": "Bartender"}
    },
    {
        "id": "entertainment-service",
        "text": "Entertainment services include DJ, live bands, and other performers for events.",
        "metadata": {"category": "service", "name": "Entertainment"}
    },
    {
        "id": "valet-parking",
        "text": "Valet Parking options include Royal Valet Service and Standard Valet.",
        "metadata": {"category": "addon", "name": "Valet Parking"}
    },
    {
        "id": "event-types",
        "text": "Event Types: Birthday, Wedding, Anniversary, Kids Party, Pre-Wedding, Corporate Event, Baby Shower, Engagement.",
        "metadata": {"category": "info", "name": "Event Types"}
    },
    {
        "id": "event-addons",
        "text": "Event Add-Ons include: Balloon Decoration (Kids Special, Floral, Love Theme), Photography (Pre-Wedding, Wedding, Baby Photoshoot), Entertainment (DJ, Choreography, Live Band).",
        "metadata": {"category": "addon", "name": "Event Add-Ons"}
    }
]

model = SentenceTransformer("all-MiniLM-L6-v2")
pc = Pinecone(api_key="pcsk_2jNZua_KoTm5ZZKaCaicbDKPGsUAaRuVvjiscyGx79qWKV2dDHyaiFN4b2zWRgbURzUSJE")
index = pc.Index("aahwanamcontext")

for doc in documents:
    vector = model.encode(doc["text"]).tolist()
    index.upsert([
        {
            "id": doc["id"],
            "values": vector,
            "metadata": doc["metadata"] | {"text": doc["text"][:1000]}  # Store a snippet for readability
        }
    ])
