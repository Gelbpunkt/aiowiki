import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="async_mediawiki",
    version="0.2.0",
    author="Jens Reidel",
    author_email="jens.reidel@gmail.com",
    description="Async Mediawiki Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gelbpunkt/async-mediawiki",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=requirements,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
