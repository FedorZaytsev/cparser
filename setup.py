from setuptools import setup, find_packages


with open('LICENSE') as f:
    license = f.read()

setup(
    name='cparser',
    version='0.1.0',
    description='Parser for C language',
    long_description="""
The aim of this project is to create parser for C language. There are several features of this parser:

Parser saves all comments. Each comment appends to the parent node.
Uses grammar for C11 (see grammar.txt for more)
Parser skip all preprocessor directives. Unfortunatelly, as a result of this, it do not build symbol table and cannot say is identificator is defined type or not.
""",
    author='Fedor Zaytsev',
    author_email='fedor.zaytsev@hotmail.com',
    url='https://github.com/FedorZaytsev/cparser',
    license=license,
    packages=['cparser']
)