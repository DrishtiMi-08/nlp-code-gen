import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from prompt_engine import build_prompt
from model import generate_code

load_dotenv()

app = FastAPI(
    title="NLP Code Generation API",
    description="Transformer-based natural language to code generation backend.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
# Allows the VS Code extension (and any local client) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response schemas ────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    raw_input: str = Field(
        ...,
        min_length=3,
        max_length=300,
        description="User intent after stripping the @gen prefix.",
        examples=["reverse an array in C++"],
    )
    max_new_tokens: int = Field(
        default=256,
        ge=32,
        le=512,
        description="Max tokens the model can generate.",
    )


class GenerateResponse(BaseModel):
    code: str
    language: str
    intent: str
    prompt_used: str


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    """Quick liveness check — returns 200 if the server is up."""
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    """
    Main endpoint.

    Accepts a raw user intent string, builds a structured prompt,
    runs it through CodeT5, and returns the generated code.

    Example body:
        { "raw_input": "reverse an array in C++" }
    """
    if not req.raw_input.strip():
        raise HTTPException(status_code=400, detail="raw_input cannot be empty.")

    # Step 1: Build prompt
    prompt_data = build_prompt(req.raw_input)

    # Step 2: Generate code
    try:
        code = generate_code(
            prompt=prompt_data["prompt"],
            max_new_tokens=req.max_new_tokens,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model inference failed: {str(e)}",
        )

    return GenerateResponse(
        code=code,
        language=prompt_data["language"],
        intent=prompt_data["intent"],
        prompt_used=prompt_data["prompt"],
    )