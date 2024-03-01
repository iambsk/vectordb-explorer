# add file (will extract section add to db)
# this manages the chromadb instance
# have deletion too https://github.com/langchain-ai/langchain/discussions/9495
import chromadb
from backend.extractor import Extractor, Document
from typing import List, Optional, Dict, Any
import os
import uuid



class FileDB:
    def __init__(self, 
                 folder: str,
                 chroma_dir: str = "./chroma",
                 collection_name: str = "default",
                 ) -> None:
        # the folder that should be watched
        self.folder: str = folder
        # the persistent chromadb location, this is going to be an sqlite file
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir) # this should be the langchain.chroma instance and should take in chroma_dir
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name) 
        self.extractor = Extractor() #import extractor
        self.file_types = ["pdf","txt"] 
        # reload() ensure everything upto date on start
        self.sync()
    
    def sync(self):
        # this will check every file and add the missing ones
        # use tqdm to show iteration over all the files ?
        for file in os.listdir(self.folder):
            if file.endswith(tuple(self.file_types)):
                self.sync_file(file)

    def sync_file(self,file):
        documents: List[Documents] = self.extractor.extract_to_documents(file)
        # check if the document was already in chromadb
        potential_docs = self.collection.get(
            where={"filename": file}
        )
        if potential_docs['ids']:
            return
        self.collection.add(documents=[doc.text for doc in documents],metadatas=[doc.metadata for doc in documents], ids=[str(uuid.uuid4()) for _ in documents])
    
    def add_file(self,file):
        """
        Moves a file from the given location to the watched folder, then syncs the file to chromadb
        """
        os.rename(file, os.path.join(self.folder, file))
        self.sync_file(file)
    
    def vector_search(
        self,
        query_texts: Optional[List[str]] = None,
        n_results: int = 10,
        where: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Query the chroma collection."""
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            **kwargs,
        )
    

    def delete(self,file):
        self.collection.delete(
            where={"filename": file}
        )

    



    

    