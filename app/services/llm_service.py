import os

import httpx
from fastapi import HTTPException


class LLMService:
    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

    async def chat(self, message: str) -> dict[str, str]:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=503, detail=f"Ollama request failed: {exc}") from exc

        answer = data.get("message", {}).get("content")
        if not answer:
            raise HTTPException(status_code=502, detail="Invalid Ollama response format")

        return {"answer": answer, "model": self.model}