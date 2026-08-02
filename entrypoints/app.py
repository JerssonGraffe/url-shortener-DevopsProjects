from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum
import httpx

app = FastAPI()


class ShortenRequest(BaseModel):
    url: str


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/shorten")
async def shorten(request: ShortenRequest):

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            "https://cleanuri.com/api/v1/shorten",
            data={
                "url": request.url
            }
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Erro ao chamar o serviço de encurtamento."
        )

    return response.json()


handler = Mangum(app)