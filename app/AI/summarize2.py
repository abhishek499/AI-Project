import os
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import ChatOpenAI
import openai
from transformers import GPT2TokenizerFast  # Use a compatible tokenizer
from tiktoken import get_encoding


async def summarizeUrls(urls):
    urls = urls[:3]  # Load only the first 3 URLs to reduce context size
    summary = []

    # Set up the LLM and summarization chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", api_key=os.getenv('chat_openai_key'))
    chain = load_summarize_chain(llm, chain_type="stuff")

    token_limit_per_doc = 1620

    for i, url in enumerate(urls):
        # Load document for the current URL
        loader = WebBaseLoader(url)
        docs = loader.load()
        summary_result = chain.invoke(docs)
        summary.append(f"{summary_result['output_text']}")
    return {"summary": summary}