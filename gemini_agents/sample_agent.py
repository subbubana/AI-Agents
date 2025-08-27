import google.generativeai as genai
# from google.genai import types # This import is not needed for GenerativeModel
# from PIL import Image
# from io import BytesIO

import os
from dotenv import load_dotenv

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")

genai.configure(api_key=GENAI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

def main():
    while True:
        prompt = input("You:")
        if prompt == "quit" or prompt == "exit":
            print("Conversation ended")
            break
        else:
            response = chat.send_message(prompt)
            print(response.text)

if __name__ == "__main__":
    main()


