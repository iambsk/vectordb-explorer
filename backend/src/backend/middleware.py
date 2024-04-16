from fastapi import FastAPI, HTTPException, UploadFile, File, Query, Depends
from typing import List, Optional
from pydantic import BaseModel
from backend.fileio import FileDB
from backend.userdb import UserDBs
import uvicorn
from backend.types import Document
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
from backend.auth import AuthStore


app = FastAPI()
auth_store = AuthStore(UserDBs(folder_prefix="./tmp/data"))

SECRET_KEY = "This is a secret key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user_db(token: str = Depends(oauth2_scheme)) -> FileDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return auth_store.get_user_db(username)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    password_hash = auth_store.get_password_hash(password)
    auth_store.register_user(username, password_hash)
    if auth_store.validate_user(username, password_hash):
        access_token = auth_store.create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")


class VectorSearchQuery(BaseModel):
    query_texts: Optional[List[str]] = None
    n_results: int = 10
    where: Optional[dict] = None


@app.get("/folder/")
def get_folder(file_db: FileDB = Depends(get_current_user_db)):
    return file_db.folder


@app.get("/chroma-dir/")
def get_chroma_dir(file_db: FileDB = Depends(get_current_user_db)):
    return file_db.chroma_dir


@app.get("/files/")
def get_files(file_db: FileDB = Depends(get_current_user_db)):
    return file_db.files


@app.post("/change-folder/")
def change_folder(
    folder: str = Query(..., description="Path of the new folder"),
    file_db: FileDB = Depends(get_current_user_db),
):
    try:
        file_db.update_folder(folder)
        return {"message": f"Folder changed to {folder}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/change-chroma-dir/")
def change_chroma_dir(
    chroma_dir: str = Query(..., description="Path of the new chroma directory"),
    file_db: FileDB = Depends(get_current_user_db),
):
    try:
        file_db.update_chroma_dir(chroma_dir)
        return {"message": f"Chroma directory changed to {chroma_dir}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sync/")
def sync_files(file_db: FileDB = Depends(get_current_user_db)):
    try:
        file_db.sync()
        return {"message": "Files synced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class FilePath(BaseModel):
    file_path: str


@app.post("/add-file/")
def add_file(file_path: FilePath, file_db: FileDB = Depends(get_current_user_db)):
    try:
        # Directly add the file using the provided path
        file_db.add_file(file_path.file_path)
        return {"message": f"File {file_path.file_path} added successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vector-search/", response_model=List[Document])
def vector_search(
    query: VectorSearchQuery, file_db: FileDB = Depends(get_current_user_db)
):
    try:
        result = file_db.vector_search(
            query_texts=query.query_texts, n_results=query.n_results, where=query.where
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete-file/")
def delete_file(
    file_path: str = Query(..., description="Path of the file to delete"),
    file_db: FileDB = Depends(get_current_user_db),
):
    try:
        file_db.delete_file(file_path)
        return {"message": f"File {file_path} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
