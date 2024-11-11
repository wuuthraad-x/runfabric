import streamlit as st
import openai
import fitz  # PyMuPDF
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")

# Streamlit App for PDF Upload and Document Chat
st.title("Chat with Your Document (RAG System)")

# Upload PDF file
uploaded_pdf = st.file_uploader("Upload your PDF document", type="pdf")

if uploaded_pdf is not None:
    # Save the PDF to a temporary file
    with open("uploaded_pdf.pdf", "wb") as f:
        f.write(uploaded_pdf.read())
    
    # Extract text from the uploaded PDF
    def extract_text_from_pdf(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    # Break text into chunks for better processing
    def chunk_text(text, max_chars=1000):
        words = text.split()
        chunks = []
        chunk = ""
        for word in words:
            if len(chunk) + len(word) + 1 > max_chars:
                chunks.append(chunk)
                chunk = ""
            chunk += " " + word
        chunks.append(chunk)  # Append the final chunk
        return chunks

    # Get embedding for text
    def get_embedding(text):
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']

    # Extract the text content from the uploaded PDF
    pdf_text = extract_text_from_pdf("uploaded_pdf.pdf")
    chunks = chunk_text(pdf_text)

    # Generate embeddings for each chunk
    chunk_embeddings = [get_embedding(chunk) for chunk in chunks]

    # Input box for user's query to chat with the document
    user_query = st.text_input("Ask a question about the document:")

    if user_query:
        # Get the embedding for the user's query
        query_embedding = get_embedding(user_query)

        # Compute similarities and find the top chunk
        similarities = [cosine_similarity([query_embedding], [chunk_embedding])[0][0] for chunk_embedding in chunk_embeddings]
        most_relevant_chunk = chunks[np.argmax(similarities)]

        # Generate a response based on the most relevant chunk
        def query_openai_with_context(query, context):
            messages = [
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided document content."},
                {"role": "user", "content": f"Document content: {context}"},
                {"role": "user", "content": f"Question: {query}"}
            ]
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message['content'].strip()

        # Get OpenAI response to the query
        answer = query_openai_with_context(user_query, most_relevant_chunk)

        # Display the response from OpenAI (answer)
        st.subheader("Response:")
        st.write(answer)
