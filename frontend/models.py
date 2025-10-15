from typing import Optional
from pydantic import BaseModel

class GenerationRequest(BaseModel):
    """Request model for STL generation."""
    description: str
    region_name: Optional[str] = None

class FileInfo(BaseModel):
    """Information about a generated file."""
    filename: str
    url: str
    type: str  # 'scad' or 'stl'
    description: str
    size_bytes: Optional[int] = None

class GenerationResponse(BaseModel):
    """Response model for STL generation."""
    success: bool
    message: str
    files: list[FileInfo] = []
    job_id: str
