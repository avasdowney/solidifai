"""Unit tests for solidifai."""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from backend.generator import STLGenerator


class TestSTLGenerator(unittest.TestCase):
    """Test cases for STLGenerator class."""

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        generator = STLGenerator(api_key="test-key")
        self.assertEqual(generator.api_key, "test-key")

    def test_init_without_api_key_raises_error(self):
        """Test that initialization without API key raises ValueError."""
        # Make sure env var is not set
        old_key = os.environ.get("OPENAI_API_KEY")
        if old_key:
            del os.environ["OPENAI_API_KEY"]

        with self.assertRaises(ValueError) as context:
            STLGenerator()

        self.assertIn("API key must be provided", str(context.exception))

        # Restore env var if it existed
        if old_key:
            os.environ["OPENAI_API_KEY"] = old_key

    def test_init_with_env_var(self):
        """Test initialization using environment variable."""
        os.environ["OPENAI_API_KEY"] = "env-test-key"
        generator = STLGenerator()
        self.assertEqual(generator.api_key, "env-test-key")
        del os.environ["OPENAI_API_KEY"]

    @patch("solidifai.generator.OpenAI")
    def test_generate_openscad_code(self, mock_openai_class):
        """Test OpenSCAD code generation."""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Mock the response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "cube([10, 10, 10]);"
        mock_client.chat.completions.create.return_value = mock_response

        # Create generator and test
        generator = STLGenerator(api_key="test-key")
        code = generator.generate_openscad_code("a 10mm cube")

        self.assertEqual(code, "cube([10, 10, 10]);")
        mock_client.chat.completions.create.assert_called_once()

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
