import unittest
import shutil
from backend.userdb import UserDBs


class UserDBTest(unittest.TestCase):
    def test_creation(self):
        userdb = UserDBs(folder_prefix=".", chroma_dir=".", collection_prefix="default")
        self.assertIsNotNone(userdb)
        self.assertEqual(userdb.folder_prefix, ".")
        self.assertEqual(userdb.chroma_dir, ".")
        self.assertEqual(userdb.collection_prefix, "default")
        
        # Cleanup the temp files
        shutil.rmtree('./chroma')
        

    def test_multiple_differ(self):
        userdb = UserDBs(folder_prefix=".", chroma_dir=".", collection_prefix="default")
        userdb.create_user_db("user1")
        userdb.create_user_db("user2")
        self.assertEqual(userdb.list_user_dbs(), ["user1", "user2"])
        user1 = userdb["user1"]
        user1.add_text("Test")

        self.assertEqual(len(user1.files), 1)
        self.assertEqual(len(userdb["user2"].files), 0)
        del userdb["user1"]
        del userdb
        shutil.rmtree('./chroma')

    def test_delete(self):
        userdb = UserDBs(folder_prefix=".", chroma_dir=".", collection_prefix="default")
        userdb.create_user_db("user1")
        userdb.create_user_db("user2")
        userdb.delete_user_db("user1")
        self.assertEqual(userdb.list_user_dbs(), ["user2"])
        
        shutil.rmtree('./chroma')

    def test_contains(self):
        userdb = UserDBs(folder_prefix=".", chroma_dir=".", collection_prefix="default")
        userdb.create_user_db("user1")
        self.assertTrue("user1" in userdb)
        self.assertFalse("user2" in userdb)
        shutil.rmtree('./chroma')

    def test_iter(self):
        userdb = UserDBs(folder_prefix=".", chroma_dir=".", collection_prefix="default")
        userdb.create_user_db("user1")
        userdb.create_user_db("user2")
        self.assertEqual(list(userdb), ["user1", "user2"])
        shutil.rmtree('./chroma')

    def test_len(self):
        userdb = UserDBs(folder_prefix=".", chroma_dir=".", collection_prefix="default")
        userdb.create_user_db("user1")
        userdb.create_user_db("user2")
        self.assertEqual(len(userdb), 2)
        shutil.rmtree('./chroma')


if __name__ == "__main__":
    unittest.main()
