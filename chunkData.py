from langchain import FAISS
from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter

import textract
from langchain.embeddings import OpenAIEmbeddings

import os

os.environ['OPENAI_API_KEY'] = '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'


def process_pdf(pdf_file_path: str):
    # Step 1 - Convert PDF to text
    doc = textract.process(pdf_file_path)

    # Step 2: Save to .txt and reopen (helps prevent issues)
    with open('source_documents/attention_is_all_you_need.txt', 'w', encoding='utf-8') as f:
        f.write(doc.decode('utf-8'))

    with open('source_documents/attention_is_all_you_need.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # Step 3: create a function to count tokens
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    def count_tokens(text: str) -> int:
        return len(tokenizer.encode(text))

    # Step 4 : Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=40,
        length_function=count_tokens,
    )

    chunks = text_splitter.create_documents([text])

    # Quick data visualization to ensure that the chunking worked right

    # Create a list of token counts
    token_counts = [count_tokens(chunk.page_content) for chunk in chunks]

    # # create a dataframe from the token counts
    # df = pd.DataFrame({'Token_count': token_counts})
    #
    # # create a histogram of the token count distribution
    # df.hist(bins=40, )
    #
    # # show the plot
    # plt.show()

    # Get embedding model
    embeddings = OpenAIEmbeddings()

    # Create a vector database
    db = FAISS.from_documents(chunks, embeddings)

    retriever = db.as_retriever()

    # retriever
    #
    # docs = retriever.get_relevant_documents("who created transformers?")
    #
    # print("\n\n".join([x.page_content[:200] for x in docs[:2]]))
