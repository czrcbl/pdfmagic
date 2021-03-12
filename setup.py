#!/usr/bin/env python
from setuptools import setup

setup(
    name="pdfmagic",
    version="0.0.1",
    description="PDF tools",
    author="Cézar Lemos",
    author_email="cezar@protonmail.com",
    url="",
    packages=["pdfmagic"],
    install_requires=["click", "PyPDF2", "tqdm"],
    entry_points={
        "console_scripts": [
            "pdfmagic=pdfmagic.main:pdfmagic",
        ],
    },
)