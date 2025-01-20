# 1. Ingest PDF file
# 2. Extract text from PDF file and split into small chunks
# 3. Feed each chunk into the embedding model
# 4. Save the embeddings into a vector database
# 5. Perform similarity search on the vector database to find similar items
# 6. Retrieve similar documents and present them to the user

import ollama

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from pdf2image.exceptions import PDFPageCountError

from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever


doc_path = r".\data\discipline.pdf"
model = "llama3.2"

if doc_path:
    try:
        loader = UnstructuredPDFLoader(file_path=doc_path)
        data = loader.load()
        print("done loading...")
    except PDFPageCountError:
        print(
            "Error: Unable to get page count. The PDF file might be corrupted or invalid."
        )
        data = None
else:
    print("Upload a pdf file to continue...")
    data = None

# Extract text from PDF files and split

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("done splitting...")

# print(f"Number of chunks: {len(chunks)}")
# print(f"First chunk: {chunks[0]}")

# Add to vector database
ollama.pull("nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="simple-rag",
)
print("done adding to vector database...")


# Retrieval


llm = ChatOllama(model=model)

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language assistant. Your tasks are to answer questions and provide information. 
    You are given a question: "{question}". Please provide an answer to the question.""",
)

retriever = MultiQueryRetriever.from_llm(vector_db.as_retriever(), llm, QUERY_PROMPT)

# Rag prompt
template = """Answer the question based Only on the following context:
{context}
Question:{question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


res = chain.invoke(input={"context": "What is the purpose of the document?"})
res = chain.invoke(input={"context": "Give me 10 important points from the document?"})
print(res)