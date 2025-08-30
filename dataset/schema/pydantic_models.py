from __future__ import annotations
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field, constr, validator
from datetime import datetime

Domain = Literal[
    "coding",
    "creative_writing",
    "factual_qa",
    "mathematical_reasoning",
    "language_translation",
    "sentiment_analysis",
]

Difficulty = Literal["easy", "medium", "hard"]
AgreementMetric = Literal["cohen_kappa", "fleiss_kappa", "krippendorff_alpha"]
ModelName = Literal["GLM4.5", "GPT-OSS", "LLaMa 3", "Gemini2.5", "Claude 3.5", "Falcon"]

class AnnotatorScore(BaseModel):
    accuracy: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    creativity: int = Field(ge=1, le=5)

class AnnotatorEntry(BaseModel):
    annotator_id: str
    scores: AnnotatorScore

class Rating(BaseModel):
    accuracy: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    creativity: int = Field(ge=1, le=5)
    notes: Optional[str] = None
    annotators: Optional[List[AnnotatorEntry]] = None

    @validator("annotators", always=True)
    def validate_annotators(cls, v):
        if v is not None and len(v) == 0:
            raise ValueError("annotators list, if provided, cannot be empty")
        return v

class Agreement(BaseModel):
    metric: AgreementMetric
    value: float = Field(ge=-1.0, le=1.0)

class Metadata(BaseModel):
    language: Optional[str] = Field(None, description="ISO 639-1/3 code")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    hash: Optional[str] = None

class ChatbotEvaluationRecord(BaseModel):
    id: constr(strip_whitespace=True, min_length=8, max_length=64)
    prompt: constr(strip_whitespace=True, min_length=3)
    domain: Domain
    difficulty: Optional[Difficulty] = None
    chatbot_responses: Dict[ModelName, Optional[str]]
    ratings: Dict[ModelName, Rating]
    agreement: Optional[Agreement] = None
    metadata: Metadata

    @validator("chatbot_responses")
    def ensure_model_keys(cls, v):
        expected = {"GLM4.5", "GPT-OSS", "LLaMa 3", "Gemini2.5", "Claude 3.5", "Falcon"}
        missing = expected - set(v.keys())
        if missing:
            raise ValueError(f"Missing responses for models: {missing}")
        return v

    @validator("ratings")
    def validate_ratings(cls, v):
        if not v:
            raise ValueError("ratings cannot be empty")
        return v

__all__ = [
    "ChatbotEvaluationRecord",
    "Rating",
    "AnnotatorEntry",
    "AnnotatorScore",
    "Agreement",
    "Metadata",
]
