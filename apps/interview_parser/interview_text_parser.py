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