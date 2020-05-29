from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="teslacamerge",
    version="0.0.1",
    description="Python tool for merging TeslaCam SavedClips",
    author="Jori van Lier",
    long_description=long_description,
    author_email="jori@jvlanalytics.nl",
    packages=["tcmlib"],
    install_requires=[
        "matplotlib==3.1.0",
        "click==7.0",
        "opencv-python==4.1.0.25",
        "tqdm==4.32.1"
    ],
    extras_require={
        "test": {
            "flake8==3.7.7",
            "pep8-naming==0.8.2",
            "pytest==4.5.0"
        },
    },
    scripts=["tcm"]
)
