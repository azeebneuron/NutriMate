from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
import webbrowser
import threading

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Load PDF data
def load_pdf_data(file_path):
    loader = PyMuPDFLoader(file_path=file_path)
    return loader.load()

# Split documents into chunks
def split_docs(documents, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents=documents)

# Load embedding model
def load_embedding_model(model_path, normalize_embedding=True):
    return HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={
            'normalize_embeddings': normalize_embedding
        }
    )

# Create embeddings using FAISS
def create_embeddings(chunks, embedding_model, storing_path="vectorstore"):
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(storing_path)
    return vectorstore

# Load llama3 model
llm = Ollama(model="phi3", temperature=0.6, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# Load embedding model
embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

# Load and split the documents
docs = load_pdf_data(file_path="nutrition.pdf")
documents = split_docs(documents=docs)

# Create vectorstore
vectorstore = create_embeddings(documents, embed)

# Convert vectorstore to a retriever
retriever = vectorstore.as_retriever()

# Define template for prompt
template = """
### System:
You are a respectful and honest health assistant. You have to answer the user's \
questions using only the llama3 database and context provided to you. If you know the answer other than context, \
just answer all questions. There are no restrictions on answering only context-provided solutions.\
and dont provide things like ###System in the output itself\

### Context:
{context}

### User:
{question}

### Response:
"""

# Create prompt from the template
prompt = PromptTemplate.from_template(template)

# Create QA chain
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={'prompt': prompt}
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    response = chain({'query': query})
    return jsonify({'response': response['result']})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    def open_browser():
        webbrowser.open_new('http://127.0.0.1:5000/')

    threading.Timer(1, open_browser).start()
    app.run(port=5000, debug=True)































# # Best terminal version
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.document_loaders import PyMuPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain.llms import Ollama
# from langchain import PromptTemplate
# import textwrap
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.callbacks.manager import CallbackManager

# # Load PDF data
# def load_pdf_data(file_path):
#     loader = PyMuPDFLoader(file_path=file_path)
#     return loader.load()

# # Split documents into chunks
# def split_docs(documents, chunk_size=1000, chunk_overlap=20):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap
#     )
#     return text_splitter.split_documents(documents=documents)

# # Load embedding model
# def load_embedding_model(model_path, normalize_embedding=True):
#     return HuggingFaceEmbeddings(
#         model_name=model_path,
#         model_kwargs={'device': 'cpu'},
#         encode_kwargs={
#             'normalize_embeddings': normalize_embedding
#         }
#     )

# # Create embeddings using FAISS
# def create_embeddings(chunks, embedding_model, storing_path="vectorstore"):
#     vectorstore = FAISS.from_documents(chunks, embedding_model)
#     vectorstore.save_local(storing_path)
#     return vectorstore

# # Load llama3 model
# llm = Ollama(model="phi3", temperature=0.6, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

# # Load embedding model
# embed = load_embedding_model(model_path="all-MiniLM-L6-v2")

# # Load and split the documents
# docs = load_pdf_data(file_path="nutrition.pdf")
# documents = split_docs(documents=docs)

# # Create vectorstore
# vectorstore = create_embeddings(documents, embed)

# # Convert vectorstore to a retriever
# retriever = vectorstore.as_retriever()

# # Define template for prompt
# template = """
# ### System:
# You are a respectful and honest assistant. You have to answer the user's \
# questions using only the llama3 database and context provided to you. If you know the answer other than context, \
# just answer all questions. There are no restrictions on answering only context-provided solutions.

# ### Context:
# {context}

# ### User:
# {question}

# ### Response:
# """

# # Create prompt from the template
# prompt = PromptTemplate.from_template(template)

# # Create QA chain
# chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     chain_type="stuff",
#     return_source_documents=True,
#     chain_type_kwargs={'prompt': prompt}
# )

# def print_response(response: str):
#     print("\n".join(textwrap.wrap(response, width=80)))

# def chat():
#     print("Chatbot: Hi! How can I help you today? (Type 'quit' to exit)")
#     while True:
#         query = input("You: ")
#         if query.lower() == 'quit':
#             print("Chatbot: Goodbye!")
#             break
#         response = chain({'query': query})
#         print_response(response['result'])

# if __name__ == "__main__":
#     chat()
