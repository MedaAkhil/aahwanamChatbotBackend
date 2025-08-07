import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI with your Groq endpoint and key
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def send_prompt_to_groq(prompt, model="llama3-8b-8192"):
    system_prompt = (
        "You are a bot for Aahwanam platform. You only have to decide the tables to choose based on the user prompt "
        "and return the table number(s) in a Python list.\n\n"
        "The database has the following tables and their respective columns:\n"
        "(1). services(service_name, description)\n"
        "(2). services_packages(package_name, base_price, description)\n"
        "(3). vendor_service_locations(city, state)\n\n"
        f"This is the user prompt: '{prompt}'\n\n"
        "Respond only with the table number(s) in a list, e.g., [1], [2, 3], etc."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


print(send_prompt_to_groq("next week i have my birthday celebration in mumbai"))
print("next week i have my birthday celebration in mumbai")

print(send_prompt_to_groq("next week i have my birthday celebration"))
print("next week i have my birthday celebration")

print(send_prompt_to_groq("next week i have my birthday celebration in mumbai what are all the services i might require"))
print("next week i have my birthday celebration in mumbai what are all the services i might require")

print(send_prompt_to_groq("what packages does aahwanam offers"))
print("what packages does aahwanam offers")
