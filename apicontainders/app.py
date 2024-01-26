from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
from datetime import datetime
import os

app = FastAPI()

# MongoDB connection
try:
    client = MongoClient(os.environ.get("MONGODB_URI"))
    db = client["imagedb"]  # Create a new database named "imagedb"
    image_collection = db["imagecollection"]  # Create a new collection named "imagecollection"

    if "imagedb" not in client.list_database_names():
        print("Creating database: imagedb")
        client.admin.command("create", "imagedb")
    else:
        print("database already exists")

    if "imagecollection" not in db.list_collection_names():
        print("Creating collection: imagecollection")
        db.create_collection("imagecollection")
    else:
        print("collections already exists")
    # Check if the connection is successful
    client.server_info()

    print("MongoDB connection was successful")

except Exception as e:
    print(f"Unable to connect to MongoDB. Error: {e}")
    raise

class Image(BaseModel):
    id: Optional[str]
    url: str
    created_at: Optional[datetime] = None

# Function to get all images from the database
def get_all_images():
    return [{"id": str(image["_id"]), "url": image["url"], "created_at": image["created_at"]} for image in image_collection.find()]

# Function to add a new image to the database
async def add_image(new_image):
    new_image_data = {
        "url": new_image.url,
        "created_at": new_image.created_at
    }
    result = image_collection.insert_one(new_image_data)  # Await MongoDB operation
    new_image.id = str(result.inserted_id)
    return new_image

# Function to delete an image by ID
def delete_image(image_id):
    result = image_collection.delete_one({"_id": image_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Image with id {image_id} not found")

# Get all images
@app.get("/images", response_model=List[Image])
async def images():
    return get_all_images()

# Add a new image
@app.post("/add_image", response_model=Image, status_code=status.HTTP_201_CREATED)
async def add_image_endpoint(image: Image):
    added_image = await add_image(image)  # Await the coroutine and return the result
    return added_image

# Delete an image
@app.delete("/delete_image/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image_endpoint(image_id: str):
    delete_image(image_id)
    return None  # Return None as the response for successful deletion

