import chromadb
from backend.extractor import Extractor, Document
from typing import List, Optional, Dict, Any
import os, shutil
import uuid
from pathlib import Path


class FileDB:
    def __init__(
        self,
        folder: str,
        chroma_dir: str = "./chroma",
        collection_name: str = "default",
    ) -> None:
        # Resolve and make the folder absolute
        self.folder: str = str(Path(folder).resolve().absolute())
        # Ensure the folder exists
        os.makedirs(self.folder, exist_ok=True)

        self.chroma_dir = str(Path(chroma_dir).resolve().absolute())
        # Ensure the chroma_dir exists
        os.makedirs(self.chroma_dir, exist_ok=True)

        # the persistent chromadb location, this is going to be an sqlite file
        self.chroma_client = chromadb.PersistentClient(
            path=chroma_dir
        )  # this should be the langchain.chroma instance and should take in chroma_dir
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )
        self.extractor = Extractor()  # import extractor
        self.file_types = ["pdf", "txt"]
        #  ensure everything upto date on start
        self.sync()

    @property
    def files(self):
        return [os.path.join(self.folder, file) for file in os.listdir(self.folder)]

    def update_folder(self, folder):
        self.folder = folder
        self.sync()

    def update_chroma_dir(self, chroma_dir):
        self.chroma_dir = chroma_dir
        self.chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection.name
        )
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
        for id, text, metadata in zip(
            documents["ids"], documents["documents"], documents["metadatas"]
        ):
            filename = metadata["filename"]
            if filename not in [
                os.path.join(self.folder, file) for file in os.listdir(self.folder)
            ]:
                self.collection.delete(ids=[id])

    def sync_file(self, filepath):
        path = str(Path(filepath).resolve().absolute())
        if not path.endswith(tuple(self.file_types)):
            raise ValueError(f"File type not supported: {path}")
        # check if the document was already in chromadb
        potential_docs = self.collection.get(where={"filename": path})
        if potential_docs["ids"]:
            return
        documents = self.extractor.extract_to_documents(path)
        if not documents:
            print("No documents extracted")
            return

        self.collection.add(
            documents=[doc.text for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            ids=[str(uuid.uuid4()) for _ in documents],
        )

    def add_file(self, file):
        """
        Moves a file from the given location to the watched folder, then syncs the file to chromadb
        """
        # copy the file to the folder
        try:
            shutil.copy(file, self.folder)
        except shutil.SameFileError:
            pass
        self.sync_file(os.path.join(self.folder, os.path.basename(file)))
        # self.sync()

    def add_text(self, text: str, metadata: dict = {}):
        filename = metadata.get("filename", f"{str(uuid.uuid4())}.txt")
        with open(os.path.join(self.folder, filename), "w") as f:
            f.write(text)
        self.sync_file(os.path.join(self.folder, filename))

    def vector_search(
        self,
        query_texts: Optional[List[str]] = None,
        n_results: int = 10,
        where: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Query the chroma collection."""
        docs = self._vector_search(
            query_texts=query_texts, n_results=n_results, where=where, **kwargs
        )
        return [
            Document(text=text, metadata=metadata)
            for text, metadata in zip(docs["documents"][0], docs["metadatas"][0])
        ]

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

    def delete_file(self, file: str):
        path = str(Path(file).resolve().absolute())
        print("Driectory contents: ", os.listdir(self.folder))
        os.remove(path)
        self.collection.delete(where={"filename": path})
        self.sync()
        print(f"Deleted {path}")
        print(f"Filedirs: {self.files}")
        print("Driectory contents: ", os.listdir(self.folder))
    
    def rename_folder(self, new_folder: str):
        new_folder = str(Path(new_folder).resolve().absolute())
        if os.path.exists(new_folder):
            shutil.copytree(self.folder, new_folder)
            shutil.rmtree(self.folder)
        else:
            os.rename(self.folder, new_folder)
            
        self.folder = new_folder
        self.sync()
    
    def rename_chroma_dir(self, new_chroma_dir: str):
        new_chroma_dir = str(Path(new_chroma_dir).resolve().absolute())
        self.chroma_dir = new_chroma_dir
        collection_name = self.collection.name
        if os.path.exists(new_chroma_dir):
            self.chroma_client = chromadb.PersistentClient(path=new_chroma_dir)
            self.collection = self.chroma_client.get_or_create_collection(
                name=collection_name
            )
            return 
        # Else Delete it
        del self.chroma_client
        del self.collection.name
        # Create a temp client to force the unloading of the old one (gc no worky)
        self.chroma_client = chromadb.PersistentClient(path=f'chroma_dir/nil')
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )
        os.mkdir(new_chroma_dir)
        shutil.move(self.chroma_dir, new_chroma_dir)
        # delete the temp
        del self.chroma_client
        del self.collection
        #create new one
        self.chroma_client = chromadb.PersistentClient(path=new_chroma_dir)
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name
        )
        #sync to make sure everythings fine
        self.sync()
    
    def __del__(self):
        self.chroma_client.reset()
        del self.extractor
        del self.chroma_client
        del self.collection
        
