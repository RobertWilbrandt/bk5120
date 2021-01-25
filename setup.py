"""Setup of Beckhoff BK5120 CANopen bus coupler test"""

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="bk5120",
    version="0.1",
    author="Robert Wilbrandt",
    author_email="robert@stamm-wilbrandt.de",
    description="Small python library to test the Beckhoff BK5120 CANopen bus coupler",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=["scripts/bk5120-console"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
)
