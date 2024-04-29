def format_source_citation(source_text):
    #Escape special characters that can cause issues with formatting
    ##source_text = source_text.replace("# ","\# ")
    #Split the source_documents result into each document
    ##source_list = list(source_text[1:-1].split("Document(page_content=")) 
    ##source_list.pop(0)
    source_list = source_text
    source_count = len(source_list)
    source_counter = 0
    formatted_text = ''
    #Loop through each document and create a string to show in the tool top
    for document in source_list:
        source_counter = source_counter+1
        source_without_linebreaks = str(document)
        source_without_linebreaks = source_without_linebreaks[14:-1].replace("# ","\# ")
        source_without_linebreaks = source_without_linebreaks.replace("\\n"," ")

        formatted_text = formatted_text + f'''
# Source {source_counter} of {source_count}
{source_without_linebreaks}

        '''

    return formatted_text