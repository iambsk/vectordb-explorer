# Extract text from file, section it with langchain sectioner, then make langchain documents
# include metadata in documents
# use textract
import textract

class Extractor:
    # def __init__():

    def extract_to_langchain(self,file: str):
        content: str = textract.process(file)
        metadata: dict = {} #include filename
        # extract
        # section
    
    def content(self,file: str):
        # just returns the content of the file
        pass
