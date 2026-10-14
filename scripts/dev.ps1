# Dev server for model-registry-board
$env:LLM_MODE = "mock"
uvicorn backend.main:app --reload --port 8000
