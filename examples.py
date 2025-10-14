"""Example usage of the solidifai library."""

import os
from backend.generator import STLGenerator

def main():
    """Run examples of STL generation."""
    
    # Make sure API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    # Initialize generator
    generator = STLGenerator(api_key=api_key)
    
    # Example 1: Simple cube
    print("Example 1: Generating a simple cube...")
    generator.generate(
        description="a cube with 20mm sides",
        output_path="examples/cube.stl"
    )
    
    # Example 2: Cylinder
    print("\nExample 2: Generating a cylinder...")
    generator.generate(
        description="a cylinder with 15mm diameter and 40mm height",
        output_path="examples/cylinder.stl"
    )
    
    # Example 3: More complex object
    print("\nExample 3: Generating a phone stand...")
    generator.generate(
        description="a phone stand with a 60 degree angle, base 80mm wide, 60mm deep",
        output_path="examples/phone_stand.stl"
    )
    
    print("\nAll examples generated! Check the examples/ directory.")

if __name__ == "__main__":
    main()
