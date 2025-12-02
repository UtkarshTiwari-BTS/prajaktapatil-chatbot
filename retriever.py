from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search_cosine(query, vectorizer, embeddings, chunks, top_k=2):
    query_vec = vectorizer.transform([query]).toarray()
    similarities = cosine_similarity(query_vec, embeddings)[0]
    top_k_idx = np.argsort(similarities)[-top_k:][::-1]
    return "\n\n".join(chunks[i] for i in top_k_idx)
