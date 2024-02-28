import textract
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Extractor:
    def __init__(self):

        self.documents = None

        # init splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=80
        )

    def extract_to_langchain(self, file: str):
        content: list[str] = textract.process(file).decode('utf-8')
        metadata: dict = {} #include filename

        # Use sectioner to organize content into sections
        sections = self.splitter.create_documents(content)

        # prepare metadata
        metadata = {
            "filename": file, # add other metadata when needed
        }

        # Create LangChain documents from sections
        self.documents = [{"text": section, "metadata": metadata} for section in sections]

    def content(self,file: str):
        return self.documents
