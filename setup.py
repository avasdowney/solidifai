from setuptools import setup, find_packages

setup(
    name="solidifai",
    version="0.1.0",
    description="Generate STL files from plain text descriptions using AI",
    author="avasdowney",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "solidpython2>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "solidifai=solidifai.cli:main",
        ],
    },
    python_requires=">=3.8",
)
