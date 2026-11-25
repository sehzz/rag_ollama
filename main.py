from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama
import os

CHAT_HISTORY = ""

def load_documents():
    files = os.listdir("data")
    sorted_files = sorted(files)
    all_pages = []

    for file in sorted_files:
        loader = PyPDFLoader(f"data/{file}")
        pages = loader.load()

        if pages:
            all_pages.extend(pages)

    return all_pages

def chunking():
    all_pages = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 150
    )
    chunks = splitter.split_documents(all_pages)
    return chunks

def embeddings():
    #### uncomment this when saving a new vector db ####
    #chunks = chunking()
    embeddings = OllamaEmbeddings(model="bge-m3")

    ##### use this to create the vector db again ##########
    #vector_db = FAISS.from_documents(chunks, embeddings)
    #vector_db.save_local("porche_911_investigations")

    ###### using the existing vector db from disk
    vector_db = FAISS.load_local(
        "porche_911_investigations",
        embeddings,
        allow_dangerous_deserialization = True
    )

    return vector_db




def retreive_context(question):
    vector_db = embeddings()

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 5}
    )
    retreived_chunks = retriever.invoke(
        question
    )

    context = ""

    for chunk in retreived_chunks:
        context += chunk.page_content + "\n\n"

    return context

def chat(question, chat_history):
    llm = ChatOllama(model="qwen2.5:1.5b")
    context = retreive_context(question)

    response = llm.invoke(
        f"""
        Answer ONLY using the provided context.
        Answer strictly using the provided context. When quoting official designations, codes, or foreign-language terms, reproduce the exact wording from the text without translating or paraphrasing.

        If the answer cannot be found in the context, say:
        "I don't know based on the case files."

        Chat History:
        {chat_history}

        Context:
        {context}

        Question:
        {question}
        """
    )

    return response.content


def run():
    history = CHAT_HISTORY
    while True:
        question = input("Question: ")

        if question.lower() in ("bye", "exit"):
            break

        response = chat(question, history)

        history += f"""
        User: {question}

        Assistant: {response}
        """

        print("=" * 80)
        print(response)
        print("=" * 80)



if __name__ == "__main__":
    #ques = "What is the paint code and official German designation for the Slate Grey finish on Commission No. SG-774-BLK?"
    run()