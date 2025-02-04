import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")


def extract_text_from_files(files):
    text = ""
    for file in files:
        if file.name.endswith(".pdf"):
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file.name.endswith(".txt"):
            text += file.read().decode("utf-8")
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200, length_function=len, separators=["\n\n", "\n", " "])
    return text_splitter.split_text(text)


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer
the question. If you don't know the answer, say that you
don't know. DON'T MAKE UP ANYTHING.

Context: {context}

Question: {question}

Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key, temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except RuntimeError:
        st.error("FAISS index not found. Please upload and process files first.")
        return

    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    st.write("Reply:", response["output_text"])


def main():
    st.set_page_config(page_title="Chat with Documents")
    st.header("Chat with your PDF using Gemini 📚")

    user_question = st.text_input("Ask a question about your document")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Upload Your Documents:")
        files = st.file_uploader("Upload PDF or Text Files", accept_multiple_files=True, type=["pdf", "txt"])

        if st.button("Submit & Process"):
            if files:
                with st.spinner("Processing..."):
                    raw_text = extract_text_from_files(files)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.success("Processing Complete!")
                    else:
                        st.error("Could not extract text from the uploaded files.")
            else:
                st.error("Please upload at least one file.")


if __name__ == "__main__":
    main()
