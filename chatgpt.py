import os
import time

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

import vector

load_dotenv()

api_key = os.getenv('API_KEY')

os.environ['OPENAI_API_KEY'] = api_key

# documents to extract info from
source_documents = "source_documents/syrros.txt"

# ingest the document to create
index = vector.ingest(source_documents)

st.title("🦜️🔗 GPT-Filoxeno 🌴🌞")

# Access session state
if 'submit' not in st.session_state:
    st.session_state['submit'] = False

col1, col2, col3, col4, col5 = st.columns(5)

# default destination
default_destination = "Syrros"

# destination
destination = col1.text_input('Destination', default_destination)

# from date
from_date = col2.date_input('Select start date')

# to date
to_date = col3.date_input('Select end date')

# number of travelers
number_of_travelers = col4.slider('Number of travelers', min_value=1, max_value=4, step=1)

# number of rooms
number_of_rooms = col5.slider('Number of rooms', min_value=1, max_value=4, step=1)

# interests prompt
# prompt = st.text_input('What are you interested in mate?')

prompt_template = "Act as a travel agent, keep a funny, friendly approach. Provide me with the best recommendations " \
                  f"for my trip in {destination} island. We will be {number_of_travelers} people." \
                  f"We will be in {destination} from {from_date} to {to_date}."
if st.button('Search'):
    st.session_state['submit'] = True

if st.session_state['submit']:
    try:
        with st.spinner('Hmm.. Let me think about that...'):
            start = time.time()
            response = index.query(prompt_template, llm=ChatOpenAI())
            end = time.time()

        st.write(response)
        elapsed_time = round(end - start, 2)
        st.write(f"Answer took: {elapsed_time} seconds")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter a valid prompt.")
