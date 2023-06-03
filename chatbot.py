import pyttsx3
import speech_recognition as sr
import openai
import streamlit as st
# import pyttsx3
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
load_dotenv()
from gtts import gTTS
import streamlit.components.v1 as components
import pygame
from language_map import language_code

# end


openai.api_key = "***************************************************"
st.title("Chatbot :  *Speech-Sync*")

col3, col4 = st.columns([2, 3])
with col3 :
        st.subheader("Enter Your Language")
with col4 :
        lang = st.text_input(label="", key="lang",placeholder="Enter Your Language")
        if not lang:
             lang="tamil"

set_subheader = """
    <style>
        .css-10trblm{
            margin-top:20px !important;
            color: white;
        }
    </style>
"""
st.markdown(set_subheader,unsafe_allow_html=True)

model = "gpt-4"

set_page_bg_img = '''
    <style>
        .appview-container{
        background-image: url("https://img.freepik.com/premium-photo/blue-background-with-focus-spot-light-3d-rendering_295303-3774.jpg?size=626&ext=jpg&ga=GA1.1.829580816.1685678940&semt=ais");
        background-size: cover;
    }
    </style>
'''
st.markdown(set_page_bg_img, unsafe_allow_html=True)

def speech_To_Text():
    r = sr.Recognizer()

    # Start recording audio from the microphone
    with sr.Microphone() as source:
        st.write("Say something!")
        audio = r.listen(source)

    # Recognize speech using Google Speech Recognition
    try:
        # st.write("You said: " + r.recognize_google(audio))
        query = r.recognize_google(audio)
        return query
    except sr.UnknownValueError:
        st.write("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        st.write(
            "Could not request results from Google Speech Recognition service; {0}".format(e))

    # st.write("from function",query)


if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

def speak(s,language):
    tts = gTTS(text=s, lang=language, slow=False)
    output_file = "response.mp3"
    tts.save(output_file)
    pygame.mixer.init() # Initialize Pygame mixer
    pygame.mixer.music.load(output_file)    # Load the saved MP3 file
    pygame.mixer.music.play()   # Play the MP3 file
    while pygame.mixer.music.get_busy():    # Wait until the playback finishes
        continue
    pygame.mixer.quit() # Clean up the resources
    os.remove(output_file)  # Delete the temporary MP3 file

button_text = ':white[Click to speak]'

col5,col1, col2 = st.columns([2,2, 1])

with col5:
        st.subheader("Enter Your Text")

with col1:
        query = st.text_input(label="", key="input",placeholder="Enter Your Text")

with col2:
        talk = st.button(button_text,use_container_width=True)


css_Button = '''
<style>
    .stButton > button {
        margin-top : 32px;
        border-radius : 1px
    }
</style>
'''
st.markdown(css_Button, unsafe_allow_html=True)


# css_box = """
#     <style>
#         .element-container{
#             background-color : green;
#         }
#     </style>
# """
# st.markdown(css_box, unsafe_allow_html=True)

if talk:
    query = speech_To_Text()
prompt = """
    LANGUAGE={0}
    INPUT={1}
    INSTRUCTION :if the LANGUAGE is english Translate the INPUT to LANGUAGE and if the LANGUAGE is a foreign language translate it to english and avoid words like \"the translation is\" the answer should contain only the translation. You must not give any other explanations or transliteration. I repeat Don't give any explanations or a transliteration. Don't give any transliteration in brackets.Don't give any explanations
""".format(lang,query)

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()
if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", prompt)
        response = get_chatgpt_response(messages, "gpt-3.5-turbo")
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
    try :
        speak(response,language_code(lang))
    except NameError : 
        pass
