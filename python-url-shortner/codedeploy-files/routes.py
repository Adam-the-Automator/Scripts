from fastapi import FastAPI, Response, status, Request
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from pydantic import BaseModel
import datetime
import shortuuid
import os

app = FastAPI()
client = MongoClient(os.environ.get('MONGO_URI'))
url_collection = client['ata-url-app']

# Retrieve long_url from database and redirect to long_url
@app.get("/detail")
async def detail():
    return {"message":"REST API for generating short URLs"}


# Retrieve long_url from database and redirect to long_url
@app.get("/{short_url_id}")
async def root(response: Response, request: Request):
    short_url_id = request.url.path.split('/')[1]

    data = url_collection.urls.find_one({"url_id": short_url_id})

    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'Url for {} not found'.format(data)}

    return RedirectResponse(data['long_url'])


class UrlModel(BaseModel):
    url: str


# Insert long_url to database
@app.post("/shorty")
def url(url: UrlModel, response: Response):
    print(url)
    if url is not None and type(url.url) == str:
        url_id = shortuuid.uuid()
        short_url = "http://localhost:8000/{0}".format(url_id)

        data = {
            "long_url": url.url,
            "short_url": short_url,
            "dateCreated": datetime.datetime.now(),
            "url_id": url_id
        }

        url_collection.urls.insert_one(data)

        return {"short_url": short_url}

    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return {'message': 'No valid url in request body'}
