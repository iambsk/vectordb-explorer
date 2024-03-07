import chromadb
from backend.extractor import Extractor, Document
from typing import List, Optional, Dict, Any
import os, shutil
import uuid



class FileDB:
    def __init__(self, 
                 folder: str,
                 chroma_dir: str = "./chroma",
                 collection_name: str = "default",
                 ) -> None:
        # the folder that should be watched
        self.folder: str = folder
        self.chroma_dir = chroma_dir
        # the persistent chromadb location, this is going to be an sqlite file
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir) # this should be the langchain.chroma instance and should take in chroma_dir
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name) 
        self.extractor = Extractor() #import extractor
        self.file_types = ["pdf","txt"] 
        # reload() ensure everything upto date on start
        self.sync()
    
    @property
    def files(self):
        return [os.path.join(self.folder, file) for file in os.listdir(self.folder)]
    
    def update_folder(self,folder):
        self.folder = folder
        self.sync()
    
    def update_chroma_dir(self,chroma_dir):
        self.chroma_dir = chroma_dir
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection.name)
        self.sync()
        
    def sync(self):
        """
        Syncs the files in the watched folder with chromadb.
        Uses the folder as the source of truth. Will delete any documents in chromadb that are not in the folder.
        """
        for file in os.listdir(self.folder):
            if file.endswith(tuple(self.file_types)):
                self.sync_file(os.path.join(self.folder, file))
    
        documents = self.collection.get()
        for id,text,metadata in zip(documents['ids'],documents['documents'],documents['metadatas']):
            filename = metadata['filename']
            if filename not in [os.path.join(self.folder, file) for file in os.listdir(self.folder)]:
                self.collection.delete(ids=[id])
    
    def sync_file(self,file):
        if not file.endswith(tuple(self.file_types)):
            raise ValueError(f"File type not supported: {file}")
        documents = self.extractor.extract_to_documents(file)
        if not documents:
            print("No documents extracted")
            return
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
        # copy the file to the folder
        shutil.copy(file, self.folder)
        
        self.sync_file(file)
    
    def vector_search(self,
                      query_texts: Optional[List[str]] = None,
                      n_results: int = 10,
                      where: Optional[Dict[str, str]] = None,
                      **kwargs: Any
    ) -> List[Document]:
        """Query the chroma collection."""
        docs = self._vector_search(query_texts=query_texts,n_results=n_results,where=where,**kwargs)
        return [Document(text=text,metadata=metadata) for text,metadata in zip(docs['documents'][0],docs['metadatas'][0])]
    
    
    def _vector_search(
        self,
        query_texts: Optional[List[str]] = None,
        n_results: int = 10,
        where: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[dict]:
        """Query the chroma collection."""
        return self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            **kwargs,
        )
    
    

    def delete_file(self,file: str):
        os.remove(file)

        self.collection.delete(
            where={"filename": file}
        )

    



    

    