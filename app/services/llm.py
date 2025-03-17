from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI



load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")

if GEMINI_API is None:
    raise Exception("GEMINI_API_KEY is not set")

llm = ChatGoogleGenerativeAI(temperature=0.7,  model="gemini-1.5-pro",google_api_key=GEMINI_API)
global_memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)


def load_content(file):
    if file.endswith(".pdf"):
        return PyPDFLoader(file).load()
    if file.endswith(".txt"):
        return TextLoader(file).load()
    if file.endswith(".csv"):
        return CSVLoader(file).load()
    if file.endswith(".docx"):
        return Docx2txtLoader(file).load()
    else:
        raise Exception("Unsupported file format")
    
def split_embed(data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitted_data = text_splitter.split_documents(data)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=GEMINI_API)
    vectorstore = FAISS.from_documents(splitted_data, embedding=embeddings)
    return vectorstore

def document_loader(file):
    if file:
        load_text = load_content(file)
        return split_embed(load_text)
    else:
        raise Exception("No file path provided")

def document_chat(file, text):
    vectorstore = document_loader(file)
    relevant_docs = vectorstore.similarity_search(text, k=3)
    context_text = "\n\n".join([doc.page_content for doc in relevant_docs]) if relevant_docs else ""
    past_messages = global_memory.chat_memory.messages
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant.
    Document content:
    ---
    {context}
    ---
    Below is the conversation history so far:
    {history}

    User's question: {question}
    Answer as best you can, referencing both the document content and conversation history.
    """)

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "context": context_text,
        "history": past_messages,
        "question": text
    })

    global_memory.chat_memory.add_user_message(text)
    global_memory.chat_memory.add_ai_message(response)

    return response

def handle_chat(file, text):
    if file:
        response = document_chat(file, text)
        
        return response
    else:
        prompt = PromptTemplate.from_template(
            """You are a helpful assistant.
            Current conversation:
            {history}
            Human: {input}
            AI Assistant:"""
        )
        chain = prompt | llm | StrOutputParser()
        past_messages = global_memory.load_memory_variables({}).get("chat_history", [])
        
        response = chain.invoke({"input": text, "history": past_messages})
        
        global_memory.chat_memory.add_user_message(text)
        global_memory.chat_memory.add_ai_message(response)
        
        return response


