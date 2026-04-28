# AI Support Agent - Devlog

## 2026-04-28 - Day 2

### Zrobione
- Dodany `/health` i działa.
- Dodany `/ollama-health` z realnym checkiem do Ollama (`/api/tags`).
- Dodane schemy API:
  - `ChatRequest(message)`
  - `ChatResponse(answer, model)`
- Endpoint `/chat` istnieje (aktualnie mock / lub real call - weryfikować testem).

### Decyzje techniczne
- Kontrakty request/response przez Pydantic (styl produkcyjny).
- Konfiguracja modelu i URL przez zmienne środowiskowe:
  - `OLLAMA_BASE_URL`
  - `OLLAMA_MODEL`

### Co dalej
- Ustabilizować `/chat`:
  1. realny call do Ollama
  2. obsługa timeout/errors
  3. walidacja odpowiedzi upstream

  ### Update - /chat real call confirmed
- Zweryfikowano `POST /chat` przez curl.
- Endpoint zwraca odpowiedź z Ollama (`llama3.2:latest`).
- Flow end-to-end działa: FastAPI -> Ollama -> FastAPI.
- Następny krok: hardening błędów (503/502) dla stabilności API.

### Update - Day 3 start (service layer)
- Rozpoczęto wydzielanie logiki LLM do `app/services/llm_service.py`.
- Cel: odseparować HTTP layer od logiki integracji z Ollama.
- Endpoint `/chat` będzie wywoływać serwis zamiast trzymać logikę inline.

### Update - env loading in service
- Dodano `load_dotenv()` w `llm_service`.
- Serwis LLM czyta konfigurację z `.env` w sposób jawny i stabilny.

### Update - router extraction (health)
- Endpoint `/health` został przeniesiony z `main.py` do `app/routers/health.py`.
- `main.py` teraz składa aplikację przez `include_router`.
- Kierunek: cienkie `main.py`, endpointy w warstwie `routers`.

### Update - router extraction (ollama-health)
- Endpoint `/ollama-health` przeniesiony do `app/routers/health.py`.
- `main.py` uproszczony: tylko inicjalizacja app i podpinanie routerów.
- Potwierdzono działanie: `/health`, `/ollama-health`, `/chat`.

### Update - Day 4 (schemas extraction)
- Przeniesiono `ChatRequest` i `ChatResponse` do `app/schemas/chat.py`.
- Router `chat.py` korzysta teraz z importu schem.
- Rozdzielono warstwy: router (HTTP) vs schemas (kontrakty DTO).

### Update - Day 4 (core config)
- Dodano `app/core/config.py` jako centralne źródło ustawień.
- `llm_service` korzysta teraz z `settings` zamiast lokalnego `os.getenv`.
- Uporządkowano konfigurację pod dalszą rozbudowę (DB, app settings).