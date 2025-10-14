import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Ensure parent directory is in sys.path for local test runs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.generator import STLGenerator, generate

class TestSTLGenerator(unittest.TestCase):
    def test_init_default(self):
        gen = STLGenerator()
        self.assertIsInstance(gen, STLGenerator)
        self.assertTrue(hasattr(gen, 'client'))

    def test_init_custom_region_model(self):
        gen = STLGenerator(region_name='us-west-2', model_id='test-model')
        self.assertEqual(gen.region_name, 'us-west-2')
        self.assertEqual(gen.model_id, 'test-model')

    @patch('backend.generator.boto3.client')
    def test_generate_openscad_code(self, mock_boto_client):
        # Mock Bedrock response
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_response = MagicMock()
        # Simulate Claude response body
        mock_response.get.return_value.read.return_value = b'{"content": [{"text": "cube(10);"}]}'
        mock_client.invoke_model.return_value = mock_response

        gen = STLGenerator()
        code = gen.generate_openscad_code("a 10mm cube")
        self.assertEqual(code, "cube(10);")
        mock_client.invoke_model.assert_called()

    @patch('backend.generator.subprocess.run')
    def test_openscad_to_stl_success(self, mock_run):
        # Simulate successful OpenSCAD CLI conversion
        mock_run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=0, stdout='', stderr='')]
        gen = STLGenerator()
        with tempfile.TemporaryDirectory() as tmpdir:
            stl_path = os.path.join(tmpdir, 'test.stl')
            # Create a dummy STL file to simulate successful conversion
            with open(stl_path, 'wb') as f:
                f.write(b'0' * 100)  # 100 bytes
            result = gen.openscad_to_stl('cube(10);', stl_path)
            self.assertTrue(result)

    @patch('backend.generator.subprocess.run')
    def test_openscad_to_stl_failure(self, mock_run):
        # Simulate OpenSCAD CLI not found
        mock_run.side_effect = FileNotFoundError()
        gen = STLGenerator()
        with tempfile.TemporaryDirectory() as tmpdir:
            stl_path = os.path.join(tmpdir, 'fail.stl')
            result = gen.openscad_to_stl('cube(10);', stl_path)
            self.assertFalse(result)

    @patch('backend.generator.STLGenerator.generate_openscad_code')
    @patch('backend.generator.STLGenerator.openscad_to_stl')
    def test_module_level_generate(self, mock_stl, mock_code):
        mock_code.return_value = 'cube(10);'
        mock_stl.return_value = True
        result = generate('cube', 'output.stl')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()

    @patch("solidifai.generator.OpenAI")
    def test_generate_openscad_code_strips_markdown(self, mock_openai_class):
        """Test that markdown code blocks are stripped."""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Mock response with markdown
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "```openscad\ncube([10, 10, 10]);\n```"
        mock_client.chat.completions.create.return_value = mock_response

        # Create generator and test
        generator = STLGenerator(api_key="test-key")
        code = generator.generate_openscad_code("a cube")

        self.assertEqual(code, "cube([10, 10, 10]);")

    @patch("solidifai.generator.subprocess.run")
    def test_openscad_to_stl_without_openscad_installed(self, mock_run):
        """Test behavior when OpenSCAD is not installed."""
        # Mock subprocess to raise FileNotFoundError (OpenSCAD not found)
        mock_run.side_effect = FileNotFoundError()

        generator = STLGenerator(api_key="test-key")

        with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as tmp:
            output_path = tmp.name

        try:
            result = generator.openscad_to_stl("cube([10, 10, 10]);", output_path)
            self.assertFalse(result)

            # Check that .scad file was created
            scad_path = output_path.replace(".stl", ".scad")
            self.assertTrue(os.path.exists(scad_path))

            # Clean up
            if os.path.exists(scad_path):
                os.unlink(scad_path)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)


class TestCLI(unittest.TestCase):
    """Test cases for CLI functionality."""

    def test_cli_module_exists(self):
        """Test that CLI module can be imported."""
        from solidifai import cli
        self.assertTrue(hasattr(cli, "main"))


if __name__ == "__main__":
    unittest.main()
