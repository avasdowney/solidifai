import json
import os
import subprocess
from typing import Optional

import boto3
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "us.anthropic.claude-sonnet-4-20250514-v1:0"


class STLGenerator:
    """Generate OpenSCAD code and convert it to STL using Bedrock + OpenSCAD.

    Public API:
    - generate(description: str, output_path: str) -> bool
    """

    def __init__(
        self, region_name: Optional[str] = None,
        model_id: Optional[str] = None
    ):
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.model_id = model_id or DEFAULT_MODEL
        self.client = boto3.client("bedrock-runtime", region_name=self.region_name)

    def generate_openscad_code(
        self, description: str,
        max_tokens: int = 1500,
        temperature: float = 0.7
    ) -> str:
        """Generate OpenSCAD source for the provided description.

        Returns the OpenSCAD source string or raises RuntimeError on failure.
        """
        system_prompt = (
            "You are an expert at generating OpenSCAD code for 3D modelling. "
            "Given a text description of a 3D object, generate valid OpenSCAD code that creates that object. "
            "Return ONLY the OpenSCAD code, no explanations, comments are allowed in the code."
        )

        user_prompt = f"Generate OpenSCAD code for: {description}"

        # Claude Sonnet 4 format
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json", 
            body=json.dumps(payload)
        )

        # Parse response body
        raw = response.get("body").read()
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = None

        def _strip_markdown_fences(text: str) -> str:
            if text.startswith("```"):
                parts = text.splitlines()
                if len(parts) > 2:
                    return "\n".join(parts[1:-1]).strip()
            return text.strip()

        # Heuristics
        candidates = []

        if isinstance(parsed, dict):
            # Anthropic-style 'content' array
            if "content" in parsed and isinstance(parsed["content"], list):
                first = parsed["content"][0]
                if isinstance(first, dict) and isinstance(first.get("text"), str):
                    candidates.append(first["text"])

            # Bedrock 'outputs' array
            if "outputs" in parsed and isinstance(parsed["outputs"], list) and parsed["outputs"]:
                first = parsed["outputs"][0]
                if isinstance(first, dict):
                    content = first.get("content")
                    if isinstance(content, dict):
                        for k in ("text", "body", "output"):
                            v = content.get(k)
                            if isinstance(v, str):
                                candidates.append(v)

            # Top-level fields
            for k in ("output", "generated_text", "generatedText", "output_text", "text"):
                v = parsed.get(k)
                if isinstance(v, str):
                    candidates.append(v)

        # Raw fallback
        try:
            raw_decoded = raw.decode() if isinstance(raw, (bytes, bytearray)) else str(raw)
            if raw_decoded and raw_decoded.strip():
                candidates.append(raw_decoded)
        except Exception:
            pass

        # Pick the first non-empty candidate and clean markdown fences
        openscad_code = None
        for c in candidates:
            if isinstance(c, str) and c.strip():
                openscad_code = _strip_markdown_fences(c)
                if openscad_code:
                    break

        if not openscad_code:
            raise RuntimeError(f"Failed to extract model output from response: {raw[:500] if raw else 'empty'}")

        return openscad_code

    def openscad_to_stl(self, openscad: str, output_path: str) -> bool:
        """Convert OpenSCAD code to STL using OpenSCAD CLI.

        Returns True on successful STL creation, False otherwise (but always writes a .scad next to the .stl).
        """
        scad_path = output_path if output_path.endswith(".scad") else output_path.replace(".stl", ".scad")
        
        # Create directory if needed
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directory for {output_path}: {e}")

        # Always write the .scad file for debugging
        with open(scad_path, "w") as f:
            f.write(openscad)
        print(f"OpenSCAD code written to: {scad_path}")

        # Check if OpenSCAD is available
        try:
            subprocess.run(['openscad', '--version'], 
                          capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("❌ Error: OpenSCAD is not installed or not in PATH")
            print("Install it with: sudo apt-get install openscad")
            return False

        print(f"Converting {scad_path} to {output_path}...")
        
        try:
            # Run the conversion
            result = subprocess.run([
                'openscad',
                '-o', output_path,
                scad_path
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    size = os.path.getsize(output_path)
                    print(f"✅ Successfully created {output_path}")
                    print(f"File size: {size:,} bytes")
                    return True
                else:
                    print(f"❌ Conversion completed but STL file is empty or missing")
                    return False
            else:
                print(f"❌ Conversion failed: {result.stderr}")
                if result.stdout:
                    print(f"stdout: {result.stdout}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Conversion timed out after 60 seconds")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def generate(self, description: str, output_path: str) -> bool:
        openscad = self.generate_openscad_code(description)
        return self.openscad_to_stl(openscad, output_path)


def generate(description: str, output_path: str, region_name: Optional[str] = None, model_id: Optional[str] = None) -> bool:
    """Module-level convenience wrapper for backward compatibility."""
    gen = STLGenerator(region_name=region_name, model_id=model_id)
    return gen.generate(description, output_path)

