
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import numpy as np

# load file , read and extract text
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


#chunking of extracted text
def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks


#embedding of chunks
def create_embeddings(chunks):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(chunks)
    embeddings = matrix.toarray().astype('float32')
    return vectorizer, embeddings


def prepare_pdf_embeddings(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    vectorizer, embeddings = create_embeddings(chunks)
    return vectorizer, embeddings, chunks
