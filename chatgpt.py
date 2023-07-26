import os
import time
from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI

import constants
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

col1, col2, col3 = st.columns(3)

# number of travelers
number_of_travelers = col1.slider('Number of travelers', min_value=0, max_value=7, step=1)

# from date
from_date = col2.date_input('Select start date')

# to date
to_date = col3.date_input('Select end date')

# interests prompt
prompt = st.text_input('What are you interested in mate?')

prompt_template = "Act as a travel agent, keep a funny, friendly approach. Provide me with the best recommendations " \
                  f"for my trip in Syrros island. We will be {number_of_travelers} people." \
                  f"We will be in Syrros from {from_date} to {to_date}." \
                  f"We are  interested in {prompt}."
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
