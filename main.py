from data.emp import generate_employee_data
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from Assistant import Assistant
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE
from langchain_groq import ChatGroq

from ui import AssistantUI


if __name__ == "__main__":

    load_dotenv()

    st.set_page_config(page_title="SherpaAI solutions Onboarding", page_icon='🚀', layout= "wide")

    @st.cache_data(ttl = 3600, show_spinner="loading employee data")
    def get_user_data():
        return generate_employee_data(1)[0]
    
    @st.cache_resource(ttl = 3600, show_spinner="loading vector store")
    def init_vector_store(pdf_path):
        
        try: 
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 4000, chunk_overlap = 200
            )
            splits = text_splitter.split_documents(docs)

            embedding_function = OpenAIEmbeddings()

            persistent_path = "./data/vectorstore"

            vectorstore = Chroma.from_documents(
                documents = splits,
                embedding = embedding_function, 
                persist_directory = persistent_path

            )

            return vectorstore
        except Exception as e:
            st.error(f"failed to initialze vector store: {str(e)}")
            return None
    
    customer_data = get_user_data()
    vector_store = init_vector_store("data/clientOnboarding.pdf")

    if "customer" not in st.session_state:
        st.session_state.customer = customer_data
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "ai", "content": WELCOME_MESSAGE}]

    llm = ChatGroq(model="llama-3.1-8b-instant")

    assistant = Assistant(

        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        employee_information=st.session_state.customer,
        vector_store=vector_store,

    )




    ui = AssistantUI(assistant)
    ui.render()

