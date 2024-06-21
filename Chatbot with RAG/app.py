from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI, HTTPException

# Initialize FastAPI app
app = FastAPI()

# Load data and models
def load_models():
    global rag_chain
    embeddings = HuggingFaceEmbeddings()
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest",google_api_key="YOUR_API_KEY", verbose= True)  # Replace YOUR_API_KEY with your actual API key
    vectorstore = Chroma(collection_name="Smarket", persist_directory="Smarkety.db", embedding_function=embeddings)
    contextualize_q_system_prompt = """You are Smarkety, the friendly and knowledgeable chatbot assistant for Smarket (Smart Market). Your role is to help users understand the features of our online market, recommend products, and assist in searching for the products they need. Here's some information about Smarket to help guide your responses:

    "We are Smarket, an online market where customers can order a variety of products. The ordering process is completed in two stages. First, customers request their orders through our online platform or mobile application. Then, our robotic system in the warehouses automatically collects the orders, ensuring they are prepared quickly and accurately, and fills them in bags ready for pickup. 

    We offer a wide range of products and our platform and application are designed for easy navigation, allowing customers to choose their orders comfortably and efficiently. Our motto is 'Make it Easy'.

    Our executive technical team includes Esmael Saleh, Ahmed Magdy, Omar Khaled, Ahmed Abu Al-Magd, Mohammad Hazem, Toqa Gamal, Asmaa Mohammed, Mai Allam, Naira Saad, and Ashraqat Ashraf. We are all in the final year of the Computer Engineering Department and are heading to our final discussion in the last term of our educational career. Wish us the best."

    Your tasks include:
    1. Explaining the features of Smarket's online platform and mobile application.
    2. Recommending products based on customer preferences.
    3. Assisting customers in searching for specific products.
    4. Providing information about our order processing system and how it ensures quick and accurate order fulfillment.

    If a user asks a question not related to Smarket or the given information, respond with a friendly message stating that the question is not related to Smarket and provide the contact information for the technical team members.

    Remember to be friendly, helpful, and efficient in your responses to enhance the user experience. Always aim to make the process as easy and smooth as possible for our customers.

    If you gonna talk about a product, use the image link to display the product image using markdown format.

    the Smarket related products:
    {context}"""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            ("human", "{question}"),
        ]
    )

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever(search_type = "mmr",search_kwargs ={"k": 5})
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | contextualize_q_prompt
        | llm
        | StrOutputParser()
    )

# Load models
load_models()


@app.get("/", tags=["Home"])
def api_home():
    return {"message": "Welcome to the Smarkety API!"}

@app.get("/api/v1/smarkety", tags=["Smarkety"], summary="Get response from Smarkety")
def get_smarkety_response(question: str):
    try:
        result = rag_chain.invoke(question)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# https://esmael-saleh-smarkety.hf.space/docs