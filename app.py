import streamlit as st
import os
import google.generativeai as genai

from dotenv import load_dotenv
from st_pages import Page, show_pages

show_pages(
    [
        Page("app.py", "Quest Chat Hub", "💬"),
        Page("pages/vision.py", "Snap Speak", "📸"),
        Page("pages/invoice.py", "Invoice Xtract", "💼"),
        Page("pages/health.py", "Calorie Lens", "🍏"),
        Page("pages/chat_pdf.py", "PDF Converse", "📄"),
    ]
)

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


##initialize our streamlit app
st.set_page_config(page_title="QuestChat Hub")
st.header("How can I help you today?")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input = st.text_input("Input: ", key="input")

if input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state["chat_history"].append(("You", input))
    st.subheader("The Response is")
    final_response = ""
    for chunk in response:
        st.write(chunk.text)
        final_response += chunk.text
    st.session_state["chat_history"].append(("Bot", final_response))
st.subheader("The Chat History is")

for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")
