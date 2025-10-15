from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

from app.config.config import HUGGINGFACE_REPO_ID,HF_TOKEN
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """ Answer the following medical question in 2-3 lines maximum using only the information provided in the context.

Context:
{context}

Question:
{question}

Answer:
"""

def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE,input_variables=["context" , "question"])

def create_qa_chain():
    try:
        logger.info("Loading vector store for context")
        db = load_vector_store()

        if db is None:
            raise CustomException("Vector store not present or empty")

        llm = load_llm()

        if llm is None:
            raise CustomException("LLM not loaded")

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={'k': 1}),
            return_source_documents=False,
            chain_type_kwargs={'prompt': set_custom_prompt()}
        )

        logger.info("Successfully created the QA chain")
        return qa_chain

    except Exception as e:
        error_message = CustomException("Failed to make a QA chain", e)
        logger.error(str(error_message))
        #  Explicitly return None on failure
        return None
"""
Now it retrieved some similar results.Suppose, uh, inside the vector store, it has results like what is cancer?What is lung?Lung cancer?What is, uh, throat cancer?What is breast cancer?And what is thyroid cancer?Like that.What is blood cancer?Now, it has gathered five, uh, nearly suited documents.Blood cancer, thyroid cancer, breast cancer.But I only ask, what is cancer?So if I'm keeping it as one so it will pick the most nearest, or we can say most relevant.But if you want some, uh, randomness in the data.You want more bigger chain.So you have you can increase this k parameter so if you want more context Basically, if you want more context related to cancer.So that you can increase this k equal to 12345 like that.Okay.
Generally we keep it as three okay.Three is a standard one okay.
"""