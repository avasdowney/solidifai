# solidifai

Generate STL files from plain text descriptions using AI.

## Overview

`solidifai` is a Python application that uses generative AI (OpenAI's GPT models) to create 3D printable STL files from natural language descriptions. Simply describe what you want to create, and solidifai will generate the necessary OpenSCAD code and convert it to an STL file.

## Features

- 🤖 **AI-Powered Generation**: Uses OpenAI's GPT-4 to understand natural language descriptions
- 📐 **OpenSCAD Integration**: Generates parametric OpenSCAD code for precise 3D modeling
- 🖨️ **STL Export**: Automatically converts to STL format for 3D printing
- 🎯 **Simple CLI**: Easy-to-use command-line interface
- 💾 **Intermediate Files**: Saves OpenSCAD code for manual tweaking if needed

## Prerequisites

1. **Python 3.8+**
2. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
3. **OpenSCAD** (optional but recommended): Download from [openscad.org](https://openscad.org/)
   - Without OpenSCAD, the tool will generate `.scad` files that you can open manually

## Installation

```bash
# Clone the repository
git clone https://github.com/avasdowney/solidifai.git
cd solidifai

# Install the package
pip install -e .
```

## Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create a `.env` file in the project directory:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

### Command Line

Basic usage:

```bash
solidifai "a simple cube with 10mm sides" -o cube.stl
```

More examples:

```bash
# Create a cylinder
solidifai "a cylinder with diameter 20mm and height 30mm" -o cylinder.stl

# Create a sphere
solidifai "a sphere with radius 15mm" -o sphere.stl

# Create something more complex
solidifai "a gear with 12 teeth, 30mm outer diameter" -o gear.stl

# Create a bracket
solidifai "an L-shaped bracket with 50mm legs and 5mm thickness" -o bracket.stl
```

### Python API

You can also use solidifai as a Python library:

```python
from solidifai import STLGenerator

# Initialize the generator
generator = STLGenerator(api_key="your-api-key")

# Generate an STL file
generator.generate(
    description="a cube with rounded edges, 20mm on each side",
    output_path="rounded_cube.stl"
)
```

## How It Works

1. **Text Input**: You provide a natural language description of the 3D object
2. **AI Processing**: OpenAI's GPT-4 interprets your description and generates OpenSCAD code
3. **Code Generation**: Valid OpenSCAD code is created with appropriate parameters
4. **STL Conversion**: The OpenSCAD code is compiled to an STL file (if OpenSCAD is installed)
5. **Output**: You get both the `.scad` file (editable) and `.stl` file (3D printable)

## Output Files

For each generation, you'll get:

- **`.stl` file**: The 3D model ready for slicing and printing
- **`.scad` file**: The OpenSCAD source code, which you can edit manually

## Examples

### Simple Shapes

```bash
solidifai "cube 10mm" -o cube.stl
solidifai "cylinder height 20mm diameter 10mm" -o cylinder.stl
solidifai "sphere radius 15mm" -o sphere.stl
```

### Functional Parts

```bash
solidifai "a phone stand with 60 degree angle" -o phone_stand.stl
solidifai "a cable organizer with 5 slots" -o cable_organizer.stl
solidifai "a mounting bracket with screw holes" -o bracket.stl
```

### Creative Objects

```bash
solidifai "a dice with rounded corners" -o dice.stl
solidifai "a snowflake ornament" -o snowflake.stl
solidifai "a vase with hexagonal pattern" -o vase.stl
```

## Tips for Better Results

1. **Be Specific**: Include dimensions when possible (e.g., "10mm sides" instead of "small")
2. **Use Standard Shapes**: Reference common 3D shapes (cube, cylinder, sphere, cone, etc.)
3. **Mention Key Features**: Specify holes, slots, fillets, chamfers, etc.
4. **Iterate**: If the first result isn't perfect, edit the generated `.scad` file or try a more detailed description

## Troubleshooting

### "OpenSCAD is not installed"
If you see this warning, the tool will still generate the `.scad` file. You can:
- Install OpenSCAD from [openscad.org](https://openscad.org/)
- Open the `.scad` file manually in OpenSCAD
- Export to STL from OpenSCAD's File menu

### "OpenAI API key must be provided"
Make sure your API key is set:
```bash
export OPENAI_API_KEY='your-key-here'
```

### Generated model doesn't look right
- Check the `.scad` file and edit it manually
- Try a more detailed or different description
- The AI might need more specific dimensions or constraints

## Project Structure

```
solidifai/
├── solidifai/
│   ├── __init__.py       # Package initialization
│   ├── generator.py      # Core STL generation logic
│   └── cli.py           # Command-line interface
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup
└── README.md            # This file
```

## Dependencies

- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=1.0.0` - Environment variable management
- `solidpython2>=2.1.0` - Python OpenSCAD library (future use)

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is open source. Feel free to use and modify as needed.

## Acknowledgments

- Built with [OpenAI's GPT-4](https://openai.com/)
- Uses [OpenSCAD](https://openscad.org/) for 3D modeling
- Inspired by the need for rapid 3D prototyping

## Roadmap

- [ ] Support for multiple AI models
- [ ] Web interface
- [ ] Gallery of generated models
- [ ] Direct 3D preview in terminal
- [ ] Batch generation from multiple descriptions
- [ ] Fine-tuning for specific types of objects

---

Made with ❤️ for makers and 3D printing enthusiasts