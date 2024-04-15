from backend.fileio import FileDB 


class UserDBs:
    def __init__(
        self,
        folder_prefix: str,
        chroma_dir: str = "./chroma",
        collection_prefix: str = "default",
    ) -> None:
        self.user_dbs = {}
        self.folder_prefix = folder_prefix
        self.chroma_dir = chroma_dir
        self.collection_prefix = collection_prefix

    def get_user_db(self, user_id: str) -> FileDB:
        if user_id not in self.user_dbs:
            self.user_dbs[user_id] = FileDB(
                folder=f"{self.folder_prefix}/{user_id}",
                chroma_dir=f"{self.chroma_dir}/{user_id}",
                collection_name=f"{self.collection_prefix}_{user_id}",
            )
        return self.user_dbs[user_id]

    def create_user_db(self, user_id: str) -> FileDB:
        if user_id in self.user_dbs:
            raise ValueError(f"User {user_id} already exists")
        return self.get_user_db(user_id)
    
    def delete_user_db(self, user_id: str) -> None:
        if user_id not in self.user_dbs:
            raise ValueError(f"User {user_id} does not exist")
        del self.user_dbs[user_id]
        return None

    def list_user_dbs(self) -> list:
        return list(self.user_dbs.keys())
    
    def sync_all(self) -> None:
        for user_id, user_db in self.user_dbs.items():
            user_db.sync()
        return None
    
    def __getitem__(self, user_id: str) -> FileDB:
        return self.get_user_db(user_id)
    
    def __delitem__(self, user_id: str) -> None:
        return self.delete_user_db(user_id)
    
    def __iter__(self):
        return iter(self.user_dbs)
    
    def __len__(self):
        return len(self.user_dbs)
    
    def __contains__(self, user_id: str):
        return user_id in self.user_dbs
    
    def __repr__(self):
        return f"UserDBs({self.user_dbs})"
    
    def __str__(self):
        return f"UserDBs({self.user_dbs})"
    
    
    
    
