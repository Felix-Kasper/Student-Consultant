from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from ai_consultant import analyze_document

import os


load_dotenv()

app = FastAPI(
    title="AI Study Consultant",
    description="AI-powered PDF analysis and personalized study assistant.",
    version="1.0.0"
)


# ---------------------------------------------------------
# Student Profile
# ---------------------------------------------------------

class StudentProfile(BaseModel):
    field_of_study: str = Field(
        default="Business",
        description="Student's field of study"
    )

    semester: int = Field(
        default=1,
        ge=1,
        le=20
    )

    interests: list[str] = Field(
        default_factory=list
    )

    learning_goal: str = Field(
        default="Exam preparation"
    )

    knowledge_level: str = Field(
        default="Intermediate"
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "online",
        "service": "AI Study Consultant",
        "version": "1.0.0"
    }


# ---------------------------------------------------------
# Profile Endpoint
# ---------------------------------------------------------

@app.post("/profile")
async def create_profile(profile: StudentProfile):
    return {
        "message": "Student profile created successfully.",
        "profile": profile.model_dump()
    }


# ---------------------------------------------------------
# PDF Analysis
# ---------------------------------------------------------

@app.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...),
    profile: StudentProfile = StudentProfile()
):

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Read PDF
    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF is empty."
        )

    # Basic size protection
    max_size = 15 * 1024 * 1024

    if len(pdf_bytes) > max_size:
        raise HTTPException(
            status_code=413,
            detail="PDF is too large. Maximum size is 15 MB."
        )

    try:

        result = analyze_document(
            pdf_bytes=pdf_bytes,
            filename=file.filename,
            profile=profile.model_dump()
        )

        return JSONResponse(
            content=result
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Document analysis failed: {str(e)}"
        )


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
async def root():

    return {
        "name": "AI Study Consultant",
        "description": (
            "Upload a PDF and receive a personalized "
            "AI-powered study analysis."
        ),
        "docs": "/docs",
        "health": "/health"
    }
