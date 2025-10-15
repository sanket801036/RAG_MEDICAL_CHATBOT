from langchain_groq import ChatGroq
from app.config.config import GROQ_API_KEY
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(model_name: str = "llama-3.1-8b-instant", groq_api_key: str = GROQ_API_KEY):
    try:
        logger.info("Loading LLM from Groq using LLaMA3 model...")

        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=0.3,
            max_tokens=256,
        )

        logger.info("LLM loaded successfully from Groq.")
        return llm

    except Exception as e:
        error_message = CustomException("Failed to load an LLM from Groq", e)
        logger.error(str(error_message))
        return None

# from langchain_huggingface import HuggingFaceEndpoint
# from app.config.config import HF_TOKEN,HUGGINGFACE_REPO_ID
# from app.common.logger import get_logger
# from app.common.custom_exception import CustomException

# logger=get_logger(__name__)

# def load_llm(huggingface_repo_id: str=  HUGGINGFACE_REPO_ID,hf_tokenizer = HF_TOKEN):
#     try:
#         logger.info("Loading LLM from Huggingface")

#         llm= HuggingFaceEndpoint(
#             repo_id=huggingface_repo_id,
#             huggingfacehub_api_token=HF_TOKEN,
#             temperature=0.3,
#             max_new_tokens=256,
#             return_full_text=False,
          

#         )
#         logger.info("LLM loaded sucesfully...")
#         return llm
    
#     except Exception as e:
#         error_message = CustomException("Failed to load an LLM ", e)
#         logger.error(str(error_message))
#         # return None

# """
# In terms of temperature means randomness.Lower the temperature.lower is the randomness of the model higher the temperature higher the randomness of the model.So we don't want much creative model.We want only less creative models.So let's keep it 0.3 okay.

# Max length means that max length of the response.Suppose you ask it, what is your name?So it will, uh, generate the response.
# My name is Maddie Bott.So this is the number of tokens that it generated.My name is Maddie Bought five tokens.So you have to list the number of tokens.So let's keep it to 256.That is the standard.Okay, now return full text.We want only the last response.We don't want all the things that LM has done.We want only the last answer, the last output, so that it will save our time as well as money.these are not truly free.All the hugging face is free, but not truly free.If you generate too many tokens, you will be charged.You will not be able to use.You will exhaust your limit too soon.Okay, so let's keep it false only.
# """
