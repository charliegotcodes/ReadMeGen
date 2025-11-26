from fastapi import FastAPI 
from app.models.repo_summary import (
    ReadmeRequest,
    ReadmeInfo,
    ReadmeResponse,
    FinalizeReadmeRequest,
    FinalizeReadmeResponse
)

app = FastAPI(title="README Analyzer API")

## Testing backend skeleton (WORKING)
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate_readme", response_model=ReadmeResponse)
def generate_readme(payload : ReadmeRequest):
    content = f"# README for {payload.repo_url}\n\nPlaceholder content."
    return ReadmeResponse(content=content)