import textract
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from typing import List

class Document(BaseModel):
    text: str
    metadata: dict




class Extractor:
    def __init__(self,
                 chunk_size: int = 512,
                 chunk_overlap: int = 80):
        # init splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def extract_to_documents(self, file: str) -> List[Document]:
        content: list[str] = textract.process(file).decode('utf-8')
        metadata: dict = {} #include filename

        # Use sectioner to organize content into sections
        sections = self.splitter.create_documents(content)

        # prepare metadata
        metadata = {
            "filename": file, # add other metadata when needed
        }

        # Create LangChain documents from sections
        return [Document(text=section.page_content,metadata=metadata) for section in sections]

