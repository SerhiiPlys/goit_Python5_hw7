import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clean-folder 004 by SerhiiPlys",
    version="0.0.4",
    author="Serhii Plys",
    author_email="ultra111@ukr.net",
    description="Cleaning folder app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SerhiiPlys/goit_pyton5_well.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_namespace_packages(),
    python_requires=">=3.6",
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)
