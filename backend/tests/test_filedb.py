import unittest
from backend.fileio import FileDB
import os, shutil
from pathlib import Path
class FileIOTest(unittest.TestCase):
    def test_sync_and_search_file(self):
        filedb = FileDB(folder="./test/files", chroma_dir="./test/chroma")
        # Create a temporary file with some content
        with open('temp.txt', 'w') as file:
            file.write('Hello, World!')

        # Call the read_file function
        filedb.sync_file('temp.txt')
        results = filedb.vector_search('Hello, World!')
        # self.assertEqual(result[0], 'temp.txt')
        # assert results[0].metadata['filename'].endswith('temp.txt')
        assert results[0].text == 'Hello, World!'
        # self.assertEqual(results[0].metadata['filename'], 'temp.txt')
        # Check if the result matches the expected output
        # self.assertEqual(result, 'Hello, World!')
        del filedb

        # Clean up the temporary file
        # os.remove('temp.txt')
        shutil.rmtree('./test/files')

    def test_add_and_search_file(self):
        filedb = FileDB(folder="./test/files", chroma_dir="./test/chroma")
        # Create a temporary file with some content
        with open('temp.txt', 'w') as file:
            file.write('Hello, World!')

        # Call the add_file function
        filedb.add_file('temp.txt')
        results = filedb.vector_search('Hello, World!')
        # assert results[0].metadata['filename'].endswith('temp.txt')
        assert results[0].text == 'Hello, World!'
        # Check if the result matches the expected output
        # self.assertEqual(result, 'Hello, World!')

        del filedb
        # Clean up the temporary file
        # os.remove('temp.txt')
        # shutil.rmtree('./test/chroma')
        shutil.rmtree('./test/files')
        
    
    def test_add_and_search_text(self):
        filedb = FileDB(folder="./test/files", chroma_dir="./test/chroma")
        # Call the add_text function
        filedb.add_text('Hello, World!')
        results = filedb.vector_search('Hello, World!')
        assert results[0].text == 'Hello, World!'
        # self.assertEqual(results[0].metadata['filename'], 'temp.txt')
        # Check if the result matches the expected output
        # self.assertEqual(result, 'Hello, World!')
        del filedb
        # Clean up the temporary file
        # os.remove('temp.txt')
        # shutil.rmtree('./test/chroma')
        shutil.rmtree('./test/files')
    
    def test_delete_file(self):
        filedb = FileDB(folder="./test/files", chroma_dir="./test/chroma")
        start_len = len(filedb.files)
        # Create a temporary file with some content
        with open('temp.txt', 'w') as file:
            file.write('Hello, World!')

        # Call the add_file function
        filedb.add_file('temp.txt')
        # Call the delete_file function
        filedb.delete_file(Path('./test/files/temp.txt').resolve().absolute())
        self.assertEqual(len(filedb.files), start_len)
        # Check if the result matches the expected output
        del filedb
        shutil.rmtree('./test/files')
        

if __name__ == '__main__':
    unittest.main()