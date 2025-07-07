from setuptools import setup, Extension
from Cython.Build import cythonize

extension = Extension(
    "src.quote_maker.generator_cy",
    ["src/quote_maker/generator_cy.pyx"],
)

setup(
    ext_modules=cythonize([extension])
)