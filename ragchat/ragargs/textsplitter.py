from langchain_text_splitters import RecursiveCharacterTextSplitter , CharacterTextSplitter

def text_splitter(text_splitter,chunk_size , chunk_overlap):
    if text_splitter=="RecursiveCharacterTextSplitter":
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
    elif text_splitter=="CharacterTextSplitter":
        splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    return splitter
    