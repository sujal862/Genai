from pdf2image import convert_from_path
from ..db.collections.files import files_collection
from bson import ObjectId
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Function to encode the image


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_file(id: str, file_path: str):
    await files_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "processing"}})

    await files_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "coverting to image"}})

    # Step 1: Convert pdf to image
    images = convert_from_path(file_path)
    image_paths = []

    for i, page in enumerate(images):
        image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
        os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
        page.save(image_save_path, 'JPEG')
        image_paths.append(image_save_path)

    await files_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": "coverting to image success"}})

    # Step 2: send image to gpt

    # Encode all images to base64 at the right time
    base64_image = [encode_image(img) for img in image_paths]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Based on the resume below, Roast this resume"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image[0]}"},
                    },
                ],
            }
        ],
    )

    # update roast result in db
    await files_collection.update_one({"_id": ObjectId(id)}, {
        "$set": {
            "status": "processed",
            "result": response.choices[0].message.content
        }
    })



# # Valkey : to use it we use rq package for python
# The Worker:
# To start executing enqueued function calls (i.e worker) in the background, start a worker from your project’s directory:

# ** rq worker --with-scheduler (run this on terminal to get o/p of queue worker)
