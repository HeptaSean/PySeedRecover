import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="PySeedRecover",
    version="0.1.0",
    author="Benjamin Braatz",
    author_email="bb@bbraatz.eu",
    description="Recover BIP-39 Mnemonic Seed Phrases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HeptaSean/PySeedRecover",
    packages=["seedrecover"],
    install_requires=[
    ],
    extras_require={
        "dev": [
            "pydocstyle",
            "pycodestyle",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": ["seedrecover=seedrecover.main:main"],
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
