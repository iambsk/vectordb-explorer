from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from typing import List, Optional
from pydantic import BaseModel
from file_db import FileDB  # Assuming your class is saved in file_db.py
import uvicorn
from backend.tyeps import Document

app = FastAPI()

file_db = FileDB(folder="./sample/sample_files", chroma_dir="./sample/chroma")

class VectorSearchQuery(BaseModel):
    query_texts: Optional[List[str]] = None
    n_results: int = 10
    where: Optional[dict] = None

@app.get("/folder/")
def get_folder():
    return {"folder": file_db.folder}

@app.get("/chroma-dir/")
def get_chroma_dir():
    return {"chroma_dir": file_db.chroma_dir}

@app.get("/files/")
def get_files():
    return file_db.files

@app.post("/change-folder/")
def change_folder(folder: str = Query(..., description="Path of the new folder")):
    try:
        file_db.update_folder(folder)
        return {"message": f"Folder changed to {folder}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/change-chroma-dir/")
def change_chroma_dir(chroma_dir: str = Query(..., description="Path of the new chroma directory")):
    try:
        file_db.update_chroma_dir(chroma_dir)
        return {"message": f"Chroma directory changed to {chroma_dir}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync/")
def sync_files():
    try:
        file_db.sync()
        return {"message": "Files synced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class FilePath(BaseModel):
    file_path: str

@app.post("/add-file/")
def add_file(file_path: FilePath):
    try:
        # Directly add the file using the provided path
        file_db.add_file(file_path.file_path)
        return {"message": f"File {file_path.file_path} added successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vector-search/", response_model=List[Document])
def vector_search(query: VectorSearchQuery):
    try:
        result = file_db.vector_search(
            query_texts=query.query_texts, 
            n_results=query.n_results, 
            where=query.where
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-file/")
def delete_file(file_path: str = Query(..., description="Path of the file to delete")):
    try:
        file_db.delete_file(file_path)
        return {"message": f"File {file_path} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
