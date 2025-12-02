
from embeddings import prepare_pdf_embeddings
from retriever import search_cosine
from openai import AzureOpenAI



# llm 
def ask_llm(question, context, api_key, endpoint, api_version, deployment):

    client = AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )

    prompt = f"""
    Use ONLY the context to answer.
    Question: {question}
    Context: {context}
    Provide only the final answer. Nothing else.
    """

    response = client.chat.completions.create(
        model=deployment,  
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()



#  CLASS created
class PDFChatbot:

    def __init__(self, pdf_path):
       self.vectorizer, self.embeddings, self.chunks = prepare_pdf_embeddings(pdf_path)

    def ask(self, question, api_key, endpoint, api_version, deployment):
        context = search_cosine(question, self.vectorizer, self.embeddings, self.chunks)
        return ask_llm(question, context, api_key, endpoint, api_version, deployment)
