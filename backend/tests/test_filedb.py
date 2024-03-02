import unittest
from backend.fileio import FileDB
import os, shutil

class FileIOTest(unittest.TestCase):
    def test_sync_and_search_file(self):
        filedb = FileDB(folder=".") 
        # Create a temporary file with some content
        with open('temp.txt', 'w') as file:
            file.write('Hello, World!')

        # Call the read_file function
        filedb.sync_file('temp.txt')
        result = filedb.vector_search('Hello, World!')
        self.assertEqual(result['metadatas'][0][0]['filename'], 'temp.txt')
        # Check if the result matches the expected output
        # self.assertEqual(result, 'Hello, World!')

        # Clean up the temporary file
        os.remove('temp.txt')
        shutil.rmtree('./chroma')

    def test_add_and_search_file(self):
        filedb = FileDB(folder=".")
        # Create a temporary file with some content
        with open('temp.txt', 'w') as file:
            file.write('Hello, World!')

        # Call the add_file function
        filedb.add_file('temp.txt')
        result = filedb.vector_search('Hello, World!')
        self.assertEqual(result['metadatas'][0][0]['filename'], 'temp.txt')
        # Check if the result matches the expected output
        # self.assertEqual(result, 'Hello, World!')

        # Clean up the temporary file
        os.remove('temp.txt')
        shutil.rmtree('./chroma')

if __name__ == '__main__':
    unittest.main()