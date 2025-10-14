"""FastAPI web application for solidifai STL generator."""

import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.generator import STLGenerator


# Initialize FastAPI app
app = FastAPI(
    title="Solidifai Web Interface",
    description="Generate STL files from text descriptions using AI",
    version="1.0.0"
)

# Create directories for templates and generated files
TEMPLATE_DIR = Path(__file__).parent / "templates"
STATIC_DIR = Path(__file__).parent / "static"
OUTPUT_DIR = Path(__file__).parent / "generated"

TEMPLATE_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/generated", StaticFiles(directory=str(OUTPUT_DIR)), name="generated")

# Initialize templates
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


class GenerationRequest(BaseModel):
    """Request model for STL generation."""
    description: str
    region_name: Optional[str] = None


class GenerationResponse(BaseModel):
    """Response model for STL generation."""
    success: bool
    message: str
    stl_url: Optional[str] = None
    scad_url: Optional[str] = None
    job_id: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_model=GenerationResponse)
async def generate_stl(request: GenerationRequest):
    """Generate STL file from description."""
    try:
        # Create unique job ID
        job_id = str(uuid.uuid4())[:8]
        
        # Initialize generator
        generator = STLGenerator(region_name=request.region_name)
        
        # Create output paths
        stl_filename = f"{job_id}.stl"
        scad_filename = f"{job_id}.scad"
        stl_path = OUTPUT_DIR / stl_filename
        scad_path = OUTPUT_DIR / scad_filename
        
        # Generate the STL
        success = generator.generate(
            description=request.description,
            output_path=str(stl_path)
        )
        
        # Prepare response
        response = GenerationResponse(
            success=success,
            job_id=job_id,
            message="Generation completed successfully!" if success else "Generation completed with warnings. STL conversion may have failed, but SCAD file is available.",
            scad_url=f"/generated/{scad_filename}"
        )
        
        # Add STL URL if file exists
        if stl_path.exists():
            response.stl_url = f"/generated/{stl_filename}"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-form")
async def generate_stl_form(
    request: Request,
    description: str = Form(...),
    region_name: str = Form(default="us-east-1")
):
    """Generate STL from HTML form submission."""
    try:
        # Create generation request
        gen_request = GenerationRequest(
            description=description,
            region_name=region_name if region_name else None
        )
        
        # Generate STL
        result = await generate_stl(gen_request)
        
        # Return result page
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request,
                "result": result,
                "description": description
            }
        )
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": e.detail,
                "description": description
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": str(e),
                "description": description
            }
        )


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files."""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type
    media_type = "application/octet-stream"
    if filename.endswith(".stl"):
        media_type = "application/sla"
    elif filename.endswith(".scad"):
        media_type = "text/plain"
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type=media_type
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "solidifai-web"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)