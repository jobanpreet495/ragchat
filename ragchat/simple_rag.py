
from ragchat.ragargs.textsplitter import text_splitter
from ragchat.document_loader import DocumentLoader
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings , OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


class naive_rag:
    """
    A simplified Retrieval-Augmented Generation (RAG) pipeline for document processing.

    Args:
        path (str): Path to the input document (.txt, .pdf, .docx).
        text_splitter (str): Text splitting method (`RecursiveCharacterTextSplitter`, `CharacterTextSplitter`).
        chunk_size (int, optional): Number of characters per chunk (default: 1000).
        chunk_overlap (int, optional): Overlap between chunks (default: 200).
        embedding_platform (obj, optional): Embedding model for retrieval (default: `sentence-transformers/all-MiniLM-L6-v2`, supported: `OpenAIEmbeddings`).
        model (obj, optional): Language model for generation (default: `openai`, supports `openai` , `huggingface`).
        api_key (str) : Define API key . For default parameters provide groq API .

    Description:
        This class implements a simple RAG approach to split documents, retrieve relevant content using embeddings, and generate responses using a language model.
    """

    def __init__(self, path, text_splitter="RecursiveCharacterTextSplitter", chunk_size=1000, chunk_overlap=200, 
                 embedding_model="sentence-transformers/all-MiniLM-L6-v2", model="openai", api_key=""):
       
        self.path = path
        self.text_splitter = text_splitter
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.model = model
        self.api_key = api_key  



    def fit(self):
        # Load Documents data
        loader = DocumentLoader(self.path)
        text  = loader.load_document()
        # Split text into chunks
        splitter= text_splitter(self.text_splitter,self.chunk_size , self.chunk_overlap)
        texts = splitter.split_text(text)

        # Create embeddings and vector store
       
        if self.embedding_model=="openai":
            embedding_model = OpenAIEmbeddings(openai_api_key=self.api_key)
       
        elif self.embedding_model.split('/')[0] =="sentence-transformers":
            embedding_model = HuggingFaceEmbeddings(model_name=self.embedding_model.split('/')[1])
        vectorstore = FAISS.from_texts(texts , embedding_model)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
    def chat(self,question):
        
        context = self.retriever.invoke(question)
        prompt = hub.pull("rlm/rag-prompt")
        prompt = prompt.format(context=context , question=question)
        if self.model=="openai":
            llm = ChatOpenAI(model="gpt-4o-mini",openai_api_key = self.api_key)


        chain = prompt | llm |  StrOutputParser()
        answer = chain.invoke(question)
        return answer


