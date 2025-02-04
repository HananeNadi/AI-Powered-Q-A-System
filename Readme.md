# Chat with Your PDF using Gemini 

## Overview
This Python application allows you to upload a PDF and ask questions about its content using natural language. The system employs a Language Learning Model (LLM) to generate responses based on the document, ensuring that answers remain relevant and accurate.

## Features
- Load and process PDF documents.

- Ask natural language questions about the document.

- Receive AI-generated responses specific to the document content.

- Ensures responses remain relevant to the uploaded document.

## How It Works

1. Upload a PDF file.

2. The application extracts text from the document.

3. The text is processed and stored in a vector database.

4. You can ask questions related to the document.

5. The LLM generates responses based on the document content.


## Technologies Used

- Streamlit for the web interface.

- PyPDF2 for extracting text from PDFs.

- LangChain for managing conversational AI.

- FAISS for vector-based document retrieval.

- Google Gemini AI for generating responses.

- dotenv for managing environment variables.

## Home page
![System](https://github.com/user-attachments/assets/def17790-adde-4d52-9f7a-699b1c1c241d)

## Try the App 🚀
You can try the application live at:
👉 [Chat with Your PDF]([https://your-username-your-repo-name.streamlit.app/](https://ai-powered-q-a-system-boemtd6mtfphlggenujbd3.streamlit.app/))


## Setup
### Prerequisites
Make sure you have the following installed:
- Python 3.8+
- A Google API key with access to Gemini AI

### Clone the Repository
```sh
git clone <repository-url>
cd <project-directory>
```
### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up Environment Variables
Create a **.env** file and add your Google API key:
```sh
GOOGLE_API_KEY=your_google_api_key
```
### Usage
Run the application using:
```sh
streamlit run app.py
```



Developed with ❤️ by Hanane Nadi.
