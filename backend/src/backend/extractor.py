import textract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.types import Document
from typing import List



class Extractor:
    def __init__(self,
                 chunk_size: int = 512,
                 chunk_overlap: int = 80):
        # init splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def extract_to_text(self, file: str) -> str:
        return textract.process(file).decode('utf-8')
    
    def extract_to_documents(self, file: str) -> List[Document]:
        print(f"Extracting text from {file}")
        try:
            content: str = textract.process(file).decode('utf-8')
        except Exception as e:
            print(f"Error extracting text from {file}: {e}")
            return []
        metadata: dict = {} #include filename
        # Use sectioner to organize content into sections
        sections = self.splitter.create_documents([content])

        # prepare metadata
        metadata = {
            "filename": file, # add other metadata when needed
        }

        # Create LangChain documents from sections
        return [Document(text=section.page_content,metadata=metadata) for section in sections]

