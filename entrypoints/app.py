from urllib.parse import urlparse

import boto3
import httpx
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from datetime import UTC, datetime


app = FastAPI()

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("url-shortener-table")


class ShortenRequest(BaseModel):
    url: str


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/shorten")
async def shorten(request: ShortenRequest):

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "https://tinyurl.com/api-create.php",
            params={
                "url": request.url
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Erro ao encurtar URL."
        )

    short_url = response.text.strip()

    short_code = urlparse(short_url).path.lstrip("/")

    table.put_item(
        Item={
            "short_code": short_code,
            "original_url": request.url,
            "short_url": short_url,
            "created_at": datetime.now(UTC).isoformat(),

        }
    )

    return {
        "short_code": short_code,
        "short_url": short_url,
        "original_url": request.url,
    }


handler = Mangum(app)