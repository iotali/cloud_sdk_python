from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iotsdk",
    version="1.0.0",
    author="IoT SDK Team",
    author_email="your-email@example.com",
    description="IoT云平台SDK，提供与IoT云平台交互的简便方法",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/iotsdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
) 