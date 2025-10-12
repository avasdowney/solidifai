"""Main STL generator module using OpenAI and OpenSCAD."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from openai import OpenAI


class STLGenerator:
    """Generate STL files from text descriptions using AI."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the STL generator.

        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided or set in OPENAI_API_KEY environment variable"
            )
        self.client = OpenAI(api_key=self.api_key)

    def generate_openscad_code(self, description: str) -> str:
        """
        Generate OpenSCAD code from a text description using OpenAI.

        Args:
            description: Plain text description of the 3D object to create.

        Returns:
            OpenSCAD code as a string.
        """
        system_prompt = """You are an expert at generating OpenSCAD code for 3D modeling.
Given a text description of a 3D object, generate valid OpenSCAD code that creates that object.

Guidelines:
- Use clear, simple OpenSCAD syntax
- Include comments explaining key parts
- Use appropriate parameters for dimensions
- Center objects at origin when possible
- Return ONLY the OpenSCAD code, no explanations or markdown formatting
- Make sure the code is valid and will compile
"""

        user_prompt = f"Generate OpenSCAD code for: {description}"

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
        )

        openscad_code = response.choices[0].message.content.strip()

        # Clean up any markdown code blocks if present
        if openscad_code.startswith("```"):
            lines = openscad_code.split("\n")
            # Remove first and last lines (```)
            openscad_code = "\n".join(lines[1:-1])

        return openscad_code

    def openscad_to_stl(self, openscad_code: str, output_path: str) -> bool:
        """
        Convert OpenSCAD code to an STL file.

        Args:
            openscad_code: The OpenSCAD code to compile.
            output_path: Path where the STL file should be saved.

        Returns:
            True if successful, False otherwise.
        """
        # Check if openscad is available
        try:
            subprocess.run(
                ["openscad", "--version"],
                capture_output=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: OpenSCAD is not installed or not in PATH.")
            print("Please install OpenSCAD from https://openscad.org/")
            print("Saving OpenSCAD code instead...")

            # Save the .scad file instead
            scad_path = output_path.replace(".stl", ".scad")
            with open(scad_path, "w") as f:
                f.write(openscad_code)
            print(f"OpenSCAD code saved to: {scad_path}")
            print("You can open this file in OpenSCAD and export to STL manually.")
            return False

        # Create a temporary .scad file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".scad", delete=False
        ) as temp_scad:
            temp_scad.write(openscad_code)
            temp_scad_path = temp_scad.name

        try:
            # Run OpenSCAD to convert to STL
            subprocess.run(
                [
                    "openscad",
                    "-o",
                    output_path,
                    temp_scad_path,
                ],
                check=True,
                capture_output=True,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error converting to STL: {e}")
            print(f"STDERR: {e.stderr.decode()}")

            # Save the .scad file for debugging
            scad_path = output_path.replace(".stl", ".scad")
            with open(scad_path, "w") as f:
                f.write(openscad_code)
            print(f"OpenSCAD code saved to: {scad_path}")
            return False
        finally:
            # Clean up temporary file
            if os.path.exists(temp_scad_path):
                os.unlink(temp_scad_path)

    def generate(self, description: str, output_path: str) -> bool:
        """
        Generate an STL file from a text description.

        Args:
            description: Plain text description of the 3D object.
            output_path: Path where the STL file should be saved.

        Returns:
            True if successful, False otherwise.
        """
        print(f"Generating 3D model for: {description}")
        print("Calling OpenAI to generate OpenSCAD code...")

        # Generate OpenSCAD code
        openscad_code = self.generate_openscad_code(description)
        print("OpenSCAD code generated successfully!")

        # Save the intermediate .scad file
        scad_path = output_path.replace(".stl", ".scad")
        with open(scad_path, "w") as f:
            f.write(openscad_code)
        print(f"OpenSCAD code saved to: {scad_path}")

        # Convert to STL
        print("Converting to STL format...")
        success = self.openscad_to_stl(openscad_code, output_path)

        if success:
            print(f"STL file created successfully: {output_path}")
        else:
            print(f"STL conversion failed, but OpenSCAD code is available at: {scad_path}")

        return success
