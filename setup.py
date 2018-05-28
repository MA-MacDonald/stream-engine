import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stream_engine",
    version="0.0.4",
    author="Michael MacDonald",
    author_email="macdonald.michael.anthon@gmail.com",
    description="Matplotlib extension to plot real time data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MA-MacDonald/stream-engine",
    packages=setuptools.find_packages(),
	install_requires=[
          'matplotlib==2.0.0',
		  'scipy==0.19.0',
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
