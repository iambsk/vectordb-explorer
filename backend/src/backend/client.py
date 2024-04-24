import requests
from backend.types import Document


class FileDBClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    @property
    def folder(self):
        response = requests.get(f"{self.base_url}/folder/")
        return response.json()

    @property
    def chroma_dir(self):
        response = requests.get(f"{self.base_url}/chroma-dir/")
        return response.json()

    def change_folder(self, folder: str):
        response = requests.post(
            f"{self.base_url}/change-folder/", json={"folder": folder}
        )
        return response.json()

    def change_chroma_dir(self, chroma_dir: str):
        response = requests.post(
            f"{self.base_url}/change-chroma-dir/", json={"chroma_dir": chroma_dir}
        )
        return response.json()

    def sync_files(self):
        response = requests.post(f"{self.base_url}/sync/")
        return response.json()

    def add_file(self, file_path: str):
        response = requests.post(
            f"{self.base_url}/add-file/", json={"file_path": file_path}
        )
        return response.json()

    def vector_search(self, query_texts=None, n_results=10, where=None):
        payload = {"query_texts": query_texts, "n_results": n_results, "where": where}
        response = requests.post(f"{self.base_url}/vector-search/", json=payload)
        return response.json()

    def delete_file(self, file_path: str):
        params = {"file_path": file_path}
        response = requests.delete(f"{self.base_url}/delete-file/", params=params)
        return response.json()


class AuthFileDBClient(FileDBClient):
    def __init__(self, username: str = None, password: str = "", base_url="http://127.0.0.1:8000"):
        super().__init__(base_url)
        
        self.username = username
        self.password = password
        self.token = self.get_token()

    def get_token(self):
        """Authenticate with the server and retrieve the access token."""
        if not self.username:
            response = requests.post(f"{self.base_url}/create-temp-user")
            res_data = response.json()
            self.username = res_data["username"]
            self.password = res_data["password"]
            return res_data["access_token"]
        response = requests.post(
            f"{self.base_url}/token",
            data={"username": self.username, "password": self.password},
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Authentication failed")

    def user_to_permanent(self, username, password):
        """Convert a temporary token to a real token."""
        
        json_data = {
        "temp_username": self.username,
        "temp_password": self.password,
        "new_username": username,
        "new_password": password
    }
        response = requests.post(f"{self.base_url}/convert-to-permanent", json=json_data)
        if response.status_code == 400:
            pass
        elif response.status_code == 200:
            pass
        else:
            raise Exception("Conversion failed")
        self.username = username
        self.password = password
        self.token = self.get_token()
        
    
    def _get_headers(self):
        """Generate headers dict including the Authorization header."""
        return {"Authorization": f"Bearer {self.token}"}

    def _make_request(self, method, url, **kwargs):
        """General request method with authentication header."""
        headers = self._get_headers()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        response = requests.request(method, url, **kwargs)
        if response.status_code == 401:  # Token may have expired
            self.token = self.get_token()  # Refresh token
            kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
            response = requests.request(method, url, **kwargs)  # Retry request
        return response

    @property
    def folder(self):
        response = self._make_request("GET", f"{self.base_url}/folder/")
        return response.json()

    @property
    def chroma_dir(self):
        response = self._make_request("GET", f"{self.base_url}/chroma-dir/")
        return response.json()

    def change_folder(self, folder: str):
        response = self._make_request(
            "POST", f"{self.base_url}/change-folder/", json={"folder": folder}
        )
        return response.json()

    def change_chroma_dir(self, chroma_dir: str):
        response = self._make_request(
            "POST",
            f"{self.base_url}/change-chroma-dir/",
            json={"chroma_dir": chroma_dir},
        )
        return response.json()

    def sync_files(self):
        response = self._make_request("POST", f"{self.base_url}/sync/")
        return response.json()

    def add_file(self, file_path: str):
        response = self._make_request(
            "POST", f"{self.base_url}/add-file/", json={"file_path": file_path}
        )
        return response.json()

    def vector_search(self, query_texts=None, n_results=10, where=None):
        payload = {"query_texts": query_texts, "n_results": n_results, "where": where}
        response = self._make_request(
            "POST", f"{self.base_url}/vector-search/", json=payload
        )
        res = response.json()
        return [Document(text=doc["text"], metadata=doc["metadata"]) for doc in res]

    def delete_file(self, file_path: str):
        response = self._make_request(
            "DELETE", f"{self.base_url}/delete-file/", params={"file_path": file_path}
        )
        return response.json()
