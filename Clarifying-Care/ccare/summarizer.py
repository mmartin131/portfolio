from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA 
from langchain.vectorstores import FAISS   


import torch
import pandas as pd
import streamlit as st

import citation_source as cs

def get_doctor_prompt(template,question):
    B_INST, E_INST = "<s>[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"


    prompt_template =  B_INST + B_SYS + str(template) + E_SYS + str(question) + E_INST

    return prompt_template

def generate_summary(llm, textarea_inputnotes, chain_progress_bar):
    #Setup and run the model
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    documents = [Document(page_content=x) for x in text_splitter.split_text(textarea_inputnotes)]

    all_splits = text_splitter.split_documents(documents)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model_name = "sentence-transformers/all-mpnet-base-v2"
    if device.type == 'cuda':
        model_kwargs = {"device": "cuda"}
        embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
    else:
        embeddings = HuggingFaceEmbeddings(model_name=model_name)


    vectorstore = FAISS.from_documents(all_splits, embeddings)

    chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=vectorstore.as_retriever(), return_source_documents=True)

    # Pull in the prompts from the excel file
    df_instructions = pd.read_excel(r"","Instructions")

    # Setup the progress bar
    final_markdown_list = []
    final_sources_list = []
    progress_counter = 0
    progress_totalsteps = len(df_instructions)
    height_md = 500
    final_markdown = f'''
![N|Solid](https://i.ibb.co/2SP897D/Clarifying-Care-Logo-V2.png)
# Patient Discharge Summary

'''
    #final_markdown = "![N|Solid](https://i.ibb.co/2SP897D/Clarifying-Care-Logo-V2.png)  "
    #final_markdown = final_markdown + "# Patient Discharge Summary  "

    # Loops through each row in the excel file
    for index, row in df_instructions.iterrows():

        # Sends the prompt to the model and captures the result
        chain_progress_bar.progress(progress_counter/progress_totalsteps, text='Generating ' + str(row["Section"]) + ' Summary...' )
        result = chain({"query": get_doctor_prompt(row["Prompt Template"],row["Question"])})

        # Adds a new markdown control under the previous one with the results from the model along with any pre-defined markdown that should be concatenated before and after this section
        st.markdown(str(row["Pre-Markdown"]) + str(result['result']) + str(row["Post-Markdown"]), unsafe_allow_html=True, help=cs.format_source_citation(result['source_documents']))

        # Appends the result to a variable. This is the source that is rendered by the download button
        final_markdown = final_markdown + str(row["Pre-Markdown"]) + str(result['result']) + str(row["Post-Markdown"])
        ###final_markdown = final_markdown + str(row["Pre-Markdown"]) + str(row["Post-Markdown"])

        # Increment up the progress bar
        progress_counter = progress_counter + 1

    return final_markdown

