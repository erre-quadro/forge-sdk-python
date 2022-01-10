import setuptools

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requirements = [l for l in f.read().splitlines() if l.strip()]

setuptools.setup(
    name="autodesk-forge-sdk",
    version="0.1.2",
    author="Petr Broz",
    author_email="petr.broz@autodesk.com",
    description="Unofficial Autodesk Forge SDK for Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/petrbroz/forge-sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/petrbroz/forge-sdk-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=["autodesk_forge_sdk"]),
    python_requires=">=3.6",
    install_requires=requirements,
)
