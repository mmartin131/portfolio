# CHANGE HISTORY
#----------------------------------------------------------------------------
# V2.0 - Chris - Major UI change and source citation
# V2.1 - Jose / Shalini - Introduced Cuda and GPU processing to improve speed
# V2.2 - Chris - 1) Detect if Cuda is compatible and switch to CPU if not. 2) Changed chunk size from 1000 to 250 3) Lab results now format as a proper markdown table 4) Get a readability score at the bottom after the discharge is created.
# V2.3 - Jose - 1) Removed Souce Citation and printing loop (to enable other features) 2) UI changes to allow two side by side with the markdown format 3) Page Word stats now under the text box 4) threadsn and gpu for shalini use case, will be revised in fuure
# V2.4 - Megan: updated to use template "Instructions_Template_v4.xlsx" with updated recommendations section
#Future Changes Needed: Enabling source citation, fixing the table formating, finalize threads and gpu layers, enable state in order to not clear out the markdown text
#----------------------------------------------------------------------------

import pandas as pd
import torch

import streamlit as st
st.set_page_config(layout="wide", page_title = "Clarifying Care")

from langchain.llms import LlamaCpp

#Import local modules
import read_scores as rs
import citation_source as cs
import summarizer as summ

#If running on the EC2 instance, use 100 gpu_layers, else 0
gpu_layers = 100 if torch.cuda.is_available() else 0

llm = LlamaCpp(
    model_path="../streamlit/models/llama-2-7b-chat.Q4_0.gguf",
    temperature=0.1,
    max_tokens=512,
    top_p=1,
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=gpu_layers
)

st.session_state['model_complete'] = False           

def intro():
    
    st.image('../Logo.png', width=200)

    tab1, tab2, tab3 = st.tabs(["Demo", "Analytics", "Our Mission"])


    # Demo Tab
    with tab1:
        # Create a container to hold the intial input text area the user enters the original discharge summary into. The container spans the entire width of the page and no other controls are visible until the user presses generate discharge summary.
        container_inputnotes = st.empty()
        container_inputnotes.container(border=False)
        with container_inputnotes:

            st.write(
                """
                Place in your own text and see the conversion to our simplified version following SBAR standards.
                """
            )

            textarea_inputnotes = ""
            submitButton = False

            with st.form(key='form1'):
                    textarea_inputnotes = st.text_area("Enter Hospital Notes :", height=500)
                    submitButton = st.form_submit_button(label = '💖 Generate Summary')

        # Create another container that will contain a formatted version of the user's input text and the resulting discharge summary. It is hidden until the user clicks the discharge summary button.
        container_output = st.container(border=False)
        with container_output:
            
            # The container contains 2 columns. The first column contains the user's hospital notes from the textbox that have been rendered as static text, and the second holds the markdown discharge summary
            c1, c2= st.columns([0.35,0.65])
            
            # Create a column and a blank control that will eventually be populated with the user's hospital notes from the textbox (rendered as static text)
            with c1:
                container_textinputnotes = st.empty()
                
            # Create a column that will contain the discharge summary as it gets generated
            with c2: 
                 
                # Controls all the actions that happen after the user clicks the 'Generate Summary' button. 
                if submitButton:
                    st.session_state['model_complete'] = False

                    # Populate the text control in the left column with the user's input text
                    with container_textinputnotes.container(border=True):
                        st.markdown("# Hospital Notes")
                        string_originalnotes = textarea_inputnotes
                        st.session_state['string_originalnotes'] = string_originalnotes
                        text_inputnotes = st.text(textarea_inputnotes)
                    
                    #container_dischargesummary.container(border=True)
                    with st.container(border=True):
                        # Render the header at the beginning so the container border shows even before the discharge summary begins getting created.
                        st.markdown("# Patient Discharge Summary")

                        # Create a progress bar that will appear below the Patient Discharge Summary title while rendering but is hidden afterwards
                        chain_progress_bar = st.progress(0, text='Initializing Model...')

                        # Hide the original text area the user populated
                        container_inputnotes.empty()

                        final_markdown = summ.generate_summary(llm, textarea_inputnotes, chain_progress_bar)
                        st.session_state['final_markdown'] = final_markdown

                        # At this point the discharge summary has now been rendered and we can show the download button and readability summary
                        st.session_state['model_complete'] = True

                        # Hide the progress bar at the top
                        chain_progress_bar.empty()

                        # Show the download button
                        st.markdown("")
                        st.download_button(label="Download Summary",
                                    data=final_markdown,
                                    file_name="summary.md",
                                    mime='text/csv')
                        
                        #Add PDF download
                        # with open("markdown.md", "w") as file:
                        #     file.write(final_markdown)

                        # doc = aw.Document("markdown.md")
                        # doc.save("summary.pdf")
                        # with open("summary.pdf", "rb") as file:
                        #     st.download_button(label="Download Summary",
                        #             data=file,
                        #             file_name="summary.pdf",
                        #             mime='text/csv')
                        


        with tab2:
            def click_button_readabilityscore():
                markdown_readabilityscore.markdown(rs.calculate_readability_scores(st.session_state['string_originalnotes'],st.session_state['final_markdown']))

            st.markdown("# Discharge Readability Score")

            container_readabilityscore = st.container(border=False)
            with container_readabilityscore:
                markdown_readabilityscore = st.markdown("Please generate a discharge summary, then return to this tab to analyze the readability of it.")
                
                
            if st.button("Calculate Readability Score", type="primary"):
                markdown_readabilityscore.markdown(rs.calculate_readability_scores(st.session_state['string_originalnotes'],st.session_state['final_markdown']))
                



        with tab3:    
            st.markdown(
                """
                Our mission is to simplify the hopsital discharge summary process by creating discharge summaries and making them more patient friendly.
                
                ### How do we accomplish our mission? 
                - Creating Discharge Summaries
                    - Prompt Engineering an LLM with hospital records, in this discharge notes in the dicharge csv from MIMIC IV Notes 
                - More Patient Friendly
                    - Following SBAR Format
                    - Validating the sumnmary requires a lower grade level of reading comprehention


                **Check the demo below** to see some examples
                of how we can simplify medical text!

                ### Text Demo: 
                - Place in your own text and see the conversion to our simplified version following SBAR standards

            """
            )

intro()