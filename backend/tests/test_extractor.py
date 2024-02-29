import unittest
from backend.extractor import Extractor
import os, shutil

class ExtractorTest(unittest.TestCase):
    def test_extract_file(self):
        extractor = Extractor()
        # Create a temporary file with some content
        with open('temp.txt', 'w') as file:
            file.write('Hello, World!')
        text = extractor.extract_to_text('temp.txt')
        self.assertEqual(text, 'Hello, World!')


        os.remove('temp.txt')

if __name__ == '__main__':
    unittest.main()