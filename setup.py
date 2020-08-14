from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="teslacamerge",
    version="0.1.0",
    description="Python tool for merging TeslaCam SavedClips",
    author="Jori van Lier",
    long_description=long_description,
    author_email="jori@jvlanalytics.nl",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.2.0",
        "click>=7.0",
        "opencv-python>=4.2",
        "numpy>=1.18.0"
    ],
    extras_require={
        "test": {
            "flake8",
            "pep8-naming",
            "pytest"
        },
    },
    scripts=["tcm"]
)
