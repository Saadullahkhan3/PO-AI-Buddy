from setuptools import setup, find_packages

# Read version from package
def get_version():
    with open("po_ai_buddy/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
        else:
            raise ValueError("setup.py: version isn't found.")

with open("README.md") as f:
    long_description = f.read()

setup(
    name='po_ai_buddy',
    version=get_version(),
    packages=find_packages(),
    install_requires=[
        "instructor",
    ],
    entry_points={
        "console_scripts": [
            "po = po_ai_buddy:main"
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
