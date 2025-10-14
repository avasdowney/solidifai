# solidifai

Generate STL files from plain text descriptions using AI.

## Overview

`solidifai` is a Python web application that uses generative AI (AWS Bedrock with Claude) to create 3D printable STL files from natural language descriptions. Simply describe what you want to create through the web interface, and solidifai will generate the necessary OpenSCAD code and convert it to an STL file.

## Features

- 🤖 **AI-Powered Generation**: Uses AWS Bedrock with Claude to understand natural language descriptions
- 📐 **OpenSCAD Integration**: Generates parametric OpenSCAD code for precise 3D modeling
- 🖨️ **STL Export**: Automatically converts to STL format for 3D printing
- � **Web Interface**: Beautiful, responsive web interface for easy usage
- 💾 **Intermediate Files**: Saves OpenSCAD code for manual tweaking if needed
- 📁 **File Downloads**: Direct download links for both .scad and .stl files

## Prerequisites

1. **Python 3.8+**
2. **AWS Account and Credentials**: Configure AWS credentials with access to Bedrock
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

Configure your AWS credentials using one of these methods:

### Option 1: AWS CLI
```bash
aws configure
```

### Option 2: Create a `.env` file
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1
```

## Usage

1. **Start the web server:**
   ```bash
   python run_web.py
   ```

2. **Open your browser:**
   Navigate to http://localhost:8000

3. **Generate models:**
   - Enter a description like "a simple cube with 10mm sides"
   - Optionally select an AWS region
   - Click "Generate STL File"
   - Download the generated .scad and .stl files

### Example Descriptions:
- "a cylinder with diameter 20mm and height 30mm"
- "a sphere with radius 15mm" 
- "a gear with 12 teeth, 30mm outer diameter"
- "an L-shaped bracket with 50mm legs and 5mm thickness"
- "a phone stand with 60 degree viewing angle"


## How It Works

1. **Text Input**: You provide a natural language description of the 3D object
2. **AI Processing**: AWS Bedrock with Claude interprets your description and generates OpenSCAD code
3. **Code Generation**: Valid OpenSCAD code is created with appropriate parameters
4. **STL Conversion**: The OpenSCAD code is compiled to an STL file (if OpenSCAD is installed)
5. **Output**: You get both the `.scad` file (editable) and `.stl` file (3D printable)

## Output Files

For each generation, you'll get:

- **`.stl` file**: The 3D model ready for slicing and printing
- **`.scad` file**: The OpenSCAD source code, which you can edit manually

## Examples

### Simple Shapes
- "cube 10mm"
- "cylinder height 20mm diameter 10mm"
- "sphere radius 15mm"

### Functional Parts
- "a phone stand with 60 degree angle"
- "a cable organizer with 5 slots"
- "a mounting bracket with screw holes"

### Creative Objects
- "a dice with rounded corners"
- "a snowflake ornament"
- "a vase with hexagonal pattern"

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

### "AWS credentials not found"
Make sure your AWS credentials are configured:
```bash
aws configure
# or
export AWS_ACCESS_KEY_ID='your-access-key'
export AWS_SECRET_ACCESS_KEY='your-secret-key'
```

### Generated model doesn't look right
- Check the `.scad` file and edit it manually
- Try a more detailed or different description
- The AI might need more specific dimensions or constraints


## Dependencies

- `boto3>=1.28.0` - AWS SDK for Python (includes Bedrock client)
- `python-dotenv>=1.0.0` - Environment variable management
- `fastapi>=0.104.0` - Web framework
- `uvicorn>=0.24.0` - ASGI server
- `jinja2>=3.1.0` - Template engine

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is open source. Feel free to use and modify as needed.

## Acknowledgments

- Built with [AWS Bedrock](https://aws.amazon.com/bedrock/) and [Anthropic's Claude](https://www.anthropic.com/)
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