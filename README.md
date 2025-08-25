# 🧠 Aahwanam Chatbot Backend

This is a CLI-based chatbot backend for the Aahwanam platform that uses Groq's LLM, Pinecone for context-based search, and MySQL for real-time data.

---

## 🧭 Program Flow

1. **User Prompt Input**:  
   User enters a query in the terminal.

2. **Groq Table Decision**:  
   The prompt is passed to `askGroqWhichTable(prompt)` (from `testbotOnlyGroq.py`) to determine which table(s) the bot needs to query (e.g., services, packages, or location-based services).

3. **MySQL Realtime Data Fetch**:  
   Based on the table identified, the bot uses helper functions in `dbHelper.py` to fetch relevant data from the MySQL database.

4. **Contextual Search (Pinecone)**:  
   The prompt is embedded using SentenceTransformer and queried against a Pinecone index (`aahwanamcontext`) to retrieve relevant context.

5. **Prompt Construction**:  
   The prompt is built with:
   - Pinecone context
   - Real-time MySQL data
   - Chat history

6. **Groq API Call**:  
   The constructed prompt is sent to Groq’s LLaMA3 model, and the response is printed as the bot's reply.

7. **Loop Continues**:  
   The conversation continues until the user exits manually.

---

## 🚀 How to Run This Project

### 1. Clone the Repository

```bash
python main.py