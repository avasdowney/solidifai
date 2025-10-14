from setuptools import setup, find_packages

setup(
    name="solidifai",
    version="0.1.0",
    description="Generate STL files from plain text descriptions using AI",
    author="avasdowney",
    packages=["frontend", "backend"],
    install_requires=[
        "boto3>=1.28.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "jinja2>=3.1.0",
        "python-multipart>=0.0.6",
    ],
    # No entry points needed - use run_web.py directly
    python_requires=">=3.8",
)
