import requests

class FileDBClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def sync_files(self):
        response = requests.post(f"{self.base_url}/sync/")
        return response.json()

    def add_file(self, file_path: str):
        response = requests.post(f"{self.base_url}/add-file/", json={"file_path": file_path})
        return response.json()

    def vector_search(self, query_texts=None, n_results=10, where=None):
        payload = {
            "query_texts": query_texts,
            "n_results": n_results,
            "where": where
        }
        response = requests.post(f"{self.base_url}/vector-search/", json=payload)
        return response.json()

    def delete_file(self, file_path: str):
        params = {"file_path": file_path}
        response = requests.delete(f"{self.base_url}/delete-file/", params=params)
        return response.json()