def get_data_from_word(path_to_file):
    from docx import Document

    # Creating a word file object
    doc_object = open(path_to_file, "rb")

    # creating word reader object
    doc_reader = Document(doc_object)
    data = ""

    for p in doc_reader.paragraphs:
        data += p.text + "\n"

    return data

def convert_docs(docx_data):
    try:
        file_data = docx_data.split('\n')
        paragraphs = []
        s = 0
        f = 3
        for x in range(len(file_data)//3):
            paragraphs.append(file_data[s:f])
            s+=3
            f+=3
        import pandas as pd
        interview_df = pd.DataFrame(paragraphs)
        interview_df.columns = ['time','speaker','text']
        return interview_df
    except:
        pass