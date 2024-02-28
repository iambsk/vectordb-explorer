'''The data models gonna depend on the method, each gets its own

For search:
string query

For add_file():
File object

For delete_file():
string file path 
all of these should be post request
'''
from fastapi import FastAPI, HTTPException, status, Query, Response
from pydantic import BaseModel

app = FastAPI()

# Define the model
class Search(BaseModel):
    query: str

class add_file(BaseModel):
    file: str

class delete_file(BaseModel):
    filepath: str

# temp array to store the files
db = [{}] 

#declaring it as a parameter
@app.post("/search/")
async def search(item: Search):
    db.search(item.query)
    return item


#declaring it as a parameter
@app.post("/items/")
async def create_item(item: add_file):
    return item

#implementing the get items endpoint
@app.get("/items/")
def get_all_items():
    return {"files": db}

#creating the "search" endpoint
@app.post("/items/{item_id}")
def create_file(item_id: int, response: Response):
    if item_id in db:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "File already exists"}
    db.append(item_id)
    return {"item_id": item_id}

#deleting the "item" endpoint
@app.delete("/items/{item_id}")
def delete_file(item_id: int, response: Response):
    if item_id not in db:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "File does not exist"}
    db.remove(item_id)
    return {"item_id": item_id}

'''
abstract everything we do here into an easy function for the front end like: search()
'''

