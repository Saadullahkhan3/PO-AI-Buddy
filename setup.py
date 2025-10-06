from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='po_ai_buddy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # depencencies
        # 'numpy',
        # 'pandas',
    ],
    entry_points={
        "console_scripts": [
            "po = po_ai_buddy:main"
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
