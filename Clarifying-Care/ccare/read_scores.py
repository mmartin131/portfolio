import textstat
import streamlit as st

# Function to calculate the readability scores of the input text
def show_readability_scores(original_text,model_text):
    st.markdown(calculate_readability_scores(original_text,model_text))

def calculate_readability_scores(original_text,model_text):
    """Function to calculate the desired readability scores when
    a text is passed to the function."""
    score_results = f'''
        |Readability Test|Original Discharge Summary|Clarifying Care|
        |---|---|---|
        |**dale_chall** | **{textstat.dale_chall_readability_score(original_text)}** | **{textstat.dale_chall_readability_score(model_text)}** |
        |flesch_reading_ease | {textstat.flesch_reading_ease(original_text)} | {textstat.flesch_reading_ease(model_text)} |
        |flesch_kincaid_grade | {textstat.flesch_kincaid_grade(original_text)} | {textstat.flesch_kincaid_grade(model_text)} |
        |gunning_fog | {textstat.gunning_fog(original_text)} | {textstat.gunning_fog(model_text)} |
        |SMOG_index | {textstat.smog_index(original_text)} | {textstat.smog_index(model_text)} |
        |consensus_score | {textstat.text_standard(original_text, float_output=False)} | {textstat.text_standard(model_text, float_output=False)} |
        |sentence_count | {textstat.sentence_count(original_text)} | {textstat.sentence_count(model_text)} |
        |word_count | {textstat.lexicon_count(original_text, removepunct=True)} | {textstat.lexicon_count(model_text, removepunct=True)} |
        |reading_time | {textstat.reading_time(original_text, ms_per_char=14.69)} | {textstat.reading_time(model_text, ms_per_char=14.69)} |

        ***

        ##### Definitions:

        **dale_chall** - The Dale-Chall readability score gauges how difficult a text is to understand by analyzing its vocabulary and sentence length. This is the recommended readability score to reference.

        **flesch_reading_ease** - The Flesch-Reading Ease score reflects how easy a text is to read by considering average sentence length and the number of syllables per word.  

        **flesch_kincaid_grade** - The Flesch-Kincaid Grade Level score estimates the U.S. education level needed to comprehend the text.  

        **gunning_fog** - The Gunning Fog Index calculates the years of formal education required to grasp a text on the first try, based on sentence length and complex vocabulary.  

        **SMOG_index** - The SMOG Index, which stands for "Simple Measure of Gobbledygook," estimates the years of education someone needs to understand a written passage.  

        **consensus_score** - The consensus score in readability combines multiple readability formulas to provide a more comprehensive picture of a text's difficulty.  

        **sentence_count** - The total number of sentences in the discharge summary.  

        **word_count** - The total number of words in the discharge summary.  

        **reading_time** - The estimated time it would take to read the discharge summary (assuming 14.7 ms per character).  


        ***      
        '''
    return score_results