from setuptools import setup, find_packages

setup(
    name="ragchat",  # name of your package
    version="0.1",  # initial version
    packages=find_packages(),  # automatically find packages in your directory
    install_requires=[  # list dependencies from requirements.txt
        line.strip() for line in open("requirements.txt").readlines()
    ],
    description="A Retrieval-Augmented Generation chat library",
    long_description=open("README.md").read(),  # add description from README
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ragchat",  # replace with your GitHub URL
    author="team",
    author_email="your.email@example.com",
    classifiers=[  # additional metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # specify the Python version
)
