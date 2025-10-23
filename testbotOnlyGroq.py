import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI with your Groq endpoint and key
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)
def sendGroqRequest(prompt, systemPrompt, model="llama3-8b-8192"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
def askGroqWhichTable(prompt, model="llama3-8b-8192"):
    system_prompt = (
        "You are a bot for Aahwanam platform. You only have to decide the tables to choose based on the user prompt "
        "and return the table number(s) in a Python list.\n\n"
        "The database has the following tables and their respective columns:\n"
        "(1). services(service_name, description) This database table gives you all the services that the platform offers for the events like Decoration, Bartender, Chef, Valet Parking, Makeup&hair, pandit, Entertainment, Mehndi, Photographer services\n"
        "(2). services_packages(package_name, base_price, description) This table in the database have the details about budget friendly packages at lowest price and every package is applicable to only a single services like Basic Package | 2000.00 | When you provide all supplies, we provide the bartender. Royal Package | 6000.00 | Premium valet experience.this are two of the example data in the table for the valetparking and bartender services packages in the same way it has the packages for all the services\n"
        "(3). vendor_service_locations(city, state) this table give the data about the services offered by vendors in specific region such as a state or a city so that user can search based on the their event location or the user location\n\n"
        f"This is the user prompt: '{prompt}'\n\n"
        "Respond only with the table number(s) in a list, e.g., [1], [2], [3], [1, 2], [2, 3], [1, 3], [1, 2, 3] etc."
        "if there is any city name in the prompt add the [3] to the response and also at the end the city or the state name and at the ^ symbol at the start of the name"
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




if __name__ == "__main__":
    print('1 services, 2 packages, 3 locations\n\n')
    
    print(askGroqWhichTable("next week i have my birthday celebration in mumbai"))
    print("Prompt1: next week i have my birthday celebration in mumbai")

    print(askGroqWhichTable("next week i have my birthday celebration"))
    print("Prompt2: next week i have my birthday celebration")

    print(askGroqWhichTable("next week i have my birthday celebration in mumbai what are all the services i might require"))
    print("Prompt3: next week i have my birthday celebration in mumbai what are all the services i might require")

    print(askGroqWhichTable("10000"))
    print("Prompt4: 10000")

    print(askGroqWhichTable("i have an event give me budget friendly plan for that"))
    print("Prompt4: i have an event give me budget friendly plan for that")
