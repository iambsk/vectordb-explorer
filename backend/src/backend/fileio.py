# add file (will extract section add to db)
# this manages the chromadb instance
# have deletion too https://github.com/langchain-ai/langchain/discussions/9495


class FileDB:
    def __init__(self, 
                 folder: str,
                 chroma_dir: str = "chroma.sqlite"
                 
                 ) -> None:
        # the folder that should be watched
        self.folder: str = folder
        # the persistent chromadb location, this is going to be an sqlite file
        self.chroma_dir: str = chroma_dir
        self.chroma = None # this should be the langchain.chroma instance and should take in chroma_dir
        self.extractor = None #import extractor
        self.file_types = ["pdf","txt"] #w
        # reload() ensure everything upto date on start
    
    def reload(self):
        # this will check every file and add the missing ones
        # use tqdm to show iteration over all the files ?
        pass

    def import_file(self,file):
        # after a file is added to the db this might not be loaded in. Call extract and then add via langchain to the chromadb 
        # if file is in dir just check to see if in chromadb
        # if file is not in dir move it into the dir
        pass
    
    def search(self,query):
        # search filenames, metadata, and vectordb
        # return langchain objects
        # maybe filter?
        pass

    def delete(self,file):
        #delete file from folder
        #delete file from chroma
        pass

    



    

    