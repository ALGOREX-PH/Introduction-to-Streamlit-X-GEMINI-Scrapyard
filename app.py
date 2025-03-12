import streamlit as st
import google.generativeai as genai
from bs4 import BeautifulSoup
import requests
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
warnings.filterwarnings("ignore")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 32768,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

SYSTEM_PROMPT = "You are a Globe Telecom Virtual Assitant."

st.set_page_config(page_title="Introduction to Streamlit and GEMINI API", page_icon="", layout="wide")

with st.sidebar :
    st.image("maia.png")
    api_key = st.text_input('Enter Gemini API token:', type='password')

    if api_key:
       try:
          genai.configure(api_key=api_key)
          model = genai.GenerativeModel('gemini-2.0-flash')
          response = model.generate_content("Hello") # Hello test
          st.success('Proceed to entering your prompt message!', icon='👉')
          
       except Exception as e:
          st.error(f"Invalid API key or error: {e}", icon="🚨")

    else:
       st.warning('Please enter your Gemini API token!', icon='⚠️')
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Dashboard", 
        ["Home", "About Us", "Chat"],
        icons = ['book', 'globe', 'tools', "tools", "tools", "tools"],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#dec960", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#262730"},
            "nav-link-selected" : {"background-color" : "#262730"}          
        })


if 'message' not in st.session_state:
    st.session_state.message = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None

# Options : Home
if options == "Home" :

   st.title('This is the Home Page')
  

elif options == "About Us" :
     st.title('This is the About Us Page')
     st.write("\n")


if options == 'Chat':
            if "chat_session" not in st.session_state:
                st.session_state.chat_session = model.start_chat(history=[])
                st.session_state.messages = []
                st.write("Chat session initialized.")

            if st.session_state.get("chat_session") is None:
                st.session_state.chat_session = model.start_chat(history=[])
                st.session_state.messages = []
                response = st.session_state.chat_session.send_message("You will act and introduce yourself as the following :  " + SYSTEM_PROMPT)
                with st.chat_message("assistant"):
                    st.markdown(response.text)

            for message in st.session_state.messages:
                if message['role'] == 'system':
                    continue
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_message := st.chat_input("Say something"):
                with st.chat_message("user"):
                    st.markdown(user_message)
                st.session_state.messages.append({"role": "user", "content": user_message})

                if st.session_state.get("chat_session"):
                        response = st.session_state.chat_session.send_message(user_message)
                        with st.chat_message("assistant"):
                            st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})