import json
import os
import subprocess
from typing import Optional

import boto3
from dotenv import load_dotenv

from backend import logger
from backend.scad_utils import extract_scad_blocks

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
        """
        Generates OpenSCAD code based on a textual description of a 3D object using a language model.
        Args:
            description (str): A text description of the desired 3D object.
            max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 1500.
            temperature (float, optional): Sampling temperature for the model's output. Defaults to 0.7.
        Returns:
            list[str]: A list of OpenSCAD code blocks extracted from the model's response.
        Notes:
            - The generated OpenSCAD code is intended to be printable on a standard 3D printer.
            - The response contains only OpenSCAD code, possibly with comments, and no explanations.
        """
        system_prompt = (
            "You are an expert at generating OpenSCAD code for 3D modelling."
            "Given a text description of a 3D object, generate valid OpenSCAD code that creates that object."
            "If the request is complex, you may create several SCAD modules each within their own code block."
            "All parts of the model must touch the build plate to ensure printability."
            "The OpenSCAD model must be feasible to print on a standard 3D printer."
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

        raw_response = json.loads(response["body"].read())["content"][0]["text"]
        scad_list = extract_scad_blocks(raw_response)

        return scad_list

    def openscad_to_stl(
        self,
        openscad: str,
        output_path: str
    ) -> bool:
        """
        Converts OpenSCAD code to an STL file using the OpenSCAD command-line tool.
        This method writes the provided OpenSCAD code to a .scad file (for debugging),
        then invokes OpenSCAD to generate an STL file at the specified output path.
        Args:
            openscad (str): The OpenSCAD code to convert.
            output_path (str): The desired output path for the STL file. If the path does not end with ".scad",
                a corresponding .scad file will be created for debugging.
        Returns:
            bool: True if the STL file was successfully created and is non-empty, False otherwise.
        Notes:
            - Requires OpenSCAD to be installed and available in the system PATH.
            - Automatically creates the output directory if it does not exist.
        """
        scad_path = output_path if output_path.endswith(".scad") else output_path.replace(".stl", ".scad")
        
        # Create directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Always write the .scad file for debugging
        with open(scad_path, "w") as f:
            f.write(openscad)
        logger.info(f"OpenSCAD code written to: {scad_path}")

        # Check if OpenSCAD is available
        try:
            subprocess.run(['openscad', '--version'],
                           capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            logger.warning(
                "OpenSCAD is not installed or not in PATH\n"
                "Install it with: sudo apt-get install openscad"
            )
            return False

        logger.info(f"Converting {scad_path} to {output_path}...")
        
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
                    logger.info(f"Successfully created {output_path} ({size:,} bytes)")
                    return True
                else:
                    logger.warning(f"Conversion completed but STL file is empty or missing")
                    return False
            else:
                logger.error(f"Conversion failed: {result.stderr}")
                if result.stdout:
                    logger.error(f"stdout: {result.stdout}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Conversion timed out after 60 seconds")
            return False
        except Exception as e:
            logger.error(f"Error: {e}")
            return False

    def generate(
        self,
        description: str,
        output_path: str
    ) -> bool:
        """
        Generates STL files from a textual description and saves them to the specified output path.

        Args:
            description (str): A textual description used to generate OpenSCAD code.
            output_path (str): The directory path where the generated STL files will be saved.

        Returns:
            bool: True if all STL files were successfully generated and saved, False otherwise.
        """
        openscad_list = self.generate_openscad_code(description)
        stl_list = []
        for openscad in openscad_list:
            stl_list.append(self.openscad_to_stl(openscad, output_path))

        return all(stl_list)


# def generate(
#     description: str,
#     output_path: str,
#     region_name: Optional[str] = None,
#     model_id: Optional[str] = None
# ) -> bool:
#     """
#     Generates an STL file based on the provided description and saves it to the specified output path.

#     Args:
#         description (str): A textual description of the object to generate.
#         output_path (str): The file path where the generated STL file will be saved.
#         region_name (Optional[str], optional): The name of the region to use for generation. Defaults to None.
#         model_id (Optional[str], optional): The identifier of the model to use for generation. Defaults to None.

#     Returns:
#         bool: True if the STL file was successfully generated and saved, False otherwise.
#     """
#     gen = STLGenerator(region_name=region_name, model_id=model_id)
#     return gen.generate(description, output_path)
