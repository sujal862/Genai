from pydantic import BaseModel, Field
from pymongo.asynchronous.collection import AsyncCollection
from ..db import database


class FileSchema(BaseModel):
    name: str = Field(..., description="Name of the file")
    status: str = Field(..., description="Status of the file")


COLLECTION_NAME = "files"
files_collection: AsyncCollection = database[COLLECTION_NAME]
