"""Command-line interface for solidifai."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from .generator import STLGenerator


def main():
    """Main CLI entry point."""
    # Load environment variables from .env file if present
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Generate STL files from text descriptions using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  solidifai "a simple cube with 10mm sides" -o cube.stl
  solidifai "a cylinder with diameter 20mm and height 30mm" -o cylinder.stl
  solidifai "a gear with 12 teeth" -o gear.stl

Note: Requires OPENAI_API_KEY environment variable to be set.
You can set it in a .env file or export it in your shell.
        """,
    )

    parser.add_argument(
        "description",
        type=str,
        help="Text description of the 3D object to create",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.stl",
        help="Output STL file path (default: output.stl)",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (if not set in environment)",
    )

    args = parser.parse_args()

    try:
        # Initialize generator
        generator = STLGenerator(api_key=args.api_key)

        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate STL
        success = generator.generate(args.description, str(output_path))

        if success:
            sys.exit(0)
        else:
            print("\nGeneration completed with warnings. Check the .scad file.")
            sys.exit(0)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
