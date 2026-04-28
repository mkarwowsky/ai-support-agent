import httpx
from fastapi import APIRouter, HTTPException

from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ollama-health")
async def ollama_health() -> dict[str, str | int]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.ollama_base_url}/api/tags")
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Ollama unreachable: {exc}") from exc

    models = data.get("models", [])
    return {"status": "ok", "ollama": "reachable", "models_count": len(models)}