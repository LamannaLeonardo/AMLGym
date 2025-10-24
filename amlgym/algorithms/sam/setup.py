from distutils.core import setup


with open("README.md") as f:
    long_description = f.read()

setup(name='n-sam',
      version='1.2.0',
      python_requires=">=3.8",
      description='Numeric Safe Action Model Learning algorithm implementation in Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Argaman Mordoch',
      packages=["sam_learning", "solvers", "observations"]
     )