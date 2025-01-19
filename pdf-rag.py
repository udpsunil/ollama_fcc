from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from pdf2image.exceptions import PDFPageCountError

import nltk
nltk.download("punkt_tab")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("averaged_perceptron_tagger_eng")

# 1. Ingest PDF file
# 2. Extract text from PDF file and split into small chunks
# 3. Feed each chunk into the embedding model
# 4. Save the embeddings into a vector database
# 5. Perform similarity search on the vector database to find similar items
# 6. Retrieve similar documents and present them to the user



doc_path = r".\data\huberman_podcast.pdf"
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

if data:
    content = data[0].page_content
    print(content)


